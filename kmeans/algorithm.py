# generates suggest clusters based upon separations of data in file.
# then processes the data into clusters based upon the number of clusters suggested.
import math
import random

class algorithm:
    data = []
    dataX = []
    dataY = []
    suggestedClusters = 0
    actualClusters = 0
    rowFormatClusters = []
    listFormatClusters = []
    clusters = []
    centroids = []
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0
    diffX = 0
    diffY = 0

    def __init__(self, data):
        self.rawdata = data
        self.clusters = []
        print("Initializing algorithm with data...")
        self.separateData()

    def separateData(self):
        """Separates the raw data into X and Y coordinates, storing them in self.data, self.dataX, and self.dataY."""
        self.rawdata = [line.split('\t') for line in self.rawdata.strip().split('\n')]
        point = {}
        counter = 0
        for dataPoint in self.rawdata:
            self.data.append([counter])
            self.dataX.append([counter])
            self.dataY.append([counter])
            self.data[counter] = [float(dataPoint[0].split(',')[0]),float(dataPoint[0].split(',')[1])]
            self.dataX[counter] = float(dataPoint[0].split(',')[0])
            self.dataY[counter] = float(dataPoint[0].split(',')[1])
            counter += 1

        self._setMinMaxDiffXY()

    def suggestClusters(self):
        """Suggests a number of clusters based on the range of X and Y coordinates in the data, attempting to find mid-points for even distribution."""
        xSuggest = 0
        ySuggest = 0

        xCentroids = [] #parallel to yCentroids, these are the suggested centroids for the X axis
        yCentroids = [] #paralell to xCentroids, these are the suggested centroids for the Y axis

        orderMagX = math.floor(math.log10(abs(self.diffX))) if self.diffX != 0 else 0
        orderMagY = math.floor(math.log10(abs(self.diffY))) if self.diffY != 0 else 0

        lowestXMod = 9999999
        lowestYMod = 9999999

        #find the smallest whole number with the most even divisor on the X axis
        for i in range(1, int(self.diffX) + 1):
            if self.diffX % i < lowestXMod:
                xSuggest = i

        #find the smallest whole number with the most even divisor on the Y axis
        for i in range(1, int(self.diffY) + 1):
            if self.diffY % i < lowestYMod:
                ySuggest = i

        xSuggest = round(math.sqrt(xSuggest))
        ySuggest = round(math.sqrt(ySuggest))

        xyFloor = min(xSuggest, ySuggest)

        #level one reduction of cluster count.
        if (xSuggest != ySuggest):
            xyDiff = abs(xSuggest - ySuggest)
            xyDiff = round(math.log10(xyDiff))
            self.suggestClusters = xyFloor + xyDiff
        else :
            self.suggestedClusters = xSuggest

        #level two reduction of cluster count.
        if (self.suggestedClusters > 10):
            lessThan10 = False
            while (lessThan10 == False):
                self.suggestedClusters = round(self.suggestedClusters / 2)
                if (self.suggestedClusters <= 10):
                    lessThan10 = True

        return self.suggestedClusters
    def processData(self,method='minimumDistance'):
        """Processes the data into clusters based upon the specified method."""
        self.actualClusters = self.suggestedClusters #forcing this right now as no handling for input clusters exists yet.
        if self.actualClusters == 0:
           raise ValueError("Number of clusters not suggested. Call suggestClusters() first.")
        self._initializeClusters()
        match method:
            case 'minimumDistance':
                print("Processing data into clusters using minimum distance method...")
                self._setCentroids() #this case utilizes the suggested centroids and does not iterate over them.
                self.clusters = self._minimumDistance()
            case 'lloyds':
                print("Processing data into clusters using Lloyd's method...")
                self.clusters = self._lloyds()
            case _:
                print(f"Unknown method '{method}' specified. Defaulting to minimum distance method...")
                self.clusters = self._minimumDistance()
        return self.clusters

    def getClusters(self):
        return self.clusters
    
    def getRowFormatClusters(self):
        return self.rowFormatClusters
    
    def getListFormatClusters(self):
        return self.listFormatClusters
    
    def _lloyds(self):
        """This would involve initializing centroids, assigning points to clusters, and updating centroids iteratively"""
        print("Starting Lloyd's algorithm for clustering...")
        oldClusters = []
        newClusters = []
        iterationMax=4
        iteration = 0
        self._setCentroidsAtRandom() #randomly select x,y coordinates for centroids within the min/max range of the data.
        newClusters = self._minimumDistance() #take our first pass

        #TODO: visualize first pass and pause.


        while self._detectChanges(oldClusters, newClusters):
            # Logic to update centroids and reassign points to clusters
            newClusters = self._minimumDistance()  # Reassign points to clusters based on new centroids
            if self._detectChanges(oldClusters, newClusters):
                oldClusters = newClusters
                self.centroids = self._moveCentroids(oldClusters)  # Update centroids based on new clusters

            iteration += 1
            if iteration >= iterationMax:
                print("Maximum iterations reached. Stopping Lloyd's algorithm.")
                break

        print("Lloyd's algorithm completed in ", iteration, "iterations.")
        self.clusters = newClusters
        return self.clusters
    
    def _moveCentroids(self, clusters):
        """Updates centroids based on the mean of the points assigned to each cluster."""
        print("Updating centroids based on current cluster assignments...")
        newCentroids = []
        print("Current centroids:", self.centroids)
        for i, cluster in enumerate(clusters):
            if cluster["points"]:
                sumX = sum(point[0] for point in cluster["points"])
                sumY = sum(point[1] for point in cluster["points"])
                count = len(cluster["points"])
                newCentroidX = sumX / count
                newCentroidY = sumY / count
                newCentroids.append((newCentroidX, newCentroidY))
            else:
                newCentroids.append(self.centroids[i]) # If a cluster has no points, keep the old centroid
            
        print("Updated centroids:", newCentroids)
        return newCentroids

    def _setCentroidsAtRandom(self):
        """This would involve randomly assigning points to clusters and then updating centroids iteratively"""
        self.centroids = [] #reset this for each iteration
        for i in range(self.suggestedClusters):
            self.centroids.append((random.uniform(self.minX,self.maxX), random.uniform(self.minY,self.maxY)))

    def _detectChanges(self, oldClusters, newClusters):
        """Compares old and new clusters to detect changes in point assignments."""
        changesDetected = False
        if len(oldClusters) != len(newClusters):
            changesDetected = True
        else:
            for i in range(len(oldClusters)):
                oldPoints = oldClusters[i]["points"]
                newPoints = newClusters[i]["points"]
                if oldPoints != newPoints:
                    changesDetected = True
                    break

        return changesDetected
    
    def _minimumDistance(self):
        """This would involve initializing centroids, assigning points to clusters based on pure minimum sum of distance from a point's X,Y separation from a centroid X,Y."""
        rowCount = len(self.data)
        for i in range(rowCount):
            pointX = self.dataX[i]
            pointY = self.dataY[i]
            #print(f"for point {pointX}, {pointY} finding closest centroid...")
            centroidIndex = self._findCentroid(self.centroids, pointX, pointY)
            #print(f"    Point ({pointX}, {pointY}) assigned to centroid index {centroidIndex} at {self.centroids[centroidIndex]}")
            self._updateClusters(centroidIndex, pointX, pointY)

        print("Completed processing data into clusters.")
        return self.clusters

    def _findCentroid(self, centroids, pointX, pointY):
        """ locates the closests centroid for given pointX & pointY"""
        closestCentroidIndex = -1
        greatestDiff = 9999999
        for i in range(len(centroids)):
            centroidX, centroidY = centroids[i]
            diffX = abs(pointX - centroidX)
            diffY = abs(pointY - centroidY)
            diffTotal = diffX + diffY
            #print(f"        difference from centroid {i}: {centroidX}, {centroidY} = {diffTotal}")
            if (diffTotal < greatestDiff):
                greatestDiff = diffTotal
                closestCentroidIndex = i

        return closestCentroidIndex
    def _initializeClusters(self):
        """ initiatlize the cluster if it doesn't exist"""
        for i in range(self.actualClusters):
            self.clusters.append({
                "centroid": i,
                "coordinates": [],
                "points": []
            })

    def _updateClusters(self, centroidIndex, x, y):
        """ updates the specified cluster with the new x,y coordinates."""
        thisCluster = self.clusters[centroidIndex]
        if len(thisCluster["coordinates"]) == 0:
            thisCluster["coordinates"] = [self.centroids[centroidIndex][0], self.centroids[centroidIndex][1]]
        thisCoordinate = [x, y]
        thisCluster["points"].append(thisCoordinate)
    
        self.clusters[centroidIndex] = thisCluster
        self.rowFormatClusters.append(f"{centroidIndex},{x},{y}")
        self.listFormatClusters.append([centroidIndex,x,y])

    def _setCentroids(self):
        """Logic to initialize centroids based on suggestedClusters"""
        if self.actualClusters == 0:
            raise ValueError("Number of clusters not suggested. Call suggestClusters() first.")
        
        spacingX = round(self.diffX / (self.actualClusters))
        spacingY = round(self.diffY / (self.actualClusters))
        xCentroids = []
        i = self.minX
        while i <= self.maxX:
            #append this centroid to our list, but first let's ensure it's not an even distance from the other centroids.
            if (i % 2 == 0):
                xCentroidValue = i + 1
            else:
                xCentroidValue = i - 1

            xCentroids.append(i)
            i += spacingX

        yCentroids = []
        i = self.minY
        while i <= self.maxY:
            if (i % 2 == 0):
                yCentroidValue = i + 1
            else:
                yCentroidValue = i - 1
            yCentroids.append(yCentroidValue)
            i += spacingY

        i = 0
        for i in range(self.actualClusters):
            self.centroids.append((xCentroids[i], yCentroids[i]))

        print("Identified evenly spaced centroids:",self.centroids)
        return self.centroids
    
    def _setMinMaxDiffXY(self):
        """Calculates the minimum, maximum, and difference for X and Y coordinates."""
        self.minX = min(self.dataX)
        self.minY = min(self.dataY)
        self.maxX = max(self.dataX)
        self.maxY = max(self.dataY)
        self.diffX = self.maxX - self.minX
        self.diffY = self.maxY - self.minY