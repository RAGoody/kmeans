Python program that loads a .csv containing X,Y coordinates.

two parameters: input=filename.csv output=filename2.csv

expects the files to exist in ./data/input/filename.csv and writes to ./data/output/filename2.csv

Overwrites the output as a default behavior. Creates if nonexistent.

Will suggest a number of centroids to plot with equidistance centroid positions to evenly distribute the points between them.

Generates an output of cluster #,X,Y

Draws a plot with colored groups.



TODO: take parameters for # of centroids and to iterate and adjust position of them.

TODO: review why some points are being mapped to distance centroid positions.

TODO: implement Lloyd's algorithm for building/iterating clusters.
