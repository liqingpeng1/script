#coding:utf-8

#########################################################
#
#                定义服务端socket类
#
#########################################################
import socket
from time import sleep
from lib.socket.SocketBase import SocketBase


class ServerSocket(SocketBase):

    def __init__(self,host="127.0.0.1",port=5000):
        self.host = host
        self.port = port
        self.status = 0   #0代表socket停止服务，1代表socket服务运行
        self.BUF_SIZE = 1024

    #####################################################
    #                 创建一个服务端套接字
    #####################################################
    def createServerSocket(self):
        serverSocket = socket.socket()  #默认为ipv4，tcp连接
        #下面创建socketyu8上面创建的没有区别（AF_INET：ipv4，SOCK_STREAM代表使用TCP连接）
        # serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.host,self.port))
        return serverSocket

    #####################################################
    #                 启动socket服务
    #####################################################
    def startServer(self):
        self.status = 1
        server = self.createServerSocket()

        # 设置接收的连接数为1
        server.listen(1)
        server.settimeout(10)
        client, address = server.accept()

        while self.status == 1:  # 循环收发数据包，长连接
            data = client.recv(self.BUF_SIZE)
            text = data.decode()
            sleep(1)

            if text != "":
                print(text)  # python3 要使用decode
                client.send("world".encode())
                # client.close() #连接不断开，长连接

            #接收到断开连接的信息后，关闭socket；应为python的socket没有提供获取服务端自身socket的状态或者客户端是否断开了连接
            if text == "_end":
                self.close()


    def close(self):
        self.status = 0

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def setHost(self,host):
        self.host = host

    def setPort(self,port):
        self.port = port



if __name__ == "__main__":
    server = ServerSocket("localhost", 5000)
    server.createServerSocket()
    server.startServer()