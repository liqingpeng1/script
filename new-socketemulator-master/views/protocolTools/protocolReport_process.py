#coding:utf-8

from flask import Blueprint ,Response,request
from configparser import ConfigParser

from lib.protocol.report.EventReport_protocol import EventReport_protocol
from lib.protocol.report.HeartBeatReport_protocol import HeartBeatReport_protocol
from lib.protocol.report.LoginReport_protocol import LoginReport_protocol
from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.OBDReport_CAN_protocol import OBDReport_CAN_protocol
from lib.protocol.report.SecurityStatusReport_protocol import SecurityStatusReport_protocol
from lib.protocol.report.TroubleCodeReport_protocol import TroubleCode_protocol
from lib.protocol.report.VoltageDataReport_protocol import VoltageDataReport_protocol
from lib.protocol.reportPlateform.Common_res import Common_res
from lib.protocol.reportPlateform.Login_res import Login_res

from lib.socket.ClientSocket import ClientSocket
import json
import traceback
import binascii

from lib.util.jsonUtil import hasJsonDataIsNone

protocolReport_process = Blueprint('protocolReport_process', __name__)

##########################################
#   【接口类型】处理发送的自定义报文
##########################################
@protocolReport_process.route("/porcessUserdefinedMsg",methods=['POST'])
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
            conf_R.read("config/protocolTools/protocolTools.conf")
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
            data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的心跳上报报文
##########################################
@protocolReport_process.route("/porcessHeartBeatMsg",methods=['POST'])
def porcessHeartBeatMsg():
    WATER_CODE = request.form.get("WATER_CODE")
    DEV_ID = request.form.get("DEV_ID")

    data = {}
    if (WATER_CODE == None or DEV_ID == None ):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            heartBeatProtocolObj = HeartBeatReport_protocol(WATER_CODE = WATER_CODE,DEV_ID = DEV_ID)
            msg = heartBeatProtocolObj.generateHeartBeatMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】处理发送的终端登录上报报文
