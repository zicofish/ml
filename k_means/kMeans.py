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
    
datMat = mat(loadDataSet('testSet.txt'))
mycentroids, clustAssing = kMeans(datMat, 4)
plotKMeans(datMat, mycentroids, clustAssing)