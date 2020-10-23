#coding:utf-8

'''
M500车机模拟服务类
'''
import binascii
import json
import math
import os
import threading
import time
import traceback
from time import sleep

from lib.protocol.report.EventReport_protocol import EventReport_protocol
from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.OBDReport_CAN_protocol import OBDReport_CAN_protocol
from lib.protocol.report.response.Common_response import Common_response
from lib.protocol.report.response.GPRS_response import GPRS_response
from lib.protocol.report.response.Update_response import Update_response
from lib.socket.service.ProtocolSimulaterDataService import ProtocolSimulaterDataService
from lib.socket.service.websocket_service import Websocket_service


class ProtocolSimulaterService():
    def __init__(self):
        self.data = {}                       #用来接收模拟器传过来的参数
        self.carData = {}                    #保存车辆行驶数据
        self.carDataObj = None               #管理车辆行驶数据对象
        self.socket = None
        self.sendDur = 5                     #设置默认多久发一条消息
        self.serviceStatus = 0               #服务状态，0表示未启动，1表示启动
        self.websocket = None                #网页与服务的通信socket
        self.websocketId = ""               #当前连接的webSocketId
        self.timeout = 1                     #socket的超时时间
        self.gpsLine = []                    #GPS 轨迹
        self.gpsLineIndex = 0                #GPS 轨迹索引
        self.travelStatus = 0                #0，表示未行驶，1表示开始行驶同时开启了接收消息服务，2表示值开启了接收消息的服务
        self.carId = ""                      #车机号
        self.sn = 0                          #消息流水号
        self.travelDirection = 0             #行驶方向，0表示正向行驶，1表示反向行驶
        self.directAngle = 60                #汽车方向角
        self.fixPosition = 0                 #是否固定当前GPS，0：否，1：是
        '''
        为0表示正常发送，type为1表示数据写入本地
        # 用来控制发送消息的方式（是正常发送，还是将发送的数据保存到本地，不发送）
        '''
        self.sendType = 0
        self.GPSValid = 1                    #用来控制GPS数据是有效还是无效    0：无效     1：有效
        self.lngLatIsOk = 1                  #用来控制经纬度是否都为0          0：都为0    1：正常
        self.hasOBD = 1                      #行驶数据是否包含obd数据         0：否      1：是
        # 定义要发送的obd数据
        self.OBDdata = {"fireStatus":1,"ACCStatus":0,"engineSpeed":3000,"speed":0,"meterMileage":6000,"totailMileage":600,"totalOilExpen":30,"totalRunTime":10,"surplusOil":505}
        # 定义初始的obd数据，与上面的OBD数据保持一致，主要用于汽车行驶过程中数据变化量的计算
        self.OBDdataOri = {"fireStatus": 1, "ACCStatus": 0, "engineSpeed": 3000, "speed": 0, "meterMileage": 6000,"totailMileage": 600, "totalOilExpen": 30, "totalRunTime": 10,"surplusOil":505}

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
    def setWebsocketId(self):
        sleep(0.5)
        self.websocketId = self.websocket.getCurrentClientId()
    def setWebsocket(self,data):
        self.websocket = data
    def setSn(self,data):
        self.sn = data
    def setCarData(self,data):
        self.carData = data
    def setServiceStatus(self,data):
        self.serviceStatus = data
    def setCarSpeed(self,data):
        self.data["travelData"]["carSpeed"] = data
    def setEngineSpeed(self,data):
        self.OBDdata["engineSpeed"] = data
    def setOilExpend(self,data):
        self.data["travelData"]["oilExpend"] = data
    def setSurplusOil(self,data):
        self.OBDdata["surplusOil"] = data
    def setSendDur(self,data):
        self.sendDur = int(data)
    def setSendType(self,data):
        self.sendType = data
    def setGPSValid(self,data):
        self.GPSValid = data
    def setLngLatIsOk(self,data):
        self.lngLatIsOk = data
    def setTravelDirection(self,data):
        self.travelDirection = data
    def setVoltage(self,data):
        self.data["other"]["valtage"] = data
    def setFixPosition(self,data):
        self.fixPosition = data
    def setHasOBD(self,data):
        self.hasOBD = data


    def getWebsocket(self):
        return self.websocket
    def getGpsLineIndex(self):
        return self.gpsLineIndex
    def getGpsLine(self):
        return self.gpsLine
    def getTravelStatus(self):
        return self.travelStatus
    def getSn(self):
        return self.sn
    def getCarData(self):
        return self.carData
    def getTravelDirection(self):
        return self.travelDirection
    def getLatitude(self):
        return self.gpsLine[self.gpsLineIndex]["lat"]
    def getLongitude(self):
        return self.gpsLine[self.gpsLineIndex]["lng"]

    #######################################################
    # type 为0表示正常发送，type为1表示数据写入本地
    #######################################################
    def sendMsg(self,msg):
        if self.sendType == 0:
            self.socket.setTimeOut(self.timeout)
            self.socket.send(msg)
        elif self.sendType == 1:
            msgId = self.getMsgFunId(msg)
            if msgId == "0021":
                self.saveMsgLocal("event.txt",msg)
            elif msgId == "0010":
                self.saveMsgLocal("gps.txt",msg)
            elif msgId == "0012":
                self.saveMsgLocal("obd.txt",msg)
    def revMsg(self):
        self.socket.setTimeOut(self.timeout)
        return self.socket.receive()
    #发送消息，可指定消息的描述类型
    def serviceSendMsg(self,msg,type):          #type字段目前废掉没有实际意
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        self.websocket.sendMsgToClient(">>>>" + type + "：" + msg,self.websocketId)

    def serviceSend(self):
        while self.serviceStatus == 1:
            gpsMsg = ""
            OBDMsg = ""
            if self.travelStatus == 0:                                                                 #行驶服务未启动
                latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                gpsMsg = self.genGPSMsg(latitude,longitude)
            elif self.travelStatus == 1:                                                               #行驶服务启动
                if self.gpsLineIndex < len(self.gpsLine) and self.gpsLineIndex != -1:                  #如果正向行驶和反向行驶的轨迹点都没有跑完
                    OBDMsg = self.genOBDMsg(self.OBDdata["fireStatus"],self.OBDdata["ACCStatus"],self.OBDdata["engineSpeed"], \
                                            self.OBDdata["speed"],self.OBDdata["meterMileage"],self.OBDdata["totailMileage"], \
                                            self.OBDdata["totalOilExpen"],self.OBDdata["totalRunTime"])
                    # self.OBDdata["engineSpeed"] = 3000
                    self.OBDdata["speed"] = int(self.data["travelData"]["carSpeed"])
                    self.OBDdata["meterMileage"] = self.OBDdata["meterMileage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
                    self.OBDdata["totailMileage"] = self.OBDdata["totailMileage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000  / 3600))
                    self.OBDdata["meterMileage"] = int(self.OBDdata["totailMileage"] / 1000)       #让仪表里程和总里程保持一致
                    oilExpend = int(self.data["travelData"]["oilExpend"])
                    self.OBDdata["totalOilExpen"] = self.OBDdata["totalOilExpen"] + int((self.sendDur * (self.OBDdata["speed"] * 1000 / 3600)) * (1000 / (oilExpend *1000)))
                    self.OBDdata["totalRunTime"] = self.OBDdata["totalRunTime"] + self.sendDur
                    latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                    longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                    # print("经度：" + str(longitude) + "   维度：" + str(latitude))
                    gpsMsg = self.genGPSMsg(latitude, longitude)
                    if self.fixPosition == 0:                             #是否固定当前位置的判断
                        if self.travelDirection == 0:
                            if self.gpsLineIndex < len(self.gpsLine):
                                self.gpsLineIndex = self.gpsLineIndex + 1     #正向行驶
                        else:
                            if self.gpsLineIndex > 0:
                                self.gpsLineIndex = self.gpsLineIndex - 1     #反向行驶
                elif self.gpsLineIndex == len(self.gpsLine) or self.gpsLineIndex == -1:               #如果反向行驶和反向行驶刚好跑完
                    if int(self.data["travelData"]["travelLoop"]) == 0:                               #没有设置循环行驶
                        if self.travelDirection == 0:
                            self.gpsLineIndex = self.gpsLineIndex - 1
                            self.stopTravel()
                            self.websocket.sendMsgToClient("gps轨迹跑完，自动停止行驶！",self.websocketId)
                        else:
                            self.gpsLineIndex = self.gpsLineIndex + 1
                            self.stopTravel()
                            self.websocket.sendMsgToClient("gps轨迹跑完，自动停止行驶！", self.websocketId)
                    else:                                                                             #设置了循环行驶
                        if self.travelDirection == 0:
                            self.gpsLineIndex = self.gpsLineIndex - 1
                            self.travelDirection = 1
                            self.websocket.sendMsgToClient("gps轨迹正向行驶跑完，变换行驶方向......",self.websocketId)
                        else:
                            self.gpsLineIndex = self.gpsLineIndex + 1
                            self.travelDirection = 0
                            self.websocket.sendMsgToClient("gps轨迹反向行驶跑完，变换行驶方向......",self.websocketId)
                        OBDMsg = self.genOBDMsg(self.OBDdata["fireStatus"], self.OBDdata["ACCStatus"],self.OBDdata["engineSpeed"], \
                                                self.OBDdata["speed"], self.OBDdata["meterMileage"],self.OBDdata["totailMileage"], \
                                                self.OBDdata["totalOilExpen"], self.OBDdata["totalRunTime"])
                        # self.OBDdata["engineSpeed"] = 3000
                        self.OBDdata["speed"] = int(self.data["travelData"]["carSpeed"])
                        self.OBDdata["meterMileage"] = self.OBDdata["meterMileage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
                        self.OBDdata["totailMileage"] = self.OBDdata["totailMileage"] + int(self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
                        self.OBDdata["meterMileage"] = int(self.OBDdata["totailMileage"] / 1000) # 让仪表里程和总里程保持一致
                        oilExpend = int(self.data["travelData"]["oilExpend"])
                        self.OBDdata["totalOilExpen"] = self.OBDdata["totalOilExpen"] + int((self.sendDur * (self.OBDdata["speed"] * 1000 / 3600)) * (1000 / (oilExpend * 1000)))
                        self.OBDdata["totalRunTime"] = self.OBDdata["totalRunTime"] + self.sendDur
                        latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                        longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                        gpsMsg = self.genGPSMsg(latitude, longitude)
                self.carDataObj.setTodayTotalMilleage(self.carData["curDayTravel"]["todayTotalMilleage"] + self.OBDdata["totailMileage"] - self.OBDdataOri["totailMileage"])
                self.carDataObj.setTheMilleage(self.carData["curDayTravel"]["theMilleage"] + self.OBDdata["totailMileage"] -self.OBDdataOri["totailMileage"])
                self.carDataObj.setTotalMilleage(self.carData["travelData"]["totalMilleage"] + self.OBDdata["totailMileage"] - self.OBDdataOri["totailMileage"])
                temp = self.OBDdata["totailMileage"]
                self.OBDdataOri["totailMileage"] = temp
                self.carDataObj.setTodayTodayTotalOil(self.carData["curDayTravel"]["todayTotalOil"] + self.OBDdata["totalOilExpen"] - self.OBDdataOri["totalOilExpen"])
                self.carDataObj.setTheOil(self.carData["curDayTravel"]["theOil"] + self.OBDdata["totalOilExpen"] - self.OBDdataOri["totalOilExpen"])
                self.carDataObj.setTotalOil(self.carData["travelData"]["totalOil"] + self.OBDdata["totalOilExpen"] - self.OBDdataOri["totalOilExpen"])
                self.OBDdataOri["totalOilExpen"] = self.OBDdata["totalOilExpen"]
                self.carDataObj.setTodayTodayTotalTime(self.carData["curDayTravel"]["todayTotalTime"] + self.OBDdata["totalRunTime"] - self.OBDdataOri["totalRunTime"])
                self.carDataObj.setTheTime(self.carData["curDayTravel"]["theTime"] + self.OBDdata["totalRunTime"] - self.OBDdataOri["totalRunTime"])
                self.carDataObj.setTotalTime(self.carData["travelData"]["totalTime"] + self.OBDdata["totalRunTime"] - self.OBDdataOri["totalRunTime"])
                self.OBDdataOri["totalRunTime"] = self.OBDdata["totalRunTime"]
            if OBDMsg != "":
                if self.hasOBD == 1:
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

    def serviceRev(self):
        self.serviceStatus = 2              #2代表只启动了接收消息的进程，1代表了接收和发送都启动了
        while self.serviceStatus != 0:
            self.socket.setTimeOut(self.timeout)
            d = self.revMsg()
            d = str(binascii.b2a_hex(d))[2:][:-1]
            type = self.getMsgFunId(d)
            info = type + "<<<<：" + d
            self.websocket.sendMsgToClient(info,self.websocketId)
            self.doResponse(d)

    #启动与页面交互的websockt服务
    def websocketService(self):
        self.websocket = Websocket_service()
        self.websocket.setHost("0.0.0.0")
        self.websocket.setPort(5005)
        self.websocket.startWebsocketServer()

    #启动定时发送消息和接收消息的服务
    def startService(self):
        self.serviceStatus = 1
        t1 = threading.Thread(target=self.serviceSend,args=())
        t1.start()

    #启动与页面交互的websocket服务
    def startWebsocketService(self):
        if self.websocket == None:
            t = threading.Thread(target=self.websocketService, args=())
            t.start()
            t2 = threading.Thread(target=self.serviceRev, args=())
            t2.start()
            t3 = threading.Thread(target=self.setWebsocketId, args=())
            t3.start()

    # 为websocket服务添加一个新的客户端连接
    def addNewWebsocket(self):
        t2 = threading.Thread(target=self.serviceRev, args=())
        t2.start()
        t3 = threading.Thread(target=self.setWebsocketId, args=())
        t3.start()

    #停止定时发送消息的服务
    def stopService(self):
        self.serviceStatus = 0
        self.gpsLine = []
        self.gpsLineIndex = 0
        self.travelStatus = 0

    def closeSocket(self):
        try:
            self.socket.close()
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()

    #停止websocket服务
    def stopWebsocketService(self):
        try:
            self.websocket.close()
            self.websocket = None
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()

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

    #获取收到消息的功能id
    def getMsgFunId(self,msg):
        funId = msg[26:30]
        return funId
    #收到 某些类型的消息后执行回复操作
    def doResponse(self,msg):
        msgFunId = self.getMsgFunId(msg)
        if msgFunId == "8105":
            msg = GPRS_response(DEV_ID=self.carId).generateMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1
            type = self.getMsgFunId(msg)
            self.websocket.sendMsgToClient(type + ">>>>查询GPSR通信参数应答：" + msg,self.websocketId)
        elif msgFunId == "8201":
            msg = Common_response(DEV_ID=self.carId,resId="8201").generateCommonMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1
            type = self.getMsgFunId(msg)
            self.websocket.sendMsgToClient(type + ">>>>终端重启应答：" + msg,self.websocketId)
        elif msgFunId == "8205":
            msg = Common_response(DEV_ID=self.carId,resId="8205").generateCommonMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1
            type = self.getMsgFunId(msg)
            self.websocket.sendMsgToClient(type + ">>>>设置GPSR通信参数应答：" + msg,self.websocketId)
        elif msgFunId == "8206":
            msg = Common_response(DEV_ID=self.carId,resId="8206").generateCommonMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1
            type = self.getMsgFunId(msg)
            self.websocket.sendMsgToClient(type + ">>>>设置车辆OBD适配信息应答：" + msg,self.websocketId)
        elif msgFunId == "8300":
            msg = Update_response(DEV_ID=self.carId).generateUpdateMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1
            type = self.getMsgFunId(msg)
            self.websocket.sendMsgToClient(type + ">>>>升级_平台通知终端远程升级应答：" + msg,self.websocketId)

    #设置GPS轨迹
    def setGpsLine(self,fileName):
        with open("data/protocolTools/GPSLines/" + fileName,"r",encoding="utf-8") as fi:
            content = fi.read()
            conJson = json.loads(content)
            if(int(self.data["travelData"]["travelDirection"]) == 0):
                self.gpsLine = conJson["GPSLine"]
            else:
                self.gpsLine = conJson["GPSLine"][::-1]     #反转gps数组

    #点火，发送点火事件
    def fireOn(self):
        self.OBDdata["engineSpeed"] = 3000
        self.OBDdata["speed"] = int(self.data["travelData"]["carSpeed"])
        if not os.path.exists("data/protocolTools/carData/" + self.carId + ".json"):
            psdsObj = ProtocolSimulaterDataService()
            data = psdsObj.genDataTemplate()
            psdsObj.writeToFile("data/protocolTools/carData/" + self.carId + ".json",data)
        #读取车机行驶数据
        with open("data/protocolTools/carData/" + self.carId + ".json", "r", encoding="utf-8") as fi:
            content = fi.read()
            conJson = json.loads(content)
            conJson["curDayTravel"]["theMilleage"] = 0             # 本次行驶总里程
            conJson["curDayTravel"]["theOil"] = 0                  # 本次行驶总油耗
            conJson["curDayTravel"]["theTime"] = 0                 # 本次行驶总时间
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            dateTimeM = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            dateM = time.strftime("%Y-%m-%d", timeArray)
            timeM = time.strftime("%H:%M:%S", timeArray)
            dataFile = self.carId + ".json"
            self.carDataObj = ProtocolSimulaterDataService("data/protocolTools/carData/", dataFile)
            self.carDataObj.setData(conJson)
            if dateM == conJson["time"]["date"]:
                self.OBDdata["totailMileage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdataOri["totailMileage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdata["totalOilExpen"] = conJson["travelData"]["totalOil"]
                self.OBDdataOri["totalOilExpen"] = conJson["travelData"]["totalOil"]
                self.OBDdata["totalRunTime"] = conJson["travelData"]["totalTime"]
                self.OBDdataOri["totalRunTime"] = conJson["travelData"]["totalTime"]
            else:                                                          #如果不是当天日期，则将日期设置为当天，并写入车辆数据文件
                conJson["curDayTravel"]["todayTotalMilleage"] = 0             # 今日行驶总里程
                conJson["curDayTravel"]["todayTotalOil"] = 0                  # 今日行驶总油耗
                conJson["curDayTravel"]["todayTotalTime"] = 0                 # 今日行驶总时间
                self.carDataObj.setTodayTotalMilleage(0)
                self.carDataObj.setTodayTodayTotalOil(0)
                self.carDataObj.setTodayTodayTotalTime(0)
                self.carDataObj.setDateTime2file(dateTimeM)
                self.carDataObj.setDate2file(dateM)
                self.carDataObj.setTime2file(timeM)
                self.OBDdata["totailMileage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdataOri["totailMileage"] = conJson["travelData"]["totalMilleage"]
                self.OBDdata["totalOilExpen"] = conJson["travelData"]["totalOil"]
                self.OBDdataOri["totalOilExpen"] = conJson["travelData"]["totalOil"]
                self.OBDdata["totalRunTime"] = conJson["travelData"]["totalTime"]
                self.OBDdataOri["totalRunTime"] = conJson["travelData"]["totalTime"]
            self.carData = self.carDataObj.fixDataTemplate(conJson)

        jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                 "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                             "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                             "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                             "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800",
                             "totalOil": "100000",
                             "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                 "securityData": {"securityStatus": 137, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                  "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                "0010": {"allRapidlyAccelerateCount": "5", "allSharpSlowdownCount": "6", "allSharpTurn": "4",
                         "dataProperty": "1"}}}
        jdata["event"]["0010"]["allRapidlyAccelerateCount"] = self.carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
        jdata["event"]["0010"]["allSharpSlowdownCount"] = self.carData["event"]["threeRapid"]["totalSharpSlowdown"]
        jdata["event"]["0010"]["allSharpTurn"] = self.carData["event"]["threeRapid"]["totalSharpTurn"]
        jdata["DEV_ID"] = self.carId
        obj = EventReport_protocol(data=jdata)
        gpsData = self.genGPSData2()
        obj.setGPSPkg(gpsData)
        obj.setEventType("0010")
        msg = obj.generateEventMsg()
        type = self.getMsgFunId(msg)
        self.sendMsg(msg)
        self.sn = self.sn + 1
        self.websocket.sendMsgToClient(type + ">>>>：" + msg, self.websocketId)

        sleep(0.1)
        gpsMsg = self.genGPSMsg(self.gpsLine[0]["lat"],self.gpsLine[0]["lng"])
        type = self.getMsgFunId(gpsMsg)
        self.sendMsg(gpsMsg)
        self.sn = self.sn + 1
        self.websocket.sendMsgToClient(type + ">>>>：" + gpsMsg,self.websocketId)
        sleep(0.1)
        OBDMsg = self.genOBDMsg(self.OBDdata["fireStatus"],1,self.OBDdata["engineSpeed"], \
                                            self.OBDdata["speed"],self.OBDdata["meterMileage"],self.OBDdata["totailMileage"], \
                                            self.OBDdata["totalOilExpen"],self.OBDdata["totalRunTime"])
        type = self.getMsgFunId(OBDMsg)
        self.sendMsg(OBDMsg)
        self.sn = self.sn + 1
        self.websocket.sendMsgToClient(type + ">>>>：" + OBDMsg,self.websocketId)

    # 熄火，发送熄火事件
    def fireOff(self):
        gpsLineIndex = self.gpsLineIndex
        if gpsLineIndex >= len(self.gpsLine):
            gpsLineIndex = gpsLineIndex - 1
        self.OBDdata["engineSpeed"] = 0
        self.OBDdata["speed"] = 0
        self.OBDdata["meterMileage"] = self.OBDdata["meterMileage"] + int(
            self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
        self.OBDdata["totailMileage"] = self.OBDdata["totailMileage"] + int(
            self.sendDur * (self.OBDdata["speed"] * 1000 / 3600))
        oilExpend = int(self.data["travelData"]["oilExpend"])
        self.OBDdata["totalOilExpen"] = self.OBDdata["totalOilExpen"] + int(
            (self.sendDur * (self.OBDdata["speed"] * 1000 / 3600)) * (1000 / (oilExpend * 1000)))
        self.OBDdata["totalRunTime"] = self.OBDdata["totalRunTime"] + self.sendDur
        OBDMsg = self.genOBDMsg(self.OBDdata["fireStatus"], self.OBDdata["ACCStatus"], self.OBDdata["engineSpeed"], \
                                self.OBDdata["speed"], self.OBDdata["meterMileage"], self.OBDdata["totailMileage"], \
                                self.OBDdata["totalOilExpen"], self.OBDdata["totalRunTime"])
        if gpsLineIndex >= len(self.gpsLine):
            gpsLineIndex = gpsLineIndex - 1
        latitude = self.gpsLine[gpsLineIndex]["lat"]
        longitude = self.gpsLine[gpsLineIndex]["lng"]
        gpsMsg = self.genGPSMsg(latitude, longitude)
        if OBDMsg != "":
            self.sendMsg(OBDMsg)
            type = self.getMsgFunId(OBDMsg)
            info = type + ">>>>：" + OBDMsg
            self.websocket.sendMsgToClient(info, self.websocketId)
        sleep(0.1)
        if gpsMsg != "":
            self.sendMsg(gpsMsg)
            type = self.getMsgFunId(gpsMsg)
            info = type + ">>>>：" + gpsMsg
            self.websocket.sendMsgToClient(info, self.websocketId)
        sleep(0.5)
        jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                 "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                             "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                             "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                             "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800",
                             "totalOil": "100000",
                             "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                 "securityData": {"securityStatus": 137, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                  "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                "0011": {"allRapidlyAccelerateCount": "5", "allSharpSlowdownCount": "6", "allSharpTurn": "4",
                         "dataProperty": "1"}}}
        jdata["event"]["0011"]["allRapidlyAccelerateCount"] = self.carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
        jdata["event"]["0011"]["allSharpSlowdownCount"] = self.carData["event"]["threeRapid"]["totalSharpSlowdown"]
        jdata["event"]["0011"]["allSharpTurn"] = self.carData["event"]["threeRapid"]["totalSharpTurn"]
        jdata["DEV_ID"] = self.carId
        obj = EventReport_protocol(data=jdata)
        gpsData = self.genGPSData2()
        obj.setGPSPkg(gpsData)
        obj.setEventType("0011")
        msg = obj.generateEventMsg()
        type = self.getMsgFunId(msg)
        self.sendMsg(msg)
        self.sn = self.sn + 1
        self.websocket.sendMsgToClient(type + ">>>>：" + msg, self.websocketId)

        # sleep(0.1)
        # gpsMsg = self.genGPSMsg(self.gpsLine[gpsLineIndex]["lat"], self.gpsLine[gpsLineIndex]["lng"])
        # type = self.getMsgFunId(gpsMsg)
        # self.sendMsg(gpsMsg)
        # self.sn = self.sn + 1
        # self.websocket.sendMsgToClient(type + ">>>>：" + gpsMsg,self.websocketId)

    #根据特定参数，生成GPS消息
    def genGPSMsg(self,latitude,longtitude,direct=0):
        gpsObj = GPSReport_protocol(DEV_ID=self.carId,WATER_CODE=self.sn)
        gpsObj.setLatitude(latitude)
        gpsObj.setLongitude(longtitude)
        gpsObj.setSpeed(int(self.data["travelData"]["carSpeed"]))
        gpsObj.setOBDSpeed(int(self.data["travelData"]["carSpeed"]))
        gpsObj.setValtage(self.data["other"]["valtage"])
        if self.lngLatIsOk == 0:
            gpsObj.setLatitude(0)
            gpsObj.setLongitude(0)
        if self.GPSValid == 1:
            gpsObj.setGpsValid(1)
        elif self.GPSValid == 0:
            gpsObj.setGpsValid(0)
        gpsObj.setDirectionAngle(self.getDirAngle())
        timeS = int(time.time()) - 8 * 3600 + int(self.data["timeDif"])
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        gpsObj.setUTCTime(UTCTime)
        gpsObj.setGPSTimestamp(timeS)
        msg = gpsObj.generateGpsMsg()
        return msg
    #根据特定参数，生成GPS消息体，不包含消息头
    def genGPSData(self,latitude,longtitude):
        gpsObj = GPSReport_protocol(DEV_ID=self.carId,WATER_CODE=self.sn)
        gpsObj.setLatitude(latitude)
        gpsObj.setLongitude(longtitude)
        gpsObj.setSpeed(int(self.data["travelData"]["carSpeed"]))
        gpsObj.setOBDSpeed(int(self.data["travelData"]["carSpeed"]))
        gpsObj.setValtage(self.data["other"]["valtage"])
        if self.lngLatIsOk == 0:
            gpsObj.setLatitude(0)
            gpsObj.setLongitude(0)
        if self.GPSValid == 1:
            gpsObj.setGpsValid(1)
        elif self.GPSValid == 0:
            gpsObj.setGpsValid(0)
        gpsObj.setDirectionAngle(self.getDirAngle())
        timeS = int(time.time()) - 8 * 3600 + int(self.data["timeDif"])
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        gpsObj.setUTCTime(UTCTime)
        gpsObj.setGPSTimestamp(timeS)
        data = gpsObj.generateGpsData()
        return data
    #根据当前所在GPS点，生成GPS消息体，不包含消息头
    def genGPSData2(self):
        gpsLineIndex = self.gpsLineIndex
        if gpsLineIndex >= len(self.gpsLine):
            gpsLineIndex = gpsLineIndex - 1
        gpsObj = GPSReport_protocol(DEV_ID=self.carId,WATER_CODE=self.sn)
        # gpsObj.setLatitude(self.gpsLine[self.gpsLineIndex]["lat"])
        # gpsObj.setLongitude(self.gpsLine[self.gpsLineIndex]["lng"])
        gpsObj.setLatitude(self.gpsLine[gpsLineIndex]["lat"])
        gpsObj.setLongitude(self.gpsLine[gpsLineIndex]["lng"])
        gpsObj.setSpeed(int(self.data["travelData"]["carSpeed"]))
        gpsObj.setOBDSpeed(int(self.data["travelData"]["carSpeed"]))
        gpsObj.setValtage(self.data["other"]["valtage"])
        if self.lngLatIsOk == 0:
            gpsObj.setLatitude(0)
            gpsObj.setLongitude(0)
        if self.GPSValid == 1:
            gpsObj.setGpsValid(1)
        elif self.GPSValid == 0:
            gpsObj.setGpsValid(0)
        gpsObj.setDirectionAngle(self.getDirAngle())
        timeS = int(time.time()) - 8 * 3600 + int(self.data["timeDif"])
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        gpsObj.setUTCTime(UTCTime)
        gpsObj.setGPSTimestamp(timeS)
        data = gpsObj.generateGpsData()
        return data

    # 根据特定参数，生成OBD CAN消息
    def genOBDMsg(self,fireStatus=1,ACCStatus=0,engineSpeed=300,speed=0,meterMileage=6000, \
                  totailMileage=600,totalOilExpend=30,totalRunTime=10):
        OBDObj = OBDReport_CAN_protocol(DEV_ID=self.carId,WATER_CODE=self.sn)
        timeS = int(time.time()) - 8 * 3600 + int(self.data["timeDif"])
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        OBDObj.setInfoTime(UTCTime)
        OBDObj.setFireStatus(fireStatus)
        OBDObj.setACCStatus(ACCStatus)
        OBDObj.setEngineSpeed(engineSpeed)                 # 设置发动机转速
        OBDObj.setSpeed(speed)                             # 设置车辆速度
        OBDObj.setMeterMileage(meterMileage)               # 设置仪表里程值
        OBDObj.setTotalMileage(totailMileage)              # 设置总里程值
        OBDObj.setTotalOilExpend(totalOilExpend)           # 设置总耗油量
        OBDObj.setTotalRunTime(totalRunTime)               # 设置车辆运行时间
        OBDObj.setSurplusOil(self.OBDdata["surplusOil"])   # 设置剩余油量
        OBDObj.setEngineSpeed(self.OBDdata["engineSpeed"]) # 设置发动机转速
        OBDObj.setVoltage(self.data["other"]["valtage"])   # 设置电瓶电压
        msg = OBDObj.generateOBDReportCANMsg()
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

    #测试方向角转换的函数（测试用）
    def getDirAngleTest(self):
        lngCut = (116.410665 - 116.423888) * 1000000
        latCut = (39.929267 - 39.930484) * 1000000
        val = lngCut / latCut
        dire = math.atan2(1, val) * 180 / math.pi
        if lngCut < 0 and latCut > 0:
            pass
            dire = 270 + 180 - dire
        elif latCut < 0 and lngCut > 0:
            dire = 270 - dire
        elif lngCut < 0 and latCut < 0:
            dire = 180 + 90 - dire

    ###########################################################
    # 将要发送的数据保存到本地
    ###########################################################
    def saveMsgLocal(self,fName,data):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        thePath = 'data/protocolTools/sendMsg'
        if not os.path.exists(thePath):
            os.makedirs(thePath)
        thePath = thePath + "/" + self.carId + "/"
        if not os.path.exists(thePath):
            os.makedirs(thePath)
        with open(thePath + fName, "a", encoding="utf-8") as fi:
            fi.write("[" + curTime +"]" + data + "\n")


if __name__ == "__main__":
    ProtocolSimulaterService().getDirAngleTest()








