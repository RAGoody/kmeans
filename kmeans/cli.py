# handles CLI variable reading
# initializes a cliParameters object
import argparse

class cli:
    parameters = {}
    def __init__(self,parameters):
        self.parser = argparse.ArgumentParser(description='K-Means Clustering Algorithm')
        self.parser.add_argument("pairs", nargs="*", help="Parameters in key=value pairs. Files expected in the appropriate data/input or data/output directories.")
        args = self.parser.parse_args()

        for pair in args.pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)  # split only on the first '='
                self.parameters[key] = value
            else:
                print(f"Warning: Skipping invalid parameter format: {pair}")
    def getParameter(self, param_name):
        return self.parameters.get(param_name, None)
    def getParameters(self):
        return self.parameters

