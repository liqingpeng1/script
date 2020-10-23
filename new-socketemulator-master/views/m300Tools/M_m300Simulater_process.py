#coding:utf-8
import os
import time

from flask import Blueprint ,Response,request,send_from_directory
from configparser import ConfigParser

import json
import traceback

from lib.protocol.m300.TravelAct_protocol_m300 import TravelAct_protocol_m300
from lib.socket.ClientSocket import ClientSocket
from lib.socket.service.M300SimulaterService import M300SimulaterService
from lib.util import fileUtil
from lib.util.fileUtil import delFile

M_m300Simulater_process = Blueprint('M_m300Simulater_process', __name__)

connects = {}                                  #用来保存连接的信息s
websocket = None                               #保存创建的websocket

##########################################
#   【接口类型】设置socket信息
##########################################
@M_m300Simulater_process.route("/porcessSocketSetting",methods=['POST'])
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
            conf_R.read("config/m300Tools/m300Simulater.conf")
            conf_W = conf_R
            conf_W["socket"]["host"] = host
            conf_W["socket"]["port"] = port
            with open("config/m300Tools/m300Simulater.conf", "w") as fi:
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
#   【接口类型】联网
##########################################
@M_m300Simulater_process.route("/porcessConnect",methods=['POST'])
def porcessConnect():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        conf_R = ConfigParser()
        conf_R.read("config/m300Tools/m300Simulater.conf")
        if not sessionId in connects.keys():
            cliSocket = ClientSocket(conf_R.get("socket", "host"), conf_R.getint("socket", "port"))
            cliSocket.connect()
            connect = {}
            connects[sessionId] = connect
            socketName = "socket_" + str(len(connects) + 1)
            connect["name"] = socketName
            service = M300SimulaterService()
            global websocket
            if websocket == None:
                service.startWebsocketService()                # 如果没有创建websocket服务，则启动新的websocket服务
                websocket = service.getWebsocket()
            else:
                service.setWebsocket(websocket)                # 给新服务设置websocket服务对象
                service.addNewWebsocket()                      # 创建一个新的websocket连接
            service.setSocket(cliSocket)
            service.setTimeout(int(params["timeout"]))
            service.setCarId(params["carId"])
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
#   【接口类型】车机登录
##########################################
@M_m300Simulater_process.route("/porcessLogin",methods=['POST'])
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
@M_m300Simulater_process.route("/porcessFireOn",methods=['POST'])
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
@M_m300Simulater_process.route("/porcessStartTravel",methods=['POST'])
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
@M_m300Simulater_process.route("/porcessStopTravel",methods=['POST'])
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
@M_m300Simulater_process.route("/porcessFireOff",methods=['POST'])
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
@M_m300Simulater_process.route("/porcessDisconnect",methods=['POST'])
def porcessDisconnect():
    params = request.get_data()
    params = json.loads(params.decode("utf-8"))
    sessionId = params["session"]["sessionId"]
    data = {}
    try:
        service = connects[sessionId]["service"]
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
@M_m300Simulater_process.route("/reset",methods=['POST'])
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
                pass
                # service.fireOff()
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
@M_m300Simulater_process.route("/fileUplad",methods=['POST'])
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
    maxPrefix = int(fileUtil.getMaxPrefixFilePre("data/m300Tools/GPSLines"))
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
        with open("data/m300Tools/GPSLines/" + filename,"w",encoding="utf-8") as fi:
            fi.write(file_content)
        # 返回给前端结果
        data["status"] = "200"
        data["message"] = "文件上传成功"
        data["file"] = fileData
    else:
        data["status"] = "4003"
        data["message"] = "文件上传失败"
    return Response(json.dumps(data), mimetype='application/json')


@M_m300Simulater_process.route("/sampleDowload")
def sampleDowload():
    return send_from_directory(r"data/m300Tools/GPSLines",filename="1_sample.json",as_attachment=True)



