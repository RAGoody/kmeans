# generates suggest clusters based upon separations of data in file.
# then processes the data into clusters based upon the number of clusters suggested.
import math

class algorithm:
    data = []
    dataX = []
    dataY = []
    suggestedClusters = 0
    actualClusters = 0
    rowFormatClusters = []
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

    def suggestClusters(self):
        # Placeholder for logic to suggest number of clusters based on data
        # For example, using the elbow method or silhouette score
        xSuggest = 0
        ySuggest = 0

        minX = min(self.dataX)
        minY = min(self.dataY)
        maxX = max(self.dataX)
        maxY = max(self.dataY)
        diffX = maxX - minX
        diffY = maxY - minY

        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        self.diffX = diffX
        self.diffY = diffY

        xCentroids = [] #parallel to yCentroids, these are the suggested centroids for the X axis
        yCentroids = [] #paralell to xCentroids, these are the suggested centroids for the Y axis

        orderMagX = math.floor(math.log10(abs(diffX))) if diffX != 0 else 0
        orderMagY = math.floor(math.log10(abs(diffY))) if diffY != 0 else 0

        lowestXMod = 9999999
        lowestYMod = 9999999

        #find the smallest whole number with the most even divisor on the X axis
        for i in range(1, int(diffX) + 1):
            if diffX % i < lowestXMod:
                xSuggest = i

        #find the smallest whole number with the most even divisor on the Y axis
        for i in range(1, int(diffY) + 1):
            if diffY % i < lowestYMod:
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
    def processData(self):
        # This would involve initializing centroids, assigning points to clusters, and updating centroids iteratively
        self.actualClusters = self.suggestedClusters #forcing this right now as no handling for input clusters exists yet.
        if self.actualClusters == 0:
            raise ValueError("Number of clusters not suggested. Call suggestClusters() first.")
        self._initializeClusters()
        self._setCentroids()
        rowCount = len(self.data)
        for i in range(rowCount):
            pointX = self.dataX[i]
            pointY = self.dataY[i]
            centroidIndex = self._findCentroid(self.centroids, pointX, pointY)
            print(f"Point ({pointX}, {pointY}) assigned to centroid index {centroidIndex} at {self.centroids[centroidIndex]}")
            self._updateClusters(centroidIndex, pointX, pointY)

        print("Comnpleted processing data into clusters.")

        return self.clusters
    def getClusters(self):
        return self.clusters
    def getRowFormatClusters(self):
        return self.rowFormatClusters
    def _findCentroid(self, centroids, pointX, pointY):
        # locates the closests centroid for given pointX & pointY
        closestCentroidIndex = -1
        greatestDiff = 9999999

        for i in range(len(centroids)):
            centroidX, centroidY = centroids[i]
            diffX = abs(pointX - centroidX)
            diffY = abs(pointY - centroidY)
            diffTotal = diffX + diffY
            if (diffTotal < greatestDiff):
                greatestDiff = diffTotal
                closestCentroidIndex = i

        return closestCentroidIndex
    def _initializeClusters(self):
        # initiatlize the cluster if it doesn't exist
        for i in range(self.actualClusters):
            self.clusters.append({
                "centroid": i,
                "coordinates": [],
                "points": []
            })
    def _updateClusters(self, centroidIndex, x, y):
        # updates the specified cluster with the new x,y coordinates.
        thisCluster = self.clusters[centroidIndex]
        if len(thisCluster["coordinates"]) == 0:
            thisCluster["coordinates"] = [self.centroids[centroidIndex][0], self.centroids[centroidIndex][1]]
        thisCoordinate = [x, y]
        thisCluster["points"].append(thisCoordinate)
    
        self.clusters[centroidIndex] = thisCluster
        self.rowFormatClusters.append(f"{centroidIndex},{x},{y}")
    def _setCentroids(self):
        # Logic to initialize centroids based on suggestedClusters
        if self.actualClusters == 0:
            raise ValueError("Number of clusters not suggested. Call suggestClusters() first.")
        
        spacingX = round(self.diffX / (self.actualClusters))
        spacingY = round(self.diffY / (self.actualClusters))
        xCentroids = []
        i = self.minX
        while i <= self.maxX:
            xCentroids.append(i)
            i += spacingX

        yCentroids = []
        i = self.minY
        while i <= self.maxY:
            yCentroids.append(i)
            i += spacingY

        i = 0
        for i in range(self.actualClusters):
            self.centroids.append((xCentroids[i], yCentroids[i]))

        print("Identified evenly spaced centroids:",self.centroids)
        return self.centroids