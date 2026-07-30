# handles basic file operations
import os

class file:
    name = ""
    path = ""
    fullPath = ""
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.path, self.name)
        if not os.path.isfile(self.fullPath):
            raise FileNotFoundError(f"File '{self.name}' does not exist.")
    def read(self):
        with open(self.fullPath, 'r') as f:
            return f.read()
    def write(self, data):
        with open(self.fullPath, 'w') as f:
            f.write(data)