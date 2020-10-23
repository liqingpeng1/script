#coding:utf-8

from flask import Blueprint ,Response,request
from configparser import ConfigParser

from lib.protocol.message.DataUpstreamTransport_msg import DataUpstreamTransport_msg
from lib.protocol.message.Location_msg import Location_msg
from lib.protocol.message.TerminalHeartbeat_msg import TerminalHeartbeat_msg
from lib.protocol.message.TerminalRegister_msg import TerminalRegister_msg
from lib.protocol.message.TerminalVersionInfo_msg import TerminalVersionInfo_msg
from lib.protocol.messagePlateform.PlateformVersionInfo_res import PlatefromVersionInfo_res
from lib.protocol.messagePlateform.PlatformCommon_res import PlatformCommon_res
from lib.protocol.report.HeartBeatReport_protocol import HeartBeatReport_protocol

from lib.socket.ClientSocket import ClientSocket
import json
import traceback
import binascii

from lib.util.jsonUtil import hasJsonDataIsNone

message_process = Blueprint('message_process', __name__)

##########################################
#   【接口类型】处理发送的自定义报文
##########################################
@message_process.route("/porcessUserdefinedMsg",methods=['POST'])
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
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            cliSocket.send(msg)
            cliSocket.setTimeOut(timeout)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的心跳消息
##########################################
@message_process.route("/porcessHeartBeatMsg",methods=['POST'])
def porcessHeartBeatMsg():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))


    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None or pkgCounts == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            heartBeatmsgObj = TerminalHeartbeat_msg()
            msg = heartBeatmsgObj.generateMsg_GUI(msgID,phoneNum,msgWaterCode,encryptionType,subPkg)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的终端注册消息
##########################################
@message_process.route("/porcessTerminalRegisterMsg",methods=['POST'])
def porcessTerminalRegisterMsg():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))

    provinceId = int(request.form.get("provinceId"))
    countyId = int(request.form.get("countyId"))
    manufacturerId = request.form.get("manufacturerId")
    terminalType = request.form.get("terminalType")
    terminalId = request.form.get("terminalId")
    licencePlateColor = int(request.form.get("licencePlateColor"))
    carSign = request.form.get("carSign")

    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None \
        or pkgCounts == None or provinceId == None or countyId == None or manufacturerId == None or terminalType == None \
        or terminalId == None or licencePlateColor == None or carSign == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            terminalRegisterObj = TerminalRegister_msg()
            msg = terminalRegisterObj.generateMsg_GUI(msgID,phoneNum,msgWaterCode,encryptionType,subPkg,provinceId,\
            countyId,manufacturerId,terminalType,terminalId,licencePlateColor,carSign)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的终端版本主动上报消息
##########################################
@message_process.route("/porcessTerminalVersionInfoUploadMsg",methods=['POST'])
def porcessTerminalVersionInfoUploadMsg():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))

    softwareVersion = request.form.get("softwareVersion")
    softwareVersionDate = request.form.get("softwareVersionDate")
    CPUId = request.form.get("CPUId")
    GMSType = request.form.get("GMSType")
    GMS_IMEI = request.form.get("GMS_IMEI")
    SIM_IMSI = request.form.get("SIM_IMSI")
    SIM_ICCID = request.form.get("SIM_ICCID")
    carType = int(request.form.get("carType"))
    VIN = request.form.get("VIN")
    totalMileage = int(request.form.get("totalMileage"))
    totalOilExpend = int(request.form.get("totalOilExpend"))
    displacement = int(request.form.get("displacement"))
    oilDensity = int(request.form.get("oilDensity"))
    OBDSerial = int(request.form.get("OBDSerial"))
    oilCalculateType = request.form.get("oilCalculateType")

    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None \
        or pkgCounts == None or softwareVersion == None or softwareVersionDate == None or CPUId == None or \
            GMSType == None or GMS_IMEI == None or SIM_IMSI == None or SIM_ICCID == None or carType == None \
            or VIN == None or totalMileage == None or totalOilExpend == None or displacement == None \
            or oilDensity == None or OBDSerial == None or oilCalculateType == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            terminalVersionInfoObj = TerminalVersionInfo_msg()
            msg = terminalVersionInfoObj.generateMsg_GUI(msgID,phoneNum,msgWaterCode,encryptionType,subPkg,softwareVersion,\
                                                      softwareVersionDate,CPUId,GMSType,GMS_IMEI,SIM_IMSI,SIM_ICCID,carType,VIN,\
                                                      totalMileage,totalOilExpend,displacement,oilDensity,OBDSerial,oilCalculateType)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatefromVersionInfo_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的终端版本主动上报消息(驾驶行程数据)
