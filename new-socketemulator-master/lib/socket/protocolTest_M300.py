#coding:utf-8
import binascii
import socket

from lib.protocol.m300.Alarm_protocol_m300 import Alarm_protocol_m300
from lib.protocol.m300.GPS_protocol_m300 import GPS_protocol_m300
from lib.protocol.m300.Heartbeat_protocol_300 import Heartbeat_protocol_300
from lib.protocol.m300.OBDCAN_protocol_m300 import OBDCAN_protocol_m300
from lib.protocol.m300.TravelAct_protocol_m300 import TravelAct_protocol_m300
from lib.protocol.m300.VersionInfo_protocol_m300 import VersionInfo_protocol_m300
from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.OBDReport_CAN_protocol import OBDReport_CAN_protocol
from lib.protocol.report.OBDReport_CAN_protocol import OBDReport_CAN_protocol
from lib.protocol.report.HeartBeatReport_protocol import HeartBeatReport_protocol
from lib.protocol.report.LoginReport_protocol import LoginReport_protocol
from lib.protocol.report.SecurityStatusReport_protocol import SecurityStatusReport_protocol
from lib.protocol.report.BaseStationReport_protocol import BaseStationReport_protocol
from lib.protocol.report.TroubleReport_protocol import TroubleReport_protocol
from lib.protocol.report.EventReport_protocol import EventReport_protocol

# host = "10.100.12.34"
# port = 8712

host = "10.100.12.32"
port = 9009

# host = "10.100.5.251"
# port = 9009

# host = "10.100.5.251"
# port = 9009

# msg = Heartbeat_protocol_300().generateMsg()                            #心跳报文
# msg = GPS_protocol_m300().generateMsg()                                 #GPS报文
# msg = VersionInfo_protocol_m300().generateMsg()                         #终端版本报文
# msg = "7e000400e14d2019120315000000957e"   #终端上报心跳协议
# msg = OBDCAN_protocol_m300().generateMsg()                              #OBD CAN报文
# msg = Alarm_protocol_m300().generateMsg()                              #报警报文
msg = TravelAct_protocol_m300().generateMsg()                             #驾驶行为报文


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

