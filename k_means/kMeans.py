'''
Created on Jun 12, 2014

@author: zhihuang
'''
from numpy import *

def loadDataSet(fileName):
    fr = open(fileName)
    dataMat = [map(float, line.strip().split('\t')) for line in fr.readlines()]
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids

def kMeans(dataSet, k, distMeas = distEclud, createCent = randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        print centroids
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis = 0)
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas = distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroid0 = mean(dataSet, axis = 0).tolist()[0]
    centList = [centroid0]
    for j in range(m):
        clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0]]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
            print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print 'the bestCentToSplit is: ', bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]
        centList.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0]] = bestClustAss
    return mat(centList), clusterAssment
    
def plotKMeans(datMat, centroids, clusterAssment):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    clusterColors = ['red', 'blue', 'green', 'yellow']
    k = shape(centroids)[0]
    for i in range(k):
        cluster = datMat[nonzero(clusterAssment[:, 0].A == i)[0]]
        ax.scatter(cluster[:, 0].flatten().A[0], cluster[:, 1].flatten().A[0], c=clusterColors[i])
        ax.scatter([centroids[i, 0]], [centroids[i, 1]], marker='^', c= clusterColors[i], s=100)
    plt.show()

#sometimes could go into local minimum and the clusters are not so good, but it does not so frequently happen    
datMat = mat(loadDataSet('testSet2.txt'))
mycentroids, clustAssing = kMeans(datMat, 3)
plotKMeans(datMat, mycentroids, clustAssing)

#seems to perform better than the above method
datMat = mat(loadDataSet('testSet2.txt'))
centList, myNewAssments = biKmeans(datMat, 3)
plotKMeans(datMat, centList, myNewAssments)
# a = mat([[23, 23,3], [23, 32, 4]])
# print a[0, :].tolist()