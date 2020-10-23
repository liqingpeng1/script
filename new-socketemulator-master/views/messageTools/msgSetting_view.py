#coding:utf-8
from configparser import ConfigParser

from flask import Blueprint, render_template ,request
import re

msgSetting_view = Blueprint('msgSetting_view', __name__)

##########################################
#   【视图类型】访问心跳消息发送页面
##########################################
@msgSetting_view.route('/msgSetting_page')
def msgSetting_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "messageTools/setting/msgSetting_page.html"
    arg["path"] = reqPath.split("/")
    # 读取config文件
    arg["socket"] = {}
    conf_R = ConfigParser()
    conf_R.read("config/messageTools/messageTools.conf")
    arg["socket"]["host"] = conf_R.get("socket", "host")
    arg["socket"]["port"] = conf_R.getint("socket", "port")
    return render_template(path,arg=arg)
