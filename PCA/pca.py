'''
Created on Jun 11, 2014

@author: zhihuang
'''
from numpy import *
def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat = 9999999):
    meanVals = mean(dataMat, axis = 0)
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar = 0)
    eigVals, eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:, eigValInd]
    lowDDataMat = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat
    
def replaceNanWithMean():
    datMat = loadDataSet('secom.data', ' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:, i].A))[0], i])
        datMat[nonzero(isnan(datMat[:, i].A))[0], i] = meanVal
    return datMat

def plotPCNum(eigVals):
    totalVariance = sum(eigVals)
    percentage = eigVals / totalVariance
    cumulative = cumsum(percentage)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax1 = fig.add_subplot(121, xlabel="Principal Component ID", ylabel="Percentage of Variance")
    ax1.plot(array(range(1, 21)), percentage[:20], marker='^')
    
    ax2 = fig.add_subplot(122, xlabel="Principal Component Number", ylabel="Cumulative Variance")
    ax2.plot(array(range(1, 21)), cumulative[:20], marker = '^')
    
    plt.show()
    

dataMat = replaceNanWithMean()
meanVals = mean(dataMat, axis = 0)
meanRemoved = dataMat - meanVals
covMat = cov(meanRemoved, rowvar = 0)
eigVals, eigVects = linalg.eig(mat(covMat))
plotPCNum(eigVals)

# dataMat = loadDataSet('testSet.txt')
# lowDMat, reconMat = pca(dataMat, 1)
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s = 90)
# ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s = 50, c = 'red')
# plt.show()