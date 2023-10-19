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
