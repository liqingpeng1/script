#coding:utf-8
import os
import time
from time import sleep

from flask import Blueprint ,Response,request,send_from_directory
from configparser import ConfigParser
import json
import traceback

from lib.protocol.message.DataUpstreamTransport_msg import DataUpstreamTransport_msg
from lib.protocol.message.Location_msg import Location_msg
from lib.socket.ClientSocket import ClientSocket
from lib.socket.service.MessageSimulaterService import MessageSimulaterService
from lib.util import fileUtil
from lib.util.fileUtil import delFile

M_simulater_process = Blueprint('M_simulater_process', __name__)

connects = {}                                  #用来保存连接的信息s
websocket = None                               #保存创建的websocket

##########################################
#   【接口类型】设置socket信息
##########################################
@M_simulater_process.route("/porcessSocketSetting",methods=['POST'])
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
            conf_R.read("config/messageTools/carSimulater.conf")
            conf_W = conf_R
            conf_W["socket"]["host"] = host
            conf_W["socket"]["port"] = port
            with open("config/messageTools/carSimulater.conf", "w") as fi:
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
#   【接口类型】车机联网
##########################################
@M_simulater_process.route("/porcessConnect",methods=['POST'])
def porcessConnect():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        conf_R = ConfigParser()
        conf_R.read("config/messageTools/carSimulater.conf")
        if not sessionId in connects.keys():
            cliSocket = ClientSocket(conf_R.get("socket", "host"), conf_R.getint("socket", "port"))
            cliSocket.connect()
            connect = {}
            connects[sessionId] = connect
            socketName = "socket_" + str(len(connects) + 1)
            connect["name"] = socketName
            service = MessageSimulaterService()
            global websocket
            if websocket == None:
                service.startWebsocketService()                # 如果没有创建websocket服务，则启动新的websocket服务
                websocket = service.getWebsocket()
            else:
                service.setWebsocket(websocket)                # 给新服务设置websocket服务对象
                service.addNewWebsocket()                      # 创建一个新的websocket连接
            service.setSocket(cliSocket)
            service.setTimeout(int(params["timeout"]))
            service.setCarId(params["phoneNum"])
            service.setSendDur(int(params["durTime"]))
            service.setData(params)                                     #传入页面传过来的数据
            service.startWebsocketService()                             #启动websocket服务
            service.startReciveService()                                #接收消息的服务
            service.setGpsLine(params["gpsLine"])
            connect["service"] = connect
            connects[sessionId]["service"] = service
            timeArray = time.localtime(int(time.time()))
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            connects[sessionId]["time"] = curTime
            connects[sessionId]["carId"] = params["phoneNum"]
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
#   【接口类型】车机登录
##########################################
@M_simulater_process.route("/porcessLogin",methods=['POST'])
def porcessLogin():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        connects[sessionId]["service"].carLogin()
        data["status"] = "200"
        data["message"] = "登录成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 登录失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】车机点火
##########################################
@M_simulater_process.route("/porcessFireOn",methods=['POST'])
def porcessFireOn():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        connects[sessionId]["service"].fireOn()
        data["status"] = "200"
        data["message"] = "点火成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 点火失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】车机开始行驶
##########################################
@M_simulater_process.route("/porcessStartTravel",methods=['POST'])
def porcessStartTravel():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        service.startService()
        service.startTravel()
        data["status"] = "200"
        data["message"] = "开始行驶成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 开始行驶失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】车机停止行驶
##########################################
@M_simulater_process.route("/porcessStopTravel",methods=['POST'])
def porcessStopTravel():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        connects[sessionId]["service"].stopTravel()
        data["status"] = "200"
        data["message"] = "停止行驶成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 停止行驶失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】车机熄火
##########################################
@M_simulater_process.route("/porcessFireOff",methods=['POST'])
def porcessFireOff():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        service.fireOff()
        service.stopTravel()
        service.stopService()
        data["status"] = "200"
        data["message"] = "熄火成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 熄火失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】车机断网
