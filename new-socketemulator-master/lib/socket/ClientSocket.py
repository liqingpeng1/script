#coding:utf-8

import socket
from time import sleep
from lib.socket.SocketBase import SocketBase
import binascii
import random
import string
import traceback

'''
定义客户端socket类
'''

class ClientSocket(SocketBase):
    def __init__(self, host="127.0.0.1", port=5000):
        #socke连接的标识，生成一个长度为8的随机字符串
        self.socketId = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        self.port = port
        self.host = host
        self.timeOut = 1                                     #设置连接超时时间
        # 0代表未连接  ， 1代表socket处于连接状态
        self.status = 0
        self.BUF_SIZE = 1024

    #####################################################
    #               连接服务器
    #####################################################
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳
        # 设置连接socket的超时时间
        self.client.settimeout(self.timeOut)
        self.client.connect((self.host, self.port))
        self.status = 1

    #####################################################
    #               发送消息
    #####################################################
    def send(self, msg):
        # 设置发送消息的超时时间
        self.client.settimeout(self.timeOut)
        self.client.send(binascii.a2b_hex(msg))

    def receive(self):
        data = ""
        try:
            # 设置接收消息的超时时间
            self.client.settimeout(self.timeOut)
            data = self.client.recv(self.BUF_SIZE)
        except BaseException as e:
            # traceback.print_exc()
            self.client.close()
            self.status = 0
            raise RuntimeError('socket 接收消息超时！')
        return data

    #####################################################
    #               断开socket
    #####################################################
    def close(self):
        # self.client.send("_end".encode())    //发送一个socket断开的命令
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        self.status = 0

    #设置服务器域名
    def setHost(self,host):
        self.host = host
    #设置要连接的服务器端口
    def setPort(self,port):
        self.port = port
    #获取该连接的socket ID号
    def getSocketId(self):
        return self.socketId
    def getSocketStatus(self):
        return self.status
    def setTimeOut(self,data):
        self.timeOut = data

if __name__ == "__main__":
    client = ClientSocket()
    client.connect()
    for i in range(0,10):
        client.send("world" + str(i))
        sleep(1)
        print(i)
    client.close()