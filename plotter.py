import pandas as pd
import time
import os


class Plotter():
    """Plotter class that keeps track of the data and does the plotting"""

    def __init__(self):
        self.numFiles = 0
        self.filePaths = []
        self.dataframes = []

    def add_file(self, filePath, dataFrame):
        """Add a file to the list of files to plot"""
        self.filePaths.append(filePath)
        self.numFiles += 1

    def remove_file(self, filePath):
        """Remove a file from the list of files to plot"""
        self.filePaths.remove(filePath)
        self.numFiles -= 1

    def get_files(self):
        """Get the list of files to plot"""
        return self.filePaths

    def load_data(self):
        """Load the data from the files"""
        print("Loading data...\n")
        for filePath in self.filePaths:
            # isolate the file name
            fileName = os.path.basename(filePath)

            t1 = time.time()
            self.dataframes.append(pd.read_csv(filePath))
            t2 = time.time()

            print(f"Loaded {fileName}: {t2-t1}")
