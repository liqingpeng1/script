#coding:utf-8

'''
定义一个终端上报OBD适配信息
'''

from lib.protocol.report.ProtocolBase import ProtocolBase


class OBDReport_protocol(ProtocolBase):
    def __init__(self):
        pass

    #####################################################
    #               生成OBD终端上报配置信息
    #####################################################
    def generateOBDReportMsg(self):
        self.getProtocalHeader()
        info = ""
        #消息头
        HEADER = "4040"
        #消息流水号
        WATER_CODE = self.getWaterCode(1000)
        #设备id
        DEV_ID = self.devid2hexString("M121501010001")
        # 功能id(GPS功能id)
        FUN_ID = "0008"
        #数据段
        data = self.generateOBDData()
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
    #               生成OBD终端上报数据包
    #####################################################
    def generateOBDData(self):
        data = ""
        #每条信息默认带两个字节
        default = "0000"
        #获取协议类型
        protocolType =  self.getProtocolTypeHex()
        #读码方式
        readType = self.getReadTypeHex()
        #防盗协议
        securityProtocal = self.getSecurityProtocalHex()
        #车型ID
        carId = self.getCarIdHex()
        #帧与帧间隔
        frameInterval = self.getFrameIntervalHex(100)
        #ECU地址
        ECU = self.getECUHex()
        #油耗系数
        oilExpend = self.getOilExpendHex(999)
        #里程系数
        mileageCoefficient = self.getMileageCoefficientHex(888)
        #排量
        displacement = self.getDisplacementHex(80)
        #油品密度
        oilDensity = self.getOilDensityHex()
        #油耗计算方法
        oilCalculateMode = self.getOilCalculateModeHex()
        #数据流读取时间
        dataFlowTime = self.getDataFlowTimeHex(60)
        #换车标志
        carSign = self.getCarSignHex()
        #车辆动力类型
        carPowerMode = self.getCarPowerModeHex()
        #最大扭矩
        maxTorque = self.getMaxTorqueHex(1000)
        #发动机缸数
        engineJar = self.getEngineJarHex(8)
        #满载电量
        fullElec = self.getFullElecHex(400)
        #里程协议编号
        mileageNum = self.getMileageNumHex()
        #OBD扫描方式
        OBDScanWay = self.getOBDScanWayHex(2)
        #保留数据
        retainData = self.getRetainDataHex()

        # data = data + default + protocolType + readType + securityProtocal + carId + frameInterval
        # data = data + ECU + oilExpend + mileageCoefficient + displacement + oilDensity + oilCalculateMode
        # data = data + dataFlowTime + carSign + carPowerMode + maxTorque + engineJar + fullElec
        # data = data + mileageNum + OBDScanWay + retainData

        data = data + default + "01" + protocolType + "02" + readType + "03" + securityProtocal + "04" + carId + "05" + frameInterval
        data = data + "06" + ECU + "07" + oilExpend + "08" + mileageCoefficient + "09" + displacement + "0A" + oilDensity + "0B" + oilCalculateMode
        data = data + "0C" + dataFlowTime + "0D" + carSign + "0E" + carPowerMode + "0F" + maxTorque + "10" + engineJar + "11" + fullElec
        data = data + "12" + mileageNum + "13" + OBDScanWay + "14" + retainData

        return data

    #####################################################

    #               获取协议类型的16进制数据
    #####################################################
    def getProtocolTypeHex(self):
        #非以下数据，其他数据为无效或错误数据，0x0000为无效数据
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
        VW_UDS = "0205"
        #禁止 / 不支持OBD功能[车机禁止访问ECU]
        FORBID = "FFFE"
        #车机自动扫描
        AUTO = "FFFF"
        return OBD_ST_HCAN

    #####################################################
    #               获取读码方式的16进制数据
    #####################################################
    def getReadTypeHex(self):
        #无效数据:0x00
        #不读取故障码
        NO_READ = "01"
        #15s读取故障码
        READ = "02"
        return READ

    #####################################################
    #               获取防盗协议的16进制数据
    #####################################################
    def getSecurityProtocalHex(self):
        #无效数据:0x00000000
        #有效数据: 0x00000001~0X000000FE:
        return "00000001"

    #####################################################
    #               获取车型id的16进制数据
    ####################################################
    def getCarIdHex(self):
        #无效数据:0x00000000 , 错误数据:其他值为错误数据
        FENG_TIAN = "00001E00"    #丰田
        BEND_TIAN = "00000900"    #本田
        RI_CHAN = "00004900"      #日产
        TONG_YONG = "00000C00"    #通用
        FU_TE = "00001F00"        #福特
        DA_ZHONG = "00001500"     #大众、奥迪、西雅特、斯柯达
        ZHONG_HUA = "00005E00"    #中华
        BI_YA_DI = "00000A00"     #比亚迪
        JIANG_HUAI = "00002C00"   #江淮
        BIAO_ZHI = "00000B00"     #标致（3008）
        DEFAULT = "0000FF00"      #出场默认车型
        return BI_YA_DI

    #####################################################
    #               获取帧与帧间隔的16进制数据
    #               无效数据:0
    #               有效数据:50~5000(单位MS)
    #               错误数据:其他值为错误数据
    ####################################################
    def getFrameIntervalHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取ECU地址的16进制数据
    #               无效数据:0x00000000
    #               有效数据:0x00000001~0xFFFFFFFF
    #               错误数据:其他
    ####################################################
    def getECUHex(self):
        return "00000001"

    #####################################################
    #               获取油耗系数的16进制数据
    #               无效数据: 0
    #               有效数据: 1~1000
    #               错误数据:其他
    ##################################################
    def getOilExpendHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取里程系数的16进制数据
    #               无效数据:0
    #               有效数据:1~1000
    #               错误数据:其他
    ##################################################
    def getMileageCoefficientHex(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取排量的16进制数据
    #               排量：实际值=设置值/10
    #               无效数据:0
    #               有效数据:5~100
    #               错误数据:其他
    #####################################################
    def getDisplacementHex(self,num):
        hexData = self.int2hexString(num)
        return hexData

    #####################################################
    #               获取油耗密度的16进制数据
    #####################################################
    def getOilDensityHex(self):
        CAI_YOU_0 = 835       #柴油0#
        CAI_YOU_10 = 840      #柴油10#
        CAI_YOU_20 = 830      #柴油20#
        CAI_YOU_5 = 840       #柴油5#
        CAI_YOU_35 = 820      #柴油35
        CAI_YOU_50 = 816      #柴油50#
        QI_YOU_90 = 722       #汽油90#
        QI_YOU_93 = 725       #汽油93#
        QI_YOU_97 = 737       #汽油97#
        QI_YOU_98 = 753       #汽油98#

        num = QI_YOU_93
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取油耗计算方式16进制数据
    #               无效数据:0x00;
    #               错误数据:其他
    #####################################################
    def getOilCalculateModeHex(self):
        MOMENT_OIL = "01"         #瞬时油耗算法
        AIR_FLOW = "02"           #空气流量算法
        INTO_STRESS = "03"        #进气歧管压力算法
        ENGINE_LOAD = "04"        #发动机绝对负荷算法
        GAS_DOOR = "05"           #节气门算法
        CAR_SPEED = "06"          #车速模拟算法
        ROTATE_SPEED = "07"       #车速转速模拟算法
        METER_OIL = "08"          #仪表油耗算累计油耗
        GUSH_OIL = "09"           #喷油量算累计油耗
        ENGINE_TORQUE = "0A"      #发动机实际扭矩
        ENGINE_TORQUE_PERSENT = "0B"   #发动机扭矩百分比

        return AIR_FLOW

    #####################################################
    #               获取数据流读取时间的16进制数据
    #               无读取数据流时间，单位秒；
    #               无效数据:0
    #               有效数据:30~200（默认30）
    #               错误数据:其他
    #####################################################
    def getDataFlowTimeHex(self,num=30):
        hexData = self.int2hexString(num)
        return hexData

    #####################################################
    #               获取换车标志16进制数据
    #               用于平台下发OBD适配信息时，标识当前车机是否已换车：
    #               无效数据:0x00
    #               错误数据:其他
    #####################################################
    def getCarSignHex(self):
        INDETERMINATION = "01"   #未确定
        NO_CHANGE = "02"         #未换车
        CHANGED = "03"           #已换车

        return NO_CHANGE

    #####################################################
    #               获取车辆动力类型16进制数据
    #               用于平台下发OBD适配信息时，标识车辆动力类型：
    #               无效数据:0x00
    #               错误数据:其他
    #####################################################
    def getCarPowerModeHex(self):
        FIRE_ENGINE = "01"        #内燃机
        FIRE_ELEC = "02"          #油电混合
        ONlY_ELEC = "03"          #纯电动车

        return FIRE_ELEC

    #####################################################
    #               发动机最大扭矩
    #               无效数据:0
    #               有效数据:100~5000（默认800）
    #               错误数据:其他；
    #####################################################
    def getMaxTorqueHex(self,num = 800):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               发动机气缸数
    #               无效数据:0
    #               有效数据:3~12（默认6）
    #               错误数据:其他；
    #####################################################
    def getEngineJarHex(self,num = 6):
        hexData = self.int2hexString(num)
        return hexData

    #####################################################
    #               电动车满载电量
    #               无效数据:0
    #               有效数据:10~1000（默认200）
    #               错误数据:其他；
    #####################################################
    def getFullElecHex(self,num = 200):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               里程协议编号
    #               无效数据:0
    #               有效数据：
    #               1~0xfe:具体的某个里程协议
    #               0xff:自动扫描里程协议
    #              有效数据:1-0xff（默认0xff:自动扫描里程协议）
    #              错误数据:无；；
    #####################################################
    def getMileageNumHex(self):
        return "ff"

    #####################################################
    #               OBD扫描优先方式
    #              有效数据:0~4（默认0）
    #              错误数据: 其他
    #####################################################
    def getOBDScanWayHex(self,num=0):
        hexData = self.int2hexString(num)
        return hexData

    #####################################################
    #               保留数据字节：0x00000000
    #####################################################
    def getRetainDataHex(self):
        return "00000000"






if __name__ == "__main__":
    # print(OBDReport_protocol().getDisplacementHex(2))
    print(OBDReport_protocol().generateOBDData())
    print(OBDReport_protocol().generateOBDReportMsg())






