#encoding:utf-8

'''
定义轿车OBD数据
'''
from lib.protocol.message.MessageBase import MessageBase


class TruckCarOBD_data(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #####################################################
    # 创建轿车OBD数据
    #####################################################
    def generateTruckCarOBD_data(self):
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
        intakeManifoldPressure = "60B0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(20)
        #大气压力 , 0 - 125kpa
        atmosphericPressure = "6330" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(28)
        #环境温度 ， -40.0℃ 到 +210℃,上传值减去 40
        envTemperature = "6460" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(65)
        #加速踏板位置 ， 0% - 100%
        acceleratorLocation = "6490" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(32)
        #燃油压力 ， 0 - 500kpa
        oilPressure = "60A0" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(276,2)
        #故障码个数
        troubleCodeNum = "6010" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(2)
        #OBD 离合器开关 ,0x00/0x01	关/开
        clutchSwitch = "5001" + self.int2hexStringByBytes(1) + "01"
        #OBD 制动刹车开关 , 0x00/0x01	关/开
        brakeSwich = "5002" + self.int2hexStringByBytes(1) + "01"
        #OBD 驻车刹车开关 , 0x00/0x01	关/开
        parkingBrakeSwitch = "5003" + self.int2hexStringByBytes(1) + "01"
        #OBD 节流阀位置 , 0% - 100%
        throttleLocation =  "5004" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(33)
        #OBD 油料使用率 , 0 - 3212.75L／h
        oilUsageRate = "5005" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(1000,2)
        #OBD 燃油温度 , 起始值-273℃ 范围(-273 到+1735)
        oilTemperature = "5006" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(299,2)
        #OBD 机油温度 , 起始值-273℃ 范围(-273 到+1735)
        engineOilTemperature = "5007" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(300,2)
        #OBD 发动机润滑油压力 , 0 - 1000kpa
        engineOilPresure = "5008" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(120)
        #OBD 制动器踏板位置 , 0% - 100%
        brekeLocation = "5009" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(31)
        #OBD 空气流量 , 0.1	G/S
        airFlow = "500A" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(800,2)

        data = data + engineSpeed + carSpeed + surplusOil + coolingLiquidTemperature + airInletTemperature
        data = data + intakeManifoldPressure + atmosphericPressure + envTemperature + acceleratorLocation + oilPressure
        data = data + troubleCodeNum + clutchSwitch + brakeSwich + parkingBrakeSwitch + throttleLocation
        data = data + oilUsageRate + oilTemperature + engineOilTemperature + engineOilPresure + brekeLocation
        data = data + airFlow
        return data

    #####################################################
    # 获取剩余油量
    #####################################################
    def getSurplusOil(self):
        # 剩余油量 ，剩余油量，单位 L 或%Bit15=0 百分比%，OBD 都为百分比Bit15=1 单位 L，显示值为上传值/10   (32768)
        units = 32768
        surplusOil = 800
        data = units + surplusOil
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex


if __name__ == "__main__":
    print(TruckCarOBD_data().generateTruckCarOBD_data())