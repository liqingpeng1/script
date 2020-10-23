#coding:utf-8

from flask import Blueprint ,Response,request
from configparser import ConfigParser

from lib.protocol.reportPlateform.Common_res import Common_res
from lib.socket.ClientSocket import ClientSocket
import json
import traceback
import binascii

from lib.util import fileUtil

mapTools_process = Blueprint('mapTools_process', __name__)

##########################################
#   【接口类型】获取模拟器的GPSline
##########################################
@mapTools_process.route("/getGPSLineList",methods=['POST'])
def getGPSLineList():
    type = int(request.form.get("type"))

    data = {}
    if (type == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            if(type == 0):
                data["status"] = "200"
                data["gpsLines"] = fileUtil.getDirFilesListMap("data/protocolTools/GPSLines")
            elif(type == 1):
                data["status"] = "200"
                data["gpsLines"] = fileUtil.getDirFilesListMap("data/m300Tools/GPSLines")
            elif(type == 2):
                data["status"] = "200"
                data["gpsLines"] = fileUtil.getDirFilesListMap("data/messageTools/GPSLines")
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】获取GPSline 数据
##########################################
@mapTools_process.route("/getGPSLineData",methods=['POST'])
def getGPSLineData():
    type = int(request.form.get("type"))
    gpsLine = request.form.get("gpsLine")

    data = {}
    if (type == None or gpsLine == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            if (type == 0):
                with open("data/protocolTools/GPSLines/" + gpsLine, "r", encoding="utf-8") as fi:
                    content = fi.read()
                    conJson = json.loads(content)
                    gpsLines = conJson["GPSLine"]
                    # theGpsLines = []
                    # for item in gpsLines:
                    #     tem = []
                    #     tem.append(float(item["lng"].replace("\n","")))
                    #     tem.append(float(item["lat"].replace("\n","")))
                data["status"] = "200"
                # data["gpsLines"] = theGpsLines
                data["GPSLine"] = gpsLines
            elif (type == 1):
                with open("data/m300Tools/GPSLines/" + gpsLine, "r", encoding="utf-8") as fi:
                    content = fi.read()
                    conJson = json.loads(content)
                    gpsLines = conJson["GPSLine"]
                    theGpsLines = []
                    for item in gpsLines:
                        tem = []
                        tem.append(float(item["lng"].replace("\n","")))
                        tem.append(float(item["lat"].replace("\n","")))
                        theGpsLines.append(tem)
                data["status"] = "200"
                data["gpsLines"] = theGpsLines
            elif (type == 2):
                with open("data/messageTools/GPSLines/" + gpsLine, "r", encoding="utf-8") as fi:
                    content = fi.read()
                    conJson = json.loads(content)
                    gpsLines = conJson["GPSLine"]
                    theGpsLines = []
                    for item in gpsLines:
                        tem = []
                        tem.append(float(item["lng"].replace("\n","")))
                        tem.append(float(item["lat"].replace("\n","")))
                        theGpsLines.append(tem)
                data["status"] = "200"
                data["gpsLines"] = theGpsLines
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

