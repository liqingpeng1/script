#coding:utf-8

from flask import Blueprint, render_template ,request
import re

from lib.util import fileUtil

mapTools_view = Blueprint('mapTools_view', __name__)

##########################################
#   【视图类型】访问模拟器页面
##########################################
@mapTools_view.route('/maptool_page')
def maptool_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "otherTools/maptool.html"
    arg["path"] = reqPath.split("/")
    arg["gpsLines"] = fileUtil.getDirFilesListMap("data/protocolTools/GPSLines")
    return render_template(path,arg=arg)