@M_m300Simulater_process.route("/delGpsLine",methods=['POST'])
def delGpsLine():
    fileName = request.form.get("fileName")
    data = {}
    if fileName == "1_sample.json":
        data["status"] = "4003"
        data["message"] = "Error：示例轨迹不可删除！"
        return Response(json.dumps(data), mimetype='application/json')
    else:
        try:
            delFile("data/m300Tools/GPSLines/",fileName)
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
@M_m300Simulater_process.route("/searchCarsimulaterData",methods=['POST'])
def searchCarsimulaterData():
    carId = request.form.get("carId")
    data = {}
    carFile = "data/m300Tools/carData/" + carId + ".json"
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
@M_m300Simulater_process.route("/getConnects",methods=['POST'])
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

#--------------------------------------  报警上报逻辑  --------------------------------------
##########################################
#   【接口类型】发送急加速事件
##########################################
@M_m300Simulater_process.route("/sendAccelerateEvent",methods=['POST'])
def sendAccelerateEvent():
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
            jdata = {"FUNID": "0007", "waterCode": "1", "DEV_ID": "M202004070000", "encryptionType": "0",
             "gps": {"dateInfo": "2020-06-05 11:28:33", "latitude": 40.22077, "longitude": 116.23128,
                     "positionStar": "2", "speed": "66.0", "direction": "55.3", "altitude": "11.0", "ACCStatus": "1",
                     "valtage": "36.0", "OBDSpeed": "66.4", "valid": 1, "tripMark": "0"}, "actType": "1",
             "accelerateTotalTimes": "2", "decelerateTotalTimes": "2", "sharpTurnTotalTimes": "2",
             "acceleration": "500", "speed": "60"}
            carData = service.getCarData()
            carData["event"]["threeRapid"]["totalRapidlyAccelerate"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"] + 1
            service.setCarData(carData)
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gps"]["dateInfo"] = curTime
            jdata["gps"]["latitude"] = service.getCurLatitude()
            jdata["gps"]["longitude"] = service.getCurLongtitude()
            jdata["gps"]["speed"] = service.getSpeed()
            jdata["gps"]["OBDSpeed"] = service.getSpeed()
            jdata["gps"]["direction"] = service.getDirAngle()
            jdata["accelerateTotalTimes"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
            jdata["decelerateTotalTimes"] = carData["event"]["threeRapid"]["totalSharpSlowdown"]
            jdata["sharpTurnTotalTimes"] = carData["event"]["threeRapid"]["totalSharpTurn"]
            jdata["DEV_ID"] = params["carId"]
            obj = TravelAct_protocol_m300(waterCode=int(jdata["waterCode"]), DEV_ID=jdata["DEV_ID"],encryptionType=int(jdata["encryptionType"]), \
                        actType=int(jdata["actType"]),accelerateTotalTimes=int(jdata["accelerateTotalTimes"]),decelerateTotalTimes=int(jdata["decelerateTotalTimes"]), \
                        sharpTurnTotalTimes=int(jdata["sharpTurnTotalTimes"]),acceleration=int(jdata["acceleration"]), speed=int(jdata["speed"]),gps=jdata["gps"])
            msg = obj.generateMsg()
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
@M_m300Simulater_process.route("/sendDecelerateEvent",methods=['POST'])
def sendDecelerateEvent():
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
            jdata = {"FUNID": "0007", "waterCode": "1", "DEV_ID": "M202004070000", "encryptionType": "0",
             "gps": {"dateInfo": "2020-06-05 11:28:33", "latitude": 40.22077, "longitude": 116.23128,
                     "positionStar": "2", "speed": "66.0", "direction": "55.3", "altitude": "11.0", "ACCStatus": "1",
                     "valtage": "36.0", "OBDSpeed": "66.4", "valid": 1, "tripMark": "0"}, "actType": "2",
             "accelerateTotalTimes": "2", "decelerateTotalTimes": "2", "sharpTurnTotalTimes": "2",
             "acceleration": "500", "speed": "60"}
            carData = service.getCarData()
            carData["event"]["threeRapid"]["totalSharpSlowdown"] = carData["event"]["threeRapid"]["totalSharpSlowdown"] + 1
            service.setCarData(carData)
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gps"]["dateInfo"] = curTime
            jdata["gps"]["latitude"] = service.getCurLatitude()
            jdata["gps"]["longitude"] = service.getCurLongtitude()
            jdata["gps"]["speed"] = service.getSpeed()
            jdata["gps"]["OBDSpeed"] = service.getSpeed()
            jdata["gps"]["direction"] = service.getDirAngle()
            jdata["accelerateTotalTimes"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
            jdata["decelerateTotalTimes"] = carData["event"]["threeRapid"]["totalSharpSlowdown"]
            jdata["sharpTurnTotalTimes"] = carData["event"]["threeRapid"]["totalSharpTurn"]
            jdata["DEV_ID"] = params["carId"]
            obj = TravelAct_protocol_m300(waterCode=int(jdata["waterCode"]), DEV_ID=jdata["DEV_ID"],encryptionType=int(jdata["encryptionType"]), \
                        actType=int(jdata["actType"]),accelerateTotalTimes=int(jdata["accelerateTotalTimes"]),decelerateTotalTimes=int(jdata["decelerateTotalTimes"]), \
                        sharpTurnTotalTimes=int(jdata["sharpTurnTotalTimes"]),acceleration=int(jdata["acceleration"]), speed=int(jdata["speed"]),gps=jdata["gps"])
            msg = obj.generateMsg()
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
#   【接口类型】发送急转弯事件
##########################################
@M_m300Simulater_process.route("/sendSharpTurnEvent",methods=['POST'])
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
            jdata = {"FUNID": "0007", "waterCode": "1", "DEV_ID": "M202004070000", "encryptionType": "0",
             "gps": {"dateInfo": "2020-06-05 11:28:33", "latitude": 40.22077, "longitude": 116.23128,
                     "positionStar": "2", "speed": "66.0", "direction": "55.3", "altitude": "11.0", "ACCStatus": "1",
                     "valtage": "36.0", "OBDSpeed": "66.4", "valid": 1, "tripMark": "0"}, "actType": "3",
             "accelerateTotalTimes": "2", "decelerateTotalTimes": "2", "sharpTurnTotalTimes": "2",
             "acceleration": "500", "speed": "60"}
            carData = service.getCarData()
            carData["event"]["threeRapid"]["totalSharpSlowdown"] = carData["event"]["threeRapid"]["totalSharpSlowdown"] + 1
            service.setCarData(carData)
            timeStamp = time.time() - 8 * 3600
            timeArray = time.localtime(timeStamp)
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            jdata["gps"]["dateInfo"] = curTime
            jdata["gps"]["latitude"] = service.getCurLatitude()
            jdata["gps"]["longitude"] = service.getCurLongtitude()
            jdata["gps"]["speed"] = service.getSpeed()
            jdata["gps"]["OBDSpeed"] = service.getSpeed()
            jdata["gps"]["direction"] = service.getDirAngle()
            jdata["accelerateTotalTimes"] = carData["event"]["threeRapid"]["totalRapidlyAccelerate"]
            jdata["decelerateTotalTimes"] = carData["event"]["threeRapid"]["totalSharpSlowdown"]
            jdata["sharpTurnTotalTimes"] = carData["event"]["threeRapid"]["totalSharpTurn"]
            jdata["DEV_ID"] = params["carId"]
            obj = TravelAct_protocol_m300(waterCode=int(jdata["waterCode"]), DEV_ID=jdata["DEV_ID"],encryptionType=int(jdata["encryptionType"]), \
                        actType=int(jdata["actType"]),accelerateTotalTimes=int(jdata["accelerateTotalTimes"]),decelerateTotalTimes=int(jdata["decelerateTotalTimes"]), \
                        sharpTurnTotalTimes=int(jdata["sharpTurnTotalTimes"]),acceleration=int(jdata["acceleration"]), speed=int(jdata["speed"]),gps=jdata["gps"])
            msg = obj.generateMsg()
            service.serviceSendMsg(msg)
            service.setSn(service.getSn() + 1)
            data["status"] = "200"
            data["message"] = "发送急转弯事件成功！"
        except BaseException as e:
            # 打印异常信息
            traceback.print_exc()
            data["status"] = "4003"
            data["message"] = "Error: 发送急转弯事件失败！"
    return Response(json.dumps(data), mimetype='application/json')


#---------------------------------------  实时控制逻辑  ---------------------------------------
##########################################
#   【接口类型】改变车速
##########################################
@M_m300Simulater_process.route("/changeCarSpeed",methods=['POST'])
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
@M_m300Simulater_process.route("/changeOilExpend",methods=['POST'])
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
@M_m300Simulater_process.route("/changeDurTime",methods=['POST'])
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