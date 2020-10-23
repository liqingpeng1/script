#encoding:utf-8

'''
定义外设数据项
'''
from lib.protocol.message.MessageBase import MessageBase


class AlarmEvent_data(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #####################################################
    # 创建报警事件数据
    #####################################################
    def generateAlarmEvent_data(self):
        data = ""
        ignition = "0001" + self.int2hexStringByBytes(0)                    #点火上报
        flameout = "0002" + self.int2hexStringByBytes(0)                    #熄火上报
        setUpDefences = "0003" + self.int2hexStringByBytes(0)               #设防上报
        withdrawGarrision = "0004" + self.int2hexStringByBytes(0)           #撤防上报
        doorOpen = "0005" + self.int2hexStringByBytes(0)                    #车门打开
        doorClose = "0006" + self.int2hexStringByBytes(0)                   #车门关闭
        systemStart = "0007" + self.int2hexStringByBytes(0)                 #系统启动
        trailCarAlarm = "0101" + self.int2hexStringByBytes(0)               #拖车报警
        locationTooLong = "0102" + self.int2hexStringByBytes(0)             #定位过长报警
        terminalPullOut = "0103" + self.int2hexStringByBytes(0)             #终端拔出报警
        terminalInsert = "0104" + self.int2hexStringByBytes(0)              #终端插入报警
        lowVoltage = "0105" + self.int2hexStringByBytes(0)                  #低电压报警
        #怠速过长报警	附带信息见 表 C6EXT1
        idlingSpeedOver = "0106" + self.int2hexStringByBytes(9) + self.getIdlingSpeedOver()
        #超速报警	附带信息见 表 C6EXT2
        overspeedAlarm = "0107" + self.int2hexStringByBytes(9) + self.getOverspeedAlarm()
        #疲劳驾驶报警	附带信息见 表 C6EXT3
        fatigueDriving = "0108" + self.int2hexStringByBytes(5) + self.getFatigueDriving()
        #水温报警	附带信息见 表 C6EXT4
        waterTemperatureAlarm = "0109" + self.int2hexStringByBytes(9) + self.getWaterTemperatureAlarm()
        highSpeedNeutralGear = "010A" + self.int2hexStringByBytes(0)         # 高速空档滑行报警
        oilExpendNotSurport = "010B" +self.int2hexStringByBytes(0)           # 油耗不支持报警
        OBDNotSurport = "010C" + self.int2hexStringByBytes(0)                # OBD 不支持报警
        lowWaterTemperatureHighSpeed = "010D" +self.int2hexStringByBytes(0)  # 低水温高转速
        buslineNotSleep = "010E" + self.int2hexStringByBytes(0)              # 总线不睡眠报警
        illegalOpenDoor = "010f" + self.int2hexStringByBytes(0)              # 非法开门
        illegalFire = "0110" + self.int2hexStringByBytes(0)                  # 非法点火
        rapidAccelerateAlarm = "0111" + self.int2hexStringByBytes(0)         # 急加速报警
        sharpSlowdownAlarm = "0112" + self.int2hexStringByBytes(0)           # 急减速报警
        sharpBendAlarm = "0113" + self.int2hexStringByBytes(0)               # 急左拐弯报警
        crashAlarm = "0114" + self.int2hexStringByBytes(0)                   # 碰撞报警
        rapidChangeLines = "0115" + self.int2hexStringByBytes(0)             # 急左变道报警
        rapidChangeRightLines = "0116" + self.int2hexStringByBytes(0)        # 急右变道报警
        sharpRightBendAlarm = "0117" + self.int2hexStringByBytes(0)          # 急右拐弯报警

        data = ignition

        # data = data + ignition + flameout + setUpDefences + withdrawGarrision + doorOpen
        # data = data + doorClose + systemStart + trailCarAlarm + locationTooLong + terminalPullOut
        # data = data + terminalInsert + lowVoltage + idlingSpeedOver + overspeedAlarm + fatigueDriving
        # data = data + waterTemperatureAlarm + highSpeedNeutralGear + oilExpendNotSurport + OBDNotSurport + lowWaterTemperatureHighSpeed
        # data = data + buslineNotSleep + illegalOpenDoor + illegalFire + rapidAccelerateAlarm + sharpSlowdownAlarm
        # data = data + sharpBendAlarm + crashAlarm + rapidChangeLines
        return data

    def generateAlarmEvent_data_GUI(self,data):
        dataHex = ""
        if ("ignition" in data.keys()):
            ignition = "0001" + self.int2hexStringByBytes(0)                    #点火上报
            dataHex = dataHex + ignition
        if ("flameout" in data.keys()):
            flameout = "0002" + self.int2hexStringByBytes(0)                    #熄火上报
            dataHex = dataHex + flameout
        if ("setUpDefences" in data.keys()):
            setUpDefences = "0003" + self.int2hexStringByBytes(0)               #设防上报
            dataHex = dataHex + setUpDefences
        if ("withdrawGarrision" in data.keys()):
            withdrawGarrision = "0004" + self.int2hexStringByBytes(0)           #撤防上报
            dataHex = dataHex + withdrawGarrision
        if ("doorOpen" in data.keys()):
            doorOpen = "0005" + self.int2hexStringByBytes(0)                    #车门打开
            dataHex = dataHex + doorOpen
        if ("doorClose" in data.keys()):
            doorClose = "0006" + self.int2hexStringByBytes(0)                   #车门关闭
            dataHex = dataHex + doorClose
        if ("systemStart" in data.keys()):
            systemStart = "0007" + self.int2hexStringByBytes(0)                 #系统启动
            dataHex = dataHex + systemStart
        if ("trailCarAlarm" in data.keys()):
            trailCarAlarm = "0101" + self.int2hexStringByBytes(0)               #拖车报警
            dataHex = dataHex + trailCarAlarm
        if ("locationTooLong" in data.keys()):
            locationTooLong = "0102" + self.int2hexStringByBytes(0)             #定位过长报警
            dataHex = dataHex + locationTooLong
        if ("terminalPullOut" in data.keys()):
            terminalPullOut = "0103" + self.int2hexStringByBytes(0)             #终端拔出报警
            dataHex = dataHex + terminalPullOut
        if ("terminalInsert" in data.keys()):
            terminalInsert = "0104" + self.int2hexStringByBytes(0)              #终端插入报警
            dataHex = dataHex + terminalInsert
        if ("lowVoltage" in data.keys()):
            lowVoltage = "0105" + self.int2hexStringByBytes(0)                  #低电压报警
            dataHex = dataHex + lowVoltage
        if ("idlingSpeedOver" in data.keys()):
            #怠速过长报警	附带信息见 表 C6EXT1
            idlingSpeedOver = "0106" + self.int2hexStringByBytes(9) + self.getIdlingSpeedOver_GUI(data["idlingSpeedOver"])
            dataHex = dataHex + idlingSpeedOver
        if ("overspeedAlarm" in data.keys()):
            #超速报警	附带信息见 表 C6EXT2
            overspeedAlarm = "0107" + self.int2hexStringByBytes(9) + self.getOverspeedAlarm_GUI(data["overspeedAlarm"])
            dataHex = dataHex + overspeedAlarm
        if ("fatigueDriving" in data.keys()):
            #疲劳驾驶报警	附带信息见 表 C6EXT3
            fatigueDriving = "0108" + self.int2hexStringByBytes(5) + self.getFatigueDriving_GUI(data["fatigueDriving"])
            dataHex = dataHex + fatigueDriving
        if ("waterTemperatureAlarm" in data.keys()):
            #水温报警	附带信息见 表 C6EXT4
            waterTemperatureAlarm = "0109" + self.int2hexStringByBytes(9) + self.getWaterTemperatureAlarm_GUI(data["waterTemperatureAlarm"])
            dataHex = dataHex + waterTemperatureAlarm
        if ("highSpeedNeutralGear" in data.keys()):
            highSpeedNeutralGear = "010A" + self.int2hexStringByBytes(0)         #高速空档滑行报警
            dataHex = dataHex + highSpeedNeutralGear
        if ("oilExpendNotSurport" in data.keys()):
            oilExpendNotSurport = "010B" +self.int2hexStringByBytes(0)           #油耗不支持报警
            dataHex = dataHex + oilExpendNotSurport
        if ("OBDNotSurport" in data.keys()):
            OBDNotSurport = "010C" + self.int2hexStringByBytes(0)                #OBD 不支持报警
            dataHex = dataHex + OBDNotSurport
        if ("lowWaterTemperatureHighSpeed" in data.keys()):
            lowWaterTemperatureHighSpeed = "010D" +self.int2hexStringByBytes(0)  #低水温高转速
            dataHex = dataHex + lowWaterTemperatureHighSpeed
        if ("buslineNotSleep" in data.keys()):
            buslineNotSleep = "010E" + self.int2hexStringByBytes(0)              #总线不睡眠报警
            dataHex = dataHex + buslineNotSleep
        if ("illegalOpenDoor" in data.keys()):
            illegalOpenDoor = "010f" + self.int2hexStringByBytes(0)              #非法开门
            dataHex = dataHex + illegalOpenDoor
        if ("illegalFire" in data.keys()):
            illegalFire = "0110" + self.int2hexStringByBytes(0)                  #非法点火
            dataHex = dataHex + illegalFire
        if ("rapidAccelerateAlarm" in data.keys()):
            rapidAccelerateAlarm = "0111" + self.int2hexStringByBytes(0)         #急加速报警
            dataHex = dataHex + rapidAccelerateAlarm
        if ("sharpSlowdownAlarm" in data.keys()):
            sharpSlowdownAlarm = "0112" + self.int2hexStringByBytes(0)           #急减速报警
            dataHex = dataHex + sharpSlowdownAlarm
        if ("sharpBendAlarm" in data.keys()):
            sharpBendAlarm = "0113" + self.int2hexStringByBytes(0)               #急左拐弯报警
            dataHex = dataHex + sharpBendAlarm
        if ("crashAlarm" in data.keys()):
            crashAlarm = "0114" + self.int2hexStringByBytes(0)                   #碰撞报警
            dataHex = dataHex + crashAlarm
        if ("rapidChangeLines" in data.keys()):
            rapidChangeLines = "0115" + self.int2hexStringByBytes(0)             #急左变道报警
            dataHex = dataHex + rapidChangeLines
        if ("rapidChangeRightLines" in data.keys()):
            rapidChangeLines = "0116" + self.int2hexStringByBytes(0)             #急右变道报警
            dataHex = dataHex + rapidChangeLines
        if ("sharpRightBendAlarm" in data.keys()):
            sharpBendAlarm = "0117" + self.int2hexStringByBytes(0)               #急右拐弯报警
            dataHex = dataHex + sharpBendAlarm
        return dataHex

    # 创建报警事件数据，数据随机产生
    def generateAlarmEvent_data_random(self):
        data = ""
        ignition = "0001" + self.int2hexStringByBytes(0)                    #点火上报
        flameout = "0002" + self.int2hexStringByBytes(0)                    #熄火上报
        setUpDefences = "0003" + self.int2hexStringByBytes(0)               #设防上报
        withdrawGarrision = "0004" + self.int2hexStringByBytes(0)           #撤防上报
        doorOpen = "0005" + self.int2hexStringByBytes(0)                    #车门打开
        doorClose = "0006" + self.int2hexStringByBytes(0)                   #车门关闭
        systemStart = "0007" + self.int2hexStringByBytes(0)                 #系统启动
        trailCarAlarm = "0101" + self.int2hexStringByBytes(0)               #拖车报警
        locationTooLong = "0102" + self.int2hexStringByBytes(0)             #定位过长报警
        terminalPullOut = "0103" + self.int2hexStringByBytes(0)             #终端拔出报警
        terminalInsert = "0104" + self.int2hexStringByBytes(0)              #终端插入报警
        lowVoltage = "0105" + self.int2hexStringByBytes(0)                  #低电压报警
        #怠速过长报警	附带信息见 表 C6EXT1
        idlingSpeedOver = "0106" + self.int2hexStringByBytes(9) + self.getIdlingSpeedOver_random()
        #超速报警	附带信息见 表 C6EXT2
        overspeedAlarm = "0107" + self.int2hexStringByBytes(9) + self.getOverspeedAlarm_random()
        #疲劳驾驶报警	附带信息见 表 C6EXT3
        fatigueDriving = "0108" + self.int2hexStringByBytes(5) + self.getFatigueDriving_random()
        #水温报警	附带信息见 表 C6EXT4
        waterTemperatureAlarm = "0109" + self.int2hexStringByBytes(9) + self.getWaterTemperatureAlarm_random()
        highSpeedNeutralGear = "010A" + self.int2hexStringByBytes(0)         #高速空档滑行报警
        oilExpendNotSurport = "010B" +self.int2hexStringByBytes(0)           #油耗不支持报警
        OBDNotSurport = "010C" + self.int2hexStringByBytes(0)                #OBD 不支持报警
        lowWaterTemperatureHighSpeed = "010D" +self.int2hexStringByBytes(0)  #低水温高转速
        buslineNotSleep = "010E" + self.int2hexStringByBytes(0)              #总线不睡眠报警
        illegalOpenDoor = "010f" + self.int2hexStringByBytes(0)              #非法开门
        illegalFire = "0110" + self.int2hexStringByBytes(0)                  #非法点火
        rapidAccelerateAlarm = "0111" + self.int2hexStringByBytes(0)         #急加速报警
        sharpSlowdownAlarm = "0112" + self.int2hexStringByBytes(0)           #急减速报警
        sharpBendAlarm = "0113" + self.int2hexStringByBytes(0)               #急左拐弯报警
        crashAlarm = "0114" + self.int2hexStringByBytes(0)                   #碰撞报警
        rapidChangeLines = "0115" + self.int2hexStringByBytes(0)             #急变道报警
        sharpRightBendAlarm = "0117" + self.int2hexStringByBytes(0)               #急右拐弯报警

        arr = []
        arr.append(ignition)
        arr.append(flameout)
        arr.append(setUpDefences)
        arr.append(withdrawGarrision)
        arr.append(doorOpen)
        arr.append(doorClose)
        arr.append(systemStart)
        arr.append(trailCarAlarm)
        arr.append(locationTooLong)
        arr.append(terminalPullOut)
        arr.append(terminalInsert)
        arr.append(lowVoltage)
        arr.append(idlingSpeedOver)
        arr.append(overspeedAlarm)
        arr.append(fatigueDriving)
        arr.append(waterTemperatureAlarm)
        arr.append(highSpeedNeutralGear)
        arr.append(oilExpendNotSurport)
        arr.append(OBDNotSurport)
        arr.append(lowWaterTemperatureHighSpeed)
        arr.append(buslineNotSleep)
        arr.append(illegalOpenDoor)
        arr.append(illegalFire)
        arr.append(rapidAccelerateAlarm)
        arr.append(sharpSlowdownAlarm)
        arr.append(sharpBendAlarm)
        arr.append(crashAlarm)
        arr.append(rapidChangeLines)
        arr.append(sharpRightBendAlarm)
        mult = self.getRandomNum(0, 29)
        temp = []
        for i in range(0, mult):
            con = self.getRandomNum(intArr=arr, mult=1)
            if con in temp:
                con = ""
            temp.append(con)
            data = data + con
        return data

    #####################################################
    # 获取怠速过长附带信息
    #####################################################
    def getIdlingSpeedOver(self):
        #报警属性  1：报警触发（无下面的数据内容项）0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(1)
        #怠速持续时间  怠速持续的时间（含报警前的预判时间），单位为秒
        idlingTimeOfDuration = self.int2hexStringByBytes(600,2)
        #怠速耗油量	单位 mL
        idlingOilExpend = self.int2hexStringByBytes(1200,2)
        #怠速最高转速	单位 RPM
        idlingEngineMaxSpeed = self.int2hexStringByBytes(5000,2)
        #怠速最低转速	单位 RPM
        idlingEngineMinSpeed = self.int2hexStringByBytes(500,2)
        data = alarmType + idlingTimeOfDuration + idlingOilExpend + idlingEngineMaxSpeed + idlingEngineMinSpeed
        return data
    def getIdlingSpeedOver_GUI(self,data):
        #报警属性  1：报警触发（无下面的数据内容项）0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(int(data["alarmType"]))
        #怠速持续时间  怠速持续的时间（含报警前的预判时间），单位为秒
        idlingTimeOfDuration = self.int2hexStringByBytes(int(data["idlingTimeOfDuration"]),2)
        #怠速耗油量	单位 mL
        idlingOilExpend = self.int2hexStringByBytes(int(data["idlingOilExpend"]),2)
        #怠速最高转速	单位 RPM
        idlingEngineMaxSpeed = self.int2hexStringByBytes(int(data["idlingEngineMaxSpeed"]),2)
        #怠速最低转速	单位 RPM
        idlingEngineMinSpeed = self.int2hexStringByBytes(int(data["idlingEngineMinSpeed"]),2)
        data = alarmType + idlingTimeOfDuration + idlingOilExpend + idlingEngineMaxSpeed + idlingEngineMinSpeed
        return data
    def getIdlingSpeedOver_random(self):
        #报警属性  1：报警触发（无下面的数据内容项）0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))
        #怠速持续时间  怠速持续的时间（含报警前的预判时间），单位为秒
        idlingTimeOfDuration = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #怠速耗油量	单位 mL
        idlingOilExpend = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #怠速最高转速	单位 RPM
        idlingEngineMaxSpeed = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #怠速最低转速	单位 RPM
        idlingEngineMinSpeed = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        data = alarmType + idlingTimeOfDuration + idlingOilExpend + idlingEngineMaxSpeed + idlingEngineMinSpeed
        return data

    #####################################################
    # 获取超速报警信息
    #####################################################
    def getOverspeedAlarm(self):
        #报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(0)
        #超速持续时间	2	WORD	怠速持续的时间（含报警前的预判时间），单位为秒
        overspeedTimeOfDuration = self.int2hexStringByBytes(700,2)
        #最高车速	2	WORD	单位 0.1KM/H
        maxSpeed = self.int2hexStringByBytes(145,2)
        #平均车速	2	WORD	单位 0.1KM/H
        averageSpeed = self.int2hexStringByBytes(70,2)
        #超速行驶距离	2	WORD	单位米
        overspeedDistance = self.int2hexStringByBytes(10000,2)
        data = alarmType + overspeedTimeOfDuration + maxSpeed + averageSpeed + overspeedDistance
        return data
    def getOverspeedAlarm_GUI(self,data):
        #报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(int(data["alarmType"]))
        #超速持续时间	2	WORD	怠速持续的时间（含报警前的预判时间），单位为秒
        overspeedTimeOfDuration = self.int2hexStringByBytes(int(data["overspeedTimeOfDuration"]),2)
        #最高车速	2	WORD	单位 0.1KM/H
        maxSpeed = self.int2hexStringByBytes(int(data["maxSpeed"]),2)
        #平均车速	2	WORD	单位 0.1KM/H
        averageSpeed = self.int2hexStringByBytes(int(data["averageSpeed"]),2)
        #超速行驶距离	2	WORD	单位米
        overspeedDistance = self.int2hexStringByBytes(int(data["overspeedDistance"]),2)
        data = alarmType + overspeedTimeOfDuration + maxSpeed + averageSpeed + overspeedDistance
        return data
    def getOverspeedAlarm_random(self):
        #报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))
        #超速持续时间	2	WORD	怠速持续的时间（含报警前的预判时间），单位为秒
        overspeedTimeOfDuration = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #最高车速	2	WORD	单位 0.1KM/H
        maxSpeed = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #平均车速	2	WORD	单位 0.1KM/H
        averageSpeed = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #超速行驶距离	2	WORD	单位米
        overspeedDistance = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        data = alarmType + overspeedTimeOfDuration + maxSpeed + averageSpeed + overspeedDistance
        return data

    #####################################################
    # 获取疲劳驾驶报警附带信息
    #####################################################
    def getFatigueDriving(self):
        #报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(0)
        #累计持续驾驶时间	4	DWORD	车辆点火行驶到报警解除的累计行驶时间，单位为秒
        totalContinueDrivingTime = self.int2hexStringByBytes(21000,4)
        data = alarmType + totalContinueDrivingTime
        return data
    def getFatigueDriving_GUI(self,data):
        #报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(int(data["alarmType"]))
        #累计持续驾驶时间	4	DWORD	车辆点火行驶到报警解除的累计行驶时间，单位为秒
        totalContinueDrivingTime = self.int2hexStringByBytes(int(data["totalContinueDrivingTime"]),4)
        data = alarmType + totalContinueDrivingTime
        return data
    def getFatigueDriving_random(self):
        #报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))
        #累计持续驾驶时间	4	DWORD	车辆点火行驶到报警解除的累计行驶时间，单位为秒
        totalContinueDrivingTime = self.int2hexStringByBytes(self.getRandomNum(0,2147483648),4)
        data = alarmType + totalContinueDrivingTime
        return data

    #####################################################
    # 获取水温报警附带信息
    #####################################################
    def getWaterTemperatureAlarm(self):
        # 报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(1)
        # 持续时长	4	DWORD	单位秒
        timeOfDuration = self.int2hexStringByBytes(11000,4)
        # 最高温度	2	WORD	单位 0.1 度
        maxTemperature = self.int2hexStringByBytes(700,2)
        # 平均温度	2	WORD	单位 0.1 度
        averageTemperature = self.int2hexStringByBytes(55,2)
        data = alarmType + timeOfDuration + maxTemperature + averageTemperature
        return data
    def getWaterTemperatureAlarm_GUI(self,data):
        # 报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(int(data["alarmType"]))
        # 持续时长	4	DWORD	单位秒
        timeOfDuration = self.int2hexStringByBytes(int(data["timeOfDuration"]),4)
        # 最高温度	2	WORD	单位 0.1 度
        maxTemperature = self.int2hexStringByBytes(int(data["maxTemperature"]),2)
        # 平均温度	2	WORD	单位 0.1 度
        averageTemperature = self.int2hexStringByBytes(int(data["averageTemperature"]),2)
        data = alarmType + timeOfDuration + maxTemperature + averageTemperature
        return data
    def getWaterTemperatureAlarm_random(self):
        # 报警属性	1	BYTE	1：报警触发（无下面的数据内容项） 0：报警解除（有下面的数据内容项）
        alarmType = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))
        # 持续时长	4	DWORD	单位秒
        timeOfDuration = self.int2hexStringByBytes(self.getRandomNum(0,2147483648),4)
        # 最高温度	2	WORD	单位 0.1 度
        maxTemperature = self.int2hexStringByBytes(self.getRandomNum(0,2500),2)
        # 平均温度	2	WORD	单位 0.1 度
        averageTemperature = self.int2hexStringByBytes(self.getRandomNum(0,1500),2)
        data = alarmType + timeOfDuration + maxTemperature + averageTemperature
        return data

if __name__ == "__main__":
    print(AlarmEvent_data().generateAlarmEvent_data())





