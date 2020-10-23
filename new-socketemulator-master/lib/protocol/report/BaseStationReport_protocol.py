#coding:utf-8

'''
定义一个终端上报基站定位数据包协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class BaseStationReport_protocol(ProtocolBase):
    def __init__(self,msgCount = 1,WATER_CODE = "0002",DEV_ID = "M121501010001",infoTime="2020-01-20 10:12:05",operators=2,serverLAC=2020,serverCellID=2022,N1LAC=2024,N1CellID=2026,N2LAC=2028,N2CellID=20202,N3LAC=20204,N3CellID=20206,N4LAC=20208,N4CellID=20220,N5LAC=20222,N5CellID=20224,N6LAC=20226,N6CellID=20228,voltage=3.6,speed=60.6,engineSpeed=2000,totalMileage=500005,totalOilExpend=600006,totalRunTime=60001,statusBit=1):
        super().__init__()
        self.msgCount = int(msgCount)  # 要发送的数据包个数
        self.WATER_CODE = int(WATER_CODE);  # 消息流水号
        self.DEV_ID = DEV_ID  # 设备id

        self.infoTime = infoTime                           #基站时间信息
        self.operators = int(operators)                    #运营商
        self.serverLAC = int(serverLAC)                    #服务器 LAC
        self.serverCellID = int(serverCellID)              #服务器CellID
        self.N1LAC = int(N1LAC)                                 #N1 LAC
        self.N1CellID = int(N1CellID)                           #N1 CellID
        self.N2LAC = int(N2LAC)                                 # N2 LAC
        self.N2CellID = int(N2CellID)                           # N2 CellID
        self.N3LAC = int(N3LAC)                                 # N3 LAC
        self.N3CellID = int(N3CellID)                           # N3 CellID
        self.N4LAC = int(N4LAC)                                 # N4 LAC
        self.N4CellID = int(N4CellID)                           # N4 CellID
        self.N5LAC = int(N5LAC)                                 # N5 LAC
        self.N5CellID = int(N5CellID)                           # N5 CellID
        self.N6LAC = int(N6LAC)                                 # N6 LAC
        self.N6CellID = int(N6CellID)                           # N6 CellID

        self.voltage = float(voltage)                           #电瓶电压
        self.speed = float(speed)                               #车速
        self.engineSpeed = int(engineSpeed)                     #发动机转速
        self.totalMileage = int(totalMileage)                   #累计里程
        self.totalOilExpend = int(totalOilExpend)               #累计油耗
        self.totalRunTime = int(totalRunTime)                   #累计行驶时间
        self.statusBit = int(statusBit)                         #状态位


    #####################################################
    #               生成基站定位数据消息
    #####################################################
    def generateBaseStationMsg(self):
        self.getProtocalHeader()
        info = ""
        # 消息头
        HEADER = "4040"
        # 消息流水号
        WATER_CODE = self.getWaterCode(self.WATER_CODE)
        # 设备id
        DEV_ID = self.devid2hexString(self.DEV_ID)
        # 功能id(GPS功能id)
        FUN_ID = "0011"
        # 数据段
        data = ""
        for i in range(0, self.msgCount):
            data += self.generateBaseStationPkg(self.generateBaseStationData())
        # 消息长度
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data) / 2))

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
    #               创建基站定位数据包，包含包个数
    #               data:传入数据包的多条数据段
    #####################################################
    def generateBaseStationPkg(self, data):
        pkgLen = len(data)
        pkgNum = (pkgLen / 2) / 55
        pkgNumHex = self.int2hexString(int(pkgNum))
        pkg = pkgNumHex + data
        return pkg

    #####################################################
    #               创建基站定位数据段
    #####################################################
    def generateBaseStationData(self):
        data = ""
        baseData = self.generateBaseStationBaseData()                       #基站基本数据
        voltage = self.getVoltageHex(self.voltage)                          #电瓶电压
        speed = self.getSpeedHex(self.speed)                                #车速
        engineSpeed = self.getEngineSpeedHex(self.engineSpeed)              #发动机转速
        totalMileage = self.getTotalMileageHex(self.totalMileage)           #累计里程
        totalOilExpend = self.getTotalOilExpendHex(self.totalOilExpend)     #累计油耗
        totalRunTime = self.getTotalRunTimeHex(self.totalRunTime)           #累计行驶时间
        statusBit = self.getStatusBitHex(self.statusBit)                    #状态位
        retain = "00"                                                       # 预留字节

        data = baseData + voltage + speed + engineSpeed + totalMileage + totalOilExpend + totalRunTime + statusBit + retain
        return data


    #####################################################
    #               创建基站定位基本数据段
    #####################################################
    def generateBaseStationBaseData(self):
        data = ""
        infoTime = self.getUTCTimeHex(self.infoTime)                        #基站时间信息
        operators = self.getOperatorsHex(self.operators)                    #运营商
        serverLAC = self.getServerLACHex(self.serverLAC)                    #服务器 LAC
        serverCellID = self.getServerCellIDHex(self.serverCellID)           #服务器CellID
        N1LAC = self.getN1LACHex(self.N1LAC)                                #N1 LAC
        N1CellID = self.getN1CellIDHex(self.N1CellID)                       #N1 CellID
        N2LAC = self.getN2LACHex(self.N2LAC)                                # N2 LAC
        N2CellID = self.getN2CellIDHex(self.N2CellID)                       # N2 CellID
        N3LAC = self.getN3LACHex(self.N3LAC)                                # N3 LAC
        N3CellID = self.getN3CellIDHex(self.N3CellID)                       # N3 CellID
        N4LAC = self.getN4LACHex(self.N4LAC)                                # N4 LAC
        N4CellID = self.getN4CellIDHex(self.N4CellID)                       # N4 CellID
        N5LAC = self.getN5LACHex(self.N5LAC)                                # N5 LAC
        N5CellID = self.getN5CellIDHex(self.N5CellID)                       # N5 CellID
        N6LAC = self.getN6LACHex(self.N6LAC)                                # N6 LAC
        N6CellID = self.getN6CellIDHex(self.N6CellID)                       # N6 CellID

        data = infoTime + operators + serverLAC + serverCellID + N1LAC + N1CellID + N2LAC + N2CellID + N3LAC + N3CellID + N4LAC + N4CellID + N5LAC + N5CellID + N6LAC + N6CellID
        return data

    #####################################################
    #               获取运营商 16进制数据
    #####################################################
    def getOperatorsHex(self,data):
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取服务器LAC 16进制数据
    #####################################################
    def getServerLACHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取服务器CellID 16进制数据
    #####################################################
    def getServerCellIDHex(self, data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N1LAC 16进制数据
    #####################################################
    def getN1LACHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N1 CellID 16进制数据
    #####################################################
    def getN1CellIDHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N2LAC 16进制数据
    #####################################################
    def getN2LACHex(self, data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N2 CellID 16进制数据
    #####################################################
    def getN2CellIDHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N3LAC 16进制数据
    #####################################################
    def getN3LACHex(self, data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N3 CellID 16进制数据
    #####################################################
    def getN3CellIDHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N4LAC 16进制数据
    #####################################################
    def getN4LACHex(self, data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N4 CellID 16进制数据
    #####################################################
    def getN4CellIDHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N5LAC 16进制数据
    #####################################################
    def getN5LACHex(self, data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N5 CellID 16进制数据
    #####################################################
    def getN5CellIDHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N6LAC 16进制数据
    #####################################################
    def getN6LACHex(self, data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取N6 CellID 16进制数据
    #####################################################
    def getN6CellIDHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取电瓶电压的16进制数据
    #          单位：0.01V
    ###################################################
    def getVoltageHex(self,data):
        dataStr = str(data)
        dataStr = dataStr.replace(".", "")
        hexData = self.int2hexString(int(dataStr))
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取车速度的16进制数据
    #          单位：0.1km/h
    ###################################################
    def getSpeedHex(self,data):
        dataStr = str(data)
        dataStr = dataStr.replace(".", "")
        hexData = self.int2hexString(int(dataStr))
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取发送机转速的16进制数据
    ###################################################
    def getEngineSpeedHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取累计里程的16进制数据
    ###################################################
    def getTotalMileageHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取累计油耗的16进制数据
    ###################################################
    def getTotalOilExpendHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取累计行驶时间的16进制数据
    ###################################################
    def getTotalRunTimeHex(self,data):
        hexData = self.int2hexString(data)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    def getStatusBitHex(self,data):
        isFire = 1                  #指示当前车辆点熄火状态：0-熄火，1-点火

        hexData = self.int2hexString(data)
        return hexData
