#coding:utf-8

'''
定义一个GPS协议的类
'''
import datetime

from lib.util import dataUtil
from lib.protocol.report.ProtocolBase import ProtocolBase

'''
终端上报GPS定位数据包
'''
class GPSReport_protocol(ProtocolBase):

    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",UTCTime="2020-01-09 18:19:38",latitude=40.22077,longitude=116.23128,speed=60,directionAngle=80.8,elevation=2999.9,positionStar=3,Pdop=0.3,Hdop=0.4,Vdop=0.5,statusBit=9,valtage=36.9,OBDSpeed=60.9,engineSpeed=3000,GPSTotalMileage=12800,totalOil=100000,totalTime=2020002,GPSTimestamp=1578565178):
        super().__init__()
        self.msgCount = int(msgCount)  # 设置默认要发送的GPS数据包个数

        self.WATER_CODE = int(WATER_CODE);  # 设置默认消息流水号
        self.DEV_ID = DEV_ID  # 设置默认设备id

        self.UTCTime = UTCTime  # 设置默认UTC时间
        self.latitude = float(latitude)  # 设置默认纬度
        self.longitude = float(longitude)  # 设置默认经度
        self.speed = float(speed)  # 设置默认速度
        self.directionAngle = float(directionAngle)  # 设置默认方向角
        self.elevation = float(elevation)  # 设置默认海拔
        self.positionStar = int(positionStar)  # 设置默认定位星数
        self.Pdop = float(Pdop)
        self.Hdop = float(Hdop)
        self.Vdop = float(Vdop)
        self.statusBit = int(statusBit)  # 设置默认状态字节
        self.valtage = float(valtage)  # 设置默认电压值
        self.OBDSpeed = float(OBDSpeed)  # 设置默认OBD车速
        self.engineSpeed = int(engineSpeed)  # 设置默认发动机转速
        self.GPSTotalMileage = int(GPSTotalMileage)  # 设置默认GPS累计里程
        self.totalOil = int(totalOil)  # 设置默认累计油耗
        self.totalTime = int(totalTime)  # 设置默认累计行驶时间
        self.GPSTimestamp = int(GPSTimestamp)  # 设置默认GPS信息时间戳

        # self.msgCount = 1                           #设置默认要发送的GPS数据包个数
        #
        # self.WATER_CODE = 1000;                     #设置默认消息流水号
        # self.DEV_ID = "M121501010001"               #设置默认设备id
        #
        # self.UTCTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    #设置默认UTC时间
        # self.latitude = 40.22077                    #设置默认纬度
        # self.longitude = 116.23128                  #设置默认经度
        # self.speed = 60.9                           #设置默认速度
        # self.directionAngle = 80.8                  #设置默认方向角
        # self.elevation = 2999.9                     #设置默认海拔
        # self.positionStar = 3                       #设置默认定位星数
        # self.Pdop = 0.3
        # self.Hdop = 0.4
        # self.Vdop = 0.5
        # self.statusBit = 175                       #设置默认状态字节
        # self.valtage = 36.9                        #设置默认电压值
        # self.OBDSpeed = 60.9                       #设置默认OBD车速
        # self.engineSpeed = 3000                    #设置默认发动机转速
        # self.GPSTotalMileage = 12800               #设置默认GPS累计里程
        # self.totalOil = 100000                     #设置默认累计油耗
        # self.totalTime = 2020002                   #设置默认累计行驶时间
        # self.GPSTimestamp = int(time.time())       #设置默认GPS信息时间戳


    #####################################################
    #               生成GPS消息
    #####################################################
    def generateGpsMsg(self):
        self.getProtocalHeader()
        info = ""
        #消息头
        HEADER = "4040"
        #消息流水号
        WATER_CODE = self.getWaterCode(self.WATER_CODE)
        #设备id
        DEV_ID = self.devid2hexString(self.DEV_ID)
        # 功能id(GPS功能id)
        FUN_ID = "0010"
        #数据段
        data = ""
        for i in range(0,self.msgCount):
            data += self.generateGpsPkg(self.generateGpsData())
        # 消息长度
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data)/2))

        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        # 校验字段
        CHECK_CODE = self.getCheckCode(info)
        info += CHECK_CODE
        # print("header:" +HEADER)
        # print("length:" + LENGTH)
        # print("water:" + WATER_CODE)
        # print("devid:" + DEV_ID)
        # print("funid:" + FUN_ID)
        # print("msg:" + info)
        return info

    #####################################################
    #               创建GPS数据包，包含包个数
    #               data:传入GPS数据包的多条数据段
    #####################################################
    def generateGpsPkg(self,data):
        pkgLen = len(data)
        pkgNum = (pkgLen / 2)/49
        pkgNumHex = self.int2hexString(int(pkgNum))
        pkg = pkgNumHex + data
        return pkg

    #####################################################
    #               创建GPS数据段
    #####################################################
    def generateGpsData(self):
        data = ""
        #UTC时间
        # UTCTime = self.getUTCTime("2020-01-03 13:05:13")
        UTCTime = self.getUTCTime(self.UTCTime)
        #纬度
        latitude = self.getLatitude(self.latitude)
        #经度
        longitude = self.getLongitude(self.longitude)
        #速度
        speed = self.getSpeed(self.speed)
        #方向角
        directionAngle = self.getDirectionAngle(self.directionAngle)
        #海拔
        elevation = self.geteElevation(self.elevation)
        #定字节星数
        positionStar = self.getPositionStar(self.positionStar)
        Pdop = self.getPdop(self.Pdop)
        Hdop = self.getHdop(self.Hdop)
        Vdop = self.getVdop(self.Vdop)
        #状态字节
        statusBit = self.getStatusBit(self.statusBit)
        #电压
        valtage = self.getValtage(self.valtage)
        #OBD车速
        OBDSpeed = self.getOBDSpeed(self.OBDSpeed)
        #发动机转速
        engineSpeed = self.getEngineSpeed(self.engineSpeed)
        #GPS累计里程
        GPSTotalMileage = self.getGPSTotalMileage(self.GPSTotalMileage)
        #累计油耗
        totalOil = self.getTotalOil(self.totalOil)
        #累计行驶时间
        totalTime = self.getTotalTime(self.totalTime)
        #GPS信息时间戳
        GPSTimestamp = self.getGPSTimestamp(self.GPSTimestamp)
        data = UTCTime + latitude + longitude + speed + directionAngle
        data = data + elevation + positionStar + Pdop + Hdop + Vdop
        data = data + statusBit + valtage + OBDSpeed + engineSpeed +GPSTotalMileage
        data = data + totalOil + totalTime + GPSTimestamp

        return data

    #####################################################
    #               数字转换为16进制字符串
    #####################################################
    def int2hexString(self,num):
        hexStr = hex(num)[2:]
        if (len(hexStr) % 2) == 1:
            hexStr = "0" + hexStr
        return hexStr


    #####################################################
    #               获取消息体长度
    #####################################################
    def getMsgLength(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取功能id
    #####################################################
    def getFunId(self,num):
        hexData = "0010"
        return hexData

    #####################################################
    #               获取校验码
    #####################################################
    def getCheckCode(self,data):
        return dataUtil.crc16(data)

    #####################################################
    #               将UTC时间转换为16进制，
    #        例如：2020-01-02   20:30:00 （年取后面2字节）则将20,01，02,20,30,00 转换为对应的6个字节
    #        theTime:传入一个类似：2020-01-03 13:05:13的一个字符串
    #####################################################
    def getUTCTime(self,theTime):
        # 获取当前时间，时间格式为：2020-01-03 13:05:13
        # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 将2020-01-03 13:05:13时间格式转换为一个数组
        # timeStr = "2020-01-03 13:05:13"
        timeStr = theTime
        timeArr = []
        timeArr.append(timeStr[2:4])
        timeArr.append(timeStr[5:7])
        timeArr.append(timeStr[8:11])
        timeArr.append(timeStr[11:13])
        timeArr.append(timeStr[14:16])
        timeArr.append(timeStr[17:19])
        UTCTime = ""
        for i in range(0, len(timeArr)):
            UTCTime += self.int2hexString(int(timeArr[i]))
        return UTCTime

    #####################################################
    #               获取一个纬度，并转换为4个字节的16进制，例如（40.22077）
    #               latitude: float 类型的纬度数据
    #####################################################
    def getLatitude(self,latitude):
        latitudeStr = str(latitude)
        latitudeStr = latitudeStr.replace(".", "")  # 去掉纬度小数点
        #纬度去掉小数点后可能之后7位，所以在后面补了一个0到8位
        while(len(latitudeStr) < 8):
            latitudeStr += "0"
        latitudeHex = hex(int(latitudeStr))
        latitudeHex = self.leftPad(str(latitudeHex)[2:], 8)
        return latitudeHex

    #####################################################
    #               获取一个经度，并转换为4个字节的16进制，例如（40.22077）
    #               latitude: float 类型的纬度数据
    #####################################################
    def getLongitude(self, num):
        longitudeStr = str(num)
        longitudeArr = longitudeStr.replace(".", "")  # 去掉经度小数点
        # 经度要求要有9位数，所以少于9位数的时候，在后面补0
        while (len(longitudeArr) < 9):
            longitudeArr += "0"
        longitudeHex = hex(int(longitudeArr))
        longitudeHex = self.leftPad(str(longitudeHex)[2:], 8)
        return longitudeHex

    #####################################################
    #               获取速度，并转换为2个字节的16进制
    #####################################################
    def getSpeed(self,num):
        speedStr = str(num)
        speedStr = speedStr.replace(".", "")  # 去掉经度小数点
        speedHex = hex(int(speedStr))
        speedHex = self.leftPad(str(speedHex)[2:], 4)
        return speedHex

    #####################################################
    #               获取方向角度（角度精确到0.1度）
    #               方向角的的传入值应该为x.x
    #               方向角2个字节表示
    #####################################################
    def getDirectionAngle(self,num):
        # angleStr = str(num)
        # angleStr = angleStr.replace(".", "")
        # angleHex = hex(int(angleStr))
        # angleHex = self.leftPad(str(angleHex)[2:], 4)
        angleHex = self.int2hexStringByBytes(int(num * 10),2)
        return angleHex

    #####################################################
    #               获取海拔（精确到0.1米）
    #               方向角的的传入值应该为x.x
    #                4个字节表示
    #####################################################
    def geteElevation(self,num):
        elevationStr = str(num)
        elevationStr = elevationStr.replace(".", "")  # 去掉经度小数点
        while (len(elevationStr) < 8):
            elevationStr = "0" + elevationStr
        elevationHex = hex(int(elevationStr))
        elevationHex = self.leftPad(str(elevationHex)[2:], 8)
        return elevationHex

    #####################################################
    #               获取定字节星数，1字节表示
    #####################################################
    def getPositionStar(self,num):
        # positionStarHex = self.int2hexString(num)   #该方法同下
        positionStarHex = hex(num)
        positionStarHex = self.leftPad(str(positionStarHex)[2:], 2)
        return positionStarHex

    #####################################################
    #      Pdop：传输数值为原始值乘以10（即放大10倍，精度0.1），1字节表示
    #####################################################
    def getPdop(self,num):
        pdopHex = self.int2hexString(int(num * 10))
        return pdopHex

    #####################################################
    #      Hdop：传输数值为原始值乘以10（即放大10倍，精度0.1），1字节表示
    #####################################################
    def getHdop(self, num):
        hdopHex = self.int2hexString(int(num * 10))
        return hdopHex

    #####################################################
    #      Hdop：传输数值为原始值乘以10（即放大10倍，精度0.1），1字节表示
    #####################################################
    def getVdop(self, num):
        vdopHex = self.int2hexString(int(num * 10))
        return vdopHex

    #####################################################
    #      获取状态字节16进制，状态字节1字节表示
    #      Bit7：GPS当前定位是否有效，0-无效，1-有效；
    #      Bit6-4：指示当前定位模式：
    #     0：自动模式；1：单GPS模式；2：单BDS模式；
    #     3：GPS+BDS双模式；其它预留；
    #     Bit3-2：定位类型；
    #     0~1：预留；2：2D定位；3：3D定位；
    #     Bit1：当前统计里程模式：
    #     0-GPS统计里程；1-OBD统计里程；
    #     Bit0：指示当前车辆点熄火状态：0-熄火，1-点火
    #####################################################
    def getStatusBit(self,num):
        fireStatus = 1      #点火状态，1表示点火，0表示熄火
        mileageWay = 0       #0里程统计模式，0表示GPS里程，4表示OBD里程
        locationWay = 8     #定位类型，8表示2D定位，12表示3D定位
        locationMode = 0        #定位模式，0表示自动模式，16表示单GPS模式，32表示单BDS模式，48表示GPS+BDS双模式
        isLocationValid = 128   #当前定位是否有效，128表示有效，0表示无效
        # num = fireStatus + mileageWay + locationWay + locationMode + isLocationValid
        statusbitHex = self.int2hexString(num)
        return statusbitHex

    #####################################################
    #      获取电压16进制值，2字节表示
    #####################################################
    def getValtage(self,num):
        valtageHex = self.int2hexStringByBytes(int(num *100),2)
        return valtageHex

    #####################################################
    #      获取OBD车速，2字节表示
    #####################################################
    def getOBDSpeed(self,num):
        OBDSpeedStr = str(num)
        OBDSpeedStr = OBDSpeedStr.replace(".", "")
        while (len(OBDSpeedStr) < 4):
            OBDSpeedStr = "0" + OBDSpeedStr
        OBDSpeedHex = hex(int(OBDSpeedStr))
        OBDSpeedHex = self.leftPad(str(OBDSpeedHex)[2:], 4)
        return OBDSpeedHex

    #####################################################
    #      获取发动机转速，2字节表示
    #####################################################
    def getEngineSpeed(self,num):
        engineSpeedStr = str(num)
        # engineSpeedStr = engineSpeedStr.replace(".", "")
        while (len(engineSpeedStr) < 4):
            engineSpeedStr = "0" + engineSpeedStr
        engineSpeedHex = hex(int(engineSpeedStr))
        engineSpeedHex = self.leftPad(str(engineSpeedHex)[2:], 4)
        return engineSpeedHex

    #####################################################
    #      获取GPS累计里程，4字节表示
    #####################################################
    def getGPSTotalMileage(self,num):
        GPSTotalMileageStr = str(num)
        # GPSTotalMileageStr = GPSTotalMileageStr.replace(".", "")
        while (len(GPSTotalMileageStr) < 8):
            GPSTotalMileageStr = "0" + GPSTotalMileageStr
        GPSTotalMileageHex = hex(int(GPSTotalMileageStr))
        GPSTotalMileageHex = self.leftPad(str(GPSTotalMileageHex)[2:], 8)
        return GPSTotalMileageHex

    #####################################################
    #      获取总油耗，4字节表示
    #####################################################
    def getTotalOil(self,num):
        totalOilStr = str(num)
        totalOilHex = hex(int(totalOilStr))
        totalOilHex = self.leftPad(str(totalOilHex)[2:], 8)
        return totalOilHex
        #以下算法同上面的算法值一样
        # hexData = self.int2hexString(num)
        # while len(hexData) < 8:
        #     hexData = "0" + hexData
        # return hexData

    #####################################################
    #      获取总行驶时间（秒），4字节表示
    #####################################################
    def getTotalTime(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #      获取GPS信息时间戳，4字节表示
    #####################################################
    def getGPSTimestamp(self,num):
        GPSTimestampHex = self.int2hexString(num)
        while len(GPSTimestampHex) < 8:
            GPSTimestampHex = "0" + GPSTimestampHex
        return GPSTimestampHex

    # 设置要发送的GPS数据包个数
    def setMsgCount(self,msgCount):
        self.msgCount = int(msgCount)

    # 设置消息流水号
    def setWATER_CODE(self,WATER_CODE ):
        self.WATER_CODE  = int(WATER_CODE)

    # 设置设备id
    def setDEV_ID(self,DEV_ID):
        self.DEV_ID = DEV_ID

    # 设置UTC时间
    def setUTCTime(self,UTCTime):
        self.UTCTime = UTCTime

    # 设置纬度
    def setLatitude(self,latitude):
        self.latitude = float(latitude)

    # 设置经度
    def setLongitude(self,longitude):
        self.longitude = float(longitude)

    # 设置速度
    def setSpeed(self,speed):
        self.speed = float(speed)

    # 设置方向角
    def setDirectionAngle(self,directionAngle):
        self.directionAngle = float(directionAngle)

    # 设置海拔
    def setElevation(self,elevation):
        self.elevation = float(elevation)

    # 设置定位星数
    def setPositionStar(self,positionStar):
        self.positionStar = int(positionStar)

    def setPdop(self,Pdop):
        self.Pdop = float(Pdop)

    def setHdop(self,Hdop):
        self.Hdop = float(Hdop)

    def setVdop(self,Vdop):
        self.Vdop = float(Vdop)

    # 设置状态字节
    def setStatusBit(self,statusBit):
        self.statusBit = int(statusBit)
    # 设置Gps 有效或者无效；0：无效     1：有效
    def setGpsValid(self,data):
        if data == 1:
            self.statusBit = self.statusBit | 1 << 7
        elif data == 0:
            self.statusBit = self.statusBit & ~(1 << 7)


    # 设置电压值
    def setValtage(self,valtage):
        self.valtage = float(valtage)

    # 设置OBD车速
    def setOBDSpeed(self,OBDSpeed):
        self.OBDSpeed = float(OBDSpeed)

    # 设置发动机转速
    def setEngineSpeed(self,engineSpeed):
        self.engineSpeed = int(engineSpeed)

    # 设置GPS累计里程
    def setGPSTotalMileage(self,GPSTotalMileage):
        self.GPSTotalMileage = int(GPSTotalMileage)

    #设置累计油耗
    def setTotalOil(self,totalOil):
        self.totalOil = int(totalOil)

    # 设置累计行驶时间
    def setTotalTime(self,totalTime):
        self.totalTime = int(totalTime)

    # 设置GPS信息时间戳
    def setGPSTimestamp(self,GPSTimestamp):
        self.GPSTimestamp = int(GPSTimestamp)

if __name__ == "__main__":
    GPSReport_protocol().generateGpsMsg()
    # Gps_protocol().getLatitude(40.22077)
    # print(Gps_protocol().getHexTime())
    print(GPSReport_protocol().getUTCTime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.datetime.now())
    # Gps_protocol().generateGpsData()
    # Gps_protocol().getLatitude(40.22077)
    # Gps_protocol().getLongitude(116.23128)
    # Gps_protocol().getDirectionAngle(0.5)
    # Gps_protocol().geteElevation(2999.9)
    # Gps_protocol().getOBDSpeed(10.1)