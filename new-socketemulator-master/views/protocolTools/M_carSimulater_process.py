#coding:utf-8
import binascii
import os
import time
from time import sleep

from flask import Blueprint ,Response,request,send_from_directory
from configparser import ConfigParser

from lib.protocol.report.EventReport_protocol import EventReport_protocol
from lib.protocol.report.LoginReport_protocol import LoginReport_protocol
from lib.protocol.report.TroubleCodeReport_protocol import TroubleCode_protocol
from lib.protocol.report.VersionReport_protocol import VersionReport_protocol
from lib.socket.ClientSocket import ClientSocket
import json
import traceback
from lib.socket.service.ProtocolSimulaterService import ProtocolSimulaterService
from lib.util import fileUtil
from lib.util.DelaySend import DelaySend
from lib.util.fileUtil import delFile
from lib.util.util import strAddSpace

M_carSimulater_process = Blueprint('M_carSimulater_process', __name__)

connects = {}                                  #用来保存连接的信息s
websocket = None                               #保存创建的websocket

##########################################
#   【接口类型】设置socket信息
##########################################
@M_carSimulater_process.route("/porcessSocketSetting",methods=['POST'])
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
            conf_R.read("config/protocolTools/carSimulater.conf")
            conf_W = conf_R
            conf_W["socket"]["host"] = host
            conf_W["socket"]["port"] = port
            with open("config/protocolTools/carSimulater.conf", "w") as fi:
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
#   【接口类型】创建一个连接
##########################################
@M_carSimulater_process.route("/createConect",methods=['POST'])
def createConect():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    timeout = int(params["timeout"])
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        conf_R = ConfigParser()
        conf_R.read("config/protocolTools/carSimulater.conf")
        if not sessionId in connects.keys():
            cliSocket = ClientSocket(conf_R.get("socket", "host"), conf_R.getint("socket", "port"))
            cliSocket.setTimeOut(timeout)
            cliSocket.connect()
            connect = {}
            connects[sessionId] = connect
            socketName = "socket_" + str(len(connects) + 1)
            connect["name"] = socketName
            service = ProtocolSimulaterService()
            service.setSocket(cliSocket)
            service.setTimeout(timeout)
            service.setData(params)
            gpsLine = params["gpsLine"]
            carId = params["carId"]
            service.setCarId(carId)
            service.setGpsLine(gpsLine)
            global websocket
            if websocket == None:
                service.startWebsocketService()          #如果没有创建websocket服务，则启动新的websocket服务
                websocket = service.getWebsocket()
            else:
                service.setWebsocket(websocket)          #给新服务设置websocket服务对象
                service.addNewWebsocket()                #创建一个新的websocket连接
            connect["service"] = connect
            connects[sessionId]["service"] = service
            timeArray = time.localtime(int(time.time()))
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            connects[sessionId]["time"] = curTime
            connects[sessionId]["carId"] = params["carId"]
            ip = request.remote_addr
            connects[sessionId]["ip"] = ip
            data["status"] = "200"
            data["message"] = "创建连接成功！"
        else:
            data["status"] = "4003"
            data["message"] = "已经创建了连接！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 连接失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】登录
