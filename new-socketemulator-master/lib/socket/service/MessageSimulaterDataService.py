#coding:utf-8

##################################################
# 定义车安优 车机行驶过程中产生的数据类
##################################################
import datetime
import json
import time


class MessageSimulaterDataService():
    def __init__(self,path="/data/protocolTools/carData/",fileName="default.json"):
        self.data = {}
        self.path = path                                                               #保存车机数据文件地址
        self.fileName = fileName                                                       #保存车机数据文件

    def setPath(self,data):
        self.path = data
    def setFileName(self,data):
        self.fileName = data
    def setData(self,data):
        self.data = data

    ####################################################
    # 生成一个默认数据模板
    ####################################################
    def genDataTemplate(self):
        data = {}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        data["time"] = {}                                                              #定义时间数据项
        data["time"]["dateTime"] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["time"]["date"] = time.strftime("%Y-%m-%d", timeArray)
        data["time"]["time"] = time.strftime("%H:%M:%S", timeArray)
        data["curDayTravel"] = {}                                                      #定义当天行驶数据项
        data["curDayTravel"]["todayTotalMilleage"] = 0                                 #今日行驶总里程
        data["curDayTravel"]["todayTotalOil"] = 0                                      #今日行驶总油耗
        data["curDayTravel"]["todayTotalTime"] = 0                                     #今日行驶总时间
        data["curDayTravel"]["theMilleage"] = 0                                        #本次行驶总里程
        data["curDayTravel"]["theOil"] = 0                                             #本次行驶总油耗
        data["curDayTravel"]["theTime"] = 0                                            #本次行驶总时间
        data["travelData"] = {}                                                        #定义所有行驶数据
        data["travelData"]["totalMilleage"] = 0                                       #行驶总里程
        data["travelData"]["totalOil"] = 0                                             #行驶总油耗
        data["travelData"]["totalTime"] = 0                                            #行驶总时间
        return data

    #设今日行驶总里程，同时写入文件
    def setTodayTotalMilleage(self,data):
        self.data["curDayTravel"]["todayTotalMilleage"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设今日行驶总油耗，同时写入文件
    def setTodayTodayTotalOil(self,data):
        self.data["curDayTravel"]["todayTotalOil"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设今日行驶总时间，同时写入文件
    def setTodayTodayTotalTime(self,data):
        self.data["curDayTravel"]["todayTotalTime"] = data
        self.writeToFile(self.path + self.fileName,self.data)

    #设本次行驶总里程，同时写入文件
    def setTheMilleage(self,data):
        self.data["curDayTravel"]["theMilleage"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设本次行驶总油耗，同时写入文件
    def setTheOil(self,data):
        self.data["curDayTravel"]["theOil"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设本次行驶总时间，同时写入文件
    def setTheTime(self,data):
        self.data["curDayTravel"]["theTime"] = data
        self.writeToFile(self.path + self.fileName,self.data)

    #设总里程，同时写入文件
    def setTotalMilleage(self,data):
        self.data["travelData"]["totalMilleage"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设总油耗，同时写入文件
    def setTotalOil(self,data):
        self.data["travelData"]["totalOil"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设总时间，同时写入文件
    def setTotalTime(self,data):
        self.data["travelData"]["totalTime"] = data
        self.writeToFile(self.path + self.fileName,self.data)

    #设今日日期时间
    def setDateTime2file(self,data):
        self.data["time"]["dateTime"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设今日日期
    def setDate2file(self,data):
        self.data["time"]["date"] = data
        self.writeToFile(self.path + self.fileName,self.data)
    #设今日时间
    def setTime2file(self,data):
        self.data["time"]["time"] = data
        self.writeToFile(self.path + self.fileName,self.data)


    ####################################################
    # 将数据写入文件
    ####################################################
    def writeToFile(self,path,data):
        with open(path,"w",encoding="utf-8") as fi:
            data = json.dumps(data)
            fi.write(data)

    ####################################################
    # 从文件读取数据
    ####################################################
    def readFromFile(self,path):
        with open(path, "r", encoding="utf-8") as fi:
            content = fi.read()
            conJson = json.loads(content)
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            dateTimeM = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            dateM = time.strftime("%Y-%m-%d", timeArray)
            timeM = time.strftime("%H:%M:%S", timeArray)
            if dateM == conJson["time"]["date"]:
                pass
            else:                                                          #如果不是当天日期，则将日期设置为当天
                conJson["time"]["dateTime"] = dateTimeM
                conJson["time"]["date"] = dateM
                conJson["time"]["time"] = timeM
                data["curDayTravel"]["todayTotalMilleage"] = 0             # 今日行驶总里程
                data["curDayTravel"]["todayTotalOil"] = 0                  # 今日行驶总油耗
                data["curDayTravel"]["todayTotalTime"] = 0                 # 今日行驶总时间
                self.setTodayTotalMilleage(0)
                self.setTodayTodayTotalOil(0)
                self.setTodayTodayTotalTime(0)
                self.setDateTime2file(dateTimeM)
                self.setDate2file(dateM)
                self.setTime2file(timeM)
            self.data = conJson


if __name__ == "__main__":
    print(MessageSimulaterDataService().genDataTemplate())
    data = MessageSimulaterDataService().genDataTemplate()
    MessageSimulaterDataService().writeToFile("../../../data/protocolTools/carData/M202003060520.json",data)