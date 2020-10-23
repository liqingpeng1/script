#encoding:utf-8

'''
定义终端版本信息主动上报
'''
from lib.protocol.message.MessageBase import MessageBase


class TerminalVersionInfo_msg(MessageBase):
    def __init__(self):
        super().__init__()          #不执行该方法，无法使用父类里面定义的属性
        pass

    #######################################################
    # 生成一条完整的消息
    #######################################################
    def generateMsg(self):
        msg = ""
        msgHeader = self.getMsgHeader()
        msgBody = self.getMsgBody()
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    # 生成一条完整的消息，针对图形界面，可传递参数
    def generateMsg_GUI(self,msgID="0205",phoneNum="13146201119",msgWaterCode=1,encryptionType=0,subPkg=0, \
                    softwareVersion="L200AB01020002", softwareVersionDate="2020-02-10", CPUId="CPU-12345678",GMSType="GMS-TYPE-123456", \
                    GMS_IMEI="GMS_IMEI_123456", SIM_IMSI="SIM_13146201119", SIM_ICCID="SIM_ICCID13146201119",carType=22, VIN="VIN_1234567891234", \
                    totalMileage=389000, totalOilExpend=420000,displacement=1500,oilDensity=80,OBDSerial=257,oilCalculateType="01"):
        msg = ""
        msgBody = self.getMsgBody_GUI(softwareVersion,softwareVersionDate,CPUId,GMSType,GMS_IMEI,SIM_IMSI,SIM_ICCID,carType,VIN,\
                   totalMileage,totalOilExpend,displacement,oilDensity,OBDSerial,oilCalculateType)
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,msgBody)
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    # 生成一条完整的消息，数据随机产生
    def generateMsg_random(self):
        msgID = "0205"
        phoneNum = self.getRandomStr(11, "0123456789")
        msgWaterCode = self.getRandomNum(1, 65535)
        encryptionType = 0
        subPkg = self.getRandomNum(intArr=[0, 8192])
        softwareVersion = "KZP200_" + self.getRandomStr(7)
        softwareVersionDate = self.getRandomDate(type=1)
        CPUId = "CPU-" + self.getRandomStr(8,"0123456789")
        GMSType = "GMS-TYPE-" + self.getRandomStr(6,"0123456789")
        GMS_IMEI = "GMS_IMEI_" + self.getRandomStr(6,"0123456789")
        SIM_IMSI = "SIM_" + self.getRandomStr(11,"0123456789")
        SIM_ICCID = "SIM_ICCID" + self.getRandomStr(11,"0123456789")
        carType = self.getRandomNum(0,65535)
        VIN = "VIN_" + self.getRandomStr(13,"0123456789")
        totalMileage = self.getRandomNum(30000,6000000)
        totalOilExpend = self.getRandomNum(30000,6000000)
        displacement = self.getRandomNum(500,3000)
        oilDensity = self.getRandomNum(80,500)
        msg = ""
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg)
        msgBody = self.getMsgBody_GUI(softwareVersion, softwareVersionDate, CPUId, GMSType, GMS_IMEI, SIM_IMSI,
                                      SIM_ICCID, carType, VIN, \
                                      totalMileage, totalOilExpend,displacement,oilDensity)
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg


    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        msg = ""
        softwareVersion = self.GBKString2Hex("L200AB01020002")                     #软件版本号
        softwareVersionDate = self.GBKString2Hex("2020-02-10")                     #终端版本日期
        CPUId = self.str2Hex("CPU-12345678")                                       #cpuId
        GSMType = self.GBKString2Hex("GSM-TYPE-123456")                            #GSM型号
        GSM_IMEI = self.GBKString2Hex("GSM_IMEI_123456")                           #GSM IMEI 号
        SIM_IMSI = self.GBKString2Hex("SIM_13146201119")                           #终端 SIM 卡 IMSI 号
        SIM_ICCID = self.GBKString2Hex("SIM_ICCID13146201119")                     #终端 SIM 卡 ICCID 号
        carType = self.int2hexStringByBytes(22,2)                                  #车系车型 ID
        VIN = self.GBKString2Hex("VIN_1234567891234")                              #汽车 VIN 码
        totalMileage = self.int2hexStringByBytes(389000,4)                         #装上终端后车辆累计总里程或车辆仪表里程（单位米）
        totalOilExpend = self.int2hexStringByBytes(420000,4)                       #装上终端后车辆累计总耗油量（ml）
        displacement = self.int2hexStringByBytes(1500,2)                           #排量
        oilDensity = self.int2hexStringByBytes(92,2)                               #油品密度
        OBDSerial = "0101"                                                         #OBD协议编号
        oilCalculateType = "01"                                                    #油耗计算方式


        msg = msg + softwareVersion + softwareVersionDate + CPUId + GSMType + GSM_IMEI
        msg = msg + SIM_IMSI + SIM_ICCID + carType + VIN + totalMileage
        msg = msg + totalOilExpend + displacement + oilDensity + OBDSerial + oilCalculateType
        return msg

    # 生成一条完整的消息，针对图形界面，可传递参数
    def getMsgBody_GUI(self,softwareVersion="L200AB01020002",softwareVersionDate="2020-02-10",CPUId="CPU-12345678",GMSType="GMS-TYPE-123456",\
                   GMS_IMEI="GMS_IMEI_123456",SIM_IMSI="SIM_13146201119",SIM_ICCID="SIM_ICCID13146201119",carType=22,VIN="VIN_1234567891234",\
                   totalMileage=389000,totalOilExpend=420000,displacement=1500,oilDensity=92,OBDSerial=257,oilCalculateType="01"):
        msg = ""
        softwareVersion = self.GBKString2Hex(softwareVersion)                              #软件版本号
        softwareVersionDate = self.GBKString2Hex(softwareVersionDate)                      #终端版本日期
        CPUId = self.str2Hex(CPUId)                                                        #cpuId
        GMSType = self.GBKString2Hex(GMSType)                                              #GMS型号
        GMS_IMEI = self.GBKString2Hex(GMS_IMEI)                                            #GSM IMEI 号
        SIM_IMSI = self.GBKString2Hex(SIM_IMSI)                                            #终端 SIM 卡 IMSI 号
        SIM_ICCID = self.GBKString2Hex(SIM_ICCID)                                          #终端 SIM 卡 ICCID 号
        carType = self.int2hexStringByBytes(carType,2)                                     #车系车型 ID
        VIN = self.GBKString2Hex(VIN)                                                      #汽车 VIN 码
        totalMileage = self.int2hexStringByBytes(totalMileage,4)                           #装上终端后车辆累计总里程或车辆仪表里程（单位米）
        totalOilExpend = self.int2hexStringByBytes(totalOilExpend,4)                       #装上终端后车辆累计总耗油量（ml）
        displacement = self.int2hexStringByBytes(displacement,2)                           #排量
        oilDensity = self.int2hexStringByBytes(oilDensity,2)                               #油密度
        OBDSerial = self.int2hexStringByBytes(OBDSerial,2)                                 #OBD协议编号
        oilCalculateType = oilCalculateType                                                #油耗计算方式

        msg = msg + softwareVersion + softwareVersionDate + CPUId + GMSType + GMS_IMEI
        msg = msg + SIM_IMSI + SIM_ICCID + carType + VIN + totalMileage
        msg = msg + totalOilExpend + displacement + oilDensity + OBDSerial + oilCalculateType
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0205"
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(msgBodyLen=int(len(self.getMsgBody()) / 2),subPkg=subPkg)  #消息体属性
        phoneNum = self.int2BCD(13146201119)                     #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                           #消息流水号
        if subPkg != 8192:
            subPkgContent = ""                                       #消息包封装项
        else:
            subPkgContent = self.getMsgPackage()
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息体属性
    def getMsgBodyProperty(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex


if __name__ == "__main__":
    pass