#coding:utf-8

from flask import Blueprint ,Response,request
from configparser import ConfigParser

import json
import traceback

setting_process = Blueprint('setting_process', __name__)

##########################################
#   【接口类型】保持设置
##########################################
@setting_process.route("/porcessSocketSetting",methods=['POST'])
def porcessSocketSetting():
    host = request.form.get("host")
    port = request.form.get("port")

    data = {}
    if (host == None or port == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            # d读取config文件
            conf_R = ConfigParser()
            conf_R.read("config/protocolTools/protocolTools.conf")
            conf_W = conf_R
            conf_W["socket"]["host"] = host
            conf_W["socket"]["port"] = port
            with open("config/protocolTools/protocolTools.conf", "w") as fi:
                conf_W.write(fi)
            data["status"] = "200"
            data["message"] = "Sucess: "
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')