##########################################
@M_carSimulater_process.route("/login",methods=['POST'])
def login():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    params["login"]["cpuId"] = strAddSpace(params["login"]["cpuId"],24)
    params["login"]["imsi"] = strAddSpace(params["login"]["imsi"], 15)
    params["login"]["ccid"] = strAddSpace(params["login"]["ccid"], 20)
    params["login"]["imei"] = strAddSpace(params["login"]["imei"], 15)

    params["version"]["verInfo"] = strAddSpace(params["version"]["verInfo"], 16)
    params["version"]["compileDate"] = strAddSpace(params["version"]["compileDate"], 10)
    params["version"]["GSM"] = strAddSpace(params["version"]["GSM"], 10)
    try:
        service = connects[sessionId]["service"]
        service.setCarId(params["carId"])
        loginObj = LoginReport_protocol(params["WATER_CODE"],params["carId"],params["login"]["cpuId"], \
                                        params["login"]["imsi"],params["login"]["ccid"],params["login"]["imei"])
        loginMsg = loginObj.generateLoginMsg()
        service.serviceSendMsg(loginMsg,"登录")
        service.setSn(service.getSn() +1)
        sleep(0.2)
        versionObj = VersionReport_protocol(1,params["WATER_CODE"],params["carId"],params["version"]["verInfo"], \
                                             params["version"]["compileDate"],params["version"]["GSM"])
        versionMsg = versionObj.generateVersionMsg()
        service.serviceSendMsg(versionMsg,"版本")
        service.setSn(service.getSn() + 1)

        # 数据补报
        if(os.path.exists("data/protocolTools/sendMsg/" + params["carId"])):
            ds = DelaySend(params["carId"], service)
            ds.sendDelayMsgs()
        else:
            pass

        data["status"] = "200"
        data["message"] = "登录成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 登录失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】点火