##########################################
@M_simulater_process.route("/porcessDisconnect",methods=['POST'])
def porcessDisconnect():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
        # connects[0]["service"].stopWebsocketService()
        service.stopTravel()
        service.stopService()
        service.socket.close()
        connects.pop(sessionId)
        data["status"] = "200"
        data["message"] = "断开连接成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 断开连接失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】车机复位
##########################################
@M_simulater_process.route("/reset",methods=['POST'])
def reset():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    global connects
    global websocket
    try:
        for key in connects:
            service = connects[key]["service"]
            service.stopTravel()
            try:
                service.fireOff()
            except BaseException as e1:
                pass
            service.stopTravel()
            service.stopService()
            service.socket.close()
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
@M_simulater_process.route("/fileUplad",methods=['POST'])
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
    maxPrefix = int(fileUtil.getMaxPrefixFilePre("data/messageTools/GPSLines"))
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
        with open("data/messageTools/GPSLines/" + filename,"w",encoding="utf-8") as fi:
            fi.write(file_content)
        # 返回给前端结果
        data["status"] = "200"
        data["message"] = "文件上传成功"
        data["file"] = fileData
    else:
        data["status"] = "4003"
        data["message"] = "文件上传失败"
    return Response(json.dumps(data), mimetype='application/json')


@M_simulater_process.route("/sampleDowload")
def sampleDowload():
    return send_from_directory(r"data/messageTools/GPSLines",filename="1_sample.json",as_attachment=True)


@M_simulater_process.route("/delGpsLine",methods=['POST'])
def delGpsLine():
    fileName = request.form.get("fileName")
    data = {}
    if fileName == "1_sample.json":
        data["status"] = "4003"
        data["message"] = "Error：示例轨迹不可删除！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            delFile("data/messageTools/GPSLines/",fileName)
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
@M_simulater_process.route("/searchCarsimulaterData",methods=['POST'])
def searchCarsimulaterData():
    carId = request.form.get("carId")
    data = {}
    carFile = "data/messageTools/carData/" + carId + ".json"
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
#   【接口类型】查询当前连接数，和连接对象
##########################################
@M_simulater_process.route("/getConnects",methods=['POST'])
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

##########################################
#   【接口类型】查询当前车辆GPS点
##########################################
@M_simulater_process.route("/searchCurCarGPS",methods=['POST'])
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

