#coding:utf-8

##################################################
# 定义M500 车机行驶过程中产生的数据类
##################################################
import datetime
import json
import time


class ProtocolSimulaterDataService():
    def __init__(self,path="/data/protocolTools/carData/",fileName="default.json"):
        self.data = {}
        self.path = path                                                               #保存车机数据文件地址
        self.fileName = fileName                                                       #保存车机数据文件

    def setPath(self,data):
        self.path = data
    def setFileName(self,data):
        self.fileName = data
    def setData(self,data):
        self.data = self.fixDataTemplate(data)

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
        data["travelData"]["totalMilleage"] = 0                                        #行驶总里程
        data["travelData"]["totalOil"] = 0                                             #行驶总油耗
        data["travelData"]["totalTime"] = 0                                            #行驶总时间
        data["event"] = {}
        data["event"]["threeRapid"] = {}                                               #急加速，急减速，急转弯基本数据
        data["event"]["threeRapid"]["totalRapidlyAccelerate"] = 0                      #急加速总次数
        data["event"]["threeRapid"]["totalSharpSlowdown"] = 0                          #急减速总次数
        data["event"]["threeRapid"]["totalSharpTurn"] = 0                              #急转弯总次数
        return data
    ####################################################
    # 修复默认数据模板
    # 用于在升级模拟器的时候，对增加的字段进行初始化
    ####################################################
    def fixDataTemplate(self,data):
        if not "event" in data:
            data["event"] = {}
            data["event"]["threeRapid"] = {}
            data["event"]["threeRapid"]["totalRapidlyAccelerate"] = 0                          # 急加速总次数
            data["event"]["threeRapid"]["totalSharpSlowdown"] = 0                              # 急减速总次数
            data["event"]["threeRapid"]["totalSharpTurn"] = 0                                  # 急转弯总次数
            if not "threeRapid" in data["event"]:
                data["event"]["threeRapid"] = {}
                data["event"]["threeRapid"]["totalRapidlyAccelerate"] = 0                      #急加速总次数
                data["event"]["threeRapid"]["totalSharpSlowdown"] = 0                          #急减速总次数
                data["event"]["threeRapid"]["totalSharpTurn"] = 0                              #急转弯总次数
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

    #设置急加速总次数，同时写入文件
    def setTotalRapidlyAccelerateCount(self,data):
        if not "event" in data:
            data["event"] = {}
            if not "threeRapid" in data["event"]:
                data["event"]["threeRapid"] = {}
        data["event"]["threeRapid"]["totalRapidlyAccelerate"] = data
        self.writeToFile(self.path + self.fileName, self.data)
    # 设置急减速总次数，同时写入文件
    def setTotalSharpSlowdown(self,data):
        if not "event" in data:
            data["event"] = {}
            if not "threeRapid" in data["event"]:
                data["event"]["threeRapid"] = {}
        data["event"]["threeRapid"]["totalSharpSlowdown"] = data
        self.writeToFile(self.path + self.fileName, self.data)
    # 设置急转弯总次数，同时写入文件
    def setTotalSharpTurn(self,data):
        if not "event" in data:
            data["event"] = {}
            if not "threeRapid" in data["event"]:
                data["event"]["threeRapid"] = {}
        data["event"]["threeRapid"]["totalSharpTurn"] = data
        self.writeToFile(self.path + self.fileName, self.data)

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
    # 将数据持久化到已经设定好的文件
    ####################################################
    def setData2file(self):
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
                self.setData2file(dateM)
                self.setTime2file(timeM)
            conJson = self.fixDataTemplate(conJson)                       #每次读取，都会对数据进行修复
            self.data = conJson


if __name__ == "__main__":
    print(ProtocolSimulaterDataService().genDataTemplate())
    data = ProtocolSimulaterDataService().genDataTemplate()
    ProtocolSimulaterDataService().writeToFile("../../../data/protocolTools/carData/M202003060520.json",data)