##########################################
@message_process.route("/porcessDataUpstreamTransportMsg",methods=['POST'])
def porcessDataUpstreamTransportMsg():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))

    msgType = request.form.get("msgType")
    time_1 = request.form.get("time_1")
    time_2 = request.form.get("time_2")
    fireLatitude = float(request.form.get("fireLatitude"))
    fireLongitude = float(request.form.get("fireLongitude"))
    unFireLatitude = float(request.form.get("unFireLatitude"))
    unFireLongitude = float(request.form.get("unFireLongitude"))
    drivingCircleLabel = int(request.form.get("drivingCircleLabel"))
    drivingCircleTotalMileageType = request.form.get("drivingCircleTotalMileageType")
    drivingCircleTotalMileage = int(request.form.get("drivingCircleTotalMileage"))
    drivingCircleTotalOil = int(request.form.get("drivingCircleTotalOil"))
    drivingCircleTotalTime = int(request.form.get("drivingCircleTotalTime"))
    drivingCircleOverSpeedTotalTime = int(request.form.get("drivingCircleOverSpeedTotalTime"))
    drivingCircleOverSpeedTotalTimes = int(request.form.get("drivingCircleOverSpeedTotalTimes"))
    drivingCircleAverageSpeed = int(request.form.get("drivingCircleAverageSpeed"))
    drivingCircleMaxSpeed = int(request.form.get("drivingCircleMaxSpeed"))
    drivingCircleIdlingTime = int(request.form.get("drivingCircleIdlingTime"))
    drivingCircleFootBrakeIsSupport = int(request.form.get("drivingCircleFootBrakeIsSupport"))
    drivingCircleFootBrakeTatalTimes = int(request.form.get("drivingCircleFootBrakeTatalTimes"))
    drivingCircleRapidlyAccelerateTimes = int(request.form.get("drivingCircleRapidlyAccelerateTimes"))
    drivingCircleSharpSlowdownTimes = int(request.form.get("drivingCircleSharpSlowdownTimes"))
    drivingCircleSharpCurveTimes = int(request.form.get("drivingCircleSharpCurveTimes"))
    speedIn20 = int(request.form.get("speedIn20"))
    speedIn20_40 = int(request.form.get("speedIn20_40"))
    speedIn40_60 = int(request.form.get("speedIn40_60"))
    speedIn60_80 = int(request.form.get("speedIn60_80"))
    speedIn80_100 = int(request.form.get("speedIn80_100"))
    speedIn100_120 = int(request.form.get("speedIn100_120"))
    speedOut120 = int(request.form.get("speedOut120"))
    rapidlyAccelerateTimes = int(request.form.get("rapidlyAccelerateTimes"))
    rapidlySharpSlowdownTimes = int(request.form.get("rapidlySharpSlowdownTimes"))
    sharpCurveTimes = int(request.form.get("sharpCurveTimes"))

    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None \
        or pkgCounts == None or time_1 == None or time_2 == None or fireLatitude == None or fireLongitude == None or \
                           unFireLatitude == None  or unFireLongitude == None or drivingCircleLabel == None or drivingCircleTotalMileageType == None or \
                           drivingCircleTotalMileage == None or drivingCircleTotalOil == None or drivingCircleTotalTime == None or \
                           drivingCircleOverSpeedTotalTime == None or drivingCircleOverSpeedTotalTimes == None or drivingCircleAverageSpeed == None or \
                           drivingCircleMaxSpeed == None or drivingCircleIdlingTime == None or drivingCircleFootBrakeIsSupport == None or \
                           drivingCircleFootBrakeTatalTimes == None or drivingCircleRapidlyAccelerateTimes == None or drivingCircleSharpSlowdownTimes == None or \
                           drivingCircleSharpCurveTimes == None or speedIn20 == None or speedIn20_40 == None or speedIn40_60 == None or speedIn60_80 == None or \
                           speedIn80_100 == None  or speedIn100_120 == None or speedOut120 == None or rapidlyAccelerateTimes == None or \
                           rapidlySharpSlowdownTimes == None or sharpCurveTimes == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            msgData = {}
            msgData["time_1"] = time_1
            msgData["time_2"] = time_2
            msgData["fireLatitude"] = fireLatitude
            msgData["fireLongitude"] = fireLongitude
            msgData["unFireLatitude"] = unFireLatitude
            msgData["unFireLongitude"] = unFireLongitude
            msgData["drivingCircleLabel"] = drivingCircleLabel
            msgData["drivingCircleTotalMileageType"] = drivingCircleTotalMileageType
            msgData["drivingCircleTotalMileage"] = drivingCircleTotalMileage
            msgData["drivingCircleTotalOil"] = drivingCircleTotalOil
            msgData["drivingCircleTotalTime"] = drivingCircleTotalTime
            msgData["drivingCircleOverSpeedTotalTime"] = drivingCircleOverSpeedTotalTime
            msgData["drivingCircleOverSpeedTotalTimes"] = drivingCircleOverSpeedTotalTimes
            msgData["drivingCircleAverageSpeed"] = drivingCircleAverageSpeed
            msgData["drivingCircleMaxSpeed"] = drivingCircleMaxSpeed
            msgData["drivingCircleIdlingTime"] = drivingCircleIdlingTime
            msgData["drivingCircleFootBrakeIsSupport"] = drivingCircleFootBrakeIsSupport
            msgData["drivingCircleFootBrakeTatalTimes"] = drivingCircleFootBrakeTatalTimes
            msgData["drivingCircleRapidlyAccelerateTimes"] = drivingCircleRapidlyAccelerateTimes
            msgData["drivingCircleSharpSlowdownTimes"] = drivingCircleSharpSlowdownTimes
            msgData["drivingCircleSharpCurveTimes"] = drivingCircleSharpCurveTimes
            msgData["speedIn20"] = speedIn20
            msgData["speedIn20_40"] = speedIn20_40
            msgData["speedIn40_60"] = speedIn40_60
            msgData["speedIn60_80"] = speedIn60_80
            msgData["speedIn80_100"] = speedIn80_100
            msgData["speedIn100_120"] = speedIn100_120
            msgData["speedOut120"] = speedOut120
            msgData["rapidlyAccelerateTimes"] = rapidlyAccelerateTimes
            msgData["rapidlySharpSlowdownTimes"] = rapidlySharpSlowdownTimes
            msgData["sharpCurveTimes"] = sharpCurveTimes

            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            DataUpstreamTransportObj = DataUpstreamTransport_msg()
            msg = DataUpstreamTransportObj.generateMsg_GUI(msgID,phoneNum,msgWaterCode,encryptionType,subPkg,msgType,msgData)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的终端版本主动上报消息(故障码数据)
