#encoding:utf-8

'''
定义新能源车 OBD 数据
'''
from lib.protocol.message.MessageBase import MessageBase


class NewEnergyCar_data(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #####################################################
    # 创建轿车OBD数据
    #####################################################
    def generateNewEnergyCar_data(self):
        data = ""
        #续航里程 , 0.1km	显示值为上传值/10
        enduranceMileage = "7001" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(22000,4)
        #剩余电量 , 0% - 100%
        surplusPower = "7002" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(55)
        #车速 , Km/h	0 - 240
        speed = "7003" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(74)
        #充电状态
        #0x0: 初始值
        # 0x1: 未充电
        # 0x2: 交流充电中
        # 0x3: 直流充电中
        # 0x4: 充电完成 0x5: Void 0x6: Void 0x7: 无效值
        chargeStatus = "7004" + self.int2hexStringByBytes(1) + "01"
        #充电桩状态 , 0x01:插入  0x00:未插入
        chargingPileStatus = "7005" + self.int2hexStringByBytes(1) + "00"
        #动力电池充放电电流	0.01A	0x0-0xFFFF
        batteryStream = "7006" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(30,2)
        #单体电芯最高电压	0．001V	0x0-0xFFFF
        batteryMaxVoltage_1 = "7007" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(7000,2)
        # 单体电芯最高电压	0．001V	0x0-0xFFFF
        batteryMaxVoltage_2 = "7008" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(7000, 2)
        #驱动电机当前转速	Rpm
        electromotorSpeed = "7009" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(5000,2)
        #驱动电机当前转矩	Nm
        electromotorTorque = "700a" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(2000,2)
        #驱动电机当前温度	C	上传值减去 40
        electromotorTemperature = "700b" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(90)
        #直流母线电压	0.001V	0x0-0xFFFF
        DCBusVotage = "700c" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(3000,2)
        #直流母线电流	0.01A	0x0-0xFFFF
        DCBusStream = "700d" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(36,2)
        #动力电池可用能量	0.01Kwh	0x0-0xFFFF
        batteryAvailablePower = "700e" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(30000,2)
        #1 号单体电池电压	V
        batteryVotage_1 = "7021" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_2 = "7022" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_3 = "7023" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_4 = "7024" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_5 = "7025" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_6 = "7026" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_7 = "7027" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_8 = "7028" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_9 = "7029" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        batteryVotage_10 = "702A" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)

        data = data + enduranceMileage + surplusPower + speed + chargeStatus + chargingPileStatus
        data = data + batteryStream + batteryMaxVoltage_1 + batteryMaxVoltage_2 + electromotorSpeed + electromotorTorque
        data = data + electromotorTemperature + DCBusVotage + DCBusStream + batteryAvailablePower + batteryVotage_1
        data = data + batteryVotage_2 + batteryVotage_3 + batteryVotage_4 + batteryVotage_5 + batteryVotage_6
        data = data + batteryVotage_7 + batteryVotage_8 + batteryVotage_9 + batteryVotage_10
        return data

if __name__ == "__main__":
    print(NewEnergyCar_data().generateNewEnergyCar_data())