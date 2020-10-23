#coding:utf-8

'''
定义一个终端安防状态上报协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class SecurityStatusReport_protocol(ProtocolBase):

    def __init__(self,msgCount = 1,WATER_CODE = 14,DEV_ID = "M121501010001",locationType=1,GPSpkg="",statusCode="ffffffffffffffffffff",securityStatus=32,doorStatus=0,lockStatus=0,windowStatus=0,lightStatus=0,onoffStatusA=0,onoffStatusB=0,dataByte=0):
        super().__init__()
        self.msgCount = int(msgCount)
        self.WATER_CODE = int(WATER_CODE)
        self.DEV_ID = DEV_ID

        self.locationType = int(locationType)     #定位类型
        #self.GPSPkg = GPSpkg &  BaseStationPkg               #GPS包或者基站包
        self.GPSPkg = "1401091213260265b86206ed8c70026103280000752f03030405af017102610bb800003200000186a0001ed2a25e16fe3a"
        self.BaseStationPkg = "1401140a0c050207e407e607e807ea07ec4eea4eec4eee4ef04efc4efe4f004f024f040024025e07d00007a125000927c60000ea610100"

        self.statusCode = statusCode         #状态掩码
        self.securityStatus = int(securityStatus)       #安全状态
        self.doorStatus = int(doorStatus)         #门状态
        self.lockStatus = int(lockStatus)         #锁状态
        self.windowStatus = int(windowStatus)     #窗户状态
        self.lightStatus = int(lightStatus)       #灯光状态
        self.onoffStatusA = int(onoffStatusA)     #开关状态A
        self.onoffStatusB = int(onoffStatusB)     #开关状态B
        self.dataByte = int(dataByte)             #数据字节

    def setLocationType(self,data):
        self.locationType = data
    def setGPSPkg(self,data):
        self.GPSPkg = data
    def setBaseStationPkg(self,data):
        self.BaseStationPkg = data

    #####################################################
    #               生成安全状态消息
    #####################################################
    def generateSecurityStatusMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"  # 消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)  # 消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)  # 设备id
        FUN_ID = "0014"  # 功能id(安全状态功能id)
        # 数据段
        data = ""
        for i in range(0, self.msgCount):
            data += self.generateSecurityStatusPkg(self.locationType,self.GPSPkg,self.generateSecurityStatusData())  # 数据段
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data) / 2))  # 消息长度

        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)  # 校验字段
        info += CHECK_CODE

        return info

    #####################################################
    #               创建安防状态数据包，包含包个数
    #               data:传入安防状态数据包的多条数据段
    #####################################################
    def generateSecurityStatusPkg(self,locationType,thePkg,data):
        nData = ""
        pkg = ""
        if locationType == 1:      #GPS定位
            locationTypeHex = self.int2hexString(locationType)
            nData = nData + locationTypeHex + thePkg + data
            pkgLen = len(nData)
            pkgNum = (pkgLen / 2) / 70
            pkgNumHex = self.int2hexString(int(pkgNum))
            pkg = pkgNumHex + nData
        elif locationType == 2:     #基站定位
            locationTypeHex = self.int2hexString(locationType)
            nData = nData + locationTypeHex + thePkg + data
            pkgLen = len(nData)
            pkgNum = (pkgLen / 2) / 76
            pkgNumHex = self.int2hexString(int(pkgNum))
            pkg = pkgNumHex + nData
        return pkg

    #####################################################
    #               创建安防状态数据段
    #####################################################
    def generateSecurityStatusData(self):
        data = ""

        # statusCode = self.getStatusCodeHex()                #状态掩码
        statusCode = self.statusCode  # 状态掩码
        securityStatus = self.getSecurityStatusHex(self.securityStatus)        #安全状态
        doorStatus = self.getDoorStatusHex(self.doorStatus)                #门状态
        lockStatus = self.getLockStatusHex(self.lockStatus)                #锁状态
        windowStatus = self.getWindowStatusHex(self.windowStatus)            #窗户状态
        lightStatus = self.getLightStatusHex(self.lightStatus)              #灯光状态
        onoffStatusA = self.getOnoffStatusAHex(self.onoffStatusA)            #开关状态A
        onoffStatusB = self.getOnoffStatusBHex(self.onoffStatusB)            #开关状态B
        dataByte = self.getDataByteHex(self.dataByte)                    #数据字节
        retain1 = "00"                                      #预留
        retain2 = "00"                                      #预留


        data = data + statusCode + securityStatus + doorStatus + lockStatus + windowStatus + lightStatus + onoffStatusA + onoffStatusB + dataByte + retain1 + retain2
        return data


    #####################################################
    #               获取安全状态16进制数据
    #               按照高位在前，低位在后的规则
    #####################################################
    def getSecurityStatusHex(self,data):
        accStatus = 0                    #acc状态，1：开 0：关
        defenseStatus = 0                 #设防撤防状态，2：设防 0：撤防
        brakeStatus = 0                    #脚刹状态，4：踩下 0：松开
        acceleratorStatus = 0             #是否踩油门，8：踩下 0：松开
        handBrakeStatus = 0                #手刹状态，16：拉起手刹 0：松开手刹
        mainSafetyBelt = 32                 #主驾驶安全带，32：插入安全带 0：松开安全带
        subSafetyBelt = 64                  #副驾驶安全带，64：插入安全带 0：松开安全带
        retain = 0                         #预留字段

        # val = accStatus +defenseStatus +brakeStatus +acceleratorStatus + handBrakeStatus + mainSafetyBelt + subSafetyBelt + retain
        hexData =  self.int2hexString(data)
        return hexData

    #####################################################
    #               获取门状态16进制数据
    #####################################################
    def getDoorStatusHex(self,data):
        lfDoorStatus = 0                  #左前门，1,：开 0：关
        rfDoorStatus = 0                  #右前门，2：开 0：关
        lbDoorStatus = 0                  #左后门，4：开 0：关
        rbDoorStatus = 0                  #右后门，8：开 0：关
        trunk = 0                         #后备箱，32：开 0：关
        enginCover = 0                    #发送机盖：64：开 0：关
        retain1 = 0                       #预留字段
        retain2 = 0                       #预留字段

        # val = lfDoorStatus + rfDoorStatus + lbDoorStatus +rbDoorStatus + trunk + enginCover + retain1 +retain2
        hexData =  self.int2hexString(data)
        return hexData

    #####################################################
    #               获取锁状态16进制数据
    #####################################################
    def getLockStatusHex(self,data):
        lfDoorLockStatus = 0                  #左前门锁状态，1：开 0：关
        rfDoorLockStatus = 0                  #右前门锁状态，2：开 0：关
        lbDoorLockStatus = 0                  #左后门锁状态，4：开 0：关
        rbDoorLockStatus = 0                  #有后门锁状态，8：开 0：关
        retain1 = 0
        retain2 = 0
        retain3 = 0
        retain4 = 0

        # val = lfDoorLockStatus + rfDoorLockStatus + lbDoorLockStatus + rbDoorLockStatus + retain1 +retain2 + retain3 +retain4
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取窗户状态16进制数据
    #####################################################
    def getWindowStatusHex(self,data):
        lfWindowStatus = 0                #左前窗，1：开 0：关
        rfWindowStatus = 0                #右前窗，2：开 0：关
        lbWindowStatus = 0                # 左后窗，4：开 0：关
        rbWindowStatus = 0                # 右后窗，8：开 0：关
        topWindowStatus = 0               #天窗开关，16：开 0：关
        lTurnLight = 0                    #左转向灯，32：开 0：关
        rTurnLight = 0                    #右转向灯，64：开 0：关
        readLight = 0                     #阅读灯，128：开 0：关

        # val = lfWindowStatus + rfWindowStatus + lbWindowStatus + rbWindowStatus + topWindowStatus + lTurnLight + rTurnLight + readLight
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取灯光状态16进制数据
    #####################################################
    def getLightStatusHex(self,data):
        lowHeadlight = 0              #近光灯，1：开 0：关
        highHeadlight = 0             #远光灯，2：开 0：关
        ffogLight = 0                 #前雾灯，4：开 0：关
        bfogLight = 0                 #后雾灯，8：开 0：关
        dangerLight = 0               #危险灯，16：开 0：关
        backCarLight = 0              #倒车灯，32：开 0：关
        autoLight = 0                 #auto灯，64：开 0：关
        widthLight = 0                #示宽灯，128：开 0：关

        # val = lowHeadlight + highHeadlight + ffogLight + bfogLight + dangerLight + backCarLight + autoLight + widthLight
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取开关状态A16进制数据
    #####################################################
    def getOnoffStatusAHex(self,data):
        machineOilWarning = 0                  #机油报警，1：开  0：关
        oilWarning = 0                         #燃油报警，2：开  0：关
        wiperWarning = 0                       #雨刷报警，4：开  0：关
        loudsspeakerWaring = 0                 #喇叭报警，8：开  0：关
        airConditionerWaring = 0               #空调，16：开     0：关
        backMirrorWaring = 0                   #后视镜状态：32开 0：关
        retain1 = 0
        retain2 = 0

        # val = machineOilWarning + oilWarning + wiperWarning + loudsspeakerWaring + airConditionerWaring + backMirrorWaring + retain1 + retain2
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取开关状态B16进制数据
    #####################################################
    def getOnoffStatusBHex(self,data):
        retain1 = 0
        retain2 = 0
        retain3 = 0
        retain4 = 0
        #档位，0：p  16：R  32：N  48：D  64：1挡  80：2挡  96：3挡  112：4挡  128：5挡  144：16挡  160：M挡  176：S挡
        gears = 0

        # val = retain1 + retain2 + retain3 + retain4 + gears
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取数据字节16进制数据
    #####################################################
    def getDataByteHex(self,data):
        V1N1 = 0                           #V1N1,1：存在  0：不存在
        retain1 = 0
        retain2 = 0
        busTotalMileage = 0                #总线总里程，8：存在  0,：不存在
        meterData = 0                      #仪表数据，16：存在   0,：不存在
        engineSpeed = 0                    #发送机转速，32：存在 0：不存在
        speed = 0                          #车辆速度，64：存在   0：不存在
        surplusOil = 0                     #剩余油量，128：存在  0：不存在

        # val = V1N1 + retain1 + retain2 + busTotalMileage +meterData + engineSpeed + speed +surplusOil
        hexData = self.int2hexString(data)
        return hexData






























