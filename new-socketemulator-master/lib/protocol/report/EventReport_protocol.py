#coding:utf-8
import time

from lib.protocol.report.GPSReport_protocol import GPSReport_protocol
from lib.protocol.report.ProtocolBase import ProtocolBase
from lib.protocol.appendix.EventClass import EventClass
from lib.protocol.report.SecurityStatusReport_protocol import SecurityStatusReport_protocol

'''
终端上事件数据包
'''

class EventReport_protocol(ProtocolBase):
    #data = {"WATER_CODE":"0003","DEV_ID":"M121501010001","gpsInfo":{"UTCTime":"2020-04-14 11:03:20","latitude":"40.22077","longitude":"116.23128","speed":"80.8","directionAngle":"80.8","elevation":"2999.9","positionStar":"3","Pdop":"0.3","Hdop":"0.4","Vdop":"0.5","statusBit":162,"valtage":"36.9","OBDSpeed":"60.9","engineSpeed":"3000","GPSTotalMileage":"12800","totalOil":"100000","totalTime":"2020002","GPSTimestamp":"1586833400"},"securityData":{"securityStatus":107,"doorStatus":0,"lockStatus":0,"windowStatus":0,"lightStatus":0,"onoffStatusA":0,"onoffStatusB":112,"dataByte":249},"event":{}}
    data = {}
    def __init__(self,msgCount = 1,WATER_CODE = 26,DEV_ID = "M202003060520",locationType=1,eventType="0030",data={}):
        super().__init__()
        self.data = data
        if len(data) == 0:
            self.msgCount = msgCount                             #数据包个数

            self.WATER_CODE = int(WATER_CODE)                    #消息流水号
            self.DEV_ID = DEV_ID                                 #设备id

            self.locationType = int(locationType)                # 定位类型
            #self.GPSPkg = GPSpkg & BaseStationPkg  # GPS包或者基站包
            timeStamp = time.time()
            timeArray = time.localtime(int(timeStamp - 8 * 3600))
            dateTimeM = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            timeHex = self.getUTCTime(dateTimeM)
            self.GPSPkg = timeHex + "0265b86206ed8c70026103280000752f03030405af017102610bb800003200000186a0001ed2a25e16fe3a"
            # self.GPSPkg = "1401091213260265b86206ed8c70026103280000752f03030405af017102610bb800003200000186a0001ed2a25e16fe3a"
            self.BaseStationPkg = "1401140a0c050207e407e607e807ea07ec4eea4eec4eee4ef04efc4efe4f004f024f040024025e07d00007a125000927c60000ea610100"
            self.eventType = eventType                           #事件类别
        else:
            self.msgCount = 1  # 数据包个数

            self.WATER_CODE = int(data["WATER_CODE"])               # 消息流水号
            self.DEV_ID = data["DEV_ID"]                            # 设备id

            self.locationType = 1                                   # 定位类型
            gpsInfo = data["gpsInfo"]
            self.gpsInfo = gpsInfo
            securityData = data["securityData"]
            self.securityData = securityData
            event = data["event"]
            self.event = event
            self.GPSPkg = GPSReport_protocol(1,self.WATER_CODE,self.DEV_ID,gpsInfo["UTCTime"],gpsInfo["latitude"],gpsInfo["longitude"]  \
                          ,gpsInfo["speed"],gpsInfo["directionAngle"],gpsInfo["elevation"],gpsInfo["positionStar"],gpsInfo["Pdop"]  \
                          ,gpsInfo["Hdop"],gpsInfo["Vdop"],gpsInfo["statusBit"],gpsInfo["valtage"],gpsInfo["OBDSpeed"],gpsInfo["engineSpeed"]  \
                          ,gpsInfo["GPSTotalMileage"],gpsInfo["totalOil"],gpsInfo["totalTime"],gpsInfo["GPSTimestamp"]).generateGpsData()

            self.securityPkg = SecurityStatusReport_protocol(1,self.WATER_CODE,self.DEV_ID,1,self.GPSPkg,"ffffffffffffffffffff" \
                               ,securityData["securityStatus"],securityData["doorStatus"],securityData["lockStatus"]  \
                               ,securityData["windowStatus"],securityData["lightStatus"],securityData["onoffStatusA"]  \
                               ,securityData["onoffStatusB"],securityData["dataByte"]).generateSecurityStatusData()
            self.BaseStationPkg = "1401140a0c050207e407e607e807ea07ec4eea4eec4eee4ef04efc4efe4f004f024f040024025e07d00007a125000927c60000ea610100"

    def setLatitude(self,data):
        self.latitude = data
    def setLongtitude(self,data):
        self.longitude = data
    def setEventType(self,data):
        self.eventType = data
    def setLocationType(self,data):
        self.locationType = data
    def setGPSPkg(self,data):
        self.GPSPkg = data
    def setBaseStationPkg(self,data):
        self.BaseStationPkg = data


    #####################################################
    #               生成事件信息消息
    #####################################################
    def generateEventMsg(self):
        self.getProtocalHeader()
        info = ""
        #消息头
        HEADER = "4040"
        #消息流水号
        WATER_CODE = self.getWaterCode(self.WATER_CODE)
        #设备id
        DEV_ID = self.devid2hexString(self.DEV_ID)
        # 功能id(GPS功能id)
        FUN_ID = "0021"
        #数据段
        data = ""
        if len(self.data) == 0:
            for i in range(0,self.msgCount):
                data += self.generateEventPkg(self.msgCount,self.generateEventData())
        else:
            for i in range(0,self.msgCount):
                data += self.generateEventPkg(self.msgCount,self.generateEventData_GUI())
            # data += self.generateEventData_GUI()
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
        return info

    #####################################################
    #               创建GPS数据包，包含包个数
    #               data:传入GPS数据包的多条数据段
    #####################################################
    def generateEventPkg(self,pkgNum,data):
        pkgNumHex = self.int2hexString(int(pkgNum))
        pkg = pkgNumHex + data
        return pkg


    #####################################################
    #               创建事件信息数据段
    #####################################################
    def generateEventData(self):
        data = ""
        locationType = self.int2hexString(self.locationType)               #定位类型
        locationData = ""                                                  #GPS包或基站包
        if self.locationType == 1:
            locationData = self.GPSPkg
        elif self.locationType == 2:
            locationData = self.BaseStationPkg
        eventType = self.eventType
        extraInfo = self.getExtraData(eventType)                                      #附带信息
        extraInfoLen = self.int2hexStringByBytes(int((len(extraInfo) / 2)),2)                #附带信息长度
        data = locationType + locationData + eventType + extraInfoLen + extraInfo
        return data
    def generateEventData_GUI(self):
        data = ""
        locationType = self.int2hexString(self.locationType)               #定位类型
        locationData = ""                                                  #GPS包或基站包
        if self.locationType == 1:
            locationData = self.GPSPkg
        elif self.locationType == 2:
            locationData = self.BaseStationPkg
        eventData = self.getExtraData_GUI(self.event)
        data = locationType + locationData + eventData
        return data

    #####################################################
    #               获取附带信息
    #####################################################
    def getExtraData(self,eventType):
        if eventType == "0001":                                          #终端插入报警
            return EventClass().terminalInsertionAlarmExtraInfo()
        elif eventType == "0002":                                        #终端拔出报警
            return EventClass().terminalPulloutAlarmExtraInfo()
        elif eventType == "0003":                                        #汽车电瓶低电压报警
            return ""
        elif eventType == "0004":                                        #终端主电断电报警
            return ""
        elif eventType == "0005":                                        #GPS模块故障报
            return ""
        elif eventType == "0006":                                        #GPS天线开路报警
            return ""
        elif eventType == "0007":                                        #GPS天线短路报警
            return ""
        elif eventType == "0008":                                        #GPS定位时间过长报警
            return ""
        elif eventType == "0009":                                        #FLASH故障报警
            return ""
        elif eventType == "000A":                                        #CAN模块故障报警
            return ""
        elif eventType == "000B":                                        #3D传感器故障报警
            return ""
        elif eventType == "000C":                                        #RTC模块故障报警
            return ""
        elif eventType == "000D":                                        #TF卡故障报警
            return ""
        elif eventType == "000E":                                        #刷卡器故障报警
            return ""
        elif eventType == "000F":                                        #汽车预点火上报
            return EventClass().preFiringExtraInfo()
        elif eventType == "0010":                                        #汽车点火上报
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            return eventObj.fireExtraInfo()
        elif eventType == "0011":                                        #汽车熄火上报
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            return eventObj.misFireExtraInfo()
        elif eventType == "0012":                                        #汽车设防上报
            return EventClass().setUpDefencesExtraInfo()
        elif eventType == "0013":                                        #汽车撤防上报
            return EventClass().setDownDefencesExtraInfo()
        elif eventType == "0014":                                        #锁车未成功提醒
            return EventClass().lockCarFaillExtraInfo()
        elif eventType == "0015":                                        #超时未设防提醒
            return EventClass().noDefencesWithTimeoutExtraInfo()
        elif eventType == "0016":                                        #设防玻璃未关提醒
            return EventClass().defencesGlassNoCloseExtraInfo()
        elif eventType == "0017":                                        #设防非法开门报警
            return EventClass().defencesIllegalCloseDoorExtraInfo()
        elif eventType == "0023":                                        #碰撞告警
            return EventClass().collisionAlarmExtraInfo()
        elif eventType == "0027":                                        #超速报警
            return EventClass().overSpeedAlarm()
        elif eventType == "0028":                                        #疲劳驾驶报警
            return EventClass().tiredDrivingAlarm()
        elif eventType == "0030":                                        #水温报警
            return EventClass().waterTemperatureAlarm()
        elif eventType == "0031":                                        #低水温高转速报警
            return EventClass().lowWaterTemperatureHighEngineSpeed()
        elif eventType == "0032":                                        #怠速时间过长报警
            return EventClass().idlingOverTime()
        elif eventType == "0033":                                        #高速空挡滑行报警
            return EventClass().highSpeedNeutralGearSlide()
        elif eventType == "0036":                                        #低档高速报警
            return EventClass().lowGearHighSpeedAlarm()
        elif eventType == "0037":                                        #高档低速报警
            return EventClass().highGearLowSpeedAlarm()
        elif eventType == "004A":                                        #剩余油量异常告警
            return EventClass().surplusOilAlarm()

    #####################################################
    #               获取附带信息(针对图形界面)
    #####################################################
    def getExtraData_GUI(self,eventData):
        data = ""
        if ("0001" in eventData.keys()):                                           # 终端插入报警
            eventObj = EventClass()
            theData = eventObj.terminalInsertionAlarmExtraInfo()
            data = data + "0001" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0002" in eventData.keys()):                                           # 终端拔出报警
            eventObj = EventClass()
            theData = eventObj.terminalInsertionAlarmExtraInfo()
            data = data + "0002" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if("0003" in eventData.keys()):                                            #汽车电瓶低电压报警
            theData = ""
            data = data + "0003" + self.int2hexStringByBytes(int((len(theData) / 2)),2) + theData
        if ("0004" in eventData.keys()):                                          #终端主电断电报警
            theData = ""
            data = data + "0004" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0010" in eventData.keys()):                                          #汽车点火上报
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.fireExtraInfo(int(eventData["0010"]["allRapidlyAccelerateCount"]), int(eventData["0010"]["allSharpSlowdownCount"]), int(eventData["0010"]["allSharpTurn"]))
            data = data + "0010" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0011" in eventData.keys()):                                          #汽车熄火上报
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.misFireExtraInfo(int(eventData["0011"]["allRapidlyAccelerateCount"]), int(eventData["0011"]["allSharpSlowdownCount"]), int(eventData["0011"]["allSharpTurn"]))
            data = data + "0011" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0012" in eventData.keys()):                                          #汽车设防上报
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.setUpDefencesExtraInfo()
            data = data + "0012" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0013" in eventData.keys()):                                          #汽车撤防上报
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.setDownDefencesExtraInfo()
            data = data + "0013" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0020" in eventData.keys()):                                          #急加速
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.rapidlyAccelerateExtraInfo(int(eventData["0020"]["allRapidlyAccelerateCount"]),int(eventData["0020"]["allSharpSlowdownCount"]),int(eventData["0020"]["allSharpTurn"]),int(eventData["0020"]["dataProperty"]))
            data = data + "0020" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0021" in eventData.keys()):                                          #急减速
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.sharpSlowdownExtraInfo(int(eventData["0021"]["allRapidlyAccelerateCount"]),
                                                          int(eventData["0021"]["allSharpSlowdownCount"]),
                                                          int(eventData["0021"]["allSharpTurn"]),
                                                          int(eventData["0021"]["dataProperty"]))
            data = data + "0021" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0022" in eventData.keys()):                                          #急转弯
            eventObj = EventClass()
            eventObj.setGPSpkg(self.GPSPkg)
            eventObj.setSecurityData(self.securityPkg)
            theData = eventObj.sharpTurnExtraInfo(int(eventData["0022"]["allRapidlyAccelerateCount"]),
                                                          int(eventData["0022"]["allSharpSlowdownCount"]),
                                                          int(eventData["0022"]["allSharpTurn"]),
                                                          int(eventData["0022"]["direction"]),
                                                          int(eventData["0022"]["dataProperty"]))
            data = data + "0022" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0023" in eventData.keys()):                                          # 碰撞告警
            eventObj = EventClass()
            theData = eventObj.collisionAlarmExtraInfo(int(eventData["0023"]["totalCount"]),
                                                  int(eventData["0023"]["dataProperty"]),)
            data = data + "0023" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0027" in eventData.keys()):                                          # 超速告警
            eventObj = EventClass()
            theData = eventObj.overSpeedAlarm(int(eventData["0027"]["alarmType"]),
                                                  int(eventData["0027"]["durationTime"]))
            data = data + "0027" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0028" in eventData.keys()):                                          # 疲劳驾驶告警
            eventObj = EventClass()
            theData = eventObj.tiredDrivingAlarm(int(eventData["0028"]["alarmType"]),
                                                  int(eventData["0028"]["durationTime"]),)
            data = data + "0028" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("002A" in eventData.keys()):                                          # 急变道告警
            eventObj = EventClass()
            theData = eventObj.rapidChangeLanes(int(eventData["002A"]["nums"]),
                                                int(eventData["002A"]["direction"]),
                                                float(eventData["002A"]["lng"]),
                                                float(eventData["002A"]["lat"]))
            data = data + "002A" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0032" in eventData.keys()):                                          # 怠速时间过长报警
            eventObj = EventClass()
            theData = eventObj.idlingOverTime(int(eventData["0032"]["alarmType"]),int(eventData["0032"]["durationTime"]),int(eventData["0032"]["oilExpend"]))
            data = data + "0032" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0036" in eventData.keys()):                                          # 低档高速报警
            eventObj = EventClass()
            theData = eventObj.lowGearHighSpeedAlarm(int(eventData["0036"]["alarmType"]),int(eventData["0036"]["durationTime"]))
            data = data + "0036" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("0037" in eventData.keys()):                                          # 高档低速报警
            eventObj = EventClass()
            theData = eventObj.lowGearHighSpeedAlarm(int(eventData["0037"]["alarmType"]),int(eventData["0037"]["durationTime"]))
            data = data + "0037" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
        if ("004A" in eventData.keys()):                                          # 高档低速报警
            eventObj = EventClass()
            theData = eventObj.surplusOilAlarm(int(eventData["004A"]["surplusOilType"]),int(eventData["004A"]["value"]))
            data = data + "004A" + self.int2hexStringByBytes(int((len(theData) / 2)), 2) + theData
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
    data = {"a":1,"b":2,"c":{"d":3}}
    data = {}
    print(len(data))