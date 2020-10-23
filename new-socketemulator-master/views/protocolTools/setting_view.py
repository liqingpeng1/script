#coding:utf-8

from flask import Blueprint, render_template ,request
from configparser import ConfigParser
import re

setting_view = Blueprint('setting_view', __name__)


##########################################
#   【视图类型】访问socket设置页面
##########################################
@setting_view.route('/socketSetting_page')
def socketSetting_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/setting/socketSetting.html"
    arg["path"] = reqPath.split("/")
    arg["socket"] = {}
    # 读取config文件
    conf_R = ConfigParser()
    conf_R.read("config/protocolTools/protocolTools.conf")
    arg["socket"]["host"] = conf_R.get("socket", "host")
    arg["socket"]["port"] = conf_R.getint("socket", "port")
    return render_template(path,arg=arg)