##########################################
@M_carSimulater_process.route("/fire",methods=['POST'])
def fire():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    durTime = int(params["durTime"])
    gpsLine = params["gpsLine"]
    carId = params["carId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        service.setCarId(carId)
        service.setGpsLine(gpsLine)
        service.fireOn()
        data["status"] = "200"
        data["message"] = "点火成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 点火失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】行驶
##########################################
@M_carSimulater_process.route("/startTravel",methods=['POST'])
def startTravel():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    durTime = int(params["durTime"])
    gpsLine = params["gpsLine"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        service.setSendDur(durTime)                #设置车机多久循环发送一次消息
        service.setGpsLine(gpsLine)
        service.startService()
        service.startTravel()
        data["status"] = "200"
        data["message"] = "行驶成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 行驶失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】停止行驶
##########################################
@M_carSimulater_process.route("/stopTravel",methods=['POST'])
def stopTravel():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        service.stopTravel()
        data["status"] = "200"
        data["message"] = "停止行驶成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 停止行驶失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】熄火
##########################################
@M_carSimulater_process.route("/unFire",methods=['POST'])
def unFire():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    gpsLine = params["gpsLine"]
    carId = params["carId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        service.setGpsLine(gpsLine)
        service.setCarId(carId)
        service.fireOff()
        service.stopTravel()
        data["status"] = "200"
        data["message"] = "熄火成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 熄火失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】关闭一个连接
##########################################
@M_carSimulater_process.route("/closeConect",methods=['POST'])
def closeConect():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        if len(connects) < 1:
            data["status"] = "4003"
            data["message"] = "没有可关闭的连接！"
        else:
            service = connects[sessionId]["service"]
            service.stopTravel()
            service.stopService()
            service.closeSocket()
            connects.pop(sessionId)
            data["status"] = "200"
            data["message"] = "关闭连接成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 关闭连接失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】复位
##########################################
@M_carSimulater_process.route("/reset",methods=['POST'])
def reset():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    data = {}
    global  connects
    global websocket
    try:
        for key in connects:
            service = connects[key]["service"]
            service.stopTravel()
            try:
                service.fireOff()
            except BaseException as e1:
                pass
            service.stopService()
            service.closeSocket()
        websocket.close()
        websocket = None
        connects = {}
        data["status"] = "200"
        data["message"] = "复位成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 复位失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】文件上传操作
##########################################
@M_carSimulater_process.route("/fileUplad",methods=['POST'])
def fileUplad():
    # 获取前端传输的文件(对象)
    f = request.files.get('file')
    file_content = f.read()
    try:
        file_content = file_content.decode("utf-8").replace("\n","")
    except BaseException as e:
        pass
    try:
        file_content = file_content.decode("gbk").replace("\n","")
    except BaseException as e:
        pass
    maxPrefix = int(fileUtil.getMaxPrefixFilePre("data/protocolTools/GPSLines"))
    filenameOrg = f.filename
    filename = str(maxPrefix + 1) + "_" + filenameOrg
    fileData = {}
    fileData["filename"] = fileUtil.removeSuffix(filenameOrg)
    fileData["filenameOri"] = filename
    # 验证文件格式（简单设定几个格式）
    types = ['json','txt']
    data = {}
    if filename.split('.')[-1] in types:
        # 保存图片
        with open("data/protocolTools/GPSLines/" + filename,"w",encoding="utf-8") as fi:
            fi.write(file_content)
        # 返回给前端结果
        data["status"] = "200"
        data["message"] = "文件上传成功"
        data["file"] = fileData
    else:
        data["status"] = "4003"
        data["message"] = "文件上传失败"
    return Response(json.dumps(data), mimetype='application/json')


@M_carSimulater_process.route("/sampleDowload")
def sampleDowload():
    return send_from_directory(r"data/protocolTools/GPSLines",filename="1_sample.json",as_attachment=True)


@M_carSimulater_process.route("/delGpsLine",methods=['POST'])
def delGpsLine():
    fileName = request.form.get("fileName")
    data = {}
    if fileName == "1_sample.json":
        data["status"] = "4003"
        data["message"] = "Error：示例轨迹不可删除！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            delFile("data/protocolTools/GPSLines/",fileName)
            data["status"] = "200"
            data["message"] = "删除轨迹成功"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 删除轨迹失败！"
        return Response(json.dumps(data), mimetype='application/json')



##########################################
#   【接口类型】查询车机行驶数据
##########################################
@M_carSimulater_process.route("/searchCarsimulaterData",methods=['POST'])
def searchCarsimulaterData():
    carId = request.form.get("carId")
    data = {}
    carFile = "data/protocolTools/carData/" + carId + ".json"
    if not os.path.exists(carFile):
        data["status"] = "200"
        data["message"] = "该车机无行驶数据！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            with open(carFile, "r", encoding="utf-8") as fi:
                content = fi.read()
                conJson = json.loads(content)
            data["status"] = "200"
            # data["carData"] = {}
            # data["carData"]["date"] = conJson["time"]["date"]
            # data["carData"]["todayTotalMilleage"] = conJson["curDayTravel"]["todayTotalMilleage"]
            # data["carData"]["todayTotalOil"] = conJson["curDayTravel"]["todayTotalOil"]
            # data["carData"]["todayTotalTime"] = conJson["curDayTravel"]["todayTotalTime"]
            data["message"] = "日期：" + conJson["time"]["date"] + "\n今日行驶总里程：" + str(conJson["curDayTravel"]["todayTotalMilleage"]) + "（米）" \
            + "\n今日行驶总油耗：" + str(conJson["curDayTravel"]["todayTotalOil"]) + "（ml）" + "\n今日行驶总时间：" + str(conJson["curDayTravel"]["todayTotalTime"]) + "（秒）" \
            + "\n------------------\n本次行驶里程：" + str(conJson["curDayTravel"]["theMilleage"]) + "（米）" \
            + "\n本次行驶油耗：" + str(conJson["curDayTravel"]["theOil"]) + "（ml）" + "\n本次行驶总时间：" + str(conJson["curDayTravel"]["theTime"]) + "（秒）"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 查询车机数据失败失败！"
        return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】查询当前车辆GPS点
##########################################
@M_carSimulater_process.route("/searchCurCarGPS",methods=['POST'])
def searchCurCarGPS():
    carId = request.form.get("carId")
    sessionId = request.form.get("sessionId")
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可查询当前车辆GPS点！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        gpsLine = service.getGpsLine()
        gpsIndex = service.getGpsLineIndex()
        latitude = gpsLine[gpsIndex]["lat"]
        longitude = gpsLine[gpsIndex]["lng"]
        gpsLen = len(gpsLine)
        data["status"] = "200"
        data["message"] = "GPS总长度：" + str(gpsLen) + "\n" + "当前GPS位置：" + str(gpsIndex) + "\n" + "当前经度：" \
        + str(longitude) + "  当前维度：" + str(latitude)
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 查询车机数据失败失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】查询当前连接数，和连接对象
##########################################
@M_carSimulater_process.route("/getConnects",methods=['POST'])
def getConnects():
    data = {}
    try:
        data["status"] = "200"
        data["userCounts"] = len(connects)
        data["result"] = str(connects)
        return Response(json.dumps(data), mimetype='application/json')
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 获取在线人数失败失败！"
    return Response(json.dumps(data), mimetype='application/json')

#---------------------------------------  发送事件逻辑  ---------------------------------------
##########################################
#   【接口类型】发送终端插入报警事件
##########################################
@M_carSimulater_process.route("/sendInsertAlarmEvent",methods=['POST'])
def sendInsertAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}

    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送终端插入报警事件！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                 "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                             "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                             "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                             "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                             "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                 "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                  "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249},
                 "event": {"0001": {}}}
        jdata["DEV_ID"] = params["carId"]
        lng = service.getLongitude()
        lat = service.getLatitude()
        jdata["gpsInfo"]["latitude"] = lat
        jdata["gpsInfo"]["longitude"] = lng
        timeStamp = time.time() - 8 * 3600
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["gpsInfo"]["UTCTime"] = curTime
        obj = EventReport_protocol(data=jdata)
        gpsData = service.genGPSData2()
        obj.setGPSPkg(gpsData)
        obj.setEventType("0001")
        msg = obj.generateEventMsg()
        service.serviceSendMsg(msg, "发送终端插入报警事件")
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送终端插入报警事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送终端插入报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送终端拔出报警事件
##########################################
@M_carSimulater_process.route("/sendPulloutAlarmEvent",methods=['POST'])
def sendPulloutAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}

    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送终端拔出报警事件！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                 "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                             "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                             "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                             "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                             "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                 "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                  "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249},
                 "event": {"0002": {}}}
        jdata["DEV_ID"] = params["carId"]
        lng = service.getLongitude()
        lat = service.getLatitude()
        jdata["gpsInfo"]["latitude"] = lat
        jdata["gpsInfo"]["longitude"] = lng
        timeStamp = time.time() - 8 * 3600
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["gpsInfo"]["UTCTime"] = curTime
        obj = EventReport_protocol(data=jdata)
        gpsData = service.genGPSData2()
        obj.setGPSPkg(gpsData)
        obj.setEventType("0002")
        msg = obj.generateEventMsg()
        service.serviceSendMsg(msg, "发送终端拔出报警事件")
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送终端拔出报警事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送终端拔出报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送汽车电瓶低电压事件
##########################################
@M_carSimulater_process.route("/sendLowVoltageEvent",methods=['POST'])
def sendLowVoltageEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}

    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送事件！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                 "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                             "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                             "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                             "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                             "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                 "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                  "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249},
                 "event": {"0003": {}}}
        jdata["DEV_ID"] = params["carId"]
        lng = service.getLongitude()
        lat = service.getLatitude()
        jdata["gpsInfo"]["latitude"] = lat
        jdata["gpsInfo"]["longitude"] = lng
        timeStamp = time.time() - 8 * 3600
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["gpsInfo"]["UTCTime"] = curTime
        obj = EventReport_protocol(data=jdata)
        gpsData = service.genGPSData2()
        obj.setGPSPkg(gpsData)
        obj.setEventType("0003")
        msg = obj.generateEventMsg()
        service.serviceSendMsg(msg, "电瓶低电压事件")
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送电瓶低电压事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送电瓶低电压事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送终端主电断电报警事件
##########################################
@M_carSimulater_process.route("/sendPowerOffEvent",methods=['POST'])
def sendPowerOffEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}

    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送事件！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                 "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                             "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                             "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                             "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                             "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                 "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                  "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249},
                 "event": {"0004": {}}}
        jdata["DEV_ID"] = params["carId"]
        lng = service.getLongitude()
        lat = service.getLatitude()
        jdata["gpsInfo"]["latitude"] = lat
        jdata["gpsInfo"]["longitude"] = lng
        timeStamp = time.time() - 8 * 3600
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["gpsInfo"]["UTCTime"] = curTime
        obj = EventReport_protocol(data=jdata)
        gpsData = service.genGPSData2()
        obj.setGPSPkg(gpsData)
        obj.setEventType("0004")
        msg = obj.generateEventMsg()
        service.serviceSendMsg(msg, "终端主电断电报警")
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送终端主电断电报警事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送终端主电断电报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急加速事件
##########################################
@M_carSimulater_process.route("/sendRapidlyAccelerateEvent",methods=['POST'])
def sendRapidlyAccelerateEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急加速事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急加速事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0020": {"allRapidlyAccelerateCount": "5", "allSharpSlowdownCount": "6", "allSharpTurn": "4",
                                 "dataProperty": "1"}}}
            carData = service.getCarData()
            carData["event"]["threeRapid"]["totalRapidlyAccelerate"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"] + 1
            service.setCarData(carData)
            jdata["event"]["0020"]["allRapidlyAccelerateCount"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
            jdata["event"]["0020"]["allSharpSlowdownCount"] = carData["event"]["threeRapid"]["totalSharpSlowdown"]
            jdata["event"]["0020"]["allSharpTurn"] = carData["event"]["threeRapid"]["totalSharpTurn"]
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0020")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "急加速事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急加速事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急加速事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急减速事件
##########################################
@M_carSimulater_process.route("/sendSharpSlowdownEvent",methods=['POST'])
def sendSharpSlowdownEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急减速事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急减速事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0021": {"allRapidlyAccelerateCount": "5", "allSharpSlowdownCount": "6", "allSharpTurn": "4",
                                 "dataProperty": "1"}}}
            carData = service.getCarData()
            carData["event"]["threeRapid"]["totalSharpSlowdown"] = carData["event"]["threeRapid"]["totalSharpSlowdown"] + 1
            service.setCarData(carData)
            jdata["event"]["0021"]["allRapidlyAccelerateCount"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
            jdata["event"]["0021"]["allSharpSlowdownCount"] = carData["event"]["threeRapid"]["totalSharpSlowdown"]
            jdata["event"]["0021"]["allSharpTurn"] = carData["event"]["threeRapid"]["totalSharpTurn"]
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0020")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "急减速事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急减速事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急减速事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急转弯事件
##########################################
@M_carSimulater_process.route("/sendSharpTurnEvent",methods=['POST'])
def sendSharpTurnEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急转弯事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急转弯事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0022": {"allRapidlyAccelerateCount": "5", "allSharpSlowdownCount": "6", "allSharpTurn": "4",
                                 "direction":"0","dataProperty": "1"}}}
            carData = service.getCarData()
            carData["event"]["threeRapid"]["totalSharpTurn"] = carData["event"]["threeRapid"]["totalSharpTurn"] + 1
            service.setCarData(carData)
            jdata["event"]["0022"]["allRapidlyAccelerateCount"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
            jdata["event"]["0022"]["allSharpSlowdownCount"] = carData["event"]["threeRapid"]["totalSharpSlowdown"]
            jdata["event"]["0022"]["allSharpTurn"] = carData["event"]["threeRapid"]["totalSharpTurn"]
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0020")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "急转弯事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急转弯事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急转弯事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送碰撞告警事件
##########################################
@M_carSimulater_process.route("/sendCollisionAlarmEvent",methods=['POST'])
def sendCollisionAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送碰撞告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送碰撞告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0023": {"totalCount": "5", "dataProperty": "1"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0023")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "碰撞告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送碰撞告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送碰撞告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送汽车设防事件
##########################################
@M_carSimulater_process.route("/sendSetUpDefencesEvent",methods=['POST'])
def sendSetUpDefencesEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送汽车设防事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送汽车设防事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0012": {}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0012")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "汽车设防事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送汽车设防事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送汽车设防事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送汽车撤防事件
##########################################
@M_carSimulater_process.route("/sendSetDownDefencesEvent",methods=['POST'])
def sendSetDownDefencesEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送汽车撤防事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送汽车撤防事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0013": {}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0013")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "汽车撤防事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送汽车撤防事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送汽车撤防事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送低档高速报警事件
##########################################
@M_carSimulater_process.route("/sendLowGearHighSpeedEvent",methods=['POST'])
def sendLowGearHighSpeedEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送低档高速报警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送低档高速报警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0036": {"alarmType": "1", "durationTime": "10"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0036")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "低档高速报警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送低档高速报警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送低档高速报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送高档低速报警报警事件
##########################################
@M_carSimulater_process.route("/sendHighGearLowSpeedEvent",methods=['POST'])
def sendHighGearLowSpeedEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送高档低速报警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送高档低速报警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0037": {"alarmType": "1", "durationTime": "10"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0037")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "高档低速报警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送高档低速报警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送高档低速报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送剩余油量异常告警报警事件
##########################################
@M_carSimulater_process.route("/sendSurplusOilAlarmEvent",methods=['POST'])
def sendSurplusOilAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送剩余油量异常告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送剩余油量异常告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "004A": {"surplusOilType": "0", "value": "30"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("004A")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "剩余油量异常告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送剩余油量异常告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送剩余油量异常告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送超速报警事件
##########################################
@M_carSimulater_process.route("/sendOverSpeedAlarmEvent",methods=['POST'])
def sendOverSpeedAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送超速告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送超速告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0027": {"alarmType": "1", "durationTime": "360"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0027")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "超速告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送超速告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送超速告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送疲劳驾驶报警事件
##########################################
@M_carSimulater_process.route("/sendTiredDrivingAlarmEvent",methods=['POST'])
def sendTiredDrivingAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送疲劳驾驶告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送疲劳驾驶告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0028": {"alarmType": "1", "durationTime": "1100"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0028")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "疲劳驾驶告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送疲劳驾驶告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送疲劳驾驶告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送怠速时间过长报警事件
##########################################
@M_carSimulater_process.route("/sendIdlingOverTimeEvent",methods=['POST'])
def sendIdlingOverTimeEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送怠速时间过长告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送怠速时间过长告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0032": {"alarmType": "1", "durationTime": "300","oilExpend":"300"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0032")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "怠速时间过长告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送怠速时间过长告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送怠速时间过长告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送怠速时间过长报警事件（解除报警）
##########################################
@M_carSimulater_process.route("/sendIdlingOverTimeOverEvent",methods=['POST'])
def sendIdlingOverTimeOverEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送怠速解除告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送怠速解除告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "0032": {"alarmType": "0", "durationTime": "500","oilExpend":"500"}}}
            jdata["DEV_ID"] = params["carId"]
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            gpsData = service.genGPSData2()
            obj.setGPSPkg(gpsData)
            obj.setEventType("0032")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "怠速解除告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送怠速解除告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送怠速解除告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急左变道报警
