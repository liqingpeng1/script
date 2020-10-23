#encoding:utf-8

'''
定义定位数据批量上传
'''
import datetime

from lib.protocol.message.MessageBase import MessageBase
from lib.protocol.message.data.AlarmEvent_data import AlarmEvent_data
from lib.protocol.message.data.CarSafeStatusInfo import CarSafeStatusInfo
from lib.protocol.message.data.Circum_data import Circum_data
from lib.protocol.message.data.NewEnergyCar_data import NewEnergyCar_data
from lib.protocol.message.data.SaloonCarOBD_data import SaloonCarOBD_data
from lib.protocol.message.data.TruckCarOBD_data import TruckCarOBD_data


class LocationDataBatchUpdate_msg(MessageBase):
    def __init__(self):
        super().__init__()
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

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        dataItemCounts = self.getDataItemCounts()               #数据项个数
        #位置数据类型 ,0：正常位置批量汇报，1：盲区补报
        locationDataType = self.int2hexStringByBytes(0)
        #位置汇报数据项
        locationData = self.getLocationData()
        msg = dataItemCounts + locationDataType + locationData
        return msg

    #######################################################
    # 位置信息汇报数据项
    #######################################################
    def getLocationData(self):
        dataBody = ""                                             #位置汇报数据体
        for i in range(0,12):
            dataBody = dataBody + self.getLocationBaseInfo()
        dataLen = self.int2hexStringByBytes(int(len(dataBody)/2),2)        #位置汇报数据体长度
        data = dataLen + dataBody
        return data


    #######################################################
    # 获取数据项个数
    #######################################################
    def getDataItemCounts(self):
        # 起始字节	标志
        # 0	1：紧急（备注：主要用于设备厂商私有协议 ASCII 文本控制指令下发） （1）
        # 1	保留
        # 2	1：终端显示器显示    （4）
        # 3	1：终端 TTS 播读   （8）
        # 4	1：广告屏显示    （16）
        # 5	0：中心导航信息，1：CAN 故障码信息   （32）
        # 6-7	保留
        bit0 = 1
        bit2 = 4
        bit3 = 8
        bit4 = 16
        bit5 = 32
        data = bit0 + bit2 + bit2 + bit4 + bit5
        dataHex = self.int2hexStringByBytes(data)
        return dataHex

    #######################################################
    # 获取位置基本信息
    #######################################################
    def getLocationBaseInfo(self):
        msg = ""
        alarmFlag = self.getAlarmFlag()                             #报警标志
        status = self.getStatus()                                   #状态
        latitude = self.getLatitude()                               #纬度
        longtitude = self.getLongtitude()                           #经度
        elevation = self.getElevation()                             #海拔高度
        speed = self.getSpeed()                                     #速度
        directionAngle = self.getDirectionAngle()                   #获取方向角度
        infoTime = self.getInfoTime()                               #获取时间

        msg = alarmFlag + status + latitude + longtitude + elevation + speed + directionAngle + infoTime
        return msg

    #######################################################
    # 获取位置附加信息
    #######################################################
    def getLocationExtraInfo(self):
        data = ""
        extraInfoId = self.int2hexStringByBytes(1)
        # 里程，DWORD，1 / 10km，对应车上里程表读数；不支持OBD时，为基于GPS车速统计的车辆累计行驶总里程。
        extra_01 = "01" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(20202020,4)
        #油量，WORD，1/10L，对应车上油量表读数
        extra_02 = "02" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(5200,2)
        #超速报警附加信息
        extra_11 = "11" + self.int2hexStringByBytes(int(len(self.getOverSpeedAlarmExtraInfo()) / 2)) + self.getOverSpeedAlarmExtraInfo()
        #进出区域/路线报警附加信息见
        extra_12 = "12" + self.int2hexStringByBytes(6) + self.getInOutAreaAlarmExtraInfo()
        #路段行驶时间不足/过长报警附加信息见
        extra_13 = "13" + self.int2hexStringByBytes(7) + self.getDrivingLongOrShortAlarmExtraInfo()
        #IO 状态位
        extra_2A = "2A" + self.int2hexStringByBytes(2) + self.getStatusBit()
        #BYTE，无线通信网络信号强度
        extra_30 = "30" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(33)
        #BYTE，GNSS 定位卫星数
        extra_31 = "31" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(2)
        #基础数据项列表
        extra_EA = "EA" + self.int2hexStringByBytes(int(len(self.getBaseDataList()) / 2)) + self.getBaseDataList()
        #轿车 OBD 数据流
        extra_EB = "EB" + self.int2hexStringByBytes(int(len(SaloonCarOBD_data().generateSaloonCarOBDData()) / 2)) + SaloonCarOBD_data().generateSaloonCarOBDData()
        #货车 OBD 数据流
        extra_EC = "EC" + self.int2hexStringByBytes(int(len(TruckCarOBD_data().generateTruckCarOBD_data()) / 2)) + TruckCarOBD_data().generateTruckCarOBD_data()
        #新能源 OBD 数据流
        extra_ED = "ED" + self.int2hexStringByBytes(int(len(NewEnergyCar_data().generateNewEnergyCar_data()) / 2)) + NewEnergyCar_data().generateNewEnergyCar_data()
        #外设数据项列表
        extra_EE = "EE" + self.int2hexStringByBytes(int(len(Circum_data().generateCircum_data()) / 2)) + Circum_data().generateCircum_data()
        #报警事件 ID 数据项列表
        extra_FA = "FA" + self.int2hexStringByBytes(int(len(AlarmEvent_data().generateAlarmEvent_data()) / 2)) + AlarmEvent_data().generateAlarmEvent_data()

        data = extra_01 + extra_02 + extra_11 + extra_12 + extra_13 + extra_FA
        # data = extra_01 + extra_02 + extra_11 + extra_12 + extra_13
        # data = data + extra_2A + extra_30 + extra_31 + extra_EA + extra_EB
        # data = data + extra_EC
        extraInfoLen = self.int2hexStringByBytes(int(len(data) / 2))
        data = extraInfoId + extraInfoLen + data
        return data


    #获取超速报警附加信息
    def getOverSpeedAlarmExtraInfo(self):
        # 0：无特定位置；
        # 1：圆形区域；
        # 2：矩形区域；
        # 3：多边形区域；
        # 4：路段
        locationType = 1
        areaId = ""                                    #若位置类型为 0，无该字段
        if locationType == 0:
            pass
        else:
            areaId = self.int2hexStringByBytes(2020,4)
        msg = self.int2hexStringByBytes(locationType) + areaId
        return msg

    #获取进出区域/路线报警附加信息
    def getInOutAreaAlarmExtraInfo(self):
        # 0：无特定位置；
        # 1：圆形区域；
        # 2：矩形区域；
        # 3：多边形区域；
        # 4：路段
        locationType = 1
        areaId = ""
        if locationType == 0:
            areaId = "00000000"
        else:
            areaId = self.int2hexStringByBytes(2020, 4)
        direction = 0                     #0-进，1-出
        msg = self.int2hexStringByBytes(locationType) + areaId + self.int2hexStringByBytes(direction)
        return msg

    #路线行驶时间不足/过长报警附加信息消息
    def getDrivingLongOrShortAlarmExtraInfo(self):
        areaId = self.int2hexStringByBytes(2020, 4)          #路段Id
        drivingTime = self.int2hexStringByBytes(36000,2)     #路段行驶时间(单位：秒)
        result = self.int2hexStringByBytes(0)                #结果，0-不足，1-过长
        msg = areaId + drivingTime + result
        return msg

    #获取状态位
    def getStatusBit(self):
        deepSleepStatus = 1             #1：深度休眠状态
        sleepStatus = 2                 #1：休眠状态
        retain = 0
        data = deepSleepStatus + sleepStatus + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #基础数据项列表
    def getBaseDataList(self):
        dataId_0001 = "0001" + self.int2hexStringByBytes(4) + self.getExpandStatusBit()
        dataId_0002 = "0002" + self.int2hexStringByBytes(4) + self.getExpandAlarmBit()
        dataId_0003 = "0003" + self.int2hexStringByBytes(5) + self.getTotalMileage()
        dataId_0004 = "0004" + self.int2hexStringByBytes(5) + self.getTotalOil()
        dataId_0005 = "0005" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(360000,4)
        dataId_0006 = "0006" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(72000,4)
        dataId_0007 = "0007" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(480000,4)
        dataId_0010 = "0010" + self.int2hexStringByBytes(int(len(self.getSpeedupInOneSeconds()) / 2)) + self.getSpeedupInOneSeconds()
        dataId_0011 = "0011" + self.int2hexStringByBytes(int(len(CarSafeStatusInfo().generateSecurityStatusData()) / 2)) + CarSafeStatusInfo().generateSecurityStatusData()
        dataId_0012 = "0012" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(36,2)
        dataId_0013 = "0013" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        #TODO 由于被置灰，所以没有实现
        # dataId_0015 = "0015" + self.int2hexStringByBytes(2)
        # dataId_0016 = "0016"
        #TODO 暂不支持
        # dataId_0017 = "0017" + self.int2hexStringByBytes(2)
        dataId_001D = "001D" + self.int2hexStringByBytes(1) + "01"
        data = dataId_0001 + dataId_0002 + dataId_0003 + dataId_0004 + dataId_0005
        data = data + dataId_0006 + dataId_0007 + dataId_0010 + dataId_0011 + dataId_0012
        data = data + dataId_0013 + dataId_001D
        return data


    '''扩展状态标志位，见 表 C1EXT1'''
    def getExpandStatusBit(self):
        defenseUndefenseRep = 0          #0：撤防上报；1：设防上报   (1)
        retain = 0
        data = defenseUndefenseRep + retain
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex
    '''扩展报警标志位，见 表 C1EXT2'''
    def getExpandAlarmBit(self):
        waterTemperatureAlarm = 1                      #1:水温报警        (1)
        idlingOverlongAlarm = 2                        #1：怠速过长报警   (2)
        rapidlyAccelerateAlarm = 4                     #1：急加速报警     (4)
        sharpSlowsownAlarm = 8                         #1：急减速报警     (8)
        sharpCurve = 16                                #1：急转弯报警     (16)
        retain5_9 = 0
        insertAlarm = 1024                             #1：插入报警      (1024)
        oilExpenseNotSupportAlarm = 2048               #1:油耗不支持报警  (2048)
        OBDNotSupportAlarm = 4096                      #1:OBD 不支持报警  (4096)
        buslineNotSleepAlarm = 8192                    #1:总线不睡眠报警  (8192)
        illegalOpenDoor = 16384                        #1:非法开门       (16384)
        retain15_16 = 0
        FLASHTroubleAlarm = 131072                     #1: FLASH 故障报警   (131072)
        CANTroubleAlarm = 262144                       #1: CAN 模块故障报警  (262144)
        D3SensorTroubleAlarm = 524288                  #1：3D 传感器故障报警  (524288)
        RTCTroubleAlarm = 1048576                      #1：RTC 模块故障报警
        retain21_31 = 0
        data = waterTemperatureAlarm + idlingOverlongAlarm + rapidlyAccelerateAlarm + sharpSlowsownAlarm + sharpCurve
        data = data + retain5_9 + insertAlarm + oilExpenseNotSupportAlarm + OBDNotSupportAlarm + buslineNotSleepAlarm
        data = data + illegalOpenDoor + retain15_16 + FLASHTroubleAlarm + CANTroubleAlarm + D3SensorTroubleAlarm
        data = data + RTCTroubleAlarm + retain21_31
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex
    '''行驶总里程'''
    def getTotalMileage(self):
        caculateType = "01"
        totalMileage = self.int2hexStringByBytes(128000,4)    #行驶总里程（单位米）
        data = caculateType + totalMileage
        return data
    '''行驶总油耗'''
    def getTotalOil(self):
        caculateType = "01"
        totalOil = self.int2hexStringByBytes(120000,4)        #总油耗（单位 mL）
        data = caculateType + totalOil
        return data
    '''此刻 1 秒内的加速度数据，见 表 C1EXT3'''
    def getSpeedupInOneSeconds(self):
        data = ""
        pointCount = 4                                        #采集的点个数 N
        collectIntercal = 100                                 #采集间隔（单位 ms），上传值为该采集间隔时间内的加速度均值
        data = data + self.int2hexStringByBytes(pointCount,2)
        data = data + self.int2hexStringByBytes(collectIntercal,2)
        speedupVal = 1000                                     #采集点加速度均值
        for i in range(0,pointCount):
            data = data + self.int2hexStringByBytes(speedupVal + 10,2)
        return data




    #######################################################
    # 获取精度信息
    #######################################################
    def getLatitude(self,data=29.40268):
        data = int(data * 1000000)
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex

    #######################################################
    # 获取纬度信息
    #######################################################
    def getLongtitude(self,data=106.54041):
        data = int(data * 1000000)
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 获取海拔高度
    #######################################################
    def getElevation(self,data=520):
        dataHex = self.int2hexStringByBytes(data, 2)
        return dataHex

    #######################################################
    # 获取海拔高度
    #######################################################
    def getSpeed(self,data=66):
        dataHex = self.int2hexStringByBytes(data, 2)
        return dataHex

    #######################################################
    # 获取方向角度
    #######################################################
    def getDirectionAngle(self,data=59):
        dataHex = self.int2hexStringByBytes(data, 2)
        return dataHex

    #######################################################
    # 获取时间
    #######################################################
    def getInfoTime(self,data="2020-02-04 18:57:04"):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = data
        data = data.replace("-","")
        data = data.replace(" ","")
        data = data.replace(":","")
        data = data[2:]
        data = self.int2BCD(int(data))
        return data

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0200"
        msgBodyProperty = self.getMsgBodyProperty(int(len(self.getMsgBody()) / 2))              #消息体属性
        phoneNum = self.int2BCD(13146201119)                     #终端手机号
        msgWaterCode = self.int2BCD(1)                           #消息流水号
        subPkgContent = ""                                       #消息包封装项
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

    #######################################################
    # 获取报警标志
    #######################################################
    def getAlarmFlag(self):
        emergencyAlarm = 1                           #紧急报警，触动报警开关后触发
        overspeedAlarm = 2                           #超速报警
        fatigueDriving = 4                           #疲劳驾驶
        dangerAlarm = 8                              #危险预警
        GNSSTrouble = 16                             #GNSS 模块发生故障
        GNSSAntennaeLost = 32                        #GNSS 天线未接或被剪断
        GNSSAntennaeShortOut = 64                    #GNSS 天线短路
        TerminalMainPowerLackVoltage = 128           #终端主电源欠压
        TerminalMainPowerLostConnect = 256           #终端主电源掉电（设备拔出告警）
        TerMinalLCDTrouble = 512                     #终端 LCD 或显示器故障
        TTSTrouble = 1024                            #TTS 模块故障
        cameraTrouble = 2048                         #摄像头故障
        ICTrouble = 4096                             #道路运输证 IC 卡模块故障
        speedEarlyWarning = 8192                     #超速预警
        fatigueDrivingearlyWarning = 16384           #疲劳驾驶预警
        retain1 = 0
        retain2 = 0
        retain3 = 0
        drivingOverTime = 262144                     #当天累计驾驶超时
        stoppingOverTime = 524288                    #超时停车
        InOutArea = 1048576                          #进出区域
        InOutRouting = 2097152                       #进出路线
        drivingLongOrShort = 4194304                 #路段行驶时间不足/过长
        routingDivergeAlarm = 8388608                #路线偏离报警
        VSSTrouble = 16777216                        #车辆 VSS 故障
        oilException = 33554432                      #车辆油量异常
        carLost = 67108864                           #车辆被盗(通过车辆防盗器)
        illegalFire = 134217728                      #车辆非法点火
        illegalMoving = 268435456                    #车辆非法位移（拖车告警）
        collisionAlarm = 536870912                   #碰撞预警
        rollOverAlarm = 1073741824                   #侧翻预警
        illegalOpenDoor = 2147483648                 #非法开门报警（终端未设置区域时， 不判断非法开门）

        data = emergencyAlarm + overspeedAlarm + fatigueDriving + dangerAlarm + GNSSTrouble + GNSSAntennaeLost
        data = data + GNSSAntennaeShortOut + TerminalMainPowerLackVoltage + TerminalMainPowerLostConnect + TerMinalLCDTrouble
        data = data + TTSTrouble + cameraTrouble + ICTrouble + speedEarlyWarning + fatigueDrivingearlyWarning
        data = data + retain1 + retain2 + retain3 + drivingOverTime + stoppingOverTime
        data = data + InOutArea + InOutRouting + drivingLongOrShort + routingDivergeAlarm + VSSTrouble
        data = data + oilException + carLost + illegalFire + illegalMoving + collisionAlarm
        data = data + rollOverAlarm + illegalOpenDoor
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex

    #######################################################
    # 获取状态
    #######################################################
    def getStatus(self):
        ACCStatus = 1                           #0：ACC 关；1： ACC 开  (1)
        locationStatus = 2                      #0：未定位；1：定位      (2)
        latitudeStatus = 0                      #0：北纬；1：南纬        (4)
        longitudeStatus = 0                     #0：东经；1：西经          (8)
        runStatus = 0                           #0：运营状态；1：停运状态      (16)
        isLocationEncrypt = 0                   #0：经纬度未经保密插件加密；1：经纬度已经保密插件加密 (32)
        retain6_7 = 0
        # 00：空车；01：半载；10：保留；11：满载(0 , 256 ,512 , 768)
        #（可用于客车的空、重车及货车的空载、满载状态表示，人工输入或传感器 获取）
        isFull = 256
        oilRouteStatus = 0                      #0：车辆油路正常；1：车辆油路断开  (1024)
        powerStatus = 0                         #0：车辆电路正常；1：车辆电路断开   (2048)
        doorLockStatus = 0                      #0：车门解锁；1：车门加锁    (4096)
        frontDoor = 0                           #0：门 1 关；1：门	1 开（前门）   (8192)
        middleDoor = 0                          #0：门 2 关；1：门	2 开（中门）   (16384)
        backDoor = 0                            #0：门 3 关；1：门	3 开（后门）   (32768)
        drivingDoor = 0                         #0：门 4 关；1：门	4 开（驾驶席门）   (65536)
        otherDoor = 0                           #0：门 5 关；1：门	5 开（自定义）   (131072)
        GPSStatus = 262144                      #0：未使用 GPS 卫星进行定位；1：使用 GPS 卫星进行定位  (262144)
        beidouStatus = 524288                   #0：未使用北斗卫星进行定位；1：使用北斗卫星进行定位  (524288)
        GLONSSStatus = 1048576                  #0：未使用 GLONASS 卫星进行定位；1：使用 GLONASS 卫星进行定位  (1048576)
        GalileoStatus = 0                       #0：未使用 Galileo 卫星进行定位；1：使用 Galileo 卫星进行定位   (2097152)
        retain22_31 = 0

        data = ACCStatus + locationStatus + latitudeStatus + longitudeStatus + runStatus
        data = data + isLocationEncrypt + retain6_7 + isFull + oilRouteStatus + powerStatus
        data = data + doorLockStatus + frontDoor + middleDoor + backDoor + drivingDoor
        data = data + otherDoor + GPSStatus + beidouStatus + GLONSSStatus + GalileoStatus
        data = data + retain22_31
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex



if __name__ == "__main__":
    print(LocationDataBatchUpdate_msg().getLocationBaseInfo())
    print(LocationDataBatchUpdate_msg().generateMsg())



