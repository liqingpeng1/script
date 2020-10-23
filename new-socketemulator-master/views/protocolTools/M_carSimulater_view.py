#coding:utf-8
from configparser import ConfigParser

from flask import Blueprint, render_template ,request
import re
from lib.util import fileUtil

M_carSimulater_view = Blueprint('M_carSimulater_view', __name__)

##########################################
#   【视图类型】访问侧车机模拟器页面
##########################################
@M_carSimulater_view.route('/M_carSimulater_page')
def M_carSimulater_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/M_carSimulater_page.html"
    arg["path"] = reqPath.split("/")
    arg["gpsLines"] = fileUtil.getDirFilesListMap("data/protocolTools/GPSLines")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问模拟器设置页面
##########################################
@M_carSimulater_view.route('/M_setting_page')
def M_setting_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/M_setting_page.html"
    arg["path"] = reqPath.split("/")
    arg["socket"] = {}
    # 读取config文件
    conf_R = ConfigParser()
    conf_R.read("config/protocolTools/carSimulater.conf")
    arg["socket"]["host"] = conf_R.get("socket", "host")
    arg["socket"]["port"] = conf_R.getint("socket", "port")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问模拟器查询车数据页面
##########################################
@M_carSimulater_view.route('/M_carSimulaterData_page')
def M_carSimulaterData_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/report/M_carSimulaterData_page.html"
    arg["path"] = reqPath.split("/")
    arg["socket"] = {}
    # 读取config文件
    conf_R = ConfigParser()
    conf_R.read("config/protocolTools/carSimulater.conf")
    arg["socket"]["host"] = conf_R.get("socket", "host")
    arg["socket"]["port"] = conf_R.getint("socket", "port")
    return render_template(path,arg=arg)