#coding:utf-8

'''
新硬件车机模拟服务类
'''
import binascii
import json
import math
import os
import threading
import time
import traceback
from time import sleep

from lib.protocol.message.Location_msg import Location_msg
from lib.protocol.message.TerminalRegister_msg import TerminalRegister_msg
from lib.protocol.message.TerminalRequestOBDInfo_msg import TerminalRequestOBDInfo_msg
from lib.protocol.message.TerminalVersionInfo_msg import TerminalVersionInfo_msg
from lib.protocol.message.response.QueryTheTerminalParam_res import QueryTheTerminalParam_res
from lib.protocol.messagePlateform.PlateformVersionInfo_res import PlatefromVersionInfo_res
from lib.socket.service.MessageSimulaterDataService import MessageSimulaterDataService
from lib.socket.service.websocket_service import Websocket_service
from lib.util.util import strAddSpace


class MessageSimulaterService():
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
        self.fixCurPosition = 0              #是否固定当前GPS点，0：不固定  1：固定
        # 定义要发送的obd数据
        self.OBDdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
         "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133, "longtitude": 106.586571,
                                        "elevation": "521", "speed": "66", "directionAngle": "59",
                                        "infoTime": "2020-04-23 13:15:37"}, "extraInfo": {"01": {"extra_01": "20202020"},
            "EA": {"0012": {"dataId_0012": "36"}},
            "EB": {"6010": "2", "6014": "0", "6040": "44", "6050": "76", "6070": "89", "6100": "505", "6110": "51",
                   "6210": "4508", "6330": "28", "6460": "65", "6490": "32", "6701": "0", "6702": "0", "6703": "1",
                   "6704": "505", "6705": "1", "6706": "505", "6707": "505", "6708": "3500", "6709": "7200000",
                   "60C0": "3000", "60D0": "60", "62f0": "801", "60F0": "88", "60B0": "20", "60A0": "276",
                   "61F0": "3700", "60E0": "154", "670a": "3700000", "670b": "123000"}}}
        # 定义初始的obd数据，与上面的OBD数据保持一致，主要用于汽车行驶过程中数据变化量的计算
        self.OBDdataOri = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
         "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133, "longtitude": 106.586571,
                                        "elevation": "521", "speed": "66", "directionAngle": "59",
                                        "infoTime": "2020-04-23 13:15:37"}, "extraInfo": {"01": {"extra_01": "20202020"},
            "EA": {"0012": {"dataId_0012": "36"}},
            "EB": {"6010": "2", "6014": "0", "6040": "44", "6050": "76", "6070": "89", "6100": "505", "6110": "51",
                   "6210": "4508", "6330": "28", "6460": "65", "6490": "32", "6701": "0", "6702": "0", "6703": "1",
                   "6704": "505", "6705": "1", "6706": "505", "6707": "505", "6708": "3500", "6709": "7200000",
                   "60C0": "3000", "60D0": "60", "62f0": "801", "60F0": "88", "60B0": "20", "60A0": "276",
                   "61F0": "3700", "60E0": "154", "670a": "3700000", "670b": "123000"}}}


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
    def getTravelDirection(self):
        return self.travelDirection
    def getGpsLine(self):
        return self.gpsLine
    def getGpsLineIndex(self):
        return self.gpsLineIndex

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
        sleep(1)
        self.websocketId = self.websocket.getCurrentClientId()
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
    def setTravelDirection(self,data):
        self.travelDirection = data
    def setFixCurPosition(self,data):
        self.fixCurPosition = data
    def setVotage(self,data):
        self.data["travelData"]["votage"] = data
    def setEngineSpeed(self,data):
        self.data["travelData"]["engineSpeed"] = data
    def setSurplusOil(self,data):
        self.data["travelData"]["surplusOil"] = data

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
        loginObj = TerminalRegister_msg()

        self.data["login"]["manufacturerId"] = strAddSpace(self.data["login"]["manufacturerId"],5)
        self.data["login"]["terminalType"] = strAddSpace(self.data["login"]["terminalType"], 20)
        self.data["login"]["terminalId"] = strAddSpace(self.data["login"]["terminalId"], 7)

        msg = loginObj.generateMsg_GUI(msgID="0100",phoneNum=int(self.data["phoneNum"]),msgWaterCode=self.sn,encryptionType=0,subPkg=0,provinceId=int(self.data["login"]["provinceId"]),\
                        countyId=int(self.data["login"]["countyId"]),manufacturerId=self.data["login"]["manufacturerId"],terminalType=self.data["login"]["terminalType"],  \
                                       terminalId=self.data["login"]["terminalId"],licencePlateColor=int(self.data["login"]["licencePlateColor"]),carSign=self.data["login"]["carSign"])
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        info = type + ">>>>：" + msg
        self.websocket.sendMsgToClient(info,self.websocketId)
        self.sn = self.sn + 1
        verObj = TerminalVersionInfo_msg()
        time.sleep(0.5)

        self.data["version"]["softwareVersion"] = strAddSpace(self.data["version"]["softwareVersion"], 14)
        self.data["version"]["CPUId"] = strAddSpace(self.data["version"]["CPUId"], 12)
        self.data["version"]["GMSType"] = strAddSpace(self.data["version"]["GMSType"], 15)
        self.data["version"]["GMS_IMEI"] = strAddSpace(self.data["version"]["GMS_IMEI"], 15)
        self.data["version"]["SIM_IMSI"] = strAddSpace(self.data["version"]["SIM_IMSI"], 15)
        self.data["version"]["SIM_ICCID"] = strAddSpace(self.data["version"]["SIM_ICCID"], 20)
        self.data["version"]["VIN"] = strAddSpace(self.data["version"]["VIN"], 17)

        msg = verObj.generateMsg_GUI(msgID="0205",phoneNum=int(self.data["phoneNum"]),msgWaterCode=self.sn,encryptionType=0,subPkg=0, \
                    softwareVersion=self.data["version"]["softwareVersion"], softwareVersionDate=self.data["version"]["softwareVersionDate"], CPUId=self.data["version"]["CPUId"], \
                    GMSType=self.data["version"]["GMSType"], GMS_IMEI=self.data["version"]["GMS_IMEI"], SIM_IMSI=self.data["version"]["SIM_IMSI"], \
                    SIM_ICCID=self.data["version"]["SIM_ICCID"],carType=int(self.data["version"]["carType"]), VIN=self.data["version"]["VIN"], \
                    totalMileage=int(self.data["version"]["totalMileage"]), totalOilExpend=int(self.data["version"]["totalOilExpend"]), \
                    displacement=int(self.data["version"]["displacement"]),oilDensity=int(self.data["version"]["oilDensity"]))
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        info = type + ">>>>：" + msg
        self.websocket.sendMsgToClient(info,self.websocketId)
        self.sn = self.sn + 1

    ########################################################
    #车机点火
    ########################################################
    def fireOn(self):
        if not os.path.exists("data/messageTools/carData/" + self.carId + ".json"):
            psdsObj = MessageSimulaterDataService()
            data = psdsObj.genDataTemplate()
            psdsObj.writeToFile("data/messageTools/carData/" + self.carId + ".json",data)
        #读取车机行驶数据
        with open("data/messageTools/carData/" + self.carId + ".json", "r", encoding="utf-8") as fi:
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
            self.carDataObj = MessageSimulaterDataService("data/messageTools/carData/", dataFile)
            self.carDataObj.setData(conJson)
            if dateM == conJson["time"]["date"]:
                self.OBDdata["extraInfo"]["01"]["extra_01"] = conJson["travelData"]["totalMilleage"]
                self.OBDdataOri["extraInfo"]["01"]["extra_01"] = conJson["travelData"]["totalMilleage"]
                self.OBDdata["extraInfo"]["EB"]["670a"] = conJson["travelData"]["totalOil"]
                self.OBDdataOri["extraInfo"]["EB"]["670a"] = conJson["travelData"]["totalOil"]
                self.OBDdata["extraInfo"]["EB"]["6709"] = conJson["travelData"]["totalTime"]
                self.OBDdataOri["extraInfo"]["EB"]["6709"] = conJson["travelData"]["totalTime"]
            else:                                                             #如果不是当天日期，则将日期设置为当天，并写入车辆数据文件
                conJson["curDayTravel"]["todayTotalMilleage"] = 0             # 今日行驶总里程
                conJson["curDayTravel"]["todayTotalOil"] = 0                  # 今日行驶总油耗
                conJson["curDayTravel"]["todayTotalTime"] = 0                 # 今日行驶总时间
                self.carDataObj.setTodayTotalMilleage(0)
                self.carDataObj.setTodayTodayTotalOil(0)
                self.carDataObj.setTodayTodayTotalTime(0)
                self.carDataObj.setDateTime2file(dateTimeM)
                self.carDataObj.setDate2file(dateM)
                self.carDataObj.setTime2file(timeM)
                self.OBDdata["extraInfo"]["01"]["extra_01"] = conJson["travelData"]["totalMilleage"]
                self.OBDdataOri["extraInfo"]["01"]["extra_01"] = conJson["travelData"]["totalMilleage"]
                self.OBDdata["extraInfo"]["EB"]["670a"] = conJson["travelData"]["totalOil"]
                self.OBDdataOri["extraInfo"]["EB"]["670a"] = conJson["travelData"]["totalOil"]
                self.OBDdata["extraInfo"]["EB"]["6709"] = conJson["travelData"]["totalTime"]
                self.OBDdataOri["extraInfo"]["EB"]["6709"] = conJson["travelData"]["totalTime"]
            self.carData = conJson

            ############################# 发送点火数据 ############################
            self.setGpsLine(self.data["gpsLine"])
            fireOnParams = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
             "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133, "longtitude": 106.586571,
                                            "elevation": "521", "speed": "0", "directionAngle": "59",
                                            "infoTime": "2020-04-21 18:03:49"}, "extraInfo": {"FA": {"ignition": "on"}}}
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            fireOnParams["phoneNum"] = self.data["phoneNum"]
            fireOnParams["msgWaterCode"] = self.sn
            fireOnParams["baseInfo"]["infoTime"] = curTime
            fireOnParams["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
            fireOnParams["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
            fireOnParams["baseInfo"]["directionAngle"] = self.getDirAngle()
            msgObj = Location_msg()
            msg = msgObj.generateMsg_GUI(fireOnParams)
            self.sendMsg(msg)
            type = self.getMsgFunId(msg)
            info = type + ">>>>：" + msg
            self.websocket.sendMsgToClient(info,self.websocketId)
            self.sn = self.sn + 1
            time.sleep(0.1)
            self.OBDdata["phoneNum"] = self.data["phoneNum"]
            self.OBDdata["msgWaterCode"] = self.sn
            self.OBDdata["baseInfo"]["infoTime"] = curTime
            self.OBDdata["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
            self.OBDdata["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
            self.OBDdata["baseInfo"]["directionAngle"] = self.getDirAngle()
            self.OBDdata["extraInfo"]["EB"]["60C0"] = 0                                                                  # 发动机转速
            self.OBDdata["extraInfo"]["EB"]["60D0"] = 0                                                                  # 车速
            self.OBDdata["extraInfo"]["EB"]["670a"] = self.carData["travelData"]["totalOil"]                             # 总油耗
            self.OBDdata["extraInfo"]["EB"]["6709"] = self.carData["travelData"]["totalTime"]                            # 总运行时间
            self.OBDdata["extraInfo"]["01"]["extra_01"] = self.carData["travelData"]["totalMilleage"]                    # 总里程
            self.OBDdata["extraInfo"]["EB"]["670b"] = self.carData["travelData"]["totalMilleage"]                        # OBD 累计里程
            obdMsg = msgObj.generateMsg_GUI(self.OBDdata)
            self.sendMsg(obdMsg)
            type = self.getMsgFunId(obdMsg)
            info = type + ">>>>：" + obdMsg
            self.websocket.sendMsgToClient(info,self.websocketId)
            self.sn = self.sn + 1

    ########################################################
    #车机行驶服务
    ########################################################
    def serviceTrave(self):
        plusMilleage = 0                      #每次增加的里程数，上报的时候要除以100，因为原始文档总里程的单位是0.1km
        plusMilleage2 = 0                     #每次增加的里程数，用于写入文件 用，写入后置为0
        while self.serviceStatus == 1:
            gpsMsg = ""
            obdMsg = ""                                                                                #对比比上一次上报，所增加的里程
            if self.travelStatus == 0:                                                                 #行驶服务未启动
                gpsParams = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                                 "subPkg": "0","pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133,
                                 "longtitude": 106.586571,"elevation": "521", "speed": "0",
                                "directionAngle": "59","infoTime": "2020-04-21 18:09:34"},
                             "extraInfo": {}}
                latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                timeStamp = time.time()
                timeArray = time.localtime(timeStamp)
                curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                gpsParams["phoneNum"] = self.data["phoneNum"]
                gpsParams["msgWaterCode"] = self.sn
                gpsParams["baseInfo"]["infoTime"] = curTime
                gpsParams["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
                gpsParams["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
                gpsParams["baseInfo"]["speed"] = int(self.data["travelData"]["carSpeed"]) * 10
                gpsParams["baseInfo"]["directionAngle"] = self.getDirAngle()
                gpsObj = Location_msg()
                gpsMsg = gpsObj.generateMsg_GUI(gpsParams)
            elif self.travelStatus == 1:                                                               #行驶服务启动
                if self.gpsLineIndex < len(self.gpsLine) and self.gpsLineIndex != -1:                  #如果正向行驶和反向行驶的轨迹点都没有跑完
                    gpsParams = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                                 "subPkg": "0", "pkgCounts": "0",
                                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133,
                                              "longtitude": 106.586571, "elevation": "521", "speed": "0",
                                              "directionAngle": "59", "infoTime": "2020-04-21 18:09:34"},
                                 "extraInfo": {}}
                    latitude = self.gpsLine[self.gpsLineIndex]["lat"]
                    longitude = self.gpsLine[self.gpsLineIndex]["lng"]
                    timeStamp = time.time()
                    timeArray = time.localtime(timeStamp)
                    curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    gpsParams["phoneNum"] = self.data["phoneNum"]
                    gpsParams["msgWaterCode"] = self.sn
                    gpsParams["baseInfo"]["infoTime"] = curTime
                    gpsParams["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
                    gpsParams["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
                    gpsParams["baseInfo"]["speed"] = int(self.data["travelData"]["carSpeed"]) * 10
                    gpsParams["baseInfo"]["directionAngle"] = self.getDirAngle()
                    gpsObj = Location_msg()
                    gpsMsg = gpsObj.generateMsg_GUI(gpsParams)

                    self.OBDdata["phoneNum"] = self.data["phoneNum"]
                    self.OBDdata["msgWaterCode"] = self.sn
                    self.OBDdata["baseInfo"]["infoTime"] = curTime
                    self.OBDdata["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
                    self.OBDdata["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
                    self.OBDdata["baseInfo"]["directionAngle"] = self.getDirAngle()
                    self.OBDdata["extraInfo"]["EA"]["0012"]["dataId_0012"] = int(self.data["travelData"]["votage"])                       # 电瓶电压
                    self.OBDdata["extraInfo"]["EB"]["60C0"] = int(self.data["travelData"]["engineSpeed"])                                 # 发动机转速
                    self.OBDdata["extraInfo"]["EB"]["62f0"] = int(self.data["travelData"]["surplusOil"])                                  # 剩余油量
                    speed = int(self.data["travelData"]["carSpeed"])
                    oilExpend = int(self.data["travelData"]["oilExpend"])
                    self.OBDdata["extraInfo"]["EB"]["60D0"] = speed                                                                                                                    # 车速
                    self.OBDdata["extraInfo"]["EB"]["670a"] = self.OBDdata["extraInfo"]["EB"]["670a"] + int((self.sendDur * (speed * 1000 / 3600)) * (1000 / (oilExpend * 1000)))      # 总油耗
                    self.OBDdata["extraInfo"]["EB"]["6709"] = self.OBDdata["extraInfo"]["EB"]["6709"] + self.sendDur                                                                   # 总运行时间
                    plusMilleage = plusMilleage + int(self.sendDur * (speed * 1000 / 3600))
                    plusMilleage2 = int(self.sendDur * (speed * 1000 / 3600))
                    self.OBDdata["extraInfo"]["01"]["extra_01"] = self.OBDdata["extraInfo"]["01"]["extra_01"] + int(plusMilleage / 100)                                                # 总里程（附加信息）
                    # OBD 累计里程，如果有该字段，则里程的计算方式使用该字段，如果没有，里程计算方式使用的是附加信息里得到总里程字段
                    self.OBDdata["extraInfo"]["EB"]["670b"] = self.OBDdata["extraInfo"]["EB"]["670b"] + int(plusMilleage2)                                                            # 总里程（OBD信息，默认使用）
                    self.OBDdata["extraInfo"]["EB"]["6708"] = int((self.OBDdata["extraInfo"]["EB"]["670b"] + int(plusMilleage2)) / 1000)                                                 # 仪表里程
                    plusMilleage = plusMilleage - int(plusMilleage / 100) * 100
                    obdObj = Location_msg()
                    obdMsg = obdObj.generateMsg_GUI(self.OBDdata)
                    if self.fixCurPosition == 0:
                        if self.travelDirection == 0:
                            if self.gpsLineIndex < len(self.gpsLine):
                                self.gpsLineIndex = self.gpsLineIndex + 1  # 正向行驶
                        else:
                            if self.gpsLineIndex > 0:
                                self.gpsLineIndex = self.gpsLineIndex - 1  # 反向行驶
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
                    gpsParams = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                                 "subPkg": "0", "pkgCounts": "0",
                                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133,
                                              "longtitude": 106.586571, "elevation": "521", "speed": "0",
                                              "directionAngle": "59", "infoTime": "2020-04-21 18:09:34"},
                                 "extraInfo": {}}
                    timeStamp = time.time()
                    timeArray = time.localtime(timeStamp)
                    curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    gpsParams["phoneNum"] = self.data["phoneNum"]
                    gpsParams["msgWaterCode"] = self.sn
                    gpsParams["baseInfo"]["infoTime"] = curTime
                    gpsParams["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
                    gpsParams["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
                    gpsParams["baseInfo"]["speed"] = int(self.data["travelData"]["carSpeed"]) * 10
                    gpsParams["baseInfo"]["directionAngle"] = self.getDirAngle()
                    gpsObj = Location_msg()
                    gpsMsg = gpsObj.generateMsg_GUI(gpsParams)

                    self.OBDdata["phoneNum"] = self.data["phoneNum"]
                    self.OBDdata["msgWaterCode"] = self.sn
                    self.OBDdata["baseInfo"]["infoTime"] = curTime
                    self.OBDdata["baseInfo"]["latitude"] = self.gpsLine[self.gpsLineIndex]["lat"]
                    self.OBDdata["baseInfo"]["longtitude"] = self.gpsLine[self.gpsLineIndex]["lng"]
                    self.OBDdata["baseInfo"]["directionAngle"] = self.getDirAngle()
                    # self.OBDdata["extraInfo"]["EB"]["60C0"] = 3000  # 发动机转速
                    self.OBDdata["extraInfo"]["EA"]["0012"]["dataId_0012"] = int(self.data["travelData"]["votage"])                       # 电瓶电压
                    self.OBDdata["extraInfo"]["EB"]["60C0"] = int(self.data["travelData"]["engineSpeed"])                                 # 发动机转速
                    self.OBDdata["extraInfo"]["EB"]["62f0"] = int(self.data["travelData"]["surplusOil"])                                  # 剩余油量
                    speed = int(self.data["travelData"]["carSpeed"])
                    oilExpend = int(self.data["travelData"]["oilExpend"])
                    self.OBDdata["extraInfo"]["EB"]["60D0"] = speed  # 车速
                    self.OBDdata["extraInfo"]["EB"]["670a"] = self.OBDdata["extraInfo"]["EB"]["670a"] + int((self.sendDur * (speed * 1000 / 3600)) * (1000 / (oilExpend * 1000)))  # 总油耗
                    self.OBDdata["extraInfo"]["EB"]["6709"] = self.OBDdata["extraInfo"]["EB"]["6709"] + self.sendDur                                                               # 总运行时间
                    plusMilleage = plusMilleage + int(self.sendDur * (speed * 1000 / 3600))
                    plusMilleage2 = int(self.sendDur * (speed * 1000 / 3600))
                    self.OBDdata["extraInfo"]["01"]["extra_01"] = self.OBDdata["extraInfo"]["01"]["extra_01"] + int(plusMilleage / 100)                                             # 总里程
                    # OBD 累计里程，如果有该字段，则里程的计算方式使用该字段，如果没有，里程计算方式使用的是附加信息里得到总里程字段
                    self.OBDdata["extraInfo"]["EB"]["670b"] = self.OBDdata["extraInfo"]["EB"]["670b"] + int(plusMilleage2)                                                          # 总里程（OBD信息，默认使用）
                    self.OBDdata["extraInfo"]["EB"]["6708"] = int((self.OBDdata["extraInfo"]["EB"]["670b"] + int(plusMilleage2)) / 1000)                                              # 仪表里程
                    plusMilleage = plusMilleage - int(plusMilleage / 100) * 100
                    obdObj = Location_msg()
                    obdMsg = obdObj.generateMsg_GUI(self.OBDdata)
            self.carDataObj.setTodayTotalMilleage(self.carData["curDayTravel"]["todayTotalMilleage"] + plusMilleage2)
            self.carDataObj.setTheMilleage(self.carData["curDayTravel"]["theMilleage"] + plusMilleage2)
            self.carDataObj.setTotalMilleage(self.carData["travelData"]["totalMilleage"] + plusMilleage2)
            temp = self.OBDdata["extraInfo"]["01"]["extra_01"]
            self.OBDdataOri["extraInfo"]["01"]["extra_01"] = temp
            self.carDataObj.setTodayTodayTotalOil(self.carData["curDayTravel"]["todayTotalOil"] + self.OBDdata["extraInfo"]["EB"]["670a"] - self.OBDdataOri["extraInfo"]["EB"]["670a"])
            self.carDataObj.setTheOil(self.carData["curDayTravel"]["theOil"] + self.OBDdata["extraInfo"]["EB"]["670a"] - self.OBDdataOri["extraInfo"]["EB"]["670a"])
            self.carDataObj.setTotalOil(self.carData["travelData"]["totalOil"] + self.OBDdata["extraInfo"]["EB"]["670a"] - self.OBDdataOri["extraInfo"]["EB"]["670a"])
            self.OBDdataOri["extraInfo"]["EB"]["670a"] = self.OBDdata["extraInfo"]["EB"]["670a"]
            self.carDataObj.setTodayTodayTotalTime(self.carData["curDayTravel"]["todayTotalTime"] + self.OBDdata["extraInfo"]["EB"]["6709"] - self.OBDdataOri["extraInfo"]["EB"]["6709"])
            self.carDataObj.setTheTime(self.carData["curDayTravel"]["theTime"] + self.OBDdata["extraInfo"]["EB"]["6709"] - self.OBDdataOri["extraInfo"]["EB"]["6709"])
            self.carDataObj.setTotalTime(self.carData["travelData"]["totalTime"] + self.OBDdata["extraInfo"]["EB"]["6709"] - self.OBDdataOri["extraInfo"]["EB"]["6709"])
            self.OBDdataOri["extraInfo"]["EB"]["6709"] = self.OBDdata["extraInfo"]["EB"]["6709"]
            if obdMsg != "":
                self.sendMsg(obdMsg)
                self.sn = self.sn + 1
                type = self.getMsgFunId(obdMsg)
                info = type + ">>>>：" + obdMsg
                self.websocket.sendMsgToClient(info,self.websocketId)
            if gpsMsg != "":
                time.sleep(0.1)
                self.sendMsg(gpsMsg)
                self.sn = self.sn + 1
                type = self.getMsgFunId(gpsMsg)
                info = type + ">>>>：" + gpsMsg
                self.websocket.sendMsgToClient(info,self.websocketId)
            sleep(self.sendDur)

    ########################################################
    #车机熄火
    ########################################################
    def fireOff(self):
        gpsLineIndex = self.gpsLineIndex
        if gpsLineIndex >= len(self.gpsLine):
            gpsLineIndex = gpsLineIndex - 1
        fireOffParams = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
         "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.569133, "longtitude": 106.586571,
                                        "elevation": "521", "speed": "0", "directionAngle": "59",
                                        "infoTime": "2020-04-21 18:09:34"}, "extraInfo": {"FA": {"flameout": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        fireOffParams["phoneNum"] = self.data["phoneNum"]
        fireOffParams["msgWaterCode"] = self.sn
        fireOffParams["baseInfo"]["infoTime"] = curTime
        fireOffParams["baseInfo"]["latitude"] = self.gpsLine[gpsLineIndex]["lat"]
        fireOffParams["baseInfo"]["longtitude"] = self.gpsLine[gpsLineIndex]["lng"]
        fireOffParams["baseInfo"]["directionAngle"] = self.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(fireOffParams)
        self.sendMsg(msg)
        type = self.getMsgFunId(msg)
        info = type + ">>>>：" + msg
        self.websocket.sendMsgToClient(info,self.websocketId)
        self.sn = self.sn + 1

    ########################################################
    #启动与页面交互的websockt服务
    ########################################################
    def websocketService(self):
        self.websocket = Websocket_service()
        self.websocket.setHost("0.0.0.0")
        self.websocket.setPort(5007)
        self.websocket.startWebsocketServer()

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
    #启动与页面交互的websocket服务
    ########################################################
    def startWebsocketService(self):
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
        if msgFunId == "8106":
            obj = QueryTheTerminalParam_res()
            obj.setMsgRes(msg)
            msg = obj.generateMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1
            type = self.getMsgFunId(msg)
            self.websocket.send(type + ">>>>查询终端参数消息应答：" + msg)
        elif msgFunId == "8205":
            dic = PlatefromVersionInfo_res(msg).getMsg()
            OBDCtrType = int(json.loads(dic)["body"]["OBDCtrType"])
            if OBDCtrType == 0:
                obj = TerminalRequestOBDInfo_msg()
                msg = obj.generateMsg_GUI(phoneNum=self.carId,msgWaterCode=self.sn)
                self.sendMsg(msg)
                self.sn = self.sn + 1
                type = self.getMsgFunId(msg)
                self.websocket.send(type + ">>>>终端请求OBD适配信息：" + msg)
        elif msgFunId == "8206":
            pass

    #设置GPS轨迹
    def setGpsLine(self,fileName):
        with open("data/messageTools/GPSLines/" + fileName,"r",encoding="utf-8") as fi:
            content = fi.read()
            conJson = json.loads(content)
            if (int(self.data["travelData"]["travelDirection"]) == 0):
                self.gpsLine = conJson["GPSLine"]
            else:
                self.gpsLine = conJson["GPSLine"][::-1]  # 反转gps数组

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
