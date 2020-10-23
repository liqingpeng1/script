#coding:utf-8
import datetime

from lib.protocol.report.ProtocolBase import ProtocolBase
from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.SecurityStatusReport_protocol import SecurityStatusReport_protocol


class EventClass(ProtocolBase):
    def __init__(self):
        self.GPSPkg = "1401091213260265b86206ed8c70026103280000752f03030405af017102610bb800003200000186a0001ed2a25e16fe3a"
        self.BaseStationPkg = "1401140a0c050207e407e607e807ea07ec4eea4eec4eee4ef04efc4efe4f004f024f040024025e07d00007a125000927c60000ea610100"
        self.securityData  = ""

    def setGPSpkg(self,data):
        self.GPSPkg = data
    def setSecurityData(self,data):
        self.securityData = data

    # 0001 终端插入报警附带信息
    def terminalInsertionAlarmExtraInfo(self,theTime=""):
        if theTime != "":
            return self.getUTCTimeHex(theTime)
        else:
            return self.getUTCTimeHex(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 0002 终端拔出报警附带信息
    def terminalPulloutAlarmExtraInfo(self,theTime=""):
        if theTime != "":
            return self.getUTCTimeHex(theTime)
        else:
            return self.getUTCTimeHex(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 000F 预点火事件附带信息
    def preFiringExtraInfo(self):
        bit0 = 1                   #1：有点火电压波形,0：无点火电压波形
        bit1 = 2                   #2：有电压和噪声点火，0：无电压和噪声点火
        bit2 = 4                   #3：有gps车速和噪声点火，0：无gps车速和噪声点火
        data = bit0 + bit1 + bit2
        return self.int2hexString(data)

    # 0010 点火事件附带信息
    def fireExtraInfo(self,allRapidlyAccelerateCount=15,allSharpSlowdownCount=15,allSharpTurn=15):
        allRapidlyAccelerateCount = self.int2hexStringByBytes(allRapidlyAccelerateCount, 2)                     # 急加速总次数
        allSharpSlowdownCount = self.int2hexStringByBytes(allSharpSlowdownCount, 2)                         # 急减速总次数
        allSharpTurn = self.int2hexStringByBytes(allSharpTurn, 2)                                  # 急转弯总次数
        securityObj = SecurityStatusReport_protocol()
        securityObj.setGPSPkg(self.GPSPkg)
        securityData = ""
        if self.securityData == "":
            securityData = securityObj.generateSecurityStatusData()                      # 安防数据
        else:
            securityData = self.securityData
        data = allRapidlyAccelerateCount + allSharpSlowdownCount + allSharpTurn + securityData
        return data

    # 0011  熄火事件附带信息
    def misFireExtraInfo(self,allRapidlyAccelerateCount=15,allSharpSlowdownCount=15,allSharpTurn=15):
        allRapidlyAccelerateCount = self.int2hexStringByBytes(allRapidlyAccelerateCount,2)                       #急加速总次数
        allSharpSlowdownCount = self.int2hexStringByBytes(allSharpSlowdownCount,2)                           #急减速总次数
        allSharpTurn = self.int2hexStringByBytes(allSharpTurn,2)                                     #急转弯总次数
        securityObj = SecurityStatusReport_protocol()
        securityObj.setGPSPkg(self.GPSPkg)
        securityData = ""
        if self.securityData == "":
            securityData = securityObj.generateSecurityStatusData()                        # 安防数据
        else:
            securityData = self.securityData
        data =  allRapidlyAccelerateCount + allSharpSlowdownCount + allSharpTurn + securityData
        return data

    # 0012 设防事件附带信息
    def setUpDefencesExtraInfo(self):
        securityObj = SecurityStatusReport_protocol()
        securityObj.setGPSPkg(self.GPSPkg)
        securityData = ""
        if self.securityData == "":
            securityData = securityObj.generateSecurityStatusData()  # 安防数据
        else:
            securityData = self.securityData
        return securityData

    # 0013 撤防事件附带信息
    def setDownDefencesExtraInfo(self):
        securityObj = SecurityStatusReport_protocol()
        securityObj.setGPSPkg(self.GPSPkg)
        securityData = ""
        if self.securityData == "":
            securityData = securityObj.generateSecurityStatusData()  # 安防数据
        else:
            securityData = self.securityData
        return securityData
        return securityData

    # 0014 锁车未成功事件附带信息
    def lockCarFaillExtraInfo(self):
        securityData = SecurityStatusReport_protocol.generateSecurityStatusData()           # 安防数据
        return securityData

    # 0015 超时未设防事件附带信息
    def noDefencesWithTimeoutExtraInfo(self):
        securityData = SecurityStatusReport_protocol.generateSecurityStatusData()           # 安防数据
        return securityData

    # 0016 设防玻璃未关事件附带信息
    def defencesGlassNoCloseExtraInfo(self):
        securityData = SecurityStatusReport_protocol.generateSecurityStatusData()           # 安防数据
        return securityData

    # 0017 设防非法开门事件附带信息
    def defencesIllegalCloseDoorExtraInfo(self):
        securityData = SecurityStatusReport_protocol.generateSecurityStatusData()           # 安防数据
        return securityData

    # 0018 设防非法点火事件附带信息
    def defencesIllegalFireExtraInfo(self):
        securityData = SecurityStatusReport_protocol.generateSecurityStatusData()  # 安防数据
        return securityData

    #0019 SOS报警事件附加信息
    def SOSAlarmEtraInfo(self,theTime):
        if theTime != "":
            return self.getUTCTimeHex(theTime)
        else:
            return self.getUTCTimeHex(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #001A   001B 充电事件附带信息
    def chargeEtraInfo(self):
        SOC = self.int2hexString(0.3 * 100)                #乘以100上传，平台除以100处理(显示小于1的小数值)
        SOH = self.int2hexString(4 * 100)                  #乘以100上传，平台除以100处理
        voltage = self.int2hexStringByBytes(3.6 * 10,2)    #乘以10上传，平台除以10处理
        chargeEventCode = self.int2hexString(3)            #充电开始报警，和后续的充电结束报警为同一编号
        data =  SOC + SOH + voltage + chargeEventCode
        return data

    # 0020 急加速报警附带信息
    def rapidlyAccelerateExtraInfo(self,totalRapidlyAccelerateCount=100,totalSharpSlowdown=200,totalSharpTurn=50,dataProperty=2):
        totalRapidlyAccelerateCount = totalRapidlyAccelerateCount                         #急加速总次数
        totalSharpSlowdown = totalSharpSlowdown                                           #急减速总次数
        totalSharpTurn = totalSharpTurn                                                   #急转弯总次数
        dataProperty = dataProperty                                                       #事件属性，1：表示事件发生时刻，前10秒的事件采样数据；2：表示事件发生时刻，后10秒的事件采样数据；
        GPSSampleData = self.GPSDataFromSeconds(10)                            #GPS 采样点 ，N秒内的GPS采样数据,170个字节
        CANSampleData = self.CANDataFromSeconds(10)                            #CAN采样点 ，N秒内的CAN采样数据，90个字节
        SENSORSampleData = self.SENSORDataFromSeconds(20)                      #SENSOR采样点 ，N秒内的SENSOR采样数据
        totalRapidlyAccelerateCount = self.int2hexStringByBytes(totalRapidlyAccelerateCount,2)
        totalSharpSlowdown = self.int2hexStringByBytes(totalSharpSlowdown,2)
        totalSharpTurn = self.int2hexStringByBytes(totalSharpTurn,2)
        dataProperty = self.int2hexStringByBytes(dataProperty,1)
        data = totalRapidlyAccelerateCount + totalSharpSlowdown + totalSharpTurn + dataProperty + GPSSampleData + CANSampleData + SENSORSampleData
        return data

    # 0021 急减速报警附带信息
    def sharpSlowdownExtraInfo(self,totalRapidlyAccelerateCount=100,totalSharpSlowdown=200,totalSharpTurn=50,dataProperty=2):
        totalRapidlyAccelerateCount = totalRapidlyAccelerateCount                         #急加速总次数
        totalSharpSlowdown = totalSharpSlowdown                                           #急减速总次数
        totalSharpTurn = totalSharpTurn                                                   #急转弯总次数
        dataProperty = dataProperty                                                       #事件属性，1：表示事件发生时刻，前10秒的事件采样数据；2：表示事件发生时刻，后10秒的事件采样数据；
        GPSSampleData = self.GPSDataFromSeconds(10)                            #GPS 采样点 ，N秒内的GPS采样数据,170个字节
        CANSampleData = self.CANDataFromSeconds(10)                            #CAN采样点 ，N秒内的CAN采样数据，90个字节
        SENSORSampleData = self.SENSORDataFromSeconds(20)                      #SENSOR采样点 ，N秒内的SENSOR采样数据
        totalRapidlyAccelerateCount = self.int2hexStringByBytes(totalRapidlyAccelerateCount,2)
        totalSharpSlowdown = self.int2hexStringByBytes(totalSharpSlowdown,2)
        totalSharpTurn = self.int2hexStringByBytes(totalSharpTurn,2)
        dataProperty = self.int2hexStringByBytes(dataProperty,1)
        data = totalRapidlyAccelerateCount + totalSharpSlowdown + totalSharpTurn + dataProperty + GPSSampleData + CANSampleData + SENSORSampleData
        return data

    # 0022 急转弯报警附带信息
    def sharpTurnExtraInfo(self,totalRapidlyAccelerateCount=100,totalSharpSlowdown=200,totalSharpTurn=50,direction=0,dataProperty=2):
        totalRapidlyAccelerateCount = totalRapidlyAccelerateCount                         #急加速总次数
        totalSharpSlowdown = totalSharpSlowdown                                           #急减速总次数
        totalSharpTurn = totalSharpTurn                                                   #急转弯总次数
        direction = direction                                                             #急转弯方向，0：向右转；1：向左转
        dataProperty = dataProperty                                                       #事件属性，1：表示事件发生时刻，前10秒的事件采样数据；2：表示事件发生时刻，后10秒的事件采样数据；
        GPSSampleData = self.GPSDataFromSeconds(10)                            #GPS 采样点 ，N秒内的GPS采样数据,170个字节
        CANSampleData = self.CANDataFromSeconds(10)                            #CAN采样点 ，N秒内的CAN采样数据，90个字节
        SENSORSampleData = self.SENSORDataFromSeconds(20)                      #SENSOR采样点 ，N秒内的SENSOR采样数据
        totalRapidlyAccelerateCount = self.int2hexStringByBytes(totalRapidlyAccelerateCount,2)
        totalSharpSlowdown = self.int2hexStringByBytes(totalSharpSlowdown,2)
        totalSharpTurn = self.int2hexStringByBytes(totalSharpTurn,2)
        direction = self.int2hexStringByBytes(direction)
        dataProperty = self.int2hexStringByBytes(dataProperty,1)
        data = totalRapidlyAccelerateCount + totalSharpSlowdown + totalSharpTurn + direction +  dataProperty + GPSSampleData + CANSampleData + SENSORSampleData
        return data

    #0023 碰撞报警附带信息
    def collisionAlarmExtraInfo(self,totalCount=7,dataProperty=2):
        totalCount = self.int2hexStringByBytes(totalCount,2)                                                         #历史碰撞总次数
        # 1：表示事件发生时刻，前10秒的事件采样数据；
        # [碰撞报警前后10秒采样数据附带信息]
        # 2：表示事件发生时刻，后10秒的事件采样数据；
        # [碰撞报警前后10秒采样数据附带信息]
        # 3：表示事件发生时刻，后120秒的事件采样数据；
        # [碰撞报警后120秒采样数据附带信息]
        dataProperty = self.int2hexString(dataProperty)
        extraInfo = self.collisionSamplingData()                                                           #附带信息
        data = totalCount + dataProperty + extraInfo
        return data

    #0023-ex 碰撞报警前后10秒采样数据附带信息
    def collisionSamplingData(self):
        GPSSampleData = self.GPSDataFromSeconds(10)                    #GPS 采样点 ，N秒内的GPS采样数据,170个字节
        CANSampleData = self.CANDataFromSeconds(10)                    #CAN采样点 ，N秒内的CAN采样数据，90个字节
        SENSORSampleData1 = self.SENSORDataFromSeconds(20)             #SENSOR采样点 ，N秒内的SENSOR采样数据
        SENSORSampleData2 = self.SENSORDataFromSeconds(40)             #S碰撞时刻前后100毫秒内的SENSOR采样数据；50ms滑动窗车平面加速度；（2.5ms采样周期）碰撞前后100毫秒内的滑动窗SENSOR采样数据
        SENSORStatus = self.int2hexString(1)                           #SENSOR状态,0:初始状态，1：学习状态，2：工作状态，其他：保留
        # 角度范围: [0, 360)；
        # 学习状态时，相对车平面内的x正半轴方向逆时针旋转角度；
        # 工作状态时，相对车头方向逆时针旋转角度。
        collisionAngle = self.int2hexStringByBytes(60,2)
        SENSORSampleData3 = self.SENSORDataFromSeconds(40)            #碰撞时刻前后100毫秒内的SENSOR采样数据；50ms滑动窗垂直车平面加速度；（2.5ms采样周期）,碰撞前后100毫秒内的滑动窗SENSOR采样数据
        SENSORCheckFlag = self.int2hexString(1)                                           #0:未初始化或者中心点偏离大于148mg，1：完成初始化或者中心点偏离小于100mg
        carSlopeAngle = self.carSlopeAngleFromSeconds(10)             #车辆倾斜角
        data = GPSSampleData + CANSampleData + SENSORSampleData1 + SENSORSampleData2 + SENSORStatus + collisionAngle + SENSORSampleData3 + SENSORCheckFlag + carSlopeAngle
        return data


    #23 GPS采样数据项
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

    #24 N秒内的GPS采样数据
    def GPSDataFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.GPSSamplingData()
        return data

    #25 加速度CAN数据项
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

    #26 N秒内的CAN采样数据
    def CANDataFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.CANSamplingData()
        return data

    #27 N秒内的SENSOR采样数据
    def SENSORDataFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.int2hexStringByBytes(30,2)              # 第N秒内的第N个0.5秒内的平均加速度值
        return data

    # 0027 超速报警
    def overSpeedAlarm(self,alarmType=0,durTime=360):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        durTimeHex = self.int2hexStringByBytes(durTime,2)
        data = alarmTypeHex + durTimeHex
        return data

    # 0028 疲劳驾驶报警
    def tiredDrivingAlarm(self,alarmType=1,durTime=11000):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        durTimeHex = self.int2hexStringByBytes(durTime, 2)
        data = alarmTypeHex + durTimeHex
        return data

    # 002A 急变道报警
    def rapidChangeLanes(self,nums=1,direction=1,lng=106.54041,lat=29.40268):
        numHex = self.int2hexStringByBytes(nums,2)                              # 急变道总次数
        directionHex = self.int2hexStringByBytes(direction)                     # 急变道方向
        dataAttrHex = self.int2hexStringByBytes(1)                              # 数据属性
        gpsesHex = self.getGpsSampleData002A(lng,lat)
        temp1 = gpsesHex
        for i in range(0,9):
            gpsesHex = gpsesHex + temp1
        CANesHex = self.getCanSampleData002A()
        temp2 = CANesHex
        for i in range(0,9):
            CANesHex = CANesHex + temp2
        sensorStatusHex = self.int2hexStringByBytes(2)
        sensorDataHex = self.getSensorSampleData()
        data = numHex + directionHex + dataAttrHex + gpsesHex + CANesHex + sensorStatusHex + sensorDataHex
        return data


        pass
    # 002A -ex Gps采样数据项
    def getGpsSampleData002A(self,lng=106.54041,lat=29.40268):
        lngHex = self.int2hexStringByBytes(int(lng * 1000000),4)
        latHex = self.int2hexStringByBytes(int(lat * 1000000),4)
        speecHex = self.int2hexStringByBytes(60,2)
        directionHex = self.int2hexStringByBytes(590,2)
        altitudeHex = self.int2hexStringByBytes(10000,4)
        statusHexBit = self.int2hexStringByBytes(1)
        data = lngHex + latHex + speecHex + directionHex + altitudeHex + statusHexBit
        return data

    # 002A - ex CAN采样数据项
    def getCanSampleData002A(self):
        speedHex = self.int2hexStringByBytes(60)
        engineSpeedHex = self.int2hexStringByBytes(3000,2)
        brakeHex = self.int2hexStringByBytes(0)
        acceleratorLocationHex = self.int2hexStringByBytes(50,2)
        airDamperHex = self.int2hexStringByBytes(100,2)
        troubleCodeNumHex = self.int2hexStringByBytes(0)
        data = speedHex + engineSpeedHex + brakeHex + acceleratorLocationHex + airDamperHex + troubleCodeNumHex
        return data
    # 002A - ex sensor采样点
    def getSensorSampleData(self):
        xHex = self.int2hexStringByBytes(10,2)
        yHex = self.int2hexStringByBytes(10, 2)
        sensorHex = xHex + yHex
        temp = sensorHex
        for i in range(0,19):
            sensorHex = sensorHex + temp
        return  sensorHex


    # 0030 水温报警
    def waterTemperatureAlarm(self,alarmType=0,curWaterTemperature=80):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        curWaterTemperatureHex = self.int2hexStringByBytes(curWaterTemperature)
        data = alarmTypeHex + curWaterTemperatureHex
        return data

    # 0031低水温高转速报警附带信息
    def lowWaterTemperatureHighEngineSpeed(self,alarmType=0,curWaterTemperature=10,engineSpeed=5000):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        curWaterTemperatureHex = self.int2hexStringByBytes(curWaterTemperature)
        engineSpeedHex = self.int2hexStringByBytes(engineSpeed,2)
        data = alarmTypeHex + curWaterTemperatureHex + engineSpeedHex
        return data

    # 0032 怠速时间过长报警
    def idlingOverTime(self,alarmType=0,durTime=300,oilExpend=500):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        durTimeHex = self.int2hexStringByBytes(durTime,2)
        oilExpendHex = self.int2hexStringByBytes(oilExpend,2)
        data = alarmTypeHex + durTimeHex + oilExpendHex
        return data


    # 0033 高速空挡滑行报警附带信息
    def highSpeedNeutralGearSlide(self,alarmType=0,durTime=30):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        durTimeHex = self.int2hexStringByBytes(durTime)
        data = alarmTypeHex + durTimeHex
        return data

    # 0036 低档高速报警附
    def lowGearHighSpeedAlarm(self,alarmType=1,durationTime=10):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        durationTimeHex = self.int2hexStringByBytes(durationTime,2)
        data = alarmTypeHex + durationTimeHex
        return data

    # 0037 高档低速报警附带信息
    def highGearLowSpeedAlarm(self,alarmType=1,durationTime=10):
        alarmTypeHex = self.int2hexStringByBytes(alarmType)
        durationTimeHex = self.int2hexStringByBytes(durationTime,2)
        data = alarmTypeHex + durationTimeHex
        return data

    def carSlopeAngleFromSeconds(self,counts):
        data = ""
        for i in range(0,counts):
            data += self.int2hexStringByBytes(60,2)                              #第1秒内倾斜角[0,180)
            data += self.int2hexStringByBytes(self.num2signedNum(-50),2)         #第1秒内侧倾角[-90, 90]，大于0右倾，小于0左倾
        return data

    #004A 剩余油量异常告警附带信息
    def surplusOilAlarm(self,surplusOilType=0,value=30):
        surplusOilTypeHex = self.int2hexStringByBytes(surplusOilType)
        valueHex = self.int2hexStringByBytes(value,2)
        data = surplusOilTypeHex + valueHex
        return data


if __name__ == "__main__":
    # print(EventClass().GPSDataFromSeconds(10))
    # print(EventClass().CANSamplingData())
    # print(EventClass().rapidlyAccelerateEtraInfo())
    # print(EventClass().carSlopeAngleFromSeconds(10))
    # print(EventClass().SENSORDataFromSeconds(40))
    # print(EventClass().carSlopeAngleFromSeconds(10))
    print(EventClass().collisionSamplingData())