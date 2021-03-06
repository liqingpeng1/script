#coding:utf-8
from configparser import ConfigParser

from flask import Blueprint, render_template ,request
import re

from lib.util import fileUtil

M_simulater_view = Blueprint('M_simulater_view', __name__)

##########################################
#   【视图类型】访问模拟器页面
##########################################
@M_simulater_view.route('/M_simulater_page')
def M_simulater_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/M_simulater_page.html"
    arg["path"] = reqPath.split("/")
    arg["gpsLines"] = fileUtil.getDirFilesListMap("data/messageTools/GPSLines")
    return render_template(path,arg=arg)

##########################################
#   【视图类型】访问模拟器设置页面
##########################################
@M_simulater_view.route('/M_simulaterSetting_page')
def M_simulaterSetting_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/message/M_simulaterSetting_page.html"
    arg["path"] = reqPath.split("/")
    arg["socket"] = {}
    # 读取config文件
    conf_R = ConfigParser()
    conf_R.read("config/messageTools/carSimulater.conf")
    arg["socket"]["host"] = conf_R.get("socket", "host")
    arg["socket"]["port"] = conf_R.getint("socket", "port")
    return render_template(path,arg=arg)