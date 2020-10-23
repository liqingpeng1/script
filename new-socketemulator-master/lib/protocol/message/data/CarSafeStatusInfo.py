#encoding:utf-8

'''
定义安防状态信息
'''
from lib.protocol.message.MessageBase import MessageBase


class CarSafeStatusInfo(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #####################################################
    #               创建安防状态数据
    #####################################################
    def generateSecurityStatusData(self):
        data = ""
        statusCode = "ffffffffffffffffffff"                 #状态掩码
        securityStatus = self.getSecurityStatusHex()        #安全状态
        doorStatus = self.getDoorStatusHex()                #门状态
        lockStatus = self.getLockStatusHex()                #锁状态
        windowStatus = self.getWindowStatusHex()            #窗户状态
        lightStatus = self.getLightStatusHex()              #灯光状态
        onoffStatusA = self.getOnoffStatusAHex()            #开关状态A
        onoffStatusB = self.getOnoffStatusBHex()            #开关状态B
        retain1 = "00"                                      #预留
        retain2 = "00"                                      #预留
        retain3 = "00"                                      # 预留


        data = data + statusCode + securityStatus + doorStatus + lockStatus + windowStatus + lightStatus + onoffStatusA + onoffStatusB + retain1 + retain2 + retain3
        return data
    def generateSecurityStatusData_GUI(self,data):
        dataHex = ""
        statusCode = data["statusCode"]                 #状态掩码
        securityStatus = self.int2hexStringByBytes(int(data["securityStatus"]))        #安全状态
        doorStatus = self.int2hexStringByBytes(int(data["doorStatus"]))                #门状态
        lockStatus = self.int2hexStringByBytes(int(data["lockStatus"]))               #锁状态
        windowStatus = self.int2hexStringByBytes(int(data["windowStatus"]))            #窗户状态
        lightStatus = self.int2hexStringByBytes(int(data["lightStatus"]))              #灯光状态
        onoffStatusA = self.int2hexStringByBytes(int(data["onoffStatusA"]))            #开关状态A
        onoffStatusB = self.int2hexStringByBytes(int(data["onoffStatusB"]))            #开关状态B
        retain1 = "00"                                      #预留
        retain2 = "00"                                      #预留
        retain3 = "00"                                      # 预留
        dataHex = dataHex + statusCode + securityStatus + doorStatus + lockStatus + windowStatus + lightStatus + onoffStatusA + onoffStatusB + retain1 + retain2 + retain3
        return dataHex
    #创建安防状态数据，数据随机产生
    def generateSecurityStatusData_random(self):
        data = ""
        statusCode = "ffffffffffffffffffff"                 #状态掩码
        securityStatus = self.getSecurityStatusHex_random()        #安全状态
        doorStatus = self.getDoorStatusHex_random()                #门状态
        lockStatus = self.getLockStatusHex_random()                #锁状态
        windowStatus = self.getWindowStatusHex_random()            #窗户状态
        lightStatus = self.getLightStatusHex_random()              #灯光状态
        onoffStatusA = self.getOnoffStatusAHex_random()            #开关状态A
        onoffStatusB = self.getOnoffStatusBHex_random()            #开关状态B
        retain1 = "00"                                      #预留
        retain2 = "00"                                      #预留
        retain3 = "00"                                      # 预留


        data = data + statusCode + securityStatus + doorStatus + lockStatus + windowStatus + lightStatus + onoffStatusA + onoffStatusB + retain1 + retain2 + retain3
        return data


    #####################################################
    #               获取安全状态16进制数据
    #               按照高位在前，低位在后的规则
    #####################################################
    def getSecurityStatusHex(self):
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
    def getSecurityStatusHex_random(self):
        val = self.getRandomNum(intArr=[0,1,2,4,8,16,32,64],mult=7)
        hexData =  self.int2hexStringByBytes(val)
        return hexData

    #####################################################
    #               获取门状态16进制数据
    #####################################################
    def getDoorStatusHex(self):
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
    def getDoorStatusHex_random(self):
        val = self.getRandomNum(intArr=[0,1,2,4,8,16,32],mult=6)
        hexData =  self.int2hexStringByBytes(val)
        return hexData

    #####################################################
    #               获取锁状态16进制数据
    #####################################################
    def getLockStatusHex(self):
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
    def getLockStatusHex_random(self):
        val = self.getRandomNum(intArr=[0,1,2,4,8],mult=4)
        hexData = self.int2hexStringByBytes(val)
        return hexData

    #####################################################
    #               获取窗户状态16进制数据
    #####################################################
    def getWindowStatusHex(self):
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
    def getWindowStatusHex_random(self):
        val = self.getRandomNum(intArr=[0,1,2,4,8,16,32,64,128],mult=8)
        hexData = self.int2hexStringByBytes(val)
        return hexData

    #####################################################
    #               获取灯光状态16进制数据
    #####################################################
    def getLightStatusHex(self):
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
    def getLightStatusHex_random(self):
        val = self.getRandomNum(intArr=[0,1,2,4,8,16,32,64,128],mult=8)
        hexData = self.int2hexStringByBytes(val)
        return hexData

    #####################################################
    #               获取开关状态A16进制数据
    #####################################################
    def getOnoffStatusAHex(self):
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
    def getOnoffStatusAHex_random(self):
        val = self.getRandomNum(intArr=[0,1,2,4,8,16,32],mult=6)
        hexData = self.int2hexStringByBytes(val)
        return hexData

    #####################################################
    #               获取开关状态B16进制数据
    #####################################################
    def getOnoffStatusBHex(self):
        retain1 = 0
        retain2 = 0
        retain3 = 0
        retain4 = 0
        #档位，0：p  16：R  32：N  48：D  64：1挡  80：2挡  96：3挡  112：4挡  128：5挡  144：6挡  160：M挡  176：S挡
        gears = 0

        val = retain1 + retain2 + retain3 + retain4 + gears
        hexData = self.int2hexStringByBytes(val)
        return hexData
    def getOnoffStatusBHex_random(self):
        val = self.getRandomNum(intArr=[0,16,32,48,64,80,96,112,128,144,160,176])
        hexData = self.int2hexStringByBytes(val)
        return hexData