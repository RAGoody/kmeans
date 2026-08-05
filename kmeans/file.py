# handles basic file operations
import os

class file:
    name = ""
    path = ""
    fullPath = ""
    fileExists = False
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.path, self.name)
        if not os.path.isfile(self.fullPath):
            print(f"File '{self.name}' does not exist.")
        else:
            self.fileExists = True
            print(f"File '{self.name}' exists.")
    def read(self):
        if self.fileExists == True:
            with open(self.fullPath, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File '{self.name}' does not exist.")  
    def write(self, data, format='',headers=''):
        match format:
            case 'csv':
                with open(self.fullPath, 'a') as f:
                    if headers:
                        f.write(f"{headers}\n")
                    for row in data:
                        csvRow = ''.join(str(value) for value in row)
                        f.write(csvRow)
                        f.write("\n")
            case 'json':
                with open(self.fullPath, 'w') as f:
                    f.write(data)
            case _:
                with open(self.fullPath, 'w') as f:
                    f.write(data)
