# coding:utf-8

'''
定义一个Sensor 采样协议的类
'''
from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.ProtocolBase import ProtocolBase


class SensorSampling_protocol(ProtocolBase):
    testData = {"time":"2020-05-15 14:42:24","dataType":"01","data":{}}
    def __init__(self, WATER_CODE=1000, DEV_ID="M121501010001",data={"time":"2020-05-15 14:42:24","dataType":"01","data":{}}):
        super().__init__()
        self.WATER_CODE = int(WATER_CODE)                            # 设置默认消息流水号
        self.DEV_ID = DEV_ID                                         # 设置默认设备id

        self.time = data["time"]                                              # 时间
        self.dataType = data["dataType"]                                       # 采样数据类型

    #####################################################
    #               生成 采样数据 消息
    #####################################################
    def generateMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                     #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                     #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                          #设备id
        FUN_ID = "0031"                                                     # 功能id
        data = ""                                                           #数据段
        data += self.generateData()
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data)/2))      # 消息长度
        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)                                # 校验字段
        info += CHECK_CODE
        return info

    #####################################################
    #               创建 车机采样 数据段
    #####################################################
    def generateData(self):
        timeHex = self.getUTCTime(self.time)
        dataTypeHex = self.dataType
        dataContentHex = self.getMicroCollisionData()
        dataLenHex = self.int2hexStringByBytes(int(len(dataContentHex) / 2),2)
        data = timeHex + dataTypeHex + dataLenHex + dataContentHex
        return data

    #####################################################
    #               获取微碰撞数据包
    #####################################################
    def getMicroCollisionData(self,totalConut=2,dataType=1):
        totalConutHex = self.int2hexStringByBytes(totalConut,2)            #历史碰撞总次数
        dataTypeHex = self.int2hexStringByBytes(dataType)
        # 1：表示事件发生时刻，前5秒的事件采样数据；
        # [微碰撞前后5秒附带数据]
        # 2：表示事件发生时刻，后5秒的事件采样数据；
        # [微碰撞前后5秒附带数据]
        # 3：表示事件发生时刻，后120秒的速度采样数据；
        # [碰撞报警后120秒采样数据附带信息]
        data = totalConutHex + dataTypeHex
        if dataType == 1 or dataType == 2:
            GPSSampleData = self.GPSDataFromSeconds(5)                                   # GPS 采样点 ，5秒内的GPS采样数据,85个字节
            CANSampleData = self.CANDataFromSeconds(5)                                   # CAN采样点 ，5秒内的CAN采样数据，90个字节
            SENSORSampleData1 = self.SENSORDataFromSeconds(10)                           # SENSOR采样点 ，10秒内的SENSOR采样数据
            collisonFBSampleData_50 = self.collisonFBSampleData(20)                      #碰撞时刻前后50毫秒内的SENSOR采样数据
            collisonFBSampleData_100 = self.collisonFBSampleData(40)                     # 碰撞时刻前后100毫秒内的SENSOR采样数据
            collisonFBSampleData_125 = self.collisonFBSampleData_xyz(50)                 #碰撞时刻前后125毫秒内的SENSOR采样数据
            data = data + GPSSampleData + CANSampleData + SENSORSampleData1 + collisonFBSampleData_50 + collisonFBSampleData_100 + collisonFBSampleData_125
        else:
            pass
        return data

    #####################################################
    # 秒内的GPS采样数据
    #####################################################
    def GPSDataFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.GPSSamplingData()
        return data

    #####################################################
    # N秒内的CAN采样数据
    #####################################################
    def CANDataFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.CANSamplingData()
        return data

    #####################################################
    #23 GPS采样数据项
    #####################################################
    def GPSSamplingData(self):
        latitude = 40.22077                                                    #纬度
        longitude = 116.23128                                                  #经度
        speed = 60.9                                                           #速度
        directionAngle = 80.8                                                  #方向角
        elevation = 2999.9                                                     #海拔
        statusBit = 1                                                          #状态位，Bit7：当前定位是否有效，0-无效，1-有效，其它Bit位预留
        latitude = GPSReport_protocol().getLatitude(latitude)
        longitude = GPSReport_protocol().getLongitude(longitude)
        speed = GPSReport_protocol().getSpeed(speed)
        directionAngle = GPSReport_protocol().getDirectionAngle(directionAngle)
        elevation = GPSReport_protocol().geteElevation(elevation)
        statusBit = GPSReport_protocol().getStatusBit(statusBit)
        data = latitude + longitude + speed + directionAngle + elevation + statusBit
        return data

    #####################################################
    #加速度CAN数据项
    #####################################################
    def CANSamplingData(self):
        speed =  65                                                              #车速
        enginSpeed =  1000                                                         #发动机转速
        brakingStatus = 0                                                       #刹车状态：1-刹车，0-未刹车，2-不支持；
        acceleratorLocation =  50                                                #油门踏板位置
        airDamper = 17                                                         #节气门开度
        troubleCount = 2                                                       #故障码个数
        speed = self.int2hexStringByBytes(speed,1)
        enginSpeed = self.int2hexStringByBytes(enginSpeed,2)
        brakingStatus = self.int2hexStringByBytes(brakingStatus,1)
        acceleratorLocation = self.int2hexStringByBytes(acceleratorLocation,2)
        airDamper = self.int2hexStringByBytes(airDamper,2)
        troubleCount = self.int2hexStringByBytes(troubleCount,1)
        data = speed + enginSpeed + brakingStatus + acceleratorLocation + airDamper + troubleCount
        return data

    #####################################################
    # N秒内的SENSOR采样数据
    #####################################################
    def SENSORDataFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.int2hexStringByBytes(30,2)              #第N秒内的第1个0.5秒内的平均加速度值
        return data

    #####################################################
    # 碰撞时刻前后N毫秒内的SENSOR采样数据
    #####################################################
    def collisonFBSampleData(self,counts):
        data = ""
        for i in range(0, counts):
            data += self.int2hexStringByBytes(30, 2)        # 第N个2.5毫秒采样点的采样加速度值
        return data

    #####################################################
    # 碰撞时刻前后N毫秒内的SENSOR采样数据 (xyz)
    #####################################################
    def collisonFBSampleData_xyz(self,counts):
        data = ""
        for i in range(0, counts):
            data += self.int2hexStringByBytes(20, 2)       # 第N个2.5毫秒采样点的x轴加速度值
            data += self.int2hexStringByBytes(30, 2)       # 第N个2.5毫秒采样点的y轴加速度值
            data += self.int2hexStringByBytes(2, 2)      # 第N个2.5毫秒采样点的z轴加速度值
        return data

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

if __name__ == "__main__":
    print(SensorSampling_protocol().generateMsg())