#--------------------------------------  报警上报逻辑  --------------------------------------
##########################################
#   【接口类型】发送终端插入报警事件
##########################################
@M_simulater_process.route("/sendTerminalInsertAlarm",methods=['POST'])
def sendTerminalInsertAlarm():
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
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
         "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                        "elevation": "521", "speed": "66", "directionAngle": "59",
                                        "infoTime": "2020-05-28 14:20:04"},
         "extraInfo": {"FA": {"terminalInsert": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
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
@M_simulater_process.route("/sendTerminalPullOutAlarm",methods=['POST'])
def sendTerminalPullOutAlarm():
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
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
         "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                        "elevation": "521", "speed": "66", "directionAngle": "59",
                                        "infoTime": "2020-05-28 14:20:04"},
         "extraInfo": {"FA": {"terminalPullOut": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
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
#   【接口类型】发送低电压报警报警事件
##########################################
@M_simulater_process.route("/sendLowVoltageAlarm",methods=['POST'])
def sendLowVoltageAlarm():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}

    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送低电压报警事件！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0", "subPkg": "0",
         "pkgCounts": "0", "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                        "elevation": "521", "speed": "66", "directionAngle": "59",
                                        "infoTime": "2020-05-28 14:20:04"},
         "extraInfo": {"FA": {"lowVoltage": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送低电压报警事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送低电压报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急加速事件
##########################################
@M_simulater_process.route("/sendRapidAccelerateAlarm",methods=['POST'])
def sendRapidAccelerateAlarm():
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
            jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                     "subPkg": "0",
                     "pkgCounts": "0",
                     "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                  "elevation": "521", "speed": "66", "directionAngle": "59",
                                  "infoTime": "2020-05-28 14:20:04"},
                     "extraInfo": {"FA": {"rapidAccelerateAlarm": "on"}}}
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["phoneNum"] = params["phoneNum"]
            jdata["msgWaterCode"] = service.getSn()
            jdata["baseInfo"]["infoTime"] = curTime
            jdata["baseInfo"]["latitude"] = service.getCurLatitude()
            jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
            jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
            msgObj = Location_msg()
            msg = msgObj.generateMsg_GUI(jdata)
            service.serviceSendMsg(msg)
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
@M_simulater_process.route("/sendSharpSlowdownAlarm",methods=['POST'])
def sendSharpSlowdownAlarm():
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
            jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                     "subPkg": "0",
                     "pkgCounts": "0",
                     "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                  "elevation": "521", "speed": "66", "directionAngle": "59",
                                  "infoTime": "2020-05-28 14:20:04"},
                     "extraInfo": {"FA": {"sharpSlowdownAlarm": "on"}}}
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["phoneNum"] = params["phoneNum"]
            jdata["msgWaterCode"] = service.getSn()
            jdata["baseInfo"]["infoTime"] = curTime
            jdata["baseInfo"]["latitude"] = service.getCurLatitude()
            jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
            jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
            msgObj = Location_msg()
            msg = msgObj.generateMsg_GUI(jdata)
            service.serviceSendMsg(msg)
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
#   【接口类型】发送急左转弯事件
##########################################
@M_simulater_process.route("/sendSharpTurnEvent",methods=['POST'])
def sendSharpTurnEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急左转弯事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急左转弯事件！"
    elif travelStatus == 1:
        try:
            jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                     "subPkg": "0",
                     "pkgCounts": "0",
                     "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                  "elevation": "521", "speed": "66", "directionAngle": "59",
                                  "infoTime": "2020-05-28 14:20:04"},
                     "extraInfo": {"FA": {"sharpBendAlarm": "on"}}}
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["phoneNum"] = params["phoneNum"]
            jdata["msgWaterCode"] = service.getSn()
            jdata["baseInfo"]["infoTime"] = curTime
            jdata["baseInfo"]["latitude"] = service.getCurLatitude()
            jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
            jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
            msgObj = Location_msg()
            msg = msgObj.generateMsg_GUI(jdata)
            service.serviceSendMsg(msg)
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急左转弯事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急转左弯事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急右转弯事件
##########################################
@M_simulater_process.route("/sendRightSharpTurnEvent",methods=['POST'])
def sendRightSharpTurnEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急右转弯事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送急右转弯事件！"
    elif travelStatus == 1:
        try:
            jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                     "subPkg": "0",
                     "pkgCounts": "0",
                     "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                  "elevation": "521", "speed": "66", "directionAngle": "59",
                                  "infoTime": "2020-05-28 14:20:04"},
                     "extraInfo": {"FA": {"sharpRightBendAlarm": "on"}}}
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["phoneNum"] = params["phoneNum"]
            jdata["msgWaterCode"] = service.getSn()
            jdata["baseInfo"]["infoTime"] = curTime
            jdata["baseInfo"]["latitude"] = service.getCurLatitude()
            jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
            jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
            msgObj = Location_msg()
            msg = msgObj.generateMsg_GUI(jdata)
            service.serviceSendMsg(msg)
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急右转弯事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急转右弯事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送怠速过长事件
##########################################
@M_simulater_process.route("/sendIdlingSpeedOverEvent",methods=['POST'])
def sendIdlingSpeedOverEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送怠速过长事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"idlingSpeedOver": {"alarmType": "1", "idlingTimeOfDuration": "300",
                             "idlingOilExpend": "300", "idlingEngineMaxSpeed": "2000","idlingEngineMinSpeed":"1000"}}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送怠速过长事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送怠速过长事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送怠速过长解除事件
##########################################
@M_simulater_process.route("/sendUnIdlingSpeedOverEvent",methods=['POST'])
def sendUnIdlingSpeedOverEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送怠速过长解除事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"idlingSpeedOver": {"alarmType": "0", "idlingTimeOfDuration": "500",
                             "idlingOilExpend": "500", "idlingEngineMaxSpeed": "2000","idlingEngineMinSpeed":"1000"}}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送怠速过长解除事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送怠速过长解除事件失败！"
    return Response(json.dumps(data), mimetype='application/json')


