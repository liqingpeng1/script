#coding:utf-8

from flask import Blueprint, render_template ,request
import re

message_view = Blueprint('message_view', __name__)

##########################################
#   【视图类型】访问心跳消息发送页面
##########################################
@message_view.route('/heartBeat_msg_page')
def heartBeat_msg_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/heartBeat_msg_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问用户自定义消息发送页面
##########################################
@message_view.route('/userDefined_msg_page')
def userDefined_msg_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/userDefined_msg_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问终端注册消息发送页面
##########################################
@message_view.route('/terminalRegister_msg_page')
def terminalRegister_msg_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/terminalRegister_msg_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问终端版本信息主动上报页面
##########################################
@message_view.route('/terminalVersionInfoUpload_msg_page')
def terminalVersionInfoUpload_msg_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/terminalVersionInfoUpload_msg_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问数据上行透传页面(驾驶行程数据)
##########################################
@message_view.route('/dataUpstreamTransport_msg_page')
def dataUpstreamTransport_msg_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/dataUpstreamTransport_msg_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问数据上行透传页面(故障码数据)
##########################################
@message_view.route('/dataUpstreamTransport_msg_f2_page')
def dataUpstreamTransport_msg_f2_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/dataUpstreamTransport_msg_f2_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问数据上行透传页面(休眠进入)
##########################################
@message_view.route('/dataUpstreamTransport_msg_f3_page')
def dataUpstreamTransport_msg_f3_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/dataUpstreamTransport_msg_f3_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问数据上行透传页面(休眠唤醒)
##########################################
@message_view.route('/dataUpstreamTransport_msg_f4_page')
def dataUpstreamTransport_msg_f4_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/dataUpstreamTransport_msg_f4_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】位置信息汇报
##########################################
@message_view.route('/location_msg_page')
def location_msg_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/location_msg_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)