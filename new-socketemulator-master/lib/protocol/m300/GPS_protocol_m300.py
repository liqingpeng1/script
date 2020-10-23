#encoding:utf-8

from lib.protocol.m300.M300Base import M300Base

'''
定义心跳议类
'''

class GPS_protocol_m300(M300Base):
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0,dateInfo="2020-03-27 14:34:22",latitude=40.22077,longitude=116.23128 \
                 ,positionStar=2,speed=66.0,direction=55.3,altitude=11.0,ACCStatus=0,valtage=36.0,OBDSpeed=66.4,valid=129 \
                 ,tripMark=0):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.waterCode = waterCode                    #消息流水号
        self.DEV_ID = DEV_ID                          #设备Id
        self.encryptionType = encryptionType          # 消息属性里面的是否加密字段

        self.dateInfo = dateInfo                      #日期
        self.latitude = latitude                      #维度
        self.longitude = longitude                    #经度
        self.positionStar = positionStar              #定位星数
        self.speed = speed                            #速度
        self.direction = direction                    #方向角
        self.altitude = altitude                      #海拔高度
        self.ACCStatus = ACCStatus                    #ACC状态
        self.valtage = valtage                        #汽车电瓶电压
        self.OBDSpeed = OBDSpeed                      #汽车OBD速度
        self.valid = valid                            #GPS定位是否有效
        self.tripMark = tripMark                      #驾驶循环标签
        self.reserve = "0000000000"                   #保留字段                   #设备Id

    def setLatitude(self,data):
        self.latitude = data
    def setLongitude(self,data):
        self.longitude = data
    def setDirection(self,data):
        self.direction = data
    def setDateInfo(self,data):
        self.dateInfo = data




    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0020"                                                   #功能id
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
        dateInfo = self.getDateInfo(self.dateInfo)                                      #日期
        latitude = self.int2hexStringByBytes(int(self.latitude * 1000000),4)            #维度
        longitude = self.int2hexStringByBytes(int(self.longitude * 1000000),4)          #经度
        positionStar = self.int2hexStringByBytes(self.positionStar)                     #定位星数
        speed = self.int2hexStringByBytes(int(self.speed * 10),2)                       #速度
        direction = self.int2hexStringByBytes(int(self.direction * 10),2)               #方向角
        altitude = self.int2hexStringByBytes(int(self.altitude * 10),4)                 #海拔高度
        ACCStatus = self.int2hexStringByBytes(self.ACCStatus)                           #ACC状态
        valtage = self.int2hexStringByBytes(int(self.valtage * 10),2)                   #汽车电瓶电压
        OBDSpeed = self.int2hexStringByBytes(int(self.OBDSpeed * 10),2)                 #汽车OBD速度
        # valid = self.getValid()                                                         #GPS定位是否有效
        valid = self.int2hexStringByBytes(self.valid)                                   # GPS定位是否有效
        tripMark = self.int2hexStringByBytes(self.tripMark,2)                           #驾驶循环标签
        reserve = self.reserve                                                          #保留字段
        data = dateInfo + latitude + longitude + positionStar + speed
        data = data + direction + altitude + ACCStatus + valtage + OBDSpeed
        data = data + valid + tripMark + reserve
        return data

    #获取时间信息
    def getDateInfo(self,data):
        year = self.int2hexStringByBytes(int(data[2:4]))
        month = self.int2hexStringByBytes(int(data[5:7]))
        day = self.int2hexStringByBytes(int(data[8:10]))
        hour = self.int2hexStringByBytes(int(data[11:13]))
        miniute = self.int2hexStringByBytes(int(data[14:16]))
        seconds = self.int2hexStringByBytes(int(data[17:]))
        dataHex = year + month + day + hour + miniute + seconds
        return dataHex

    def getValid(self):
        isGPSValid = 1              #Gps是否当前定位有效数据  1/0  是/否
        isFixMod = 0                #车机是否处于修车模式      128/0  是/否
        data = isGPSValid + isFixMod
        dataHex = self.int2hexStringByBytes(data)
        return dataHex

if __name__ == "__main__":
    print(GPS_protocol_m300().generateMsg())
    print(GPS_protocol_m300().getMsgBody())
