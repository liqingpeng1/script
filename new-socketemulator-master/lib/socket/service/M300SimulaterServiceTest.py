#coding:utf-8

'''
M300车机模拟服务简易测试程序，用于做临时测试
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
from lib.protocol.m300.response.GPRS_protocol_response_m300 import GPRS_protocol_response_m300
from lib.protocol.message.Location_msg import Location_msg
from lib.protocol.message.TerminalCommonMsgRes_msg import TerminalCommonMsgRes_msg
from lib.protocol.message.TerminalRegister_msg import TerminalRegister_msg
from lib.protocol.message.TerminalVersionInfo_msg import TerminalVersionInfo_msg
from lib.socket.ClientSocket import ClientSocket
from lib.socket.service.M300SimulaterDataService import M300SimulaterDataService
from lib.socket.service.MessageSimulaterDataService import MessageSimulaterDataService
from lib.socket.service.websocket_service import Websocket_service


class M300SimulaterService():
    def __init__(self):
        self.data = {}                       #用来接收模拟器传过来的参数
        self.carData = {}                    #保存车辆行驶数据
        self.carDataObj = None               #管理车辆行驶数据对象
        self.socket = None
        self.sendDur = 5                     #设置默认多久发一条消息
        self.serviceStatus = 0               #服务状态，0表示未启动，1表示启动
        self.websocket = None                #网页与服务的通信socket
        self.websocketId = ""               #当前连接的webSocketId
        self.timeout = 3600                     #socket的超时时间
        self.gpsLine = []                    #GPS 轨迹
        self.gpsLineIndex = 0                #GPS 轨迹索引
        self.travelStatus = 0                #0，表示未行驶，1表示开始行驶同时开启了接收消息服务，2表示值开启了接收消息的服务
        self.carId = "M121501010001"                      #车机号
        self.sn = 1                          #消息流水号
        self.travelDirection = 0             #行驶方向，0表示正向行驶，1表示反向行驶
        self.directAngle = 60                #汽车方向角

    #######################################################
    # type 为0表示正常发送，type为1表示数据写入本地
    #######################################################
    def sendMsg(self,msg):
        self.socket.setTimeOut(self.timeout)
        self.socket.send(msg)
        type = self.getMsgFunId(msg)
        print("发送消息：" + type + ">>>>" +  msg)

    def revMsg(self):
        self.socket.setTimeOut(self.timeout)
        return self.socket.receive()

    #发送消息，可指定消息的描述类型
    def serviceSendMsg(self,msg,type):          #type字段目前废掉没有实际意
        self.sendMsg(msg)

    def connect(self,host,port):
        cliSocket = ClientSocket(host, port)
        cliSocket.setTimeOut(self.timeout)
        cliSocket.connect()
        self.socket = cliSocket
        self.startRevService()

    def login(self):
        loginObj = Login_protocol_m300(waterCode = self.sn,DEV_ID = self.carId,encryptionType=0)
        loginMsg = loginObj.generateMsg()
        self.sendMsg(loginMsg)
        self.sn = self.sn +1
        time.sleep(1)
        versionObj = VersionInfo_protocol_m300(waterCode = self.sn,DEV_ID = self.carId,encryptionType=0,SWVersion="VSTA000GV100", \
                                               SWDate="2020-03-30",HWVersion="M1.0",GSMType="GSM_type_123456",carType="150", \
                                               engineCode=1,VINCode="VIN_CODE_01234567890")
        versionMsg = versionObj.generateMsg()
        self.sendMsg(versionMsg)
        self.sn = self.sn + 1
        time.sleep(1)

    def serviceRev(self):
        self.serviceStatus = 2              #2代表只启动了接收消息的进程，1代表了接收和发送都启动了
        while self.serviceStatus != 0:
            self.socket.setTimeOut(self.timeout)
            d = self.revMsg()
            d = str(binascii.b2a_hex(d))[2:][:-1]
            type = self.getMsgFunId(d)
            print("收到消息：" + type + "<<<<" + d)
            self.doResponse(d)

    #启动接收消息服务
    def startRevService(self):
            t2 = threading.Thread(target=self.serviceRev, args=())
            t2.start()


    #获取收到消息的功能id
    def getMsgFunId(self,msg):
        funId = msg[2:6]
        return funId
    #收到 某些类型的消息后执行回复操作
    def doResponse(self,msg):
        msgFunId = self.getMsgFunId(msg)
        if msgFunId == "8104":
            msg = GPRS_protocol_response_m300().generateMsg()
            self.sendMsg(msg)
            self.sn = self.sn + 1

if __name__ == "__main__":
    service = M300SimulaterService()
    service.connect("10.100.12.32",9009)
    time.sleep(1)
    service.login()
