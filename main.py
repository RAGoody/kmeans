#main .py
# orchestrator of functions between ./kmeans/cli.py,files.py,algorithm.py
# This program intakes a file of tab-delimited X & Y coordinates, recommends a number of clusters to create based upon the range of the X-Y coordinates in the file,
#  then groups them utilizing a kmeans algorithm.
# Output is into a file.
# Future expansion is to present a graphical representation of the clusters.

import sys
from kmeans.cli import cli

