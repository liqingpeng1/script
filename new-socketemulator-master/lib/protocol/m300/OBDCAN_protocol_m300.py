#encoding:utf-8

from lib.protocol.m300.M300Base import M300Base

'''
定义OBD CAN类
'''

class OBDCAN_protocol_m300(M300Base):
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0,timeInfo="2020-03-30 17:00:59",prototolType="11",statusMask="ffffffffffffffffffff" \
                 ,safeStatus=0,doorStatus=0,lockStatus=0,windowStatus=0,lightStatus=0,swichStatusA=0,swichStatusB=0,dataBit=0 \
                 ,dataFlowMask="fffffffd",votage=360,totalMilleageType=2,totalMilleage=3000,totalOil=300,troubleLightStatus=0 \
                 ,troubleCodeNum=2,engineSpeed=3000,speed=60,airInletTemperature=88,coolingLiquidTemperature=76,envTemperature=65 \
                 ,intakeManifoldPressure=20,oilPressure=276,atmosphericPressure=28,airFlow=550,valveLocation=51,acceleratorLocation=32 \
                 ,engineRunTime=370,troubleMileage=4508,surplusOil=801,engineLoad=52,fuelTrim=89,fireAngle=154,dashboardTotailMilleage=3000 \
                 ,carTotalRunTime=360,tripMark="0000"):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.waterCode = waterCode                    #消息流水号
        self.DEV_ID = DEV_ID                          #设备Id
        self.encryptionType = encryptionType          #消息属性里面的是否加密字段

        self.timeInfo = timeInfo                      #时间信息
        self.prototolType = prototolType              #协议类别
        self.statusMask = statusMask                  #状态掩码
        self.safeStatus = safeStatus                  #安全状态
        self.doorStatus = doorStatus                  #门状态
        self.lockStatus = lockStatus                  #锁状态
        self.windowStatus = windowStatus              #窗户状态
        self.lightStatus = lightStatus                #灯状态
        self.swichStatusA = swichStatusA              #开关状态A
        self.swichStatusB = swichStatusB              # 开关状态B
        self.dataBit = dataBit                        #数据字节
        self.retain9 = 0
        self.retail10 = 0

        self.dataFlowMask = dataFlowMask              #数据流掩码
        self.votage = votage                          #电瓶电压
        self.totalMilleageType = totalMilleageType    #总里程类别
        self.totalMilleage = totalMilleage            #行驶里程,上传值单位为m(米)
        self.totalOil = totalOil                      #总的燃油消耗量,上传值单位为ml(毫升)
        self.troubleLightStatus = troubleLightStatus  #故障灯状态(MIL)
        self.troubleCodeNum = troubleCodeNum          #故障码个数
        self.engineSpeed = engineSpeed                #发动机转速
        self.speed = speed                            #车辆速度
        self.airInletTemperature = airInletTemperature                       #进气口温度
        self.coolingLiquidTemperature = coolingLiquidTemperature             #冷却液温度
        self.envTemperature = envTemperature                                 #车辆环境温度
        self.intakeManifoldPressure = intakeManifoldPressure                 #进气歧管压力
        self.oilPressure = oilPressure                                       #燃油压力
        self.atmosphericPressure = atmosphericPressure                       #大气压力
        self.airFlow = airFlow                                               #空气流量
        self.valveLocation = valveLocation                                   #气门位置传感器
        self.acceleratorLocation = acceleratorLocation                       #油门踏板位置
        self.engineRunTime = engineRunTime                                   #发动机运行时间
        self.troubleMileage = troubleMileage                                 #故障行驶里程
        self.surplusOil = surplusOil                                         #剩余油量
        self.engineLoad = engineLoad                                         #发动机负荷
        self.fuelTrim = fuelTrim                                             #长期燃油修正(组1)
        self.fireAngle = fireAngle                                           #点火提前角
        self.dashboardTotailMilleage = dashboardTotailMilleage               #仪表总里程
        self.carTotalRunTime = carTotalRunTime                               #车辆总运行时间
        self.retail = "00000000000000000000"
        self.tripMark = tripMark                                             #驾驶循环标签

    def setTimeInfo(self,data):
        self.timeInfo = data
    def setAccstatus(self,data):
        if data == 1:
            self.safeStatus =  self.safeStatus | 1
        elif data == 0:
            self.safeStatus = self.safeStatus & ~1
    def setEngineSpeed(self,data):
        self.engineSpeed = data
    def setSpeed(self,data):
        self.speed = data
    def setDashboardTotailMilleage(self,data):
        self.dashboardTotailMilleage = data
    def setTotalMilleage(self,data):
        self.totalMilleage = data
    def setTotalOil(self,data):
        self.totalOil = data
    def setCarTotalRunTime(self,data):
        self.carTotalRunTime = data




    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0003"                                                  #功能id
        waterCode = self.int2hexStringByBytes(self.waterCode,2)         #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                      #设备id
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
        dateInfo = self.getDateInfo(self.timeInfo)                      # 日期
        prototolType = self.prototolType                                #协议类别
        statusMask = self.statusMask                                    #状态掩码
        # safeStatus = self.getSafeStatus()                               #安全状态
        # doorStatus = self.getDoorStatus()                               #门状态
        # lockStatus = self.getLockStatus()                               #锁状态
        # windowStatus = self.getWindowStatus()                           #窗户状态
        # lightStatus = self.getLightStatus()                             #灯状态
        # swichStatusA = self.getSwichStatusA()                           #开关状态A
        # swichStatusB = self.getSwichStatusB()                           # 开关状态B
        safeStatus = self.int2hexStringByBytes(self.safeStatus)            # 安全状态
        doorStatus = self.int2hexStringByBytes(self.doorStatus)            # 门状态
        lockStatus = self.int2hexStringByBytes(self.lockStatus)            # 锁状态
        windowStatus = self.int2hexStringByBytes(self.windowStatus)          # 窗户状态
        lightStatus = self.int2hexStringByBytes(self.lightStatus)           # 灯状态
        swichStatusA = self.int2hexStringByBytes(self.swichStatusA)          # 开关状态A
        swichStatusB = self.int2hexStringByBytes(self.swichStatusB)          # 开关状态B
        dataBit = self.getDataBit()                                     #数据字节
        retain9 = self.int2hexStringByBytes(self.retain9)
        retail10 = self.int2hexStringByBytes(self.retail10)

        dataFlowMask = self.dataFlowMask                                #数据流掩码
        votage = self.int2hexStringByBytes(self.votage,2)               #电瓶电压
        totalMilleageType = self.int2hexStringByBytes(self.totalMilleageType)                    #总里程类别
        totalMilleage = self.int2hexStringByBytes(self.totalMilleage,4)                          #行驶里程,上传值单位为m(米)
        totalOil = self.int2hexStringByBytes(self.totalOil,4)                                    #总的燃油消耗量,上传值单位为ml(毫升)
        troubleLightStatus = self.int2hexStringByBytes(self.troubleLightStatus)                  #故障灯状态(MIL)
        troubleCodeNum = self.int2hexStringByBytes(self.troubleCodeNum)                          #故障码个数
        engineSpeed = self.int2hexStringByBytes(self.engineSpeed,2)                              #发动机转速
        speed = self.int2hexStringByBytes(self.speed)                                            #车辆速度
        airInletTemperature = self.int2hexStringByBytes(self.airInletTemperature)                #进气口温度
        coolingLiquidTemperature = self.int2hexStringByBytes(self.coolingLiquidTemperature)      #冷却液温度
        envTemperature = self.int2hexStringByBytes(self.envTemperature)                          #车辆环境温度
        intakeManifoldPressure = self.int2hexStringByBytes(self.intakeManifoldPressure)          #进气歧管压力
        oilPressure = self.int2hexStringByBytes(self.oilPressure,2)                              #燃油压力
        atmosphericPressure = self.int2hexStringByBytes(self.atmosphericPressure)                #大气压力
        airFlow = self.int2hexStringByBytes(self.airFlow,2)                                      #空气流量
        valveLocation = self.int2hexStringByBytes(self.valveLocation,2)                          #气门位置传感器
        acceleratorLocation = self.int2hexStringByBytes(self.acceleratorLocation,2)              #油门踏板位置
        engineRunTime = self.int2hexStringByBytes(self.engineRunTime,2)                          #发动机运行时间
        troubleMileage = self.int2hexStringByBytes(self.troubleMileage,4)                        #故障行驶里程
        surplusOil = self.int2hexStringByBytes(self.surplusOil,2)                                #剩余油量
        engineLoad = self.int2hexStringByBytes(self.engineLoad)                                  #发动机负荷
        fuelTrim = self.int2hexStringByBytes(self.fuelTrim,2)                                    #长期燃油修正(组1)
        fireAngle = self.int2hexStringByBytes(self.fireAngle,2)                                  #点火提前角
        dashboardTotailMilleage = self.int2hexStringByBytes(self.dashboardTotailMilleage,4)      #仪表总里程
        carTotalRunTime = self.int2hexStringByBytes(self.carTotalRunTime,4)                      #车辆总运行时间
        retail = self.retail
        tripMark = self.tripMark                                                                 #驾驶循环标签
        data = dateInfo + prototolType + statusMask + safeStatus + doorStatus
        data = data + lockStatus + windowStatus + lightStatus + swichStatusA + swichStatusB
        data = data + dataBit + retain9 + retail10 + dataFlowMask + votage
        data = data + totalMilleageType + totalMilleage + totalOil + troubleLightStatus + troubleCodeNum
        data = data + engineSpeed + speed + airInletTemperature + coolingLiquidTemperature + envTemperature
        data = data + intakeManifoldPressure + oilPressure + atmosphericPressure + airFlow + valveLocation
        data = data + acceleratorLocation + engineRunTime + troubleMileage + surplusOil + engineLoad
        data = data + fuelTrim + fireAngle + dashboardTotailMilleage + carTotalRunTime + retail
        data = data + tripMark
        return data

    #获取安全状态
    def getSafeStatus(self):
        accStatus = 0                     #acc状态，1：开 0：关
        defenseStatus = 0                 #设防撤防状态，2：设防 0：撤防
        brakeStatus = 0                   #脚刹状态，4：踩下 0：松开
        acceleratorStatus = 0             #是否踩油门，8：踩下 0：松开
        handBrakeStatus = 0               #手刹状态，16：拉起手刹 0：松开手刹
        mainSafetyBelt = 0                #主驾驶安全带，32：插入安全带 0：松开安全带
        subSafetyBelt = 0                 #副驾驶安全带，64：插入安全带 0：松开安全带
        retain = 0                        #预留字段
        val = accStatus +defenseStatus +brakeStatus +acceleratorStatus + handBrakeStatus + mainSafetyBelt + subSafetyBelt + retain
        hexData =  self.int2hexStringByBytes(val)
        return hexData
    #获取门状态
    def getDoorStatus(self):
        lfDoorStatus = 0                  #左前门，1,：开 0：关
        rfDoorStatus = 0                  #右前门，2：开 0：关
        lbDoorStatus = 0                  #左后门，4：开 0：关
        rbDoorStatus = 0                  #右后门，8：开 0：关
        trunk = 0                         #后备箱，16：开 0：关
        enginCover = 0                    #发动机盖：32：开 0：关
        retain1 = 0                       #预留字段
        retain2 = 0                       #预留字段
        val = lfDoorStatus + rfDoorStatus + lbDoorStatus +rbDoorStatus + trunk + enginCover + retain1 +retain2
        hexData =  self.int2hexStringByBytes(val)
        return hexData
    #获取锁状态
    def getLockStatus(self):
        lfDoorLockStatus = 0                  #左前门锁状态，1：开 0：关
        rfDoorLockStatus = 0                  #右前门锁状态，2：开 0：关
        lbDoorLockStatus = 0                  #左后门锁状态，4：开 0：关
        rbDoorLockStatus = 0                  #右后门锁状态，8：开 0：关
        retain1 = 0
        retain2 = 0
        retain3 = 0
        retain4 = 0
        val = lfDoorLockStatus + rfDoorLockStatus + lbDoorLockStatus + rbDoorLockStatus + retain1 +retain2 + retain3 +retain4
        hexData = self.int2hexStringByBytes(val)
        return hexData
    #获取窗户状态
    def getWindowStatus(self):
        lfWindowStatus = 0                #左前窗，1：开 0：关
        rfWindowStatus = 0                #右前窗，2：开 0：关
        lbWindowStatus = 0                # 左后窗，4：开 0：关
        rbWindowStatus = 0                # 右后窗，8：开 0：关
        topWindowStatus = 0               #天窗开关，16：开 0：关
        lTurnLight = 0                    #左转向灯，32：开 0：关
        rTurnLight = 0                    #右转向灯，64：开 0：关
        readLight = 0                     #阅读灯，128：开 0：关
        val = lfWindowStatus + rfWindowStatus + lbWindowStatus + rbWindowStatus + topWindowStatus + lTurnLight + rTurnLight + readLight
        hexData = self.int2hexStringByBytes(val)
        return hexData
    # 灯状态
    def getLightStatus(self):
        lowHeadlight = 0              #近光灯，1：开 0：关
        highHeadlight = 0             #远光灯，2：开 0：关
        ffogLight = 0                 #前雾灯，4：开 0：关
        bfogLight = 0                 #后雾灯，8：开 0：关
        dangerLight = 0               #危险灯，16：开 0：关
        backCarLight = 0              #倒车灯，32：开 0：关
        autoLight = 0                 #auto灯，64：开 0：关
        widthLight = 0                #示宽灯，128：开 0：关
        val = lowHeadlight + highHeadlight + ffogLight + bfogLight + dangerLight + backCarLight + autoLight + widthLight
        hexData = self.int2hexStringByBytes(val)
        return hexData
    # 开关状态A
    def getSwichStatusA(self):
        machineOilWarning = 0                  #机油报警，1：开  0：关
        oilWarning = 0                         #燃油报警，2：开  0：关
        wiperWarning = 0                       #雨刷报警，4：开  0：关
        loudsspeakerWaring = 0                 #喇叭报警，8：开  0：关
        airConditionerWaring = 0               #空调，16：开     0：关
        backMirrorWaring = 0                   #后视镜状态：32开 0：关
        retain1 = 0
        retain2 = 0
        val = machineOilWarning + oilWarning + wiperWarning + loudsspeakerWaring + airConditionerWaring + backMirrorWaring + retain1 + retain2
        hexData = self.int2hexStringByBytes(val)
        return hexData
    # 开关状态B
    def getSwichStatusB(self):
        retain1 = 0
        retain2 = 0
        retain3 = 0
        retain4 = 0
        #档位，0：p  16：R  32：N  48：D  64：1挡  80：2挡  96：3挡  112：4挡  128：5挡  144：6挡  160：M挡  176：S挡
        gears = 0
        val = retain1 + retain2 + retain3 + retain4 + gears
        hexData = self.int2hexStringByBytes(val)
        return hexData
    # 数据字节
    def getDataBit(self):
        V1N1 = 0                                #VIN1，1：存在   0：不存在
        retain1 = 0
        retain2 = 0
        busMileage = 0                          #总线总里程，8：存在   0：不存在
        dashboardData = 0                       #仪表数据，16：存在   0：不存在
        engineSpeed = 0                         #发动机转速，32：存在   0：不存在
        carSpeed = 0                            #车辆速度，64：存在   0：不存在
        surplueOil = 0                          #剩余油量，128：存在   0：不存在
        val = V1N1 + retain1 + retain2 + busMileage + dashboardData + engineSpeed + carSpeed + surplueOil
        hexData = self.int2hexStringByBytes(val)
        return hexData


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

if __name__ == "__main__":
    print(OBDCAN_protocol_m300().generateMsg())

