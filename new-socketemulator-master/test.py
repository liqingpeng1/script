#coding: utf-8
import json
import logging
from configparser import ConfigParser

from lib.socket.websocket_server import WebsocketServer

def myConfigParser():
    #d读取config文件
    conf_R = ConfigParser()
    conf_R.read("config/protocolTools/protocolTools.conf")
    print(conf_R.get("socket","port"))

    #写入config文件
    conf_W = conf_R
    conf_W["socket"]["port"] = "9090"
    with open("config/protocolTools/protocolTools.conf","w") as fi:
        conf_W.write(fi)


def startWebsocketServer():
    def new_client(client, server):
        server.send_message_to_all("Hey all, a new client has joined us")

    def mysend(client,server,msg):
        print(msg)
        msgObj = json.loads(msg)
        msgtem = msgObj["msg"]
        server.send_message(client,msg)
        if(msgtem == "_end"):         #如果收到了_end 消息，那么断开连接
            print("服务端断开链接...")
            # server.shutdown()
            server.server_close()

    server = WebsocketServer(5005, host='0.0.0.0', loglevel=logging.INFO)
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(mysend)
    server.run_forever()
    server.server_close()

if __name__ == "__main__":
    startWebsocketServer()

