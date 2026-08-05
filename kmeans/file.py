# handles basic file operations
import os

class file:
    name = ""
    path = ""
    fullPath = ""
    fileExists = False
    verbose = True
    def __init__(self, path, name):
        #sets our file path and tests for the existence of the file, setting an attribute and printing output.
        #returns the file's existence status.
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.path, self.name)
        if not os.path.isfile(self.fullPath):
            print(f"File '{self.name}' does not exist.")
        else:
            self.fileExists = True
            print(f"File '{self.name}' exists.")

    def setVerbose(self, verbose):
        self.verbose = verbose
        return True
    def doesFileExist(self):
        return self.fileExists
    def read(self):
        #basic if file exists, then read the file and return.
        if self.fileExists == True:
            with open(self.fullPath, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File '{self.name}' does not exist.")  
    def write(self, data, overWrite=False, format='',headers=''):
        #handles writing data to the file.
        #does conversion of data types to specific formats.
        #currently supports list -> csv.
        if overWrite == True:
            with open(self.fullPath, 'w') as f:
                f.write("")
        match format:
            case 'csv':
                with open(self.fullPath, 'a') as f:
                    if (isinstance(data, list) == False):
                        raise ValueError("Data must be a list for list->CSV conversion. Either convert to CSV and pass into this method as a string, or pass in a list of data to be converted to CSV.  ")

                    if (self.verbose == True):
                        print(f"Writing data to file: {self.fullPath}")
                    if headers:
                        f.write(f"{headers}\n")
                    for row in data:
                        csvRow = ''.join(str(value) for value in row)
                        f.write(csvRow)
                        f.write("\n")
            case 'json':
                with open(self.fullPath, 'a') as f:
                    f.write(data)
            case _:
                with open(self.fullPath, 'a') as f:
                    f.write(data)
