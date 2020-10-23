#coding:utf-8

'''
M300车机模拟服务类
'''
import binascii
import json
import math
import os
import threading
import time
import traceback
from time import sleep

from lib.protocol.m300.Alarm_protocol_m300 import Alarm_protocol_m300
from lib.protocol.m300.GPS_protocol_m300 import GPS_protocol_m300
from lib.protocol.m300.Login_protocol_m300 import Login_protocol_m300
from lib.protocol.m300.OBDCAN_protocol_m300 import OBDCAN_protocol_m300
from lib.protocol.m300.VersionInfo_protocol_m300 import VersionInfo_protocol_m300
from lib.socket.service.M300SimulaterDataService import M300SimulaterDataService
from lib.socket.service.websocket_service import Websocket_service
from lib.util.util import strAddSpace


class M300SimulaterService():
    def __init__(self):
        self.data = {}                       #用来接收模拟器传过来的参数
        self.carData = {}                    #保存车辆行驶数据
        self.carDataObj = None               #管理车辆行驶数据对象
        self.socket = None
        self.sendDur = 5                     #设置默认多久发一条消息
        self.serviceStatus = 0               #服务状态，0表示未启动，1表示启动
        self.websocket = None                #网页与服务的通信socket
        self.websocketId = ""               # 当前连接的webSocketId
        self.timeout = 1                     #socket的超时时间
        self.gpsLine = []                    #GPS 轨迹
        self.gpsLineIndex = 0                #GPS 轨迹索引
        self.travelStatus = 0                #0，表示未行驶，1表示开始行驶同时开启了接收消息服务，2表示值开启了接收消息的服务
        self.carId = ""                      #车机号
        self.sn = 0                          #消息流水号
        self.travelDirection = 0             #行驶方向，0表示正向行驶，1表示反向行驶
        self.directAngle = 59                #定义默认方向角
        '''
        为0表示正常发送，type为1表示数据写入本地
        # 用来控制发送消息的方式（是正常发送，还是将发送的数据保存到本地，不发送）
        '''
        self.sendType = 0
        self.GPSValid = 1                    #用来控制GPS数据是有效还是无效    0：无效     1：有效
        self.lngLatIsOk = 1                  #用来控制经纬度是否都为0          0：都为0    1：正常
        # 定义要发送的obd数据
        self.OBDdata = {"accStatus":1,"engineSpeed":300,"speed":0,"dashboardTotailMilleage":6000,"totalMilleage":60,"totalOil":30,"carTotalRunTime":10}
        # 定义初始的obd数据，与上面的OBD数据保持一致，主要用于汽车行驶过程中数据变化量的计算
        self.OBDdataOri = {"accStatus":1,"engineSpeed": 300, "speed": 0,"dashboardTotailMilleage": 6000, "totalMilleage":60,"totalOil": 30, "carTotalRunTime": 10}

    def getSn(self):
        return self.sn
    def getWebsocket(self):
        return self.websocket
    def getTravelStatus(self):
        return self.travelStatus
    def getCurLatitude(self):
        return self.gpsLine[self.gpsLineIndex]["lat"]
    def getCurLongtitude(self):
        return self.gpsLine[self.gpsLineIndex]["lng"]
    def getCarData(self):
        return self.carData
    def getSpeed(self):
        return int(self.data["travelData"]["carSpeed"])


    #设置套接字
    def setSocket(self,data):
        self.socket = data
    def setSendDur(self,data):
        self.sendDur = data
    def setTimeout(self,data):
        self.timeout = data
    def setCarId(self,data):
        self.carId = data
    def setData(self,data):
        self.data = data
    def setCarData(self,data):
        self.carData = data
    def setWebsocketId(self):
        sleep(1)
        self.websocketId = self.websocket.getCurrentClientId()
        print(self.websocketId)
    def setWebsocket(self,data):
        self.websocket = data
    def setSn(self,data):
        self.sn = data
    def setCarSpeed(self,data):
        self.data["travelData"]["carSpeed"] = data
    def setOilExpend(self,data):
        self.data["travelData"]["oilExpend"] = data
    def setSendDur(self,data):
        self.sendDur = data

    def sendMsg(self,msg):
        self.socket.setTimeOut(self.timeout)
        self.socket.send(msg)
    def revMsg(self):
        self.socket.setTimeOut(self.timeout)
        return self.socket.receive()
    #websocket向网页发送消息
    def serviceSendMsg(self,msg):
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        self.websocket.sendMsgToClient(">>>>" + type + "：" + msg,self.websocketId)

    ########################################################
    #车机登录
    ########################################################
    def carLogin(self):
        loginObj = Login_protocol_m300(waterCode=self.sn,DEV_ID=self.data["carId"])
        msg = loginObj.generateMsg()
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        info = type + ">>>>：" + msg
        self.websocket.sendMsgToClient(info,self.websocketId)
        self.sn = self.sn + 1
        time.sleep(0.5)

        self.data["version"]["SWVersion"] = strAddSpace(self.data["version"]["SWVersion"], 12)
        self.data["version"]["HWVersion"] = strAddSpace(self.data["version"]["HWVersion"], 4)
        self.data["version"]["GSMType"] = strAddSpace(self.data["version"]["GSMType"], 15)
        self.data["version"]["VINCode"] = strAddSpace(self.data["version"]["VINCode"], 20)

        verObj = VersionInfo_protocol_m300(waterCode=self.sn,DEV_ID=self.data["carId"],SWVersion=self.data["version"]["SWVersion"], \
                SWDate=self.data["version"]["SWDate"],HWVersion=self.data["version"]["HWVersion"], GSMType=self.data["version"]["GSMType"], \
                carType=int(self.data["version"]["carType"]),engineCode=int(self.data["version"]["engineCode"]),VINCode=self.data["version"]["VINCode"])
        msg = verObj.generateMsg()
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        info = type + ">>>>：" + msg
        self.websocket.sendMsgToClient(info, self.websocketId)
        self.sn = self.sn + 1

    ########################################################
    #车机点火
    ########################################################
    def fireOn(self):
        if not os.path.exists("data/m300Tools/carData/" + self.carId + ".json"):
            psdsObj = M300SimulaterDataService()
            data = psdsObj.genDataTemplate()
            psdsObj.writeToFile("data/m300Tools/carData/" + self.carId + ".json",data)
        #读取车机行驶数据
        with open("data/m300Tools/carData/" + self.carId + ".json", "r", encoding="utf-8") as fi:
            ############################# 读取车机的数据 ############################
            content = fi.read()
            conJson = json.loads(content)
            conJson["curDayTravel"]["theMilleage"] = 0                    # 本次行驶总里程
            conJson["curDayTravel"]["theOil"] = 0                         # 本次行驶总油耗
            conJson["curDayTravel"]["theTime"] = 0                        # 本次行驶总时间
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            dateTimeM = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            dateM = time.strftime("%Y-%m-%d", timeArray)
            timeM = time.strftime("%H:%M:%S", timeArray)
            dataFile = self.carId + ".json"
            self.carDataObj = M300SimulaterDataService("data/m300Tools/carData/", dataFile)
            self.carDataObj.setData(conJson)
            if dateM == conJson["time"]["date"]:
                self.OBDdata["totalMilleage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdataOri["totalMilleage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdata["totalOil"] = conJson["travelData"]["totalOil"]
                self.OBDdataOri["totalOil"] = conJson["travelData"]["totalOil"]
                self.OBDdata["carTotalRunTime"] = conJson["travelData"]["totalTime"]
                self.OBDdataOri["carTotalRunTime"] = conJson["travelData"]["totalTime"]
            else:                                                             #如果不是当天日期，则将日期设置为当天，并写入车辆数据文件
                conJson["curDayTravel"]["todayTotalMilleage"] = 0  # 今日行驶总里程
                conJson["curDayTravel"]["todayTotalOil"] = 0  # 今日行驶总油耗
                conJson["curDayTravel"]["todayTotalTime"] = 0  # 今日行驶总时间
                self.carDataObj.setTodayTotalMilleage(0)
                self.carDataObj.setTodayTodayTotalOil(0)
                self.carDataObj.setTodayTodayTotalTime(0)
                self.carDataObj.setDateTime2file(dateTimeM)
                self.carDataObj.setDate2file(dateM)
                self.carDataObj.setTime2file(timeM)
                self.OBDdata["totalMilleage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdataOri["totalMilleage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdata["totalOil"] = conJson["travelData"]["totalOil"]
                self.OBDdataOri["totalOil"] = conJson["travelData"]["totalOil"]
                self.OBDdata["carTotalRunTime"] = conJson["travelData"]["totalTime"]
                self.OBDdataOri["carTotalRunTime"] = conJson["travelData"]["totalTime"]
            self.carData = self.carDataObj.fixDataTemplate(conJson)
            # self.carData = conJson

            ############################# 发送点火数据 ############################
            fireOnParams = {"FUNID": "0021", "waterCode": "1", "DEV_ID": "M202004070000", "encryptionType": "0",
             "GPSData": {"dateInfo": "2020-05-29 15:23:48", "latitude": 40.22077, "longitude": 116.23128,
                         "positionStar": "2", "speed": "66.0", "direction": "55.3", "altitude": "11.0",
                         "ACCStatus": "1", "valtage": "36.0", "OBDSpeed": "66.4", "valid": 1, "tripMark": "0"},
             "OBDCANData": {"statusMask": "ffffffffffffffffffff", "safeStatus": 0, "doorStatus": 0, "lockStatus": 0,
                            "windowStatus": 0, "lightStatus": 0, "swichStatusA": 0, "swichStatusB": 0},
             "GSMData": {"operatorType": "1", "LAC": "1234", "CellId": "5678"}, "alarm": {"0001": {}}}
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            fireOnParams["DEV_ID"] = self.data["carId"]
            fireOnParams["waterCode"] = self.sn
            fireOnParams["GPSData"]["dateInfo"] = curTime
            fireOnParams["GPSData"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
            fireOnParams["GPSData"]["longitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
            fireOnParams["GPSData"]["direction"] = self.getDirAngle()
            msgObj = Alarm_protocol_m300(data=fireOnParams)
            msg = msgObj.generateMsg()
            self.sendMsg(msg)
            type = self.getMsgFunId(msg)
            info = type + ">>>>：" + msg
            self.websocket.sendMsgToClient(info,self.websocketId)
            self.sn = self.sn + 1
            time.sleep(0.1)

            gpsMsg = self.genGPSMsg(float(self.gpsLine[0]["lat"]), float(self.gpsLine[0]["lng"]))
            type = self.getMsgFunId(gpsMsg)
            self.sendMsg(gpsMsg)
            self.sn = self.sn + 1
            self.websocket.sendMsgToClient(type + ">>>>：" + gpsMsg, self.websocketId)
            sleep(0.1)
            OBDMsg = self.genOBDMsg(1, self.OBDdata["engineSpeed"],self.OBDdata["speed"], self.OBDdata["dashboardTotailMilleage"], \
                                    self.OBDdata["totalMilleage"],self.OBDdata["totalOil"], self.OBDdata["carTotalRunTime"])
            type = self.getMsgFunId(OBDMsg)
            self.sendMsg(OBDMsg)
            self.sn = self.sn + 1
            self.websocket.sendMsgToClient(type + ">>>>：" + OBDMsg, self.websocketId)

    ########################################################
    #车机行驶服务
    ########################################################
    def serviceTrave(self):
        while self.serviceStatus == 1:
            gpsMsg = ""
            OBDMsg = ""
            if self.travelStatus == 0:                                                                 #行驶服务未启动
                latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                gpsMsg = self.genGPSMsg(latitude,longitude)
            elif self.travelStatus == 1:                                                               #行驶服务启动
                if self.gpsLineIndex < len(self.gpsLine) and self.gpsLineIndex != -1:                  #如果正向行驶和反向行驶的轨迹点都没有跑完
                    OBDMsg = self.genOBDMsg(1, self.OBDdata["engineSpeed"], self.OBDdata["speed"],self.OBDdata["dashboardTotailMilleage"], \
                                            self.OBDdata["totalMilleage"], self.OBDdata["totalOil"],self.OBDdata["carTotalRunTime"])
                    self.OBDdata["engineSpeed"] = 3000
                    self.OBDdata["speed"] = int(self.data["travelData"]["carSpeed"])
                    self.OBDdata["dashboardTotailMilleage"] = self.OBDdata["dashboardTotailMilleage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
                    self.OBDdata["totalMilleage"] = self.OBDdata["totalMilleage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000  / 3600))
                    oilExpend = int(self.data["travelData"]["oilExpend"])
                    self.OBDdata["totalOil"] = self.OBDdata["totalOil"] + int((self.sendDur * (self.OBDdata["speed"] * 1000 / 3600)) * (1000 / (oilExpend *1000)))
                    self.OBDdata["carTotalRunTime"] = self.OBDdata["carTotalRunTime"] + self.sendDur
                    latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                    longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                    gpsMsg = self.genGPSMsg(latitude, longitude)
                    if self.travelDirection == 0:
                        self.gpsLineIndex = self.gpsLineIndex + 1     #正向行驶
                    else:
                        self.gpsLineIndex = self.gpsLineIndex - 1     #反向行驶
                elif self.gpsLineIndex == len(self.gpsLine) or self.gpsLineIndex == -1:               #如果反向行驶和反向行驶刚好跑完
                    if int(self.data["travelData"]["travelLoop"]) == 0:                               #没有设置循环行驶
                        self.gpsLineIndex = self.gpsLineIndex - 1
                        self.stopTravel()
                        self.websocket.sendMsgToClient("gps轨迹跑完，自动停止行驶！",self.websocketId)
                    else:                                                                             #设置了循环行驶
                        if self.travelDirection == 0:
                            self.gpsLineIndex = self.gpsLineIndex - 1
                            self.travelDirection = 1
                            self.websocket.sendMsgToClient("gps轨迹正向行驶跑完，变换行驶方向......",self.websocketId)
                        else:
                            self.gpsLineIndex = self.gpsLineIndex + 1
                            self.travelDirection = 0
                            self.websocket.sendMsgToClient("gps轨迹反向行驶跑完，变换行驶方向......",self.websocketId)
                        OBDMsg = self.genOBDMsg(1, self.OBDdata["engineSpeed"], self.OBDdata["speed"],self.OBDdata["dashboardTotailMilleage"], \
                                                self.OBDdata["totalMilleage"], self.OBDdata["totalOil"],self.OBDdata["carTotalRunTime"])
                        self.OBDdata["engineSpeed"] = 3000
                        self.OBDdata["speed"] = int(self.data["travelData"]["carSpeed"])
                        self.OBDdata["dashboardTotailMilleage"] = self.OBDdata["dashboardTotailMilleage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
                        self.OBDdata["totalMilleage"] = self.OBDdata["totalMilleage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
                        oilExpend = int(self.data["travelData"]["oilExpend"])
                        self.OBDdata["totalOil"] = self.OBDdata["totalOil"] + int((self.sendDur * (self.OBDdata["speed"] * 1000 / 3600)) * (1000 / (oilExpend * 1000)))
                        self.OBDdata["carTotalRunTime"] = self.OBDdata["carTotalRunTime"] + self.sendDur
                        latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                        longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                        gpsMsg = self.genGPSMsg(latitude, longitude)
                self.carDataObj.setTodayTotalMilleage(self.carData["curDayTravel"]["todayTotalMilleage"] + self.OBDdata["totalMilleage"] - self.OBDdataOri["totalMilleage"])
                self.carDataObj.setTheMilleage(self.carData["curDayTravel"]["theMilleage"] + self.OBDdata["totalMilleage"] -self.OBDdataOri["totalMilleage"])
                self.carDataObj.setTotalMilleage(self.carData["travelData"]["totalMilleage"] + self.OBDdata["totalMilleage"] - self.OBDdataOri["totalMilleage"])
                temp = self.OBDdata["totalMilleage"]
                self.OBDdataOri["totalMilleage"] = temp
                self.carDataObj.setTodayTodayTotalOil(self.carData["curDayTravel"]["todayTotalOil"] + self.OBDdata["totalOil"] - self.OBDdataOri["totalOil"])
                self.carDataObj.setTheOil(self.carData["curDayTravel"]["theOil"] + self.OBDdata["totalOil"] - self.OBDdataOri["totalOil"])
                self.carDataObj.setTotalOil(self.carData["travelData"]["totalOil"] + self.OBDdata["totalOil"] - self.OBDdataOri["totalOil"])
                self.OBDdataOri["totalOil"] = self.OBDdata["totalOil"]
                self.carDataObj.setTodayTodayTotalTime(self.carData["curDayTravel"]["todayTotalTime"] + self.OBDdata["carTotalRunTime"] - self.OBDdataOri["carTotalRunTime"])
                self.carDataObj.setTheTime(self.carData["curDayTravel"]["theTime"] + self.OBDdata["carTotalRunTime"] - self.OBDdataOri["carTotalRunTime"])
                self.carDataObj.setTotalTime(self.carData["travelData"]["totalTime"] + self.OBDdata["carTotalRunTime"] - self.OBDdataOri["carTotalRunTime"])
                self.OBDdataOri["carTotalRunTime"] = self.OBDdata["carTotalRunTime"]
            if OBDMsg != "":
                self.sendMsg(OBDMsg)
                self.sn = self.sn + 1
                type = self.getMsgFunId(OBDMsg)
                info = type + ">>>>：" + OBDMsg
                self.websocket.sendMsgToClient(info,self.websocketId)
            if gpsMsg != "":
                sleep(0.1)
                self.sendMsg(gpsMsg)
                self.sn = self.sn + 1
                type = self.getMsgFunId(gpsMsg)
                info = type + ">>>>：" + gpsMsg
                self.websocket.sendMsgToClient(info,self.websocketId)
            sleep(self.sendDur)

    # 熄火，发送熄火事件
    def fireOff(self):
        gpsLineIndex = self.gpsLineIndex
        if gpsLineIndex >= len(self.gpsLine):
            gpsLineIndex = gpsLineIndex - 1

        fireOffParams = {"FUNID": "0021", "waterCode": "1", "DEV_ID": "M202004070000", "encryptionType": "0",
         "GPSData": {"dateInfo": "2020-05-29 15:23:48", "latitude": 40.22077, "longitude": 116.23128,
                     "positionStar": "2", "speed": "66.0", "direction": "55.3", "altitude": "11.0",
                     "ACCStatus": "1", "valtage": "36.0", "OBDSpeed": "66.4", "valid": 1, "tripMark": "0"},
         "OBDCANData": {"statusMask": "ffffffffffffffffffff", "safeStatus": 0, "doorStatus": 0, "lockStatus": 0,
                        "windowStatus": 0, "lightStatus": 0, "swichStatusA": 0, "swichStatusB": 0},
         "GSMData": {"operatorType": "1", "LAC": "1234", "CellId": "5678"}, "alarm": {"0002": {}}}
        timeStamp = time.time() - 8 * 3600
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        fireOffParams["DEV_ID"] = self.data["carId"]
        fireOffParams["waterCode"] = self.sn
        fireOffParams["GPSData"]["dateInfo"] = curTime
        fireOffParams["GPSData"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
        fireOffParams["GPSData"]["longitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
        fireOffParams["GPSData"]["direction"] = self.getDirAngle()
        msgObj = Alarm_protocol_m300(data=fireOffParams)
        msg = msgObj.generateMsg()
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        info = type + ">>>>：" + msg
        self.websocket.sendMsgToClient(info,self.websocketId)
        self.sn = self.sn + 1
        # time.sleep(0.1)
        # gpsMsg = self.genGPSMsg(float(self.gpsLine[0]["lat"]), float(self.gpsLine[0]["lng"]))
        # type = self.getMsgFunId(gpsMsg)
        # self.sendMsg(gpsMsg)
        # self.sn = self.sn + 1
        # self.websocket.sendMsgToClient(type + ">>>>：" + gpsMsg, self.websocketId)
        # sleep(0.1)
        # OBDMsg = self.genOBDMsg(0, self.OBDdata["engineSpeed"],self.OBDdata["speed"], self.OBDdata["dashboardTotailMilleage"], \
        #                         self.OBDdata["totalMilleage"], self.OBDdata["totalOil"], self.OBDdata["carTotalRunTime"])
        # type = self.getMsgFunId(OBDMsg)
        # self.sendMsg(OBDMsg)
        # self.sn = self.sn + 1
        # self.websocket.sendMsgToClient(type + ">>>>：" + OBDMsg, self.websocketId)

    #根据特定参数，生成GPS消息
    def genGPSMsg(self,latitude,longtitude):
        gpsObj = GPS_protocol_m300(waterCode=self.sn,DEV_ID=self.data["carId"])
        gpsObj.setLatitude(float(latitude))
        gpsObj.setLongitude(float(longtitude))
        gpsObj.setDirection(self.getDirAngle())
        timeS = int(time.time()) - 8 * 3600
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        gpsObj.setDateInfo(UTCTime)
        msg = gpsObj.generateMsg()
        return msg
    #根据特定参数，生成GPS消息体，不包含消息头
    def genGPSData(self,latitude,longtitude):
        gpsObj = GPS_protocol_m300(waterCode=self.sn,DEV_ID=self.data["carId"])
        gpsObj.setLatitude(float(latitude))
        gpsObj.setLongitude(float(longtitude))
        gpsObj.setDirection(self.getDirAngle())
        timeS = int(time.time()) - 8 * 3600
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        gpsObj.setDateInfo(UTCTime)
        data = gpsObj.generateMsg()
        return data
    #根据当前所在GPS点，生成GPS消息体，不包含消息头
    def genGPSData2(self):
        gpsObj = GPS_protocol_m300(waterCode=self.sn,DEV_ID=self.data["carId"])
        gpsObj.setLatitude(self.gpsLine[self.gpsLineIndex]["lat"])
        gpsObj.setLongitude(self.gpsLine[self.gpsLineIndex]["lng"])
        gpsObj.setDirection(self.getDirAngle())
        timeS = int(time.time()) - 8 * 3600
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        gpsObj.setDateInfo(UTCTime)
        data = gpsObj.generateMsg()
        return data

    # 根据特定参数，生成OBD CAN消息
    def genOBDMsg(self,accStatus=1,engineSpeed=300,speed=0,dashboardTotailMilleage=6000,totalMilleage=60,totalOil=30,carTotalRunTime=10):
        OBDObj = OBDCAN_protocol_m300(waterCode=self.sn,DEV_ID=self.data["carId"])
        timeS = int(time.time()) - 8 * 3600
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        OBDObj.setTimeInfo(UTCTime)
        OBDObj.setAccstatus(accStatus)
        OBDObj.setEngineSpeed(engineSpeed)                            # 设置发动机转速
        OBDObj.setSpeed(speed)                                        # 设置车辆速度
        OBDObj.setDashboardTotailMilleage(dashboardTotailMilleage)    # 设置仪表里程值
        OBDObj.setTotalMilleage(totalMilleage)                        # 设置总里程值
        OBDObj.setTotalOil(totalOil)                                  # 设置总耗油量
        OBDObj.setCarTotalRunTime(carTotalRunTime)                    # 设置车辆运行时间
        msg = OBDObj.generateMsg()
        return msg

    ###########################################################
    #获取方向角
    ###########################################################
    def getDirAngle(self):
        dire = self.directAngle
        if self.travelDirection == 0:
            if self.gpsLineIndex == 0:
                return int(self.directAngle)
            lngCut = (float(self.gpsLine[self.gpsLineIndex]["lng"]) - float(self.gpsLine[self.gpsLineIndex - 1]["lng"])) * 1000000
            latCut = (float(self.gpsLine[self.gpsLineIndex]["lat"]) - float(self.gpsLine[self.gpsLineIndex - 1]["lat"])) * 1000000
            if latCut == 0:   #除数维度不能为0
                latCut = 1
            if lngCut == 0 or latCut == 0:
                return int(self.directAngle)
            val = lngCut / latCut
            dire = math.atan2(1, val) * 180 / math.pi
            if lngCut > 0 and latCut > 0:
                dire = 90 - dire
            if lngCut < 0 and latCut > 0:
                dire = 270 + 180 - dire
            elif latCut < 0 and lngCut > 0:
                dire = 270 - dire
            elif lngCut < 0 and latCut < 0:
                dire = 180 + 90 - dire
            self.directAngle = dire
        elif self.travelDirection == 1:
            if self.gpsLineIndex == (len(self.gpsLine) - 1):
                return int(self.directAngle)
            lngCut = (float(self.gpsLine[self.gpsLineIndex]["lng"]) - float(self.gpsLine[self.gpsLineIndex + 1]["lng"])) * 1000000
            latCut = (float(self.gpsLine[self.gpsLineIndex]["lat"]) - float(self.gpsLine[self.gpsLineIndex + 1]["lat"])) * 1000000
            if latCut == 0:   #除数维度不能为0
                latCut = 1
            if lngCut == 0 or latCut == 0:
                return int(self.directAngle)
            val = lngCut / latCut
            dire = math.atan2(1, val) * 180 / math.pi
            if lngCut > 0 and latCut > 0:
                dire = 90 - dire
            if lngCut < 0 and latCut > 0:
                dire = 270 + 180 - dire
            elif latCut < 0 and lngCut > 0:
                dire = 270 - dire
            elif lngCut < 0 and latCut < 0:
                dire = 180 + 90 - dire
            self.directAngle = dire
        return int(dire)





    ########################################################
    # 接收消息的服务
    ########################################################
    def serviceRev(self):
        self.serviceStatus = 2              #2代表只启动了接收消息的进程，1代表了接收和发送都启动了
        while self.serviceStatus != 0:
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            self.socket.setTimeOut(self.timeout)
            d = self.revMsg()
            d = str(binascii.b2a_hex(d))[2:][:-1]
            type = self.getMsgFunId(d)
            info = type + "<<<<：" + d
            self.websocket.sendMsgToClient(info,self.websocketId)
            self.doResponse(d)

    ########################################################
    #启动与页面交互的websockt服务
    ########################################################
    def websocketService(self):
        self.websocket = Websocket_service()
        self.websocket.setHost("0.0.0.0")
        self.websocket.setPort(5009)
        self.websocket.startWebsocketServer()

    ########################################################
    #启动与页面交互的websocket服务
    ########################################################
    def startWebsocketService(self):
        time.sleep(0.5)
        if self.websocket == None:
            t = threading.Thread(target=self.websocketService, args=())
            t.start()
            t3 = threading.Thread(target=self.setWebsocketId, args=())
            t3.start()

    # 为websocket服务添加一个新的客户端连接
    def addNewWebsocket(self):
        t3 = threading.Thread(target=self.setWebsocketId, args=())
        t3.start()

    ########################################################
    #停止websocket服务
    ########################################################
    def stopWebsocketService(self):
        try:
            self.websocket.close()
            self.websocket = None
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()

    ########################################################
    #关闭车机的连接
    ########################################################
    def closeSocket(self):
        try:
            self.socket.close()
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc

    ########################################################
    #获取收到消息的功能id
    ########################################################
    def getMsgFunId(self,msg):
        funId = msg[2:6]
        return funId

    ########################################################
    #收到 某些类型的消息后执行回复操作
    ########################################################
    def doResponse(self,msg):
        msgFunId = self.getMsgFunId(msg)

    #设置GPS轨迹
    def setGpsLine(self,fileName):
        with open("data/m300Tools/GPSLines/" + fileName,"r",encoding="utf-8") as fi:
            content = fi.read()
            conJson = json.loads(content)
            self.gpsLine = conJson["GPSLine"]

    ########################################################
    #启动接收消息的服务
    ########################################################
    def startReciveService(self):
        t2 = threading.Thread(target=self.serviceRev, args=())
        t2.start()

    ########################################################
    # 开启发送消息的服务
    ########################################################
    def startService(self):
        self.serviceStatus = 1
        t1 = threading.Thread(target=self.serviceTrave,args=())
        t1.start()

    ########################################################
    #停止发送消息的服务
    ########################################################
    def stopService(self):
        self.serviceStatus = 0
        self.gpsLine = []
        self.gpsLineIndex = 0
        self.travelStatus = 0

    ########################################################
    # 开始行驶
    ########################################################
    def startTravel(self):
        self.travelStatus = 1

    ########################################################
    # 停止行驶
    ########################################################
    def stopTravel(self):
        self.travelStatus = 0
        self.serviceStatus = 0