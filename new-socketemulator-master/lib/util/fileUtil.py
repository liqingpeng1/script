#coding:utf-8

'''
文件操作辅助类
'''
import os

###############################################
# 获取目录下的所有文件名
###############################################
def getDirFiles(filePath):
    files = os.listdir(filePath)
    return files
###############################################
# 获取目录下的所有文件名，去掉前缀
###############################################
def getDirFilesNoPrefix(filePath):
    files = os.listdir(filePath)
    for i in range(0,len(files)):
        files[i] = removeFilePrefix(files[i])
    return files
###############################################
# 获取目录下的所有文件名，以map形式
###############################################
def getDirFilesListMap(filePath):
    files = os.listdir(filePath)
    filesMap = {}
    for i in range(len(files) - 1,-1,-1):
        filesMap[files[i]] = removeSuffix(removeFilePrefix(files[i]))
    return filesMap

###############################################
# 文件名去掉前缀
###############################################
def removeFilePrefix(fileName):
    noPrefixFileName = fileName.split("_")[1]
    return noPrefixFileName

###############################################
# 获取当前目录前缀最大的文件
###############################################
def getMaxPrefixFile(filePath):
    theFileName = getDirFiles(filePath)[-1]
    return  theFileName

###############################################
# 获取当前目录前缀最大的文件的前缀
###############################################
def getMaxPrefixFilePre(filePath):
    fileList = getDirFiles(filePath)
    thePrefix = 0
    for temp in fileList:
        curPrefix = int(temp.split("_")[0])
        if thePrefix < curPrefix:
            thePrefix = curPrefix
    return thePrefix

###############################################
# 去掉文件后缀
###############################################
def removeSuffix(fileName):
    theFileName = fileName.split(".")[0]
    return theFileName

###############################################
# 删除文件
###############################################
def delFile(path,fileName):
    # fi = fileName + ".txt"
    fi = fileName
    theFile = path + fi
    if os.path.exists(theFile):
        os.remove(theFile)
    # fi = fileName + ".json"
    # theFile = path + fi
    # if os.path.exists(theFile):
    #     os.remove(theFile)



if __name__ == "__main__":
    # print(getDirFiles("../../data/protocolTools/GPSLines"))
    # print(getMaxPrefixFile("../../data/protocolTools/GPSLines"))
    # print(getMaxPrefixFilePre("../../data/protocolTools/GPSLines"))
    # print(getDirFilesNoPrefix("../../data/protocolTools/GPSLines"))
    # print(getDirFilesListMap("../../data/protocolTools/GPSLines"))
    delFile("../../data/protocolTools/GPSLines/","11_testLine")
