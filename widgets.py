from tkinter import filedialog
import customtkinter as ctk
import time
import os
import pandas as pd
from threading import Thread, Event
import UI
import re


class FileSelector(UI.GUI):
    def __init__(self, frame, plotter):
        self.frame = frame
        self.plotter = plotter
        self.file_path = ""

        self.widgetFrame = ctk.CTkFrame(self.frame)

        self.filesLabel = ctk.CTkLabel(self.widgetFrame, text="Files to Plot:")
        self.filesLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.fileLabel = ctk.CTkLabel(self.widgetFrame, text="File Path:")
        self.fileLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.fileEntry = ctk.CTkEntry(self.widgetFrame)
        self.fileEntry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.fileEntry.configure(state="disabled")

        self.fileButton = ctk.CTkButton(
            self.widgetFrame, text="Select File", command=self.select_file)
        self.fileButton.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    def select_file(self):
        # open file dialog
        self.file_path = filedialog.askopenfilename(
            title="Select File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))

        # write file path to entry
        self.fileEntry.configure(state="normal")
        self.fileEntry.delete(0, "end")
        self.fileEntry.insert(0, self.file_path)
        self.fileEntry.configure(state="disabled")

        # Replace button with remove button
        self.fileButton.destroy()
        self.fileButton = ctk.CTkButton(
            self.widgetFrame, text="x", command=self.remove_file, fg_color="red")
        self.fileButton.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        # Add a FileLoading widget to the fileFrame
        self.fileLoader = FileLoading(self.widgetFrame, self.file_path)
        self.fileLoader.grid(row=1, column=0, columnspan=3,
                             sticky="nsew", padx=5, pady=5)

        #

    def remove_file(self):
        # remove file from plotter
        
        self.file_path = ""

        # remove from entry
        self.fileEntry.configure(state="normal")
        self.fileEntry.delete(0, "end")
        self.fileEntry.insert(0, "")
        self.fileEntry.configure(state="disabled")

        # replace remove button with select file button
        self.fileButton.destroy()
        self.fileButton = ctk.CTkButton(
            self.widgetFrame, text="Select File", command=self.select_file)
        self.fileButton.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    def grid(self, **gridoptions):
        self.widgetFrame.grid(**gridoptions)


class FileLoading(UI.GUI):
    def __init__(self, frame, filePath):
        self.frame = frame
        self.dataframe = None

        self.widgetFrame = ctk.CTkFrame(self.frame)

        self.loadingLabel = ctk.CTkLabel(self.widgetFrame, text="")
        self.loadingLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # button to start loading the file
        self.loadButton = ctk.CTkButton(
            self.widgetFrame, text="Load", command=lambda: self.start_loading(filePath))
        self.loadButton.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Add preview of header
        self.headerPreviewLabel = ctk.CTkLabel(
            self.widgetFrame, text="Preview")
        self.headerPreviewLabel.grid(
            row=1, column=0, sticky="w", padx=5, pady=5)

        previewFrame = ctk.CTkFrame(
            self.widgetFrame)
        previewFrame.grid(row=2, column=0, columnspan=3,
                          sticky="nsew", padx=5, pady=5)
        self.headerPreview = ctk.CTkTextbox(
            previewFrame, wrap="none", width=400)
        self.headerPreview.insert("0.0", "Loading preview...")

        self.headerPreview.configure(state="disabled")

        self.headerPreview.grid(
            row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # find the header
        startRow, header = self.find_header(filePath)
        print(startRow, header)
        # load the preview
        self.load_preview(filePath)

    def start_loading(self, filePath):

        # Create a thread to load the data in the background while the UI is still responsive
        loadThread = Thread(target=lambda: self.load_data(filePath))
        loadThread.start()

        # remove the header preview
        self.headerPreviewLabel.destroy()
        self.headerPreview.destroy()

    def load_data(self, filePath, startRow=0, endRow=None):
        """Load the data from the files"""
        # isolate the file name

        fileName = os.path.basename(filePath)

        # Update UI to show that the file is loading
        self.loadingLabel.configure(
            text=f"Loading {fileName}...", fg_color="blue")
        self.loadingLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        t1 = time.time()
        try:
            self.dataframe = pd.read_csv(
                filePath, skiprows=startRow, nrows=endRow-startRow)
        except:
            self.loadingLabel.configure(
                text=f"Error loading {fileName}", fg_color="red")
            self.loadingLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            return

        t2 = time.time()

        self.plotter.add_file(filePath, self.dataframe)

        # Update UI to show that the file has been loaded
        self.loadingLabel.configure(
            text=f"Loaded {fileName} in {t2-t1} seconds")
        self.loadingLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    def unload_data(self):
        self.dataframe = None

    def load_preview(self, filePath):
        # load the first 50 rows of the file

        preview = pd.read_csv(filePath, nrows=100)

        # find the row with the header

        # Add the row index as column in the dataframe
        preview.insert(0, "Row", preview.index)

        # add it to the preview
        self.headerPreview.configure(state="normal")
        self.headerPreview.delete("0.0", "end")
        self.headerPreview.insert("0.0", preview)
        self.headerPreview.configure(state="disabled")

    def find_header(self, filePath):
        # load the first 100 rows of the file and find the row with the header
   
        with open(filePath, "r") as file:
            for i in range(100):
                line = file.readline()
                headerMatch = re.match(r"^([a-zA-Z\-_\(\)\{\}\[\]:\s(\d)?]+,)*[a-zA-z\-_\(\)\{\}\[\]:\s]+$", line)
                if headerMatch:
                    return i, headerMatch.match(0)
        return None, None

    def grid(self, **gridoptions):
        self.widgetFrame.grid(**gridoptions)