##########################################
@M_carSimulater_process.route("/sendRapidChangeLeftLanes",methods=['POST'])
def sendRapidChangeLeftLanes():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急左变道告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急左变道告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "002A": {"nums":1,"direction":1,"lng":106.54041,"lat":29.40268}}}
            jdata["DEV_ID"] = params["carId"]
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            jdata["event"]["002A"]["lng"] = lng
            jdata["event"]["002A"]["lat"] = lat
            obj = EventReport_protocol(data=jdata)
            obj.setEventType("002A")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "急左变道告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急左变道告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送怠速解除告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急右变道报警
##########################################
@M_carSimulater_process.route("/sendRapidChangeRightLanes",methods=['POST'])
def sendRapidChangeRightLanes():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急右变道告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急右变道告警事件！"
    elif travelStatus == 1:
        try:
            jdata = {"WATER_CODE": "0003", "DEV_ID": "M121501010001",
                     "gpsInfo": {"UTCTime": "2020-04-30 14:59:33", "latitude": "40.22077", "longitude": "116.23128",
                                 "speed": "80.8", "directionAngle": "80.8", "elevation": "2999.9", "positionStar": "3",
                                 "Pdop": "0.3", "Hdop": "0.4", "Vdop": "0.5", "statusBit": 162, "valtage": "36.9",
                                 "OBDSpeed": "60.9", "engineSpeed": "3000", "GPSTotalMileage": "12800", "totalOil": "100000",
                                 "totalTime": "2020002", "GPSTimestamp": "1588229973"},
                     "securityData": {"securityStatus": 107, "doorStatus": 0, "lockStatus": 0, "windowStatus": 0,
                                      "lightStatus": 0, "onoffStatusA": 0, "onoffStatusB": 112, "dataByte": 249}, "event": {
                        "002A": {"nums":1,"direction":0,"lng":106.54041,"lat":29.40268}}}
            jdata["DEV_ID"] = params["carId"]
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            lng = service.getLongitude()
            lat = service.getLatitude()
            jdata["event"]["002A"]["lng"] = lng
            jdata["event"]["002A"]["lat"] = lat
            jdata["gpsInfo"]["latitude"] = lat
            jdata["gpsInfo"]["longitude"] = lng
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gpsInfo"]["UTCTime"] = curTime
            obj = EventReport_protocol(data=jdata)
            obj.setEventType("002A")
            msg = obj.generateEventMsg()
            service.serviceSendMsg(msg, "急右变道告警事件")
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急右变道告警事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急右变道告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')


