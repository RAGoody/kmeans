#main .py
# orchestrator of functions between ./kmeans/cli.py,files.py,algorithm.py
# This program intakes a file of tab-delimited X & Y coordinates, recommends a number of clusters to create based upon the range of the X-Y coordinates in the file,
#  then groups them utilizing a kmeans algorithm.
# Output is into a file.
# Future expansion is to present a graphical representation of the clusters.

from kmeans.cli import cli
from kmeans.file import file
from kmeans.algorithm import algorithm

import sys

parameters = cli(parameters=['input', 'output', 'method'])
print(parameters.getParameters())

inputFile = file(path="data/input", name=parameters.getParameter('input'))
print(f"Reading input file: {inputFile.fullPath}")
inputData = inputFile.read()

alg = algorithm(data=inputData, display=True)
suggestedClusterCount = alg.suggestClusterCount()
print(f"Suggested number of clusters: {suggestedClusterCount}")

alg.processData(method=parameters.getParameter('method'))

outputFile = file(path="data/output", name=parameters.getParameter('output'))
outputFile.write(alg.getRowFormatClusters(),True,'csv','cluster,x,y')