##########################################
@protocolReport_process.route("/porcessLoginMsg",methods=['POST'])
def porcessLoginBeatMsg():
    WATER_CODE = request.form.get("WATER_CODE")
    DEV_ID = request.form.get("DEV_ID")

    cpuId = request.form.get("cpuId")
    imsi = request.form.get("imsi")
    ccid = request.form.get("ccid")
    imei = request.form.get("imei")

    data = {}
    if (WATER_CODE == None or DEV_ID == None or cpuId == None or imsi == None or ccid == None or imei == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            loginProtocolObj = LoginReport_protocol(WATER_CODE = WATER_CODE,DEV_ID = DEV_ID,cpuId=cpuId,imsi=imsi,ccid=ccid,imei=imei)
            msg = loginProtocolObj.generateLoginMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = data["orgRev"] = json.loads(Login_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的GPS上报报文
##########################################
@protocolReport_process.route("/porcessGPSMsg",methods=['POST'])
def porcessGPSMsg():
    WATER_CODE = request.form.get("WATER_CODE")
    DEV_ID = request.form.get("DEV_ID")
    msgCount = request.form.get("msgCount")

    UTCTime = request.form.get("UTCTime")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    speed = request.form.get("speed")
    directionAngle = request.form.get("directionAngle")
    elevation = request.form.get("elevation")
    positionStar = request.form.get("positionStar")
    Pdop = request.form.get("Pdop")
    Hdop = request.form.get("Hdop")
    Vdop = request.form.get("Vdop")
    statusBit = request.form.get("statusBit")
    valtage = request.form.get("valtage")
    OBDSpeed = request.form.get("OBDSpeed")
    engineSpeed = request.form.get("engineSpeed")
    GPSTotalMileage = request.form.get("GPSTotalMileage")
    totalOil = request.form.get("totalOil")
    totalTime = request.form.get("totalTime")
    GPSTimestamp = request.form.get("GPSTimestamp")

    data = {}
    if (WATER_CODE == None or DEV_ID == None or msgCount == None or UTCTime == None or latitude == None or longitude == None or speed == None or directionAngle == None or elevation == None or positionStar == None or Pdop == None or Hdop == None or Vdop == None or statusBit == None or valtage == None or OBDSpeed == None or engineSpeed == None or GPSTotalMileage == None or totalTime == None or GPSTimestamp == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            # d读取config文件
            conf_R = ConfigParser()
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            GPSProtocolObj = GPSReport_protocol(msgCount = msgCount,WATER_CODE = WATER_CODE,DEV_ID = DEV_ID,UTCTime= UTCTime,latitude=latitude,longitude=longitude,speed=speed,directionAngle=directionAngle,elevation=elevation,positionStar=positionStar,Pdop=Pdop,Hdop=Hdop,Vdop=Vdop,statusBit=statusBit,valtage=valtage,OBDSpeed=OBDSpeed,engineSpeed=engineSpeed,GPSTotalMileage=GPSTotalMileage,totalOil=totalOil,totalTime=totalTime,GPSTimestamp=GPSTimestamp)
            msg = GPSProtocolObj.generateGpsMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】处理发送的OBD_CAN上报报文
##########################################
@protocolReport_process.route("/porcessOBD_CAN_Msg",methods=['POST'])
def porcessOBD_CAN_Msg():
    WATER_CODE = request.form.get("WATER_CODE")
    DEV_ID = request.form.get("DEV_ID")
    msgCount = request.form.get("msgCount")

    infoTime = request.form.get("infoTime")
    dataFlowCode = request.form.get("dataFlowCode")
    protocolType = request.form.get("protocolType")
    fireStatus = request.form.get("fireStatus")
    ACCStatus = request.form.get("ACCStatus")
    voltage = request.form.get("voltage")
    troubleLightStatus = request.form.get("troubleLightStatus")
    toubleCodeCount = request.form.get("toubleCodeCount")
    engineSpeed = request.form.get("engineSpeed")
    speed = request.form.get("speed")
    meterMileage = request.form.get("meterMileage")
    mileageStatisticsStyle = request.form.get("mileageStatisticsStyle")
    totalMileage = request.form.get("totalMileage")
    troubleMileage = request.form.get("troubleMileage")
    totalOilExpend = request.form.get("totalOilExpend")
    surplusOil = request.form.get("surplusOil")
    totalRunTime = request.form.get("totalRunTime")
    totalEngineTime = request.form.get("totalEngineTime")
    airIntoAisleTemperture = request.form.get("airIntoAisleTemperture")
    coolingLiquidTemperture = request.form.get("coolingLiquidTemperture")
    envTemperture = request.form.get("envTemperture")
    ariIntoPress = request.form.get("ariIntoPress")
    oilPressure = request.form.get("oilPressure")
    atmosphericPressure = request.form.get("atmosphericPressure")
    airFlow = request.form.get("airFlow")
    valveLocationSensor = request.form.get("valveLocationSensor")
    acceleratorLocation = request.form.get("acceleratorLocation")
    engineLoad = request.form.get("engineLoad")
    fuelTrim = request.form.get("fuelTrim")
    fireAngle = request.form.get("fireAngle")
    B1S1oxygenSensorVoltage = request.form.get("B1S1oxygenSensorVoltage")
    B1S2oxygenSensorVoltage = request.form.get("B1S2oxygenSensorVoltage")
    B1S1oxygenSensorElectricity = request.form.get("B1S1oxygenSensorElectricity")
    B1S2oxygenSensorElectricity = request.form.get("B1S2oxygenSensorElectricity")
    momentOilExpend = request.form.get("momentOilExpend")
    meterOilExpend = request.form.get("meterOilExpend")
    engineAbsoluteLoad = request.form.get("engineAbsoluteLoad")
    steeringWheelAngle = request.form.get("steeringWheelAngle")
    torquePercentage = request.form.get("torquePercentage")
    gearsLocation = request.form.get("gearsLocation")
    GPSSpeed = request.form.get("GPSSpeed")
    GPSMileage = request.form.get("GPSMileage")

    data = {}
    if (msgCount == None or WATER_CODE == None or DEV_ID == None or infoTime == None or dataFlowCode == None or protocolType == None or fireStatus == None or ACCStatus == None or voltage == None or troubleLightStatus == None or toubleCodeCount == None or engineSpeed == None or speed == None or meterMileage == None or mileageStatisticsStyle == None or totalMileage == None or troubleMileage == None or totalOilExpend == None or surplusOil == None or totalRunTime == None or totalEngineTime == None or airIntoAisleTemperture == None or coolingLiquidTemperture == None or envTemperture == None or ariIntoPress == None or oilPressure == None or atmosphericPressure == None or airFlow == None or valveLocationSensor == None or acceleratorLocation == None or engineLoad == None or fuelTrim == None or fireAngle == None or B1S1oxygenSensorVoltage == None or B1S2oxygenSensorVoltage == None or B1S1oxygenSensorElectricity == None or B1S2oxygenSensorElectricity == None or momentOilExpend == None or meterOilExpend == None or engineAbsoluteLoad == None or steeringWheelAngle == None or torquePercentage == None or gearsLocation == None or GPSSpeed == None or GPSMileage == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            # cliSocket = ClientSocket("183.230.194.65", 8712)
            # d读取config文件
            conf_R = ConfigParser()
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            OBD_CAN_protocolObj = OBDReport_CAN_protocol(msgCount = msgCount,WATER_CODE = WATER_CODE,DEV_ID = DEV_ID,infoTime=infoTime,dataFlowCode=dataFlowCode,protocolType=protocolType,fireStatus=fireStatus,ACCStatus=ACCStatus,voltage=voltage,troubleLightStatus=troubleLightStatus,toubleCodeCount=toubleCodeCount,engineSpeed=engineSpeed,speed=speed,meterMileage=meterMileage,mileageStatisticsStyle=mileageStatisticsStyle,totalMileage=totalMileage,troubleMileage=troubleMileage,totalOilExpend=totalOilExpend,surplusOil=surplusOil,totalRunTime=totalRunTime,totalEngineTime=totalEngineTime,airIntoAisleTemperture=airIntoAisleTemperture,coolingLiquidTemperture=coolingLiquidTemperture,envTemperture=envTemperture,ariIntoPress=ariIntoPress,oilPressure=oilPressure,atmosphericPressure=atmosphericPressure,airFlow=airFlow,valveLocationSensor=valveLocationSensor,acceleratorLocation=acceleratorLocation,engineLoad=engineLoad,fuelTrim=fuelTrim,fireAngle=fireAngle,B1S1oxygenSensorVoltage=B1S1oxygenSensorVoltage,B1S2oxygenSensorVoltage=B1S2oxygenSensorVoltage,B1S1oxygenSensorElectricity=B1S1oxygenSensorElectricity,B1S2oxygenSensorElectricity=B1S2oxygenSensorElectricity,momentOilExpend=momentOilExpend,meterOilExpend=meterOilExpend,engineAbsoluteLoad=engineAbsoluteLoad,steeringWheelAngle=steeringWheelAngle,torquePercentage=torquePercentage,gearsLocation=gearsLocation,GPSSpeed=GPSSpeed,GPSMileage=GPSMileage)
            msg = OBD_CAN_protocolObj.generateOBDReportCANMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】处理发送的终端安全状态上报报文
##########################################
@protocolReport_process.route("/porcessSecurityStatusMsg",methods=['POST'])
def porcessSecurityStatusMsg():
    WATER_CODE = request.form.get("WATER_CODE")
    DEV_ID = request.form.get("DEV_ID")
    msgCount = request.form.get("msgCount")

    statusCode = request.form.get("statusCode")
    locationType = request.form.get("locationType")
    securityStatus = request.form.get("securityStatus")
    doorStatus = request.form.get("doorStatus")
    lockStatus = request.form.get("lockStatus")
    windowStatus = request.form.get("windowStatus")
    lightStatus = request.form.get("lightStatus")
    onoffStatusA = request.form.get("onoffStatusA")
    onoffStatusB = request.form.get("onoffStatusB")
    dataByte = request.form.get("dataByte")

    data = {}
    if (WATER_CODE == None or DEV_ID == None or msgCount == None or statusCode == None or locationType == None or securityStatus == None or doorStatus == None or lockStatus == None or windowStatus == None or lightStatus == None or onoffStatusA == None or onoffStatusB == None or dataByte == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            securityStatusProtocolObj = SecurityStatusReport_protocol(WATER_CODE = WATER_CODE,DEV_ID = DEV_ID,msgCount=msgCount,statusCode=statusCode,locationType=locationType,securityStatus=securityStatus,doorStatus=doorStatus,lockStatus=lockStatus,windowStatus=windowStatus,lightStatus=lightStatus,onoffStatusA=onoffStatusA,onoffStatusB=onoffStatusB,dataByte=dataByte)
            msg = securityStatusProtocolObj.generateSecurityStatusMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】处理发送的电瓶采样上报报文
##########################################
@protocolReport_process.route("/porcessVoltageDataMsg",methods=['POST'])
def porcessVoltageDataMsg():
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
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = VoltageDataReport_protocol(WATER_CODE=params["WATER_CODE"],DEV_ID=params["DEV_ID"], \
                                        sampleNums=params["sampleNums"],sampleData=params["sampleData"])
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
            data["orgRev"] = data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的事件报文
##########################################
@protocolReport_process.route("/porcessEventMsg",methods=['POST'])
def porcessEventMsg():
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
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = EventReport_protocol(data=params)
            msg = protocolObj.generateEventMsg()
            cliSocket.send(msg)
            socRecv = cliSocket.receive()
            socRecvo = str(socRecv)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["msgSend"] = msg
            data["result"] = socRecvo
            data["rev"] = str(binascii.b2a_hex(socRecv))[2:][:-1]
            data["orgRev"] = data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的故障码报文
##########################################
@protocolReport_process.route("/porcessTroubleCodeMsg",methods=['POST'])
def porcessTroubleCodeMsg():
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
            conf_R.read("config/protocolTools/protocolTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            protocolObj = TroubleCode_protocol(WATER_CODE=params["WATER_CODE"],DEV_ID=params["DEV_ID"], \
                                        UTCTime=params["curTime"],troubleCodeNum=params["troubleCodeNum"],troubleCode=params["troubleCode"], \
                                        MILStatus=params["MILStatus"])
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
            data["orgRev"] = data["orgRev"] = json.loads(Common_res(data["rev"]).getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')







