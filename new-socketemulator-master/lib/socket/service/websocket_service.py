#coding: utf-8
import json
import logging
import threading
import time
import traceback
from time import sleep

from lib.socket.SocketBase import SocketBase
from lib.socket.websocket_server import WebsocketServer

class Websocket_service(SocketBase):
    def __init__(self,host="0.0.0.0",port=5005):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}
        self.currentClient = None

    def setHost(self,data):
        self.host = data
    def setPort(self,data):
        self.port = data

    def getCurrentClientId(self):
        return self.currentClient

    def startWebsocketServer(self):
        server = WebsocketServer(self.port, host=self.host, loglevel=logging.INFO)
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.doRev)
        self.server = server
        server.run_forever()
        server.server_close()

    #有客户端连接成功之后，回复一条消息
    def new_client(self,client, server):
        # server.send_message_to_all("连接成功......")
        clientId = "client_" + str(len(self.clients))
        data = {}
        data["code"] = "0001"                                #收到连接请求
        data["client"] = clientId
        data["msg"] = "websocket连接成功......"
        data = json.dumps(data)
        self.currentClient = clientId
        server.send_message(client, data)
        self.clients[clientId] = client
        self.connectTimeout = 1

    #收到消息之后进行处理的方法
    def doRev(self,client,server,msg):
        # server.send_message(client,"message send ...")
        data = json.loads(msg)
        code = data["code"]
        theMsg = data["msg"]
        clientId = data["client"]
        self.currentClient = clientId
        if(code == "0002"):                                       #收到一条普通消息
            data = {}
            data["code"] = "0002"
            data["client"] = clientId
            data["msg"] = "收到消息：" + theMsg
            data = json.dumps(data)
            server.send_message(client, data)
        if(code == "0000"):                                      #收到 0000 控制码的时候，关闭socket服务
            server.server_close()
            print("连接断开...")
        if(code == "0003"):                                      #断开与客户端的连接
            self.clients.pop(clientId)
            data = {}
            data["code"] = "0003"
            data["client"] = clientId
            data["msg"] = "断开连接！"
            data = json.dumps(data)
            server.send_message(client, data)
            raise Exception("客户端连接断开")


    #断开服务端的socket服务
    def close(self):
        self.server.server_close()

    #给当前连接的客户端发送消息
    def send(self,msg):
        data = {}
        data["code"] = "0002"
        data["client"] = self.currentClient
        data["msg"] = "收到消息：" + msg
        data = json.dumps(data)
        self.server.send_message(self.clients[self.currentClient],data)

    #给指定客户端发送消息
    def sendMsgToClient(self,msg,clientId):
        data = {}
        data["code"] = "0002"
        data["client"] = self.currentClient
        data["msg"] = "收到消息：" + msg
        data = json.dumps(data)
        self.server.send_message(self.clients[clientId],data)



if __name__ == "__main__":
    w = Websocket_service()
    w.setHost("127.0.0.1")
    w.setPort(5005)
    w.startWebsocketServer()