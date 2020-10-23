#coding:utf-8

from flask import Blueprint, render_template ,request
import re

protocolReport_view = Blueprint('protocolReport_view', __name__)

##########################################
#   【视图类型】访问自定义报文发送页面
##########################################
@protocolReport_view.route('/userDefined_protocol_page')
def userDefined_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/userDefined_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问心跳协议报文发送页面
##########################################
@protocolReport_view.route('/heartBeat_protocol_page')
def heartBeat_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/heartBeat_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)


##########################################
#   【视图类型】访问终端登录协议报文发送页面
##########################################
@protocolReport_view.route('/login_protocol_page')
def login_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/login_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)


##########################################
#   【视图类型】访问GPS协议报文发送页面
##########################################
@protocolReport_view.route('/GPS_protocol_page')
def GPS_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/GPS_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问OBD_CAN协议报文发送页面
##########################################
@protocolReport_view.route('/OBD_CAN_protocol_page')
def OBD_CAN_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/OBD_CAN_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)


##########################################
#   【视图类型】访问终端上报安防状态协议报文发送页面
##########################################
@protocolReport_view.route('/securityStatus_protocol_page')
def securityStatus_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/securityStatus_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)


##########################################
#   【视图类型】访问终端上报电瓶电压协议报文发送页面
##########################################
@protocolReport_view.route('/voltageData_protocol_page')
def voltageData_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/voltageData_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)


##########################################
#   【视图类型】访问终端上报事件协议报文发送页面
##########################################
@protocolReport_view.route('/event_protocol_page')
def event_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/event_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问终端上报故障码报文发送页面
##########################################
@protocolReport_view.route('/troubleCode_protocol_page')
def troubleCode_protocol_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/troubleCode_protocol_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)