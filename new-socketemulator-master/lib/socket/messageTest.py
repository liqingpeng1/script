#coding:utf-8
import binascii
import socket
import traceback

from lib.protocol.message.DataUpstreamTransport_msg import DataUpstreamTransport_msg
from lib.protocol.message.LocationDataBatchUpdate_msg import LocationDataBatchUpdate_msg
from lib.protocol.message.Location_msg import Location_msg
from lib.protocol.message.PlateformUpdateRes_msg import PlateformUpdateRes_msg
from lib.protocol.message.TerminalAuthenticate_msg import TerminalAuthenticate_msg
from lib.protocol.message.TerminalCommonMsgRes_msg import TerminalCommonMsgRes_msg
from lib.protocol.message.TerminalHeartbeat_msg import TerminalHeartbeat_msg
from lib.protocol.message.TerminalRegister_msg import TerminalRegister_msg
from lib.protocol.message.TerminalVersionInfo_msg import TerminalVersionInfo_msg
from lib.protocol.message.TextInfoUpload_msg import TextInfoUpload_msg
from lib.protocol.messagePlateform.PlateformVersionInfo_res import PlatefromVersionInfo_res
from lib.protocol.messagePlateform.PlatformCommon_res import PlatformCommon_res
from lib.protocol.messagePlateform.TerminalRegister_res import TerminalRegister_res

# host = "10.100.11.20"
# port = 9001

host = "10.100.12.32"
port = 9001

# msg = MessageBase().generateMsg()
# msg = TerminalCommonMsgRes_msg().generateMsg()       #终端通用应答
# msg = TerminalHeartbeat_msg().generateMsg()          #终端心跳
# msg = TerminalRegister_msg().generateMsg()           #终端注册
# msg = TerminalCancle_msg().generateMsg()             #终端注销
# msg = TerminalAuthenticate_msg().generateMsg()       #终端鉴权
# msg = TerminalVersionInfo_msg().generateMsg()        #终端版本信息上报
# msg = QueryTerminalParam_res().generateMsg()         #查询终端参数应答
# msg = QueryTerminalProperty_res().generateMsg()      #查询终端属性应答消息
# msg = Location_msg().generateMsg()                   #位置信息汇报
msg = DataUpstreamTransport_msg().generateMsg()      #数据上行透传消息
# msg = TerminalUpdataResult_msg().generateMsg()       #终端升级结果通知
# msg = LocationDataBatchUpdate_msg().generateMsg()    #定位数据批量上传
# msg = TextInfoUpload_msg().generateMsg()             #文本信息上传
# msg = PlateformUpdateRes_msg().generateMsg()         #平台升级数据包应答

#发送单条消息
def sendSingleMsg(msg):
    print(msg)
    BUF_SIZE = 1024

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳
    client.settimeout(1)
    try:
        client.connect((host, port))
        client.send(binascii.a2b_hex(msg))
        # client.send(bytes.fromhex(msg))
    except BaseException as e:
        traceback.print_exc()
        client.close()
        print("连接超时，socket断开")
        return
    try:
        data = client.recv(BUF_SIZE)
        # print(data)
    except BaseException as e:
        traceback.print_exc()
        client.close()
        # raise RuntimeError('socket 接收消息超时！')
        print('socket 接收消息超时！')
        return
    print(data)
    print(PlatformCommon_res(data).getOriginalMsg())
    # print(PlatformCommon_res(data).getMsg())               #解析平台通用应答消息
    # print(TerminalRegister_res(data).getMsg())           #解析终端注册应答消息
    # print(PlatefromVersionInfo_res(data).getMsg())         #解析平台版本信息包上传应答
    client.close()

def closeSocket(soc):
    soc.close
def connectSock():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳
    client.connect((host, port))
    return client
def sendMsg(client,msg):
    print("发送的消息为：" + msg)
    BUF_SIZE = 1024
    client.send(binascii.a2b_hex(msg))
    data = client.recv(BUF_SIZE)
    if PlatformCommon_res(data).getMsg()["header"]["msgId"] == "0100":     #终端注册应答
        print("收到的消息：" + str(TerminalRegister_res(data).getMsg()))
    else:
        print("收到的消息：" + str(PlatformCommon_res(data).getMsg()))     #平台通用应答
    return client
def sendMultMsg():
    pass



if __name__ == "__main__":
    sendSingleMsg(msg)

    '''
    print("发送终端注册消息")
    client = connectSock()
    msg = TerminalRegister_msg().generateMsg()           #终端注册
    sendMsg(client,msg)
    sleep(2)
    print("发送终端心跳消息")
    msg = TerminalHeartbeat_msg().generateMsg()  # 终端心跳
    sendMsg(client,msg)
    sleep(2)
    print("发送终端鉴权消息")
    msg = TerminalAuthenticate_msg().generateMsg()  # 终端鉴权
    sendMsg(client,msg)
    sleep(2)
    closeSocket(client)
    print("断开连接")
   '''