##########################################
#   【接口类型】发送超速事件
##########################################
@M_simulater_process.route("/sendOverspeedEvent",methods=['POST'])
def sendOverspeedEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送超速事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"overspeedAlarm": {"alarmType": "1", "averageSpeed": "700",
                             "maxSpeed": "145", "overspeedDistance": "10000","overspeedTimeOfDuration":"700"}}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送超速事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送超速事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送疲劳驾驶事件
##########################################
@M_simulater_process.route("/sendFatigueDrivingEvent",methods=['POST'])
def sendFatigueDrivingEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送疲劳驾驶事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"fatigueDriving": {"alarmType": "1", "totalContinueDrivingTime": "10000"}}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送疲劳驾驶事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送疲劳驾驶事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送水温报警事件
##########################################
@M_simulater_process.route("/sendWaterTemperatureEvent",methods=['POST'])
def sendWaterTemperatureEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送水温报警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"waterTemperatureAlarm": {"alarmType": "1", "averageTemperature": "280",
                              "maxTemperature": "750", "timeOfDuration": "11000"}}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送水温报警事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送水温报警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送高速空挡滑行事件
##########################################
@M_simulater_process.route("/sendHighSpeedNeutralGearEvent",methods=['POST'])
def sendHighSpeedNeutralGearEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送高速空挡滑行事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可发送高速空挡滑行事件！"
    elif travelStatus == 1:
        try:
            jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                     "subPkg": "0",
                     "pkgCounts": "0",
                     "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                                  "elevation": "521", "speed": "66", "directionAngle": "59",
                                  "infoTime": "2020-05-28 14:20:04"},
                     "extraInfo": {"FA": {"highSpeedNeutralGear": "on"}}}
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["phoneNum"] = params["phoneNum"]
            jdata["msgWaterCode"] = service.getSn()
            jdata["baseInfo"]["infoTime"] = curTime
            jdata["baseInfo"]["latitude"] = service.getCurLatitude()
            jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
            jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
            msgObj = Location_msg()
            msg = msgObj.generateMsg_GUI(jdata)
            service.serviceSendMsg(msg)
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送高速空挡滑行事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送高速空挡滑行事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送碰撞告警事件
##########################################
@M_simulater_process.route("/sendCrashAlarmEvent",methods=['POST'])
def sendCrashAlarmEvent():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送碰撞告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"crashAlarm": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
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
#   【接口类型】发送急左变道告警事件
##########################################
@M_simulater_process.route("/sendapidChangeLeftLines",methods=['POST'])
def sendapidChangeLeftLines():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急左变道告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"rapidChangeLines": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送急左变道告警事件成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送急左变道告警事件失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】发送急右变道告警事件
##########################################
@M_simulater_process.route("/sendapidChangeRightLines",methods=['POST'])
def sendapidChangeRightLines():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送急右变道告警事件！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    try:
        jdata = {"msgID": "0200", "phoneNum": "13146201119", "msgWaterCode": "1", "encryptionType": "0",
                 "subPkg": "0",
                 "pkgCounts": "0",
                 "baseInfo": {"alarmFlag": 0, "status": 262402, "latitude": 29.40268, "longtitude": 106.54041,
                              "elevation": "521", "speed": "66", "directionAngle": "59",
                              "infoTime": "2020-05-28 14:20:04"},
                 "extraInfo": {"FA": {"rapidChangeRightLines": "on"}}}
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        jdata["phoneNum"] = params["phoneNum"]
        jdata["msgWaterCode"] = service.getSn()
        jdata["baseInfo"]["infoTime"] = curTime
        jdata["baseInfo"]["latitude"] = service.getCurLatitude()
        jdata["baseInfo"]["longtitude"] = service.getCurLongtitude()
        jdata["baseInfo"]["directionAngle"] = service.getDirAngle()
        msgObj = Location_msg()
        msg = msgObj.generateMsg_GUI(jdata)
        service.serviceSendMsg(msg)
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
@M_simulater_process.route("/changeCarSpeed",methods=['POST'])
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
@M_simulater_process.route("/changeOilExpend",methods=['POST'])
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
#   【接口类型】改变发送间隔
##########################################
@M_simulater_process.route("/changeDurTime",methods=['POST'])
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
            service.setSendDur(int(params["durTime"]))
            data["status"] = "200"
            data["message"] = "改变发送间隔成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变发送间隔失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变行驶方向
