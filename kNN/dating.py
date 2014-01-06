'''
Created on 2014-1-2

@author: lenovo
'''
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import operator
from kNN import *

def plotData(matrix, label):
    colorDict = {'didntLike':'r', 'smallDoses':'b', 'largeDoses':'g'}
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(matrix[:, 0], matrix[:, 1], 20, map(lambda x: colorDict[x], label))
    plt.show()
    
def file2matrix(filename):
    fr = open(filename)
    numOfLines = len(fr.readlines())
    returnMat = zeros((numOfLines, 3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(listFromLine[-1])
        index += 1
    return returnMat, classLabelVector


def datingClassTest():
    hoRatio = 0.002
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], \
                                     datingLabels[numTestVecs:m], 3)
        print "the classifier came back with: %s, the real answer is: %s" \
        % (classifierResult, datingLabels[i])
        if(classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))
    
def classifyPerson():
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([percentTats, ffMiles, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print "You will probably like this person: ", classifierResult

classifyPerson()