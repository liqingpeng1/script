#encoding:utf-8

'''
定义轿车OBD数据
'''
from lib.protocol.message.MessageBase import MessageBase


class SaloonCarOBD_data(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #####################################################
    # 创建轿车OBD数据
    #####################################################
    def generateSaloonCarOBDData(self):
        data = ""
        #发动机转速 , 0 - 8000  rpm
        engineSpeed = "60C0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(3000,2)
        #车速 ， 0 - 240 Km/h
        carSpeed = "60D0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(60)
        #剩余油量 ，剩余油量，单位 L 或%Bit15=0 百分比%，OBD 都为百分比Bit15=1 单位 L，显示值为上传值/10
        surplusOil = "62f0" + self.int2hexStringByBytes(2) + self.getSurplusOil()
        #冷却液温度 ，-40.0℃ 到 +210℃,上传值减去 40
        coolingLiquidTemperature = "6050" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(76)
        #进气口温度 ，-40.0℃ 到 +210℃,上传值减去 40
        airInletTemperature = "60F0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(88)
        #进气(岐管绝对)压力 , 0 - 250kpa
        intakeManifoldPressure = "60B0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(20)
        #大气压力 , 0 - 125kpa
        atmosphericPressure = "6330" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(28)
        #环境温度 ， -40.0℃ 到 +210℃,上传值减去 40
        envTemperature = "6460" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(65)
        #加速踏板位置 ， 0% - 100%
        acceleratorLocation = "6490" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(32)
        #燃油压力 ， 0 - 500kpa
        oilPressure = "60A0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(276,2)
        #故障码状态 ， 发动机故障码状态
        troubleCodeStatus = "6014" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(0)
        #故障码个数
        troubleCodeNum = "6010" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(2)
        #空气流量 ， 0.1	实际值为上传值/10 0.1g/s
        airFlow = "6100" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(550,2)
        #绝对气门位置
        valveLocation = "6110" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(51,2)
        #自发动机启动运行时间 sec
        engineRunTime = "61F0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(3700,2)
        #故障行驶里程 ， Km
        troubleMileage = "6210" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(4508,4)
        #计算负荷值
        calculateLoadValue = "6040" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(44)
        #长期燃油修正(气缸列 1 和 3)
        fuelTrim = "6070" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(89,2)
        #第一缸点火正时提前角 ,显示值为上传值-64
        fireAngle = "60E0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(154,2)
        #前刹车片磨损 , 0 正常/否则，显示对应数据，单位：级
        frontBrakeBlockAbrasion = "6701" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(0)
        #后刹车片磨损 , 0 正常/否则，显示对应数据，单位：级
        backBrakeBlockAbrasion = "6702" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(0)
        #制动液液位 , 0：不正 1：正常 其他：无法使用
        brakeFluidLocation = "6703" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(1)
        #机油液位 , 显示值为上传值/1000 单位 毫米
        engineOilLocation = "6704" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(20000,2)
        #胎压报警 0：当前无警告   1：存在胎压失压 其他：不可用
        tirePressureAlarm = "6705" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(0,2)
        #冷却液液位 , 显示值为上传值-48
        coolingLiquidLocation = "6706" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(65,2)
        #续航里程 0.1 km ; 显示值为上传值/10
        enduranceMileage = "6707" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(382,4)
        #仪表里程
        dashboardMileage = "6708" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3500,4)
        #车辆总运行时间
        runTotalTime = "6709" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(7200000,4)
        #总耗油量
        totalOilExpend = "670a" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3700000,4)
        #OBD 累计里程，不支持 OBD 时，为基于 GPS 车速统计的车辆累计行驶总里程
        OBDTotalMileage = "670b" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(123000,4)


        data = data + engineSpeed + carSpeed + surplusOil + coolingLiquidTemperature + airInletTemperature
        data = data + intakeManifoldPressure + atmosphericPressure + envTemperature + acceleratorLocation + oilPressure
        data = data + troubleCodeStatus + troubleCodeNum + airFlow + valveLocation + engineRunTime
        data = data + troubleMileage + calculateLoadValue + fuelTrim + fireAngle + frontBrakeBlockAbrasion
        data = data + backBrakeBlockAbrasion + brakeFluidLocation + engineOilLocation + tirePressureAlarm + coolingLiquidLocation
        data = data + enduranceMileage + dashboardMileage + runTotalTime + totalOilExpend + OBDTotalMileage
        return data
    def generateSaloonCarOBDData_GUI(self,data):
        dataHex = ""
        if ("60C0" in data.keys()):
            #发动机转速 , 0 - 8000  rpm
            engineSpeed = "60C0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["60C0"]),2)
            dataHex = dataHex + engineSpeed
        if ("60D0" in data.keys()):
            #车速 ， 0 - 240 Km/h
            carSpeed = "60D0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["60D0"]))
            dataHex = dataHex + carSpeed
        if ("62f0" in data.keys()):
            #剩余油量 ，剩余油量，单位 L 或%Bit15=0 百分比%，OBD 都为百分比Bit15=1 单位 L，显示值为上传值/10
            surplusOil = "62f0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["62f0"]),2)
            dataHex = dataHex + surplusOil
        if ("6050" in data.keys()):
            #冷却液温度 ，-40.0℃ 到 +210℃,上传值减去 40
            coolingLiquidTemperature = "6050" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6050"]))
            dataHex = dataHex + coolingLiquidTemperature
        if ("60F0" in data.keys()):
            #进气口温度 ，-40.0℃ 到 +210℃,上传值减去 40
            airInletTemperature = "60F0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["60F0"]))
            dataHex = dataHex + airInletTemperature
        if ("60B0" in data.keys()):
            #进气(岐管绝对)压力 , 0 - 250kpa
            intakeManifoldPressure = "60B0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["60B0"]))
            dataHex = dataHex + intakeManifoldPressure
        if ("6330" in data.keys()):
            #大气压力 , 0 - 125kpa
            atmosphericPressure = "6330" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6330"]))
            dataHex = dataHex + atmosphericPressure
        if ("6460" in data.keys()):
            #环境温度 ， -40.0℃ 到 +210℃,上传值减去 40
            envTemperature = "6460" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6460"]))
            dataHex = dataHex + envTemperature
        if ("6490" in data.keys()):
            #加速踏板位置 ， 0% - 100%
            acceleratorLocation = "6490" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6490"]))
            dataHex = dataHex + acceleratorLocation
        if ("60A0" in data.keys()):
            #燃油压力 ， 0 - 500kpa
            oilPressure = "60A0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["60A0"]),2)
            dataHex = dataHex + oilPressure
        if ("6014" in data.keys()):
            #故障码状态 ， 发动机故障码状态
            troubleCodeStatus = "6014" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6014"]))
            dataHex = dataHex + troubleCodeStatus
        if ("6010" in data.keys()):
            #故障码个数
            troubleCodeNum = "6010" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6010"]))
            dataHex = dataHex + troubleCodeNum
        if ("6100" in data.keys()):
            #空气流量 ， 0.1	实际值为上传值/10 0.1g/s
            airFlow = "6100" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["6100"]),2)
            dataHex = dataHex + airFlow
        if ("6110" in data.keys()):
            #绝对气门位置
            valveLocation = "6110" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["6110"]),2)
            dataHex = dataHex + valveLocation
        if ("61F0" in data.keys()):
            #自发动机启动运行时间 sec
            engineRunTime = "61F0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["61F0"]),2)
            dataHex = dataHex + engineRunTime
        if ("6210" in data.keys()):
            #故障行驶里程 ， Km
            troubleMileage = "6210" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["6210"]),4)
            dataHex = dataHex + troubleMileage
        if ("6040" in data.keys()):
            #计算负荷值
            calculateLoadValue = "6040" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6040"]))
            dataHex = dataHex + calculateLoadValue
        if ("6070" in data.keys()):
            #长期燃油修正(气缸列 1 和 3)
            fuelTrim = "6070" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["6070"]),2)
            dataHex = dataHex + fuelTrim
        if ("60E0" in data.keys()):
            #第一缸点火正时提前角 ,显示值为上传值-64
            fireAngle = "60E0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["60E0"]),2)
            dataHex = dataHex + fireAngle
        if ("6701" in data.keys()):
            #前刹车片磨损 , 0 正常/否则，显示对应数据，单位：级
            frontBrakeBlockAbrasion = "6701" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6701"]))
            dataHex = dataHex + frontBrakeBlockAbrasion
        if ("6702" in data.keys()):
            #后刹车片磨损 , 0 正常/否则，显示对应数据，单位：级
            backBrakeBlockAbrasion = "6702" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6702"]))
            dataHex = dataHex + backBrakeBlockAbrasion
        if ("6703" in data.keys()):
            #制动液液位 , 0：不正 1：正常 其他：无法使用
            brakeFluidLocation = "6703" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["6703"]))
            dataHex = dataHex + brakeFluidLocation
        if ("6704" in data.keys()):
            #机油液位 , 显示值为上传值/1000 单位 毫米
            engineOilLocation = "6704" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["6704"]),2)
            dataHex = dataHex + engineOilLocation
        if ("6705" in data.keys()):
            #胎压报警 0：当前无警告   1：存在胎压失压 其他：不可用
            tirePressureAlarm = "6705" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["6705"]),2)
            dataHex = dataHex + tirePressureAlarm
        if ("6706" in data.keys()):
            #冷却液液位 , 显示值为上传值-48
            coolingLiquidLocation = "6706" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["6706"]),2)
            dataHex = dataHex + coolingLiquidLocation
        if ("6707" in data.keys()):
            #续航里程 0.1 km ; 显示值为上传值/10
            enduranceMileage = "6707" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["6707"]),4)
            dataHex = dataHex + enduranceMileage
        if ("6708" in data.keys()):
            #仪表里程
            dashboardMileage = "6708" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["6708"]),4)
            dataHex = dataHex + dashboardMileage
        if ("6709" in data.keys()):
            #车辆总运行时间
            runTotalTime = "6709" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["6709"]),4)
            dataHex = dataHex + runTotalTime
        if ("670a" in data.keys()):
            #总耗油量
            totalOilExpend = "670a" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["670a"]),4)
            dataHex = dataHex + totalOilExpend
        if ("670b" in data.keys()):
            #OBD 累计里程
            OBDTotalMileage = "670b" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["670b"]),4)
            dataHex = dataHex + OBDTotalMileage
        return dataHex
    def generateSaloonCarOBDData_random(self):
        data = ""
        #发动机转速 , 0 - 8000  rpm
        engineSpeed = "60C0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,8000),2)
        #车速 ， 0 - 240 Km/h
        carSpeed = "60D0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,240))
        #剩余油量 ，剩余油量，单位 L 或%Bit15=0 百分比%，OBD 都为百分比Bit15=1 单位 L，显示值为上传值/10
        surplusOil = "62f0" + self.int2hexStringByBytes(2) + self.getSurplusOil_random()
        #冷却液温度 ，-40.0℃ 到 +210℃,上传值减去 40
        coolingLiquidTemperature = "6050" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,250))
        #进气口温度 ，-40.0℃ 到 +210℃,上传值减去 40
        airInletTemperature = "60F0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,250))
        #进气(岐管绝对)压力 , 0 - 250kpa
        intakeManifoldPressure = "60B0" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,250))
        #大气压力 , 0 - 125kpa
        atmosphericPressure = "6330" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,125))
        #环境温度 ， -40.0℃ 到 +210℃,上传值减去 40
        envTemperature = "6460" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,250))
        #加速踏板位置 ， 0% - 100%
        acceleratorLocation = "6490" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,100))
        #燃油压力 ， 0 - 500kpa
        oilPressure = "60A0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,500),2)
        #故障码状态 ， 发动机故障码状态
        troubleCodeStatus = "6014" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))
        #故障码个数
        troubleCodeNum = "6010" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        #空气流量 ， 0.1	实际值为上传值/10 0.1g/s
        airFlow = "6100" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #绝对气门位置
        valveLocation = "6110" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #自发动机启动运行时间 sec
        engineRunTime = "61F0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #故障行驶里程 ， Km
        troubleMileage = "6210" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,2147483648),4)
        #计算负荷值
        calculateLoadValue = "6040" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        #长期燃油修正(气缸列 1 和 3)
        fuelTrim = "6070" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #第一缸点火正时提前角 ,显示值为上传值-64
        fireAngle = "60E0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65435),2)
        #前刹车片磨损 , 0 正常/否则，显示对应数据，单位：级
        frontBrakeBlockAbrasion = "6701" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        #后刹车片磨损 , 0 正常/否则，显示对应数据，单位：级
        backBrakeBlockAbrasion = "6702" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        #制动液液位 , 0：不正 1：正常 其他：无法使用
        brakeFluidLocation = "6703" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))
        #机油液位 , 显示值为上传值/1000 单位 毫米
        engineOilLocation = "6704" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #胎压报警 0：当前无警告   1：存在胎压失压 其他：不可用
        tirePressureAlarm = "6705" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]),2)
        #冷却液液位 , 显示值为上传值-48
        coolingLiquidLocation = "6706" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65435),2)
        #续航里程 0.1 km ; 显示值为上传值/10
        enduranceMileage = "6707" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,2147483648),4)
        #仪表里程
        dashboardMileage = "6708" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,3500),4)
        #车辆总运行时间
        runTotalTime = "6709" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,7200000),4)
        #总耗油量
        totalOilExpend = "670a" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,3700000),4)
        #OBD 累计里程
        OBDTotalMileage = "670b" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0, 3700000), 4)

        data = data + engineSpeed + carSpeed + surplusOil + coolingLiquidTemperature + airInletTemperature
        data = data + intakeManifoldPressure + atmosphericPressure + envTemperature + acceleratorLocation + oilPressure
        data = data + troubleCodeStatus + troubleCodeNum + airFlow + valveLocation + engineRunTime
        data = data + troubleMileage + calculateLoadValue + fuelTrim + fireAngle + frontBrakeBlockAbrasion
        data = data + backBrakeBlockAbrasion + brakeFluidLocation + engineOilLocation + tirePressureAlarm + coolingLiquidLocation
        data = data + enduranceMileage + dashboardMileage + runTotalTime + totalOilExpend + OBDTotalMileage
        return data

    #####################################################
    # 获取剩余油量
    #####################################################
    def getSurplusOil(self):
        # 剩余油量 ，剩余油量，单位L或% ; Bit15=0 百分比%，OBD都为百分比 ;Bit15=1 单位 L，显示值为上传值/10   (32768)
        units = 0
        surplusOil = 801
        data = units + surplusOil
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex
    def getSurplusOil_random(self):
        # 剩余油量 ，剩余油量，单位L或% ; Bit15=0 百分比%，OBD都为百分比 ;Bit15=1 单位 L，显示值为上传值/10   (32768)
        units = self.getRandomNum(intArr=[0,32768])
        surplusOil = self.getRandomNum(0,16384)
        data = units + surplusOil
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex


if __name__ == "__main__":
    print(SaloonCarOBD_data().generateSaloonCarOBDData())