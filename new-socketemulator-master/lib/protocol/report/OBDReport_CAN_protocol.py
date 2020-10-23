#coding:utf-8

'''
定义一个OBD终端上报CAN静态数据类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase


class OBDReport_CAN_protocol(ProtocolBase):

    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",infoTime="2020-01-10 16:29:19",dataFlowCode="ffffffffff",protocolType="0101",fireStatus=1,ACCStatus=1,voltage=12,troubleLightStatus=0,toubleCodeCount=0,engineSpeed=3000,speed=60,meterMileage=128500,mileageStatisticsStyle="01",totalMileage=4129040,troubleMileage=500,totalOilExpend=3500,surplusOil=505,totalRunTime=50000000,totalEngineTime=5000,airIntoAisleTemperture=42,coolingLiquidTemperture=38,envTemperture=68,ariIntoPress=20,oilPressure=550,atmosphericPressure=120,airFlow=3600,valveLocationSensor=4000,acceleratorLocation=50,engineLoad=55,fuelTrim=34,fireAngle=800,B1S1oxygenSensorVoltage=18,B1S2oxygenSensorVoltage=20,B1S1oxygenSensorElectricity=13000,B1S2oxygenSensorElectricity=13200,momentOilExpend=15,meterOilExpend=20000,engineAbsoluteLoad=32,steeringWheelAngle=10,torquePercentage=31,gearsLocation=1,GPSSpeed=72.4,GPSMileage=380000):
        pass
        self.msgCount = int(msgCount)  # 设置默认要发送的数据包个数

        self.WATER_CODE = int(WATER_CODE);  # 设置默认消息流水号
        self.DEV_ID = DEV_ID  # 设置默认设备id

        self.infoTime = infoTime  # 设置时间
        self.dataFlowCode = dataFlowCode  # 设置数据流掩码
        self.protocolType = protocolType  # 设置协议类型
        self.fireStatus = int(fireStatus)  # 设置点火状态
        self.ACCStatus = int(ACCStatus)  # 设置ACC状态
        self.voltage = float(voltage)  # 设置电瓶电压
        self.troubleLightStatus = int(troubleLightStatus)  # 设置故障灯状态(MIL)
        self.toubleCodeCount = int(toubleCodeCount)  # 设置故障码个数
        self.engineSpeed = int(engineSpeed)  # 设置发动机转速
        self.speed = int(speed)  # 设置车辆速度
        self.meterMileage = int(meterMileage)  # 设置仪表里程值
        self.mileageStatisticsStyle = mileageStatisticsStyle  # 设置里程统计方式
        self.totalMileage = int(totalMileage)  # 设置总里程值
        self.troubleMileage = int(troubleMileage)  # 设置故障行驶里程
        self.totalOilExpend = int(totalOilExpend)  # 设置总耗油量
        self.surplusOil = int(surplusOil)  # 设置剩余油量
        self.totalRunTime = int(totalRunTime)  # 设置车辆运行时间
        self.totalEngineTime = int(totalEngineTime)  # 设置发动机运行时间
        self.airIntoAisleTemperture = int(airIntoAisleTemperture)  # 设置进气口温度
        self.coolingLiquidTemperture = int(coolingLiquidTemperture)  # 设置冷却液温度
        self.envTemperture = int(envTemperture)  # 设置车辆环境温度
        self.ariIntoPress = int(ariIntoPress)  # 设置进气管压力
        self.oilPressure = int(oilPressure)  # 设置燃油压力
        self.atmosphericPressure = int(atmosphericPressure)  # 设置大气压力
        self.airFlow = int(airFlow)  # 设置空气流量
        self.valveLocationSensor = int(valveLocationSensor)  # 设置气门位置传感器
        self.acceleratorLocation = int(acceleratorLocation)  # 设置油门位置
        self.engineLoad = int(engineLoad)  # 设置发动机负荷
        self.fuelTrim = int(fuelTrim)  # 设置长期燃油修正
        self.fireAngle = int(fireAngle)  # 设置点火提前角
        self.B1S1oxygenSensorVoltage = int(B1S1oxygenSensorVoltage)  # 设置B1-S1氧传感器输出电压
        self.B1S2oxygenSensorVoltage = int(B1S2oxygenSensorVoltage)  # 设置B1-S2氧传感器输出电压
        self.B1S1oxygenSensorElectricity = int(B1S1oxygenSensorElectricity)  # 设置B1-S1氧传感器输出电流
        self.B1S2oxygenSensorElectricity = int(B1S2oxygenSensorElectricity)  # 设置B1-S2氧传感器输出电流
        self.momentOilExpend = int(momentOilExpend)  # 设置瞬时油耗
        self.meterOilExpend = int(meterOilExpend)  # 设置仪表油耗
        self.engineAbsoluteLoad = int(engineAbsoluteLoad)  # 设置发动机绝对负荷
        self.steeringWheelAngle = int(steeringWheelAngle)  # 设置方向盘转向角
        self.torquePercentage = int(torquePercentage)  # 设置扭矩百分比
        self.gearsLocation = int(gearsLocation)  # 设置档位（仅商用车）
        self.GPSSpeed = float(GPSSpeed)  # 设置GPS车速
        self.GPSMileage = int(GPSMileage)  # 设置GPS里程

    def setInfoTime(self,data):
        self.infoTime = data
    def setFireStatus(self,data):            #点火状态
        self.fireStatus = data
    def setACCStatus(self,data):             #ACC状态
        self.ACCStatus = data
    def setEngineSpeed(self,data):           #发动机转速
        self.engineSpeed = data
    def setSpeed(self,data):                 #车辆速度
        self.speed = data
    def setMeterMileage(self,data):          #汽车仪表里程值
        self.meterMileage = data
    def setTotalMileage(self,data):          #总里程
        self.totalMileage = data
    def setTroubleMileage(self,data):        #故障行驶里程
        self.troubleMileage = data
    def setTotalOilExpend(self,data):        #总油耗
        self.totalOilExpend = data
    def setSurplusOil(self,data):            #剩余油量
        self.surplusOil = data
    def setTotalRunTime(self,data):              #车辆总运行时间
        self.totalRunTime = data
    def setVoltage(self,data):
        self.voltage = float(data)


    #####################################################
    #               生成OBD终端上报CAN配置信息
    #####################################################
    def generateOBDReportCANMsg(self):
        self.getProtocalHeader()
        info = ""
        #消息头
        HEADER = "4040"
        #消息流水号
        # WATER_CODE = self.getWaterCode(1000)
        WATER_CODE = self.getWaterCode(self.WATER_CODE)
        #设备id
        # DEV_ID = self.devid2hexString("M121501010001")
        DEV_ID = self.devid2hexString(self.DEV_ID)
        # 功能id(OBD_CAN功能id)
        FUN_ID = "0012"
        #数据段
        data = ""
        for i in range(0,self.msgCount):
            data += self.generateBD_CAN_Pkg(self.generateOBD_CAN_Data())
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
    #               创建OBD的CAN数据包，包含包个数
    #               data:传入OBD的CAN数据包的多条数据段
    #####################################################
    def generateBD_CAN_Pkg(self, data):
        pkgLen = len(data)
        pkgNum = (pkgLen / 2) / 83
        # print("------------------------" + str(pkgNum))
        pkgNumHex = self.int2hexString(int(pkgNum))
        pkg = pkgNumHex + data
        return pkg

    ####################################################
    #               生成OBD终端上报CAN数据包
    #####################################################
    def generateOBD_CAN_Data(self):
        data = ""
        #时间
        # infoTime = self.getTimeHex(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        infoTime = self.getTimeHex(self.infoTime)
        #数据流掩码
        # dataFlowCode = self.getDataFlowCodeHex()
        dataFlowCode = self.dataFlowCode
        #协议类型
        # protocolType = self.getProtocolTypeHex()
        protocolType = self.protocolType
        #点火状态
        fireStatus = self.getFireStatusHex(self.fireStatus)
        #ACC状态
        ACCStatus = self.getACCStatusHex(self.ACCStatus)
        #电瓶电压
        voltage = self.getVoltageHex(self.voltage)
        #故障灯状态(MIL)
        troubleLightStatus = self.getTroubleLightStatusHex(self.troubleLightStatus)
        #故障码个数
        toubleCodeCount = self.getToubleCodeCountHex(self.toubleCodeCount)
        #发动机转速
        engineSpeed = self.getEngineSpeedHex(self.engineSpeed)
        #车辆速度
        speed = self.getSpeedHex(self.speed)
        #仪表里程值
        meterMileage = self.getMeterMileageHex(self.meterMileage)
        #里程统计方式
        # mileageStatisticsStyle = self.getMileageStatisticsStyleHex()
        mileageStatisticsStyle = self.mileageStatisticsStyle
        #总里程值
        totalMileage = self.getTotalMileageHex(self.totalMileage)
        #故障行驶里程
        troubleMileage = self.getTroubleMileageHex(self.troubleMileage)
        #总耗油量
        totalOilExpend = self.getTotalOilExpendHex(self.totalOilExpend)
        #剩余油量
        surplusOil = self.getSurplusOilHex(self.surplusOil)
        #车辆总运行时间
        totalRunTime  = self.getTotalRunTimeHex(self.totalRunTime)
        #发动机运行时间
        totalEngineTime = self.getTotalEngineTimeHex(self.totalEngineTime)
        #进气口温度
        airIntoAisleTemperture = self.getAirIntoAisleTempertureHex(self.airIntoAisleTemperture)
        #冷却液温度
        coolingLiquidTemperture = self.getCoolingLiquidTempertureHex(self.coolingLiquidTemperture)
        #车辆环境温度
        envTemperture = self.getEnvTempertureHex(self.envTemperture)
        #进气管压力
        ariIntoPress = self.getAriIntoPressHex(self.ariIntoPress)
        #燃油压力
        oilPressure = self.getOilPressureHex(self.oilPressure)
        #大气压力
        atmosphericPressure = self.getAtmosphericPressureHex(self.atmosphericPressure)
        #空气流量
        airFlow = self.getAirFlowHex(self.airFlow)
        #气门位置传感器
        valveLocationSensor = self.getValveLocationSensorHex(self.valveLocationSensor)
        #油门位置
        acceleratorLocation = self.getAcceleratorLocationHex(self.acceleratorLocation)
        #发动机负荷
        engineLoad = self.getEngineLoadHex(self.engineLoad)
        #长期燃油修正
        fuelTrim = self.getFuelTrimHex(self.fuelTrim)
        #点火提前角
        fireAngle = self.getFireAngleHex(self.fireAngle)
        #B1-S1氧传感器输出电压
        B1S1oxygenSensorVoltage = self.getB1S1OxygenSensorVoltageHex(self.B1S1oxygenSensorVoltage)
        # B1-S2氧传感器输出电压
        B1S2oxygenSensorVoltage = self.getB1S2OxygenSensorVoltageHex(self.B1S2oxygenSensorVoltage)
        #B1-S1氧传感器输出电流
        B1S1oxygenSensorElectricity = self.B1S1oxygenSensorElectricityHex(self.B1S1oxygenSensorElectricity)
        # B1-S2氧传感器输出电流
        B1S2oxygenSensorElectricity = self.B1S2oxygenSensorElectricityHex(self.B1S2oxygenSensorElectricity)
        #瞬时油耗
        momentOilExpend = self.getMomentOilExpendHex(self.momentOilExpend)
        #仪表油耗
        meterOilExpend = self.getMeterOilExpendHex(self.meterOilExpend)
        #发动机绝对负荷
        engineAbsoluteLoad = self.getEngineAbsoluteLoadHex(self.engineAbsoluteLoad)
        #方向盘转向角
        steeringWheelAngle = self.getSteeringWheelAngleHex(self.steeringWheelAngle)
        #扭矩百分比
        torquePercentage = self.getTorquePercentageHex(self.torquePercentage)
        #档位（仅商用车）
        gearsLocation = self.getGearsLocationHex(self.gearsLocation)
        # #GPS车速
        # GPSSpeed = self.getGPSSpeedHex(self.GPSSpeed)
        # #GPS里程
        # GPSMileage = self.getGPSMileageHex(self.GPSMileage)
        # #预留字段
        # retain  = self.getRetainHex()
        data = data + infoTime + dataFlowCode + protocolType + fireStatus + ACCStatus + voltage + troubleLightStatus
        data = data + toubleCodeCount + engineSpeed + speed + meterMileage + mileageStatisticsStyle + totalMileage
        data = data + troubleMileage + totalOilExpend + surplusOil + totalRunTime + totalEngineTime + airIntoAisleTemperture
        data = data + coolingLiquidTemperture + envTemperture + ariIntoPress + oilPressure + atmosphericPressure + airFlow
        data = data + valveLocationSensor + acceleratorLocation + engineLoad + fuelTrim + fireAngle
        data = data + B1S1oxygenSensorVoltage + B1S2oxygenSensorVoltage + B1S1oxygenSensorElectricity + B1S2oxygenSensorElectricity
        data = data + momentOilExpend + meterOilExpend + engineAbsoluteLoad + steeringWheelAngle + torquePercentage
        data = data + gearsLocation  # + GPSSpeed + GPSMileage + retain

        return data

    ####################################################
    #         将U时间转换为16进制，
    #        例如：2020-01-02   20:30:00 （年取后面2字节）则将20,01，02,20,30,00 转换为对应的6个字节
    #        theTime:传入一个类似：2020-01-03 13:05:13的一个字符串
    #####################################################
    def getTimeHex(self, theTime):
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
        time = ""
        for i in range(0, len(timeArr)):
            time += self.int2hexString(int(timeArr[i]))
        return time

    ####################################################
    #          获取数据流掩码的16进制数据
    #         数据流掩码，标识以下可支持的各数据流字段，每个BIT位表示一个数据流字段；
    #####################################################
    def getDataFlowCodeHex(self):
        return "0102030405"

    ####################################################
    #          获取协议类型的16进制数据
    #####################################################
    def getProtocolTypeHex(self):
        OBD_ST_HCAN = "0101"
        OBD_ST_MCAN = "0102"
        OBD_EX_HCAN = "0103"
        OBD_EX_MCAN = "0104"
        OBD_FK = "0105"
        OBD_K_ADDR = "0106"
        OBD_ISO = "0107"
        OBD_VPW = "0108"
        OBD_PWM = "0109"
        VW_ST_HCAN = "0201"
        VW_BOSCH = "0202"
        VW_TP_CAN = "0203"
        VW_K_ADDR = "0204"
        VW_UDS = "VW_UDS"
        return OBD_ST_HCAN

    ####################################################
    #          获取点火状态的16进制数据
    #          0：熄火   1：点火
    #####################################################
    def getFireStatusHex(self,num=1):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取ACC状态的16进制数据
    #          0：OFF   1：ON
    #####################################################
    def getACCStatusHex(self,num = 1):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取电瓶电压的16进制数据
    #          单位：0.01V
    ###################################################
    def getVoltageHex(self,num):
        valtage = int(num * 100)
        valtageHex = self.int2hexStringByBytes(valtage,2)
        return valtageHex

    ####################################################
    #          获取故障灯状态的16进制数据
    #          if(Bit0) ON  else     OFF
    #####################################################
    def getTroubleLightStatusHex(self,num = 0):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取故障个数的16进制数据
    #####################################################
    def getToubleCodeCountHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取发动机转速的16进制数据
    #####################################################
    def getEngineSpeedHex(self,num):
        engineSpeedStr = str(num)
        while (len(engineSpeedStr) < 4):
            engineSpeedStr = "0" + engineSpeedStr
        engineSpeedHex = hex(int(engineSpeedStr))
        engineSpeedHex = self.leftPad(str(engineSpeedHex)[2:], 4)
        return engineSpeedHex

    ####################################################
    #          获取车辆速度的16进制数据
    #####################################################
    def getSpeedHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取仪表里程值的16进制数据
    #####################################################
    def getMeterMileageHex(self,num):
        totalMeterStrHex = self.int2hexStringByBytes(num,4)
        return totalMeterStrHex

    ####################################################
    #          获取里程统计方式的16进制数据
    #          总里程类型：
    #          00：GPS里程统计方式
    #          01：OBD里程统计方式
    #####################################################
    def getMileageStatisticsStyleHex(self):
        GPS = "00"
        OBD = "01"
        return GPS

    ####################################################
    #          获取总里程值的16进制数据
    #          行驶里程,上报值单位为m(米)
    #####################################################
    def getTotalMileageHex(self,num):
        totalMileageStr = str(num)
        totalMileageStrHex = hex(int(totalMileageStr))
        totalMileageStrHex = self.leftPad(str(totalMileageStrHex)[2:], 8)
        return totalMileageStrHex

    ####################################################
    #          获取故障行驶里程的16进制数据(km)
    #####################################################
    def getTroubleMileageHex(self,num):
        dataStr = str(num)
        dataHex = hex(int(dataStr))
        dataHex = self.leftPad(str(dataHex)[2:], 8)
        return dataHex

    ####################################################
    #          获取总油耗量的16进制数据(ml 毫升)
    #####################################################
    def getTotalOilExpendHex(self,num):
        dataStr = str(num)
        dataHex = hex(int(dataStr))
        dataHex = self.leftPad(str(dataHex)[2:], 8)
        return dataHex

    ####################################################
    #          获取剩余油量的16进制数据
    #          剩余油量，单位L或 %
    #          bit15 == 0 百分比 % OBD都为百分比
    #          bit15 == 1 单位L
    #         显示值为上报值 / 10
    #####################################################
    def getSurplusOilHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取车辆总运行时间的16进制数据(单位秒)
    #####################################################
    def getTotalRunTimeHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取发动机总运行时间的16进制数据(单位秒)
    #####################################################
    def getTotalEngineTimeHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取进气口温度的16进制数据
    #          进气口温度(上报范围0~255)
    #          显示值为上报值 - 40(实际范围 - 40~215)
    #####################################################
    def getAirIntoAisleTempertureHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取l冷却液温度的16进制数据
    #          进气口温度(上报范围0~255)
    #          显示值为上报值 - 40(实际范围 - 40~215)
    #####################################################
    def getCoolingLiquidTempertureHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取车辆环境温度的16进制数据
    #          进气口温度(上报范围0~255)
    #          显示值为上报值 - 40(实际范围 - 40~215)
    #####################################################
    def getEnvTempertureHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取进气管压力的16进制数据
    #          进气歧管压力        (10~105kpa)
    #####################################################
    def getAriIntoPressHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取燃油压力的16进制数据
    #####################################################
    def getOilPressureHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取大气压力的16进制数据
    #####################################################
    def getAtmosphericPressureHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取空气流量的16进制数据
    #####################################################
    def getAirFlowHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取气门位置传感器的16进制数据
    #####################################################
    def getValveLocationSensorHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取油门位置的16进制数据
    #          显示值为上报值/10    ( 0~100)
    #####################################################
    def getAcceleratorLocationHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取发动机负荷的16进制数据
    #          发动机负荷，   0~100
    #####################################################
    def getEngineLoadHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取长期燃油修正的16进制数据
    #          显示值为(上报值/10)-100
    ##################################################
    def getFuelTrimHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取点火提前角的16进制数据
    #          显示值为(上报值/10)-64
    ##################################################
    def getFireAngleHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取B1-S1氧传感器输出电压的16进制数据
    #          显示值为上传值/10，单位0.1V
    ####################################################
    def getB1S1OxygenSensorVoltageHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取B1-S2氧传感器输出电压的16进制数据
    #          显示值为上传值/10，单位0.1V
    ####################################################
    def getB1S2OxygenSensorVoltageHex(self, num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取B1-S1氧传感器输出电流的16进制数据
    #          显示值为（上传值/100）-128，单位0.01mA
    ####################################################
    def B1S1oxygenSensorElectricityHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取B1-S2氧传感器输出电流的16进制数据
    #          显示值为（上传值/100）-128，单位0.01mA
    ####################################################
    def B1S2oxygenSensorElectricityHex(self, num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取瞬时油耗的16进制数据
    #          显示值为（上传值/100），单位L/h
    ####################################################
    def getMomentOilExpendHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取仪表油耗的16进制数据
    #          总的燃油消耗量,上报值单位为ml(毫升)
    ####################################################
    def getMeterOilExpendHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取发动机绝对负荷的16进制数据
    #          显示值为（上传值/100），单位%
    ####################################################
    def getEngineAbsoluteLoadHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取方向盘转向角的16进制数据
    #          显示值为（上传值/10）-3276.7
    ####################################################
    def getSteeringWheelAngleHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取方扭矩百分比的16进制数据
    #          显示值为0~100，单位%
    ####################################################
    def getTorquePercentageHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取档位（仅商用车）的16进制数据
    #          商用车：0为空档，1－16为前进档，17-20为后退档，21为P档
    ####################################################
    def getGearsLocationHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    ####################################################
    #          获取GPS车速的16进制数据
    #          车辆速度，单位0.1Km/h
    ####################################################
    def getGPSSpeedHex(self,num):
        dataStr = str(num)
        dataStr = dataStr.replace(".", "")  # 去掉经度小数点
        dataHex = hex(int(dataStr))
        dataHex = self.leftPad(str(dataHex)[2:], 4)
        return dataHex

    ####################################################
    #          获取GPS里程的16进制数据
    #          GPS里程，单位M
    ####################################################
    def getGPSMileageHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 8:
            hexData = "0" + hexData
        return hexData

    ####################################################
    #          获取预留字段的16进制数据
    ####################################################
    def getRetainHex(self):
        return "0000000000000000000000"

if __name__ == "__main__":
    # print(OBDReport_CAN_protocol().getTotalMileageHex(128500))
    OBDReport_CAN_protocol().generateOBD_CAN_Data()

