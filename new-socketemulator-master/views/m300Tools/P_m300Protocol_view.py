#coding:utf-8
from configparser import ConfigParser

from flask import Blueprint, render_template ,request
import re

P_m300Protocol_view = Blueprint('P_m300Protocol_view', __name__)

##########################################
#   【视图类型】访问socket设置页面
##########################################
@P_m300Protocol_view.route('/socketSetting_page')
def socketSetting_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/socketSetting_page.html"
    arg["path"] = reqPath.split("/")
    arg["socket"] = {}
    # 读取config文件
    conf_R = ConfigParser()
    conf_R.read("config/m300Tools/m300Tools.conf")
    arg["socket"]["host"] = conf_R.get("socket", "host")
    arg["socket"]["port"] = conf_R.getint("socket", "port")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问用户自定义消息页面
##########################################
@P_m300Protocol_view.route('/P_userDefined_m300_page')
def P_userDefined_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_userDefined_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问心跳协议页面
##########################################
@P_m300Protocol_view.route('/P_heartBeat_m300_page')
def P_heartBeat_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_heartBeat_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问登录协议页面
##########################################
@P_m300Protocol_view.route('/P_login_m300_page')
def P_login_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_login_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问版本协议页面
##########################################
@P_m300Protocol_view.route('/P_version_m300_page')
def P_version_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_version_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问 GPS 协议页面
##########################################
@P_m300Protocol_view.route('/P_GPS_m300_page')
def P_GPS_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_GPS_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问OBD CAN协议页面
##########################################
@P_m300Protocol_view.route('/P_CAN_m300_page')
def P_CAN_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_CAN_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问OBD CAN协议页面
##########################################
@P_m300Protocol_view.route('/P_alarm_m300_page')
def P_alarm_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_alarm_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问OBD CAN协议页面
##########################################
@P_m300Protocol_view.route('/P_travelAct_m300_page')
def P_travelAct_m300_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "m300Tools/report/P_travelAct_m300_page.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)