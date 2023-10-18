import customtkinter as ctk
from tkinter import filedialog
from plotter import Plotter
import widgets

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure


class GUI(ctk.CTk):
    def __init__(self, plotter: Plotter):
        super().__init__()

        self.title("Data Plotting GUI")
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.plotter = plotter

        # Create frame for adding files to plot
        self.fileFrame = ctk.CTkFrame(self)
        self.fileFrame.grid(row=0, column=0, sticky="nsew")

        fileLabel = ctk.CTkLabel(self.fileFrame, text="Files to Plot:")
        fileLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.add_fileselector()

    def add_fileselector(self):
        """Add a file to the list of files to plot"""
        if self.plotter.numFiles > 5:
            # Write error message to UI

            tooManyFilesLabel = ctk.CTkLabel(
                self.fileFrame, text="Can only plot 5 files at a time!", fg_color="red")
            tooManyFilesLabel.grid(
                row=self.plotter.numFiles, column=0, sticky="w", padx=5, pady=5)
            return

        # Add a FileSelector widget to the fileFrame
        fileSelector = widgets.FileSelector(self.fileFrame, self.plotter)
        fileSelector.grid(row=self.plotter.numFiles +
                          1, column=0, sticky="nsew")


if __name__ == "__main__":
    plotter = Plotter()
    GUI = GUI(plotter)
    GUI.mainloop()