#---------------------------------------  实时控制逻辑  ---------------------------------------
##########################################
#   【接口类型】改变车速
##########################################
@M_carSimulater_process.route("/changeCarSpeed",methods=['POST'])
def changeCarSpeed():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变车速！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变车速！"
    elif travelStatus == 1:
        try:
            service.setCarSpeed(params["speed"])
            data["status"] = "200"
            data["message"] = "改变车速成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变车速失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变油耗
##########################################
@M_carSimulater_process.route("/changeOilExpend",methods=['POST'])
def changeOilExpend():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变油耗！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变油耗！"
    elif travelStatus == 1:
        try:
            service.setOilExpend(params["oilExpend"])
            data["status"] = "200"
            data["message"] = "改变油耗成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变油耗失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变发动机转速
##########################################
@M_carSimulater_process.route("/changeEngineSpeed",methods=['POST'])
def changeEngineSpeed():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变发动机转速！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变发动机转速！"
    elif travelStatus == 1:
        try:
            service.setEngineSpeed(int(params["engineSpeed"]))
            data["status"] = "200"
            data["message"] = "改变发动机转速成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变发动机转速失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变发送间隔
##########################################
@M_carSimulater_process.route("/changeDurTime",methods=['POST'])
def changeDurTime():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变发送间隔！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变发送间隔！"
    elif travelStatus == 1:
        try:
            service.setSendDur(params["durTime"])
            data["status"] = "200"
            data["message"] = "改变发送间隔成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变发送间隔失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】控制是否存储消息到本地
