#encoding:utf-8
from lib.protocol.m300.GPS_protocol_m300 import GPS_protocol_m300
from lib.protocol.m300.M300Base import M300Base

'''
定义驾驶行为协议类
'''

class TravelAct_protocol_m300(M300Base):
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0,actType=1,accelerateTotalTimes=2, \
                 decelerateTotalTimes=2,sharpTurnTotalTimes=2,acceleration=500,speed=60,gps={}):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.waterCode = waterCode                    # 消息流水号
        self.DEV_ID = DEV_ID                          # 设备Id
        self.encryptionType = encryptionType          # 消息属性里面的是否加密字段

        if len(gps) == 0:
            self.GPSPkg = "14031b0e22160265b86206ed8c7002029402290000006e00016802988100000000000000"
        else:
            gpsObj = GPS_protocol_m300(3,"M121501010001",0,gps["dateInfo"],float(gps["latitude"]),float(gps["longitude"]),int(gps["positionStar"]),float(gps["speed"]), \
                                       float(gps["direction"]),float(gps["altitude"]),int(gps["ACCStatus"]),float(gps["valtage"]),float(gps["OBDSpeed"]), \
                                       int(gps["valid"]),int(gps["tripMark"]))
            self.GPSPkg = gpsObj.getMsgBody()
        self.actType = actType                                       # 驾驶行为类别
        self.accelerateTotalTimes = accelerateTotalTimes             # 急加速总次数
        self.decelerateTotalTimes = decelerateTotalTimes             # 急减速总次数
        self.sharpTurnTotalTimes = sharpTurnTotalTimes               # 急转弯总次数
        self.acceleration = acceleration                             # 事件发生时，加速度值
        self.speed = speed                                           # 事件发生时，车速度
        self.tripMark = "0000"                                       # 驾驶循环标签

    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0022"                                                   #功能id
        waterCode = self.int2hexStringByBytes(self.waterCode,2)          #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                       #设备id
        msgBody = self.getMsgBody()  # 消息体
        msgLen = int(len(msgBody) / 2)
        property = self.getMsgProperty(msgBodyLen=msgLen,encryptionType=self.encryptionType)
        checkCode = self.getCheckCode(FUNID + waterCode + DEV_ID + property + msgBody)
        msg = msg + FUNID + waterCode + DEV_ID + property + msgBody + checkCode + self.IDENTIFY
        return msg

    #################################################
    # 获取消息体
    #################################################
    def getMsgBody(self):
        gps = self.GPSPkg
        actType = self.int2hexStringByBytes(self.actType)
        accelerateTotalTimes = self.int2hexStringByBytes(self.accelerateTotalTimes,4)
        decelerateTotalTimes = self.int2hexStringByBytes(self.decelerateTotalTimes,4)
        sharpTurnTotalTimes = self.int2hexStringByBytes(self.sharpTurnTotalTimes,4)
        acceleration = self.int2hexStringByBytes(self.acceleration,2)
        speed = self.int2hexStringByBytes(self.speed)
        tripMark = self.tripMark
        data = gps + actType + accelerateTotalTimes + decelerateTotalTimes + sharpTurnTotalTimes
        data = data + acceleration + speed + tripMark
        return data





