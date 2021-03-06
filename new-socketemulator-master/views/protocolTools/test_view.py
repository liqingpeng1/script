#coding:utf-8

from flask import Blueprint, render_template ,request
from configparser import ConfigParser
import re

test_view = Blueprint('test_view', __name__)


##########################################
#   【视图类型】访问test页面
##########################################
@test_view.route('/test_page')
def test_page():
    #获取请求的路劲
    url = request.url
    reqPath = re.findall("http://(.*)$",url)[0]
    reqPath = re.findall("/(.*)$", reqPath)[0]
    arg = {}
    path = "protocolTools/test/test.html"
    arg["path"] = reqPath.split("/")
    return render_template(path,arg=arg)
