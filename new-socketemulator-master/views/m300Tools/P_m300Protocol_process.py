#coding:utf-8

from flask import Blueprint ,Response,request
from configparser import ConfigParser

from lib.protocol.m300.Alarm_protocol_m300 import Alarm_protocol_m300
from lib.protocol.m300.GPS_protocol_m300 import GPS_protocol_m300
from lib.protocol.m300.Heartbeat_protocol_300 import Heartbeat_protocol_300
from lib.protocol.m300.Login_protocol_m300 import Login_protocol_m300
from lib.protocol.m300.OBDCAN_protocol_m300 import OBDCAN_protocol_m300
from lib.protocol.m300.TravelAct_protocol_m300 import TravelAct_protocol_m300
from lib.protocol.m300.VersionInfo_protocol_m300 import VersionInfo_protocol_m300
from lib.protocol.m300Plateform.M300Common_res import M300Common_res
from lib.protocol.m300Plateform.M300Login_res import M300Login_res

from lib.socket.ClientSocket import ClientSocket
import json
import traceback
import binascii

from lib.util.jsonUtil import hasJsonDataIsNone

P_m300Protocol_process = Blueprint('P_m300Protocol_process', __name__)

##########################################
#   【接口类型】保存设置
##########################################
@P_m300Protocol_process.route("/porcessSocketSetting",methods=['POST'])
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
            conf_R.read("config/m300Tools/m300Tools.conf")
            conf_W = conf_R
            conf_W["socket"]["host"] = host
            conf_W["socket"]["port"] = port
            with open("config/m300Tools/m300Tools.conf", "w") as fi:
                conf_W.write(fi)
            data["status"] = "200"
            data["message"] = "Sucess: "
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的自定义报文
##########################################
@P_m300Protocol_process.route("/porcessUserdefinedMsg",methods=['POST'])
def porcessUserdefinedMsg():
    msg = request.form.get("msg")
    timeout = int(request.form.get("timeout"))

    data = {}
    if (msg == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            cliSocket.send(msg)
            cliSocket.setTimeOut(timeout)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的心跳上报报文
##########################################
@P_m300Protocol_process.route("/porcessHeartBeatMsg",methods=['POST'])
def porcessHeartBeatMsg():
    FUNID = request.form.get("FUNID")
    waterCode = int(request.form.get("waterCode"))
    DEV_ID = request.form.get("DEV_ID")
    encryptionType = int(request.form.get("encryptionType"))

    data = {}
    if (waterCode == None or DEV_ID == None or encryptionType == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            heartBeatProtocolObj = Heartbeat_protocol_300(waterCode = waterCode,DEV_ID = DEV_ID,encryptionType=encryptionType)
            msg = heartBeatProtocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的登录上报报文
##########################################
@P_m300Protocol_process.route("/porcessLoginMsg",methods=['POST'])
def porcessLoginMsg():
    FUNID = request.form.get("FUNID")
    waterCode = int(request.form.get("waterCode"))
    DEV_ID = request.form.get("DEV_ID")
    encryptionType = int(request.form.get("encryptionType"))

    data = {}
    if (waterCode == None or DEV_ID == None or encryptionType == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = Login_protocol_m300(waterCode = waterCode,DEV_ID = DEV_ID,encryptionType=encryptionType)
            msg = protocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Login_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的版本信息上报报文
##########################################
@P_m300Protocol_process.route("/porcessVersionMsg",methods=['POST'])
def porcessVersionMsg():
    FUNID = request.form.get("FUNID")
    waterCode = int(request.form.get("waterCode"))
    DEV_ID = request.form.get("DEV_ID")
    encryptionType = int(request.form.get("encryptionType"))

    SWVersion = request.form.get("SWVersion")
    SWDate = request.form.get("SWDate")
    HWVersion = request.form.get("HWVersion")
    GSMType = request.form.get("GSMType")
    carType = request.form.get("carType")
    engineCode = int(request.form.get("engineCode"))
    VINCode = request.form.get("VINCode")

    data = {}
    if (waterCode == None or DEV_ID == None or encryptionType == None or SWVersion == None or SWDate == None or HWVersion == None \
            or GSMType == None or carType == None or engineCode == None or VINCode == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = VersionInfo_protocol_m300(waterCode = waterCode,DEV_ID = DEV_ID,encryptionType=encryptionType,SWVersion=SWVersion \
            ,SWDate=SWDate,HWVersion=HWVersion,GSMType=GSMType,carType=carType,engineCode=engineCode,VINCode=VINCode)
            msg = protocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的GPS信息上报报文
##########################################
@P_m300Protocol_process.route("/porcessGPSMsg",methods=['POST'])
def porcessGPSMsg():
    FUNID = request.form.get("FUNID")
    waterCode = int(request.form.get("waterCode"))
    DEV_ID = request.form.get("DEV_ID")
    encryptionType = int(request.form.get("encryptionType"))

    dateInfo = request.form.get("dateInfo")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    positionStar = int(request.form.get("positionStar"))
    speed = float(request.form.get("speed"))
    direction = float(request.form.get("direction"))
    altitude = float(request.form.get("altitude"))
    ACCStatus = int(request.form.get("ACCStatus"))
    valtage = float(request.form.get("valtage"))
    OBDSpeed = float(request.form.get("OBDSpeed"))
    valid = int(request.form.get("valid"))
    tripMark = int(request.form.get("tripMark"))

    data = {}
    if (waterCode == None or DEV_ID == None or encryptionType == None or dateInfo == None or latitude == None or longitude == None \
            or positionStar == None or speed == None or direction == None or altitude == None or ACCStatus == None or valtage == None \
            or OBDSpeed == None or valid == None or tripMark == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = GPS_protocol_m300(waterCode = waterCode,DEV_ID = DEV_ID,encryptionType=encryptionType,dateInfo=dateInfo \
            ,latitude=latitude,longitude=longitude,positionStar=positionStar,speed=speed,direction=direction,altitude=altitude \
            ,ACCStatus=ACCStatus,valtage=valtage,OBDSpeed=OBDSpeed,valid=valid,tripMark=tripMark)
            msg = protocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的OBD CAN 信息上报报文
##########################################
@P_m300Protocol_process.route("/porcessCANMsg",methods=['POST'])
def porcessCANMsg():
    FUNID = request.form.get("FUNID")
    waterCode = int(request.form.get("waterCode"))
    DEV_ID = request.form.get("DEV_ID")
    encryptionType = int(request.form.get("encryptionType"))

    timeInfo = request.form.get("timeInfo")
    prototolType = request.form.get("prototolType")
    statusMask = request.form.get("statusMask")
    safeStatus = int(request.form.get("safeStatus"))
    doorStatus = int(request.form.get("doorStatus"))
    lockStatus = int(request.form.get("lockStatus"))
    windowStatus = int(request.form.get("windowStatus"))
    lightStatus = int(request.form.get("lightStatus"))
    swichStatusA = int(request.form.get("swichStatusA"))
    swichStatusB = int(request.form.get("swichStatusB"))
    dataBit = int(request.form.get("dataBit"))
    dataFlowMask = request.form.get("dataFlowMask")
    votage = int(request.form.get("votage"))
    totalMilleageType = int(request.form.get("totalMilleageType"))
    totalMilleage = int(request.form.get("totalMilleage"))
    totalOil = int(request.form.get("totalOil"))
    troubleLightStatus = int(request.form.get("troubleLightStatus"))
    troubleCodeNum = int(request.form.get("troubleCodeNum"))
    engineSpeed = int(request.form.get("engineSpeed"))
    speed = int(request.form.get("speed"))
    airInletTemperature = int(request.form.get("airInletTemperature"))
    coolingLiquidTemperature = int(request.form.get("coolingLiquidTemperature"))
    envTemperature = int(request.form.get("envTemperature"))
    intakeManifoldPressure = int(request.form.get("intakeManifoldPressure"))
    oilPressure = int(request.form.get("oilPressure"))
    atmosphericPressure = int(request.form.get("atmosphericPressure"))
    airFlow = int(request.form.get("airFlow"))
    valveLocation = int(request.form.get("valveLocation"))
    acceleratorLocation = int(request.form.get("acceleratorLocation"))
    engineRunTime = int(request.form.get("engineRunTime"))
    troubleMileage = int(request.form.get("troubleMileage"))
    surplusOil = int(request.form.get("surplusOil"))
    engineLoad = int(request.form.get("engineLoad"))
    fuelTrim = int(request.form.get("fuelTrim"))
    fireAngle = int(request.form.get("fireAngle"))
    dashboardTotailMilleage = int(request.form.get("dashboardTotailMilleage"))
    carTotalRunTime = int(request.form.get("carTotalRunTime"))
    tripMark = request.form.get("tripMark")

    data = {}
    if (waterCode == None or DEV_ID == None or encryptionType == None or timeInfo == None or prototolType == None or statusMask == None \
            or safeStatus == None or doorStatus == None or lockStatus == None or windowStatus == None or lightStatus == None or swichStatusA == None \
            or swichStatusB == None or dataBit == None or dataFlowMask == None or votage == None or totalMilleageType == None or totalMilleage == None \
            or totalOil == None or troubleLightStatus == None or troubleCodeNum == None or engineSpeed == None or speed == None or airInletTemperature == None \
            or coolingLiquidTemperature == None or envTemperature == None or intakeManifoldPressure == None or oilPressure == None or atmosphericPressure == None or airFlow == None \
            or valveLocation == None or acceleratorLocation == None or engineRunTime == None or troubleMileage == None or surplusOil == None or engineLoad == None \
            or fuelTrim == None or fireAngle == None or dashboardTotailMilleage == None or carTotalRunTime == None or tripMark == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = OBDCAN_protocol_m300(waterCode=waterCode,DEV_ID=DEV_ID,encryptionType=encryptionType,timeInfo=timeInfo,prototolType=prototolType,statusMask=statusMask \
            ,safeStatus=safeStatus,doorStatus=doorStatus,lockStatus=lockStatus,windowStatus=windowStatus,lightStatus=lightStatus,swichStatusA=swichStatusA \
            ,swichStatusB=swichStatusB,dataBit=dataBit,dataFlowMask =dataFlowMask, votage =votage, totalMilleageType =totalMilleageType, totalMilleage =totalMilleage \
            ,totalOil =totalOil, troubleLightStatus =troubleLightStatus, troubleCodeNum =troubleCodeNum, engineSpeed =engineSpeed,speed =speed, airInletTemperature =airInletTemperature \
            ,coolingLiquidTemperature =coolingLiquidTemperature, envTemperature =envTemperature, intakeManifoldPressure =intakeManifoldPressure, oilPressure =oilPressure \
            ,atmosphericPressure =atmosphericPressure, airFlow =airFlow ,valveLocation =valveLocation, acceleratorLocation =acceleratorLocation, engineRunTime =engineRunTime
            ,troubleMileage =troubleMileage, surplusOil =surplusOil, engineLoad =engineLoad,fuelTrim =fuelTrim, fireAngle =fireAngle, dashboardTotailMilleage =dashboardTotailMilleage \
            ,carTotalRunTime =carTotalRunTime, tripMark =tripMark)
            msg = protocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的报警报文
##########################################
@P_m300Protocol_process.route("/porcessAlarmMsg",methods=['POST'])
def porcessAlarmMsg():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    data = {}
    if (hasJsonDataIsNone(params)):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = Alarm_protocol_m300(waterCode=int(params["waterCode"]),DEV_ID=params["DEV_ID"],encryptionType=int(params["encryptionType"]), \
                                              alarmType=list(params["alarm"].keys())[0],data=params)
            msg = protocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的驾驶行为报文
##########################################
@P_m300Protocol_process.route("/porcessTravelActMsg",methods=['POST'])
def porcessTravelActMsg():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    data = {}
    if (hasJsonDataIsNone(params)):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/m300Tools/m300Tools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = TravelAct_protocol_m300(waterCode=int(params["waterCode"]), DEV_ID=params["DEV_ID"],encryptionType=int(params["encryptionType"]), \
                        actType=int(params["actType"]),accelerateTotalTimes=int(params["accelerateTotalTimes"]),decelerateTotalTimes=int(params["decelerateTotalTimes"]), \
                        sharpTurnTotalTimes=int(params["sharpTurnTotalTimes"]),acceleration=int(params["acceleration"]), speed=int(params["speed"]),gps=params["gps"])
            msg = protocolObj.generateMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(M300Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')