##########################################
@message_process.route("/porcessDataUpstreamTransportMsg_F2",methods=['POST'])
def porcessDataUpstreamTransportMsg_F2():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))

    msgType = request.form.get("msgType")
    infoTime = request.form.get("infoTime")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    troubleCodeNums = int(request.form.get("troubleCodeNums"))
    systemId = request.form.get("systemId")

    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None \
        or pkgCounts == None or infoTime == None or latitude == None or longitude == None or troubleCodeNums == None \
        or systemId == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            msgData = {}
            msgData["infoTime"] = infoTime
            msgData["latitude"] = latitude
            msgData["longitude"] = longitude
            msgData["troubleCodeNums"] = troubleCodeNums
            msgData["systemId"] = systemId

            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            DataUpstreamTransportObj = DataUpstreamTransport_msg()
            msg = DataUpstreamTransportObj.generateMsg_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,
                                                           msgType, msgData)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的终端版本主动上报消息(休眠进入)
##########################################
@message_process.route("/porcessDataUpstreamTransportMsg_F3",methods=['POST'])
def porcessDataUpstreamTransportMsg_F3():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))

    msgType = request.form.get("msgType")
    infoTime = request.form.get("infoTime")

    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None \
        or pkgCounts == None or infoTime == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            msgData = {}
            msgData["infoTime"] = infoTime

            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            DataUpstreamTransportObj = DataUpstreamTransport_msg()
            msg = DataUpstreamTransportObj.generateMsg_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,
                                                           msgType, msgData)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】处理发送的终端版本主动上报消息(休眠唤醒)
##########################################
@message_process.route("/porcessDataUpstreamTransportMsg_F4",methods=['POST'])
def porcessDataUpstreamTransportMsg_F4():
    msgID = request.form.get("msgID")
    phoneNum = int(request.form.get("phoneNum"))
    msgWaterCode = int(request.form.get("msgWaterCode"))
    encryptionType = int(request.form.get("encryptionType"))
    subPkg = int(request.form.get("subPkg"))
    pkgCounts = int(request.form.get("pkgCounts"))

    msgType = request.form.get("msgType")
    infoTime = request.form.get("infoTime")
    outSleepType = request.form.get("outSleepType")
    carVoltage = int(request.form.get("carVoltage"))
    vibrateOutSleepSpeedUpVal = int(request.form.get("vibrateOutSleepSpeedUpVal"))

    data = {}
    if (msgID == None or phoneNum == None or msgWaterCode == None or encryptionType == None or subPkg == None \
        or pkgCounts == None or infoTime == None):
        data["status"] = "4003"
        data["message"] = "Info: 请检查是否传入了空数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            msgData = {}
            msgData["infoTime"] = infoTime
            msgData["outSleepType"] = outSleepType
            msgData["carVoltage"] = carVoltage
            msgData["vibrateOutSleepSpeedUpVal"] = vibrateOutSleepSpeedUpVal

            conf_R = ConfigParser()
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            DataUpstreamTransportObj = DataUpstreamTransport_msg()
            msg = DataUpstreamTransportObj.generateMsg_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,
                                                           msgType, msgData)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】地理位置上报消息
##########################################
@message_process.route("/porcessLocationMsg",methods=['POST'])
def porcessLocationMsg():
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
            conf_R.read("config/messageTools/messageTools.conf")
            cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
            cliSocket.connect()
            obj = Location_msg()
            msg = obj.generateMsg_GUI(params)
            cliSocket.send(msg)
            socRecv_1 = cliSocket.receive()
            socRecv_2 = str(socRecv_1)
            cliSocket.close()
            data["status"] = "200"
            data["message"] = "Sucess: "
            data["original"] = msg
            data["result"] = socRecv_2
            msgP = PlatformCommon_res(socRecv_1)
            data["resultH"] = msgP.getOriginalMsg()
            data["parse"] = json.loads(msgP.getMsg())
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')