##########################################
@M_carSimulater_process.route("/controlStoreMsg",methods=['POST'])
def controlStoreMsg():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可存储消息！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        sendType = int(params["sendType"])
        service.setSendType(sendType)
        data["status"] = "200"
        data["message"] = "控制是否存储消息到本地成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 控制是否存储消息到本地失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变剩余油量
##########################################
@M_carSimulater_process.route("/changeSurplusOil",methods=['POST'])
def changeSurplusOil():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变剩余油量！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变剩余油量！"
    elif travelStatus == 1:
        try:
            service.setSurplusOil(int(params["surplusOil"]))
            data["status"] = "200"
            data["message"] = "改变剩余油量成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变剩余油量失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】控制GPS 是有效还是无效
##########################################
@M_carSimulater_process.route("/controlGPSValid",methods=['POST'])
def controlGPSValid():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可设置GPS有效信息！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        GPSValid = int(params["GPSValid"])
        service.setGPSValid(GPSValid)
        data["status"] = "200"
        data["message"] = "设置GPS有效信息成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 设置GPS有效信息失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】控制经纬度是正常，还是为0
##########################################
@M_carSimulater_process.route("/controlLngLatIsOk",methods=['POST'])
def controlLngLatIsOk():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可设置经纬度值！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        lngLatIsOk = int(params["lngLatIsOk"])
        service.setLngLatIsOk(lngLatIsOk)
        data["status"] = "200"
        data["message"] = "设置经纬度值成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 设置经纬度值失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】改变行驶方向
