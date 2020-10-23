#coding:utf-8
import binascii
import os
import socket
import sys

from lib.protocol.report.SensorSampling_protocol import SensorSampling_protocol
from lib.protocol.report.TroubleCodeReport_protocol import TroubleCode_protocol
from lib.protocol.report.VoltageDataReport_protocol import VoltageDataReport_protocol

curdir = os.getcwd()
cpath = curdir + "\\..\\..\\"
sys.path.append(cpath)

from lib.protocol.report.CommonReport_protocol import CommonReport_protocol
from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.OBDReport_CAN_protocol import OBDReport_CAN_protocol
from lib.protocol.report.OBDReport_CAN_protocol import OBDReport_CAN_protocol
from lib.protocol.report.HeartBeatReport_protocol import HeartBeatReport_protocol
from lib.protocol.report.LoginReport_protocol import LoginReport_protocol
from lib.protocol.report.SecurityStatusReport_protocol import SecurityStatusReport_protocol
from lib.protocol.report.BaseStationReport_protocol import BaseStationReport_protocol
from lib.protocol.report.SleepReport_protocol import SleepReport_protocol
from lib.protocol.report.TroubleReport_protocol import TroubleReport_protocol
from lib.protocol.report.EventReport_protocol import EventReport_protocol

# host = "10.100.12.34"
# port = 8712
from lib.protocol.report.VersionReport_protocol import VersionReport_protocol

host = "10.100.12.32"
port = 9008

# host = "10.100.5.251"
# port = 9008

# msg = GPSReport_protocol().generateGpsMsg()                         #GPS消息数据
# msg = OBDReport_protocol().generateOBDReportMsg()                   #OBD终端上报数据
# msg = OBDReport_CAN_protocol().generateOBDReportCANMsg()            #OBD终端上报CAN数据
# msg = HeartBeatReport_protocol().generateHeartBeatMsg()             #终端上报心跳协议
# msg = LoginReport_protocol().generateLoginMsg()                     #终端上报登录协议
# msg = SecurityStatusReport_protocol().generateSecurityStatusMsg()   #终端上报安防状态协议
# msg = BaseStationReport_protocol().generateBaseStationMsg()         #终端上报基站定位协议
# msg = TroubleReport_protocol().generateTroubleMsg()                 #终端上报故障码数据包
msg = EventReport_protocol().generateEventMsg()                      #终端上报事件数据包
# msg = VersionReport_protocol().generateVersionMsg()                   #终端上报版本信息数据包
# msg = SleepReport_protocol().generateSleepMsg()                       #终端休眠数据包
# msg = CommonReport_protocol().generateCommonMsg()                       #通用应答消息
# msg = VoltageDataReport_protocol().generateMsg()                     #终端上报电瓶电压采样数据
# msg = TroubleCode_protocol().generateMsg()                             #终端上报故障码数据包
# msg = SensorSampling_protocol().generateMsg()                            #1.2.37终端上报Sensor采样数据
print(msg)
BUF_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳
client.connect((host, port))
client.send(binascii.a2b_hex(msg))

# client.send(bytes.fromhex(msg))
data = client.recv(BUF_SIZE)
print(data)
print(binascii.b2a_hex(data))
client.close()