##########################################
@M_simulater_process.route("/changeTravelDirection",methods=['POST'])
def changeTravelDirection():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变行驶方向！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变行驶方向！"
    elif travelStatus == 1:
        try:
            if service.travelDirection == 0:
                service.setTravelDirection(1)
            else:
                service.setTravelDirection(0)
            data["status"] = "200"
            data["message"] = "改变行驶方向成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变行驶方向失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】固定gps点
##########################################
@M_simulater_process.route("/fixCurPosition",methods=['POST'])
def fixCurPosition():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可固定gps点！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可固定gps点！"
    elif travelStatus == 1:
        try:
            service.setFixCurPosition(int(params["fixPosition"]))
            data["status"] = "200"
            if int(params["fixPosition"]) == 0:
                data["message"] = "固定gps点成功！"
            else:
                data["message"] = "取消固定gps点成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 固定gps点失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变电瓶电压
##########################################
@M_simulater_process.route("/changeVotage",methods=['POST'])
def changeVotage():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可改变电瓶电压！"
        return Response(json.dumps(data), mimetype='application/json')

    service = connects[sessionId]["service"]
    travelStatus = service.getTravelStatus()                        #获取汽车行驶状态
    if travelStatus == 0 or travelStatus == 2:
        data["status"] = "4003"
        data["message"] = "Error: 汽车还未行驶，不可改变电瓶电压！"
    elif travelStatus == 1:
        try:
            service.setVotage(params["votage"])
            data["status"] = "200"
            data["message"] = "改变电瓶电压成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变电瓶电压失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变发动机转速
##########################################
@M_simulater_process.route("/changeEngineSpeed",methods=['POST'])
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
            service.setEngineSpeed(params["engineSpeed"])
            data["status"] = "200"
            data["message"] = "改变发动机转速成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变发动机转速失败！"
    return Response(json.dumps(data), mimetype='application/json')

##########################################
#   【接口类型】改变剩余油量
##########################################
@M_simulater_process.route("/changeSurplusOil",methods=['POST'])
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
            service.setSurplusOil(params["surplusOil"])
            data["status"] = "200"
            data["message"] = "改变剩余油量成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 改变剩余油量失败！"
    return Response(json.dumps(data), mimetype='application/json')


#---------------------------------------  其他操作逻辑  ---------------------------------------
##########################################
#   【接口类型】处理发送的故障码报文
##########################################
@M_simulater_process.route("/porcessTroubleCodeMsg",methods=['POST'])
def porcessTroubleCodeMsg():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    carId = params["carId"]
    data = {}
    if not sessionId in connects.keys():
        data["status"] = "4003"
        data["message"] = "Error: 未启动服务，不可发送故障码！"
        return Response(json.dumps(data), mimetype='application/json')
    service = connects[sessionId]["service"]
    try:
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        msgWaterCode = service.getSn()
        latitude = float(service.getCurLatitude())
        longitude = float(service.getCurLongtitude())
        nums = int(params["troubleCodeNums"])
        systemId = params["systemId"]
        info = {}
        info["infoTime"] = curTime
        info["latitude"] = latitude
        info["longitude"] = longitude
        info["troubleCodeNums"] = nums
        info["systemId"] = systemId
        obj = DataUpstreamTransport_msg()
        msg = obj.generateMsg_GUI(phoneNum=carId,msgWaterCode=msgWaterCode,msgType="F2",data=info)
        service.serviceSendMsg(msg)
        service.setSn(service.getSn() + 1)
        data["status"] = "200"
        data["message"] = "发送故障码成功！"
    except BaseException as e:
        # 打印异常信息
        traceback.print_exc()
        data["status"] = "4003"
        data["message"] = "Error: 发送故障码失败！"
    return Response(json.dumps(data), mimetype='application/json')
