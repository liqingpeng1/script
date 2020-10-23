#encoding:utf-8
from lib.protocol.m300.GPS_protocol_m300 import GPS_protocol_m300
from lib.protocol.m300.M300Base import M300Base
from lib.protocol.m300.OBDCAN_protocol_m300 import OBDCAN_protocol_m300

'''
定义报警协议类
'''

class Alarm_protocol_m300(M300Base):
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0,alarmType="0001",data = {}):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.data = data
        self.waterCode = waterCode                    #消息流水号
        self.DEV_ID = DEV_ID                          #设备Id
        self.encryptionType = encryptionType          # 消息属性里面的是否加密字段

        self.alarmType = alarmType
        if len(data) == 0:
            self.GPSPkg = "14031b0e22160265b86206ed8c7002029402290000006e00016802988100000000000000"
            self.GSMPkg = "0000000000"
            self.CANStatus = "ffffffffffffffffffff00000000000000000000"
        else:
            self.waterCode = data["waterCode"]
            self.DEV_ID = data["DEV_ID"]
            self.alarm = data["alarm"]
            GPSData = data["GPSData"]
            GSMData = data["GSMData"]
            OBDData = data["OBDCANData"]
            self.GPSPkg = GPS_protocol_m300(dateInfo=GPSData["dateInfo"],latitude=float(GPSData["latitude"]),longitude=float(GPSData["longitude"]) \
                                            ,positionStar=int(GPSData["positionStar"]),speed=float(GPSData["speed"]),direction=float(GPSData["direction"]), \
                                            altitude=float(GPSData["altitude"]),ACCStatus=int(GPSData["ACCStatus"]),valtage=float(GPSData["valtage"]),OBDSpeed=float(GPSData["OBDSpeed"]), \
                                            valid=int(GPSData["valid"]) ,tripMark=int(GPSData["tripMark"])).getMsgBody()
            self.GSMPkg = self.getGSMPkg(operatorType=int(GSMData["operatorType"]),LAC=GSMData["LAC"],CellId=GSMData["CellId"])
            self.CANStatus = OBDCAN_protocol_m300(statusMask=OBDData["statusMask"],safeStatus=int(OBDData["safeStatus"]),doorStatus=int(OBDData["doorStatus"]), \
                                                       lockStatus=int(OBDData["lockStatus"]),windowStatus=int(OBDData["windowStatus"]),lightStatus=int(OBDData["lightStatus"]), \
                                                       swichStatusA=int(OBDData["swichStatusA"]),swichStatusB=int(OBDData["swichStatusB"])).getMsgBody()[14:48] + "000000"

    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0021"                                                  #功能id
        waterCode = self.int2hexStringByBytes(self.waterCode,2)         #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                      #设备id
        if len(self.data) == 0:
            msgBody = self.getMsgBody()  # 消息体
        else:
            msgBody = self.getMsgBody_GUI()  # 消息体
        msgLen = int(len(msgBody) / 2)
        property = self.getMsgProperty(msgBodyLen=msgLen,encryptionType=self.encryptionType)
        checkCode = self.getCheckCode(FUNID + waterCode + DEV_ID + property + msgBody)
        msg = msg + FUNID + waterCode + DEV_ID + property + msgBody + checkCode + self.IDENTIFY
        return msg

    #################################################
    # 获取消息体
    #################################################
    def getMsgBody(self):
        GPSPkg = self.GPSPkg
        GSMPkg = self.GSMPkg
        CANStatus = self.CANStatus
        alarmContent = ""
        if self.alarmType == "0001":                                                      #汽车点火上报
            extra = ""
            alarmContent = "0001" + self.int2hexStringByBytes(int(len(extra)/2)) + extra
        elif self.alarmType == "0002":                                                    #汽车熄火上报
            extra = ""
            alarmContent = "0002" + self.int2hexStringByBytes(int(len(extra)/2)) + extra

        return GPSPkg + GSMPkg + CANStatus + alarmContent
    def getMsgBody_GUI(self):
        GPSPkg = self.GPSPkg
        GSMPkg = self.GSMPkg
        CANStatus = self.CANStatus
        alarmContent = ""
        if (list(self.alarm.keys())[0] == "0001"):                                                      #汽车点火上报
            extra = ""
            alarmContent = "0001" + self.int2hexStringByBytes(int(len(extra)/2)) + extra
        elif (list(self.alarm.keys())[0] == "0002"):                                                    #汽车熄火上报
            extra = ""
            alarmContent = "0002" + self.int2hexStringByBytes(int(len(extra)/2)) + extra

        return GPSPkg + GSMPkg + CANStatus + alarmContent

    #################################################
    # 获取GSM信息
    ##############################################
    def getGSMPkg(self,operatorType=1,LAC="1234",CellId="5678"):
        #运营商类别      1－移动    2－联通    3－电信
        operatorType = self.int2hexStringByBytes(operatorType)
        # u16	服务器 LAC + CellID，比如  1234  5678
        # LAC和CellID各占两个字节
        LAC = self.int2hexStringByBytes(int(LAC),2)
        CellId = self.int2hexStringByBytes(int(CellId),2)
        data = operatorType + LAC + CellId
        return data


if __name__ == "__main__":
    print(Alarm_protocol_m300().generateMsg())