##########################################
@M_carSimulater_process.route("/changeTravelDirection",methods=['POST'])
def changeTravelDirection():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变改变行驶方向！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变改变行驶方向！"
    elif travelStatus == 1:
        try:
            travelDirection = service.getTravelDirection()
            if travelDirection == 0:
                service.setTravelDirection(1)
            else:
                service.setTravelDirection(0)
            data["status"] = "200"
            data["message"] = "改变改变行驶方向成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变改变行驶方向失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变电瓶电压
##########################################
@M_carSimulater_process.route("/changeValtage",methods=['POST'])
def changeValtage():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    voltage = params["other"]["voltage"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改电瓶电压！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变电瓶电压！"
    elif travelStatus == 1:
        try:
            service.setVoltage(voltage)
            data["status"] = "200"
            data["message"] = "改变电瓶电压成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变电瓶电压失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】固定或者取消固定当前GPS点
##########################################
@M_carSimulater_process.route("/fixCurPosition",methods=['POST'])
def fixCurPosition():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    fixPosition = params["fixPosition"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可设置是否固定gps点！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可设置是否固定gps点！"
    elif travelStatus == 1:
        try:
            service.setFixPosition(fixPosition)
            data["status"] = "200"
            data["message"] = "设置是否固定gps点成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 设置是否固定gps点失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】行驶过程中是否发送OBD消息
##########################################
@M_carSimulater_process.route("/setOBDSend",methods=['POST'])
def setOBDSend():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    hasOBD = int(params["hasOBD"])
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可设置是否发送OBD消息！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        service.setHasOBD(hasOBD)
        data["status"] = "200"
        data["message"] = "设置是否发送OBD消息成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 设置是否发送OBD消息失败！"
    return Response(json.dumps(data), mimetype='application/json')


#---------------------------------------  其他操作逻辑  ---------------------------------------
##########################################
#   【接口类型】处理发送的故障码报文
##########################################
@M_carSimulater_process.route("/porcessTroubleCodeMsg",methods=['POST'])
def porcessTroubleCodeMsg():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送故障码！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        conf_R = ConfigParser()
        conf_R.read("config/protocolTools/protocolTools.conf")
        cliSocket = ClientSocket(conf_R.get("socket", "host"),conf_R.getint("socket", "port"))
        cliSocket.connect()
        timeS = int(time.time()) - 8 * 3600
        timeArray = time.localtime(timeS)
        UTCTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        sn = service.getSn()
        protocolObj = TroubleCode_protocol(WATER_CODE=sn,DEV_ID=params["carId"], \
                                    UTCTime=UTCTime,troubleCodeNum=params["troubleCode"]["troubleCodeNum"],troubleCode=params["troubleCode"]["troubleCode"], \
                                    MILStatus=params["troubleCode"]["MILStatus"])
        msg = protocolObj.generateMsg()
        service.serviceSendMsg(msg, "发送故障码")
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送故障码成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 处理失败！"
    return Response(json.dumps(data), mimetype='application/json')












