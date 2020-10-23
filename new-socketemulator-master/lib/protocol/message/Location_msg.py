#encoding:utf-8

'''
定义位置信息汇报消息
'''
import datetime
from random import random

from lib.protocol.message.MessageBase import MessageBase
from lib.protocol.message.data.AlarmEvent_data import AlarmEvent_data
from lib.protocol.message.data.CarSafeStatusInfo import CarSafeStatusInfo
from lib.protocol.message.data.Circum_data import Circum_data
from lib.protocol.message.data.NewEnergyCar_data import NewEnergyCar_data
from lib.protocol.message.data.SaloonCarOBD_data import SaloonCarOBD_data
from lib.protocol.message.data.TruckCarOBD_data import TruckCarOBD_data


class Location_msg(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #######################################################
    # 生成一条完整的消息
    #######################################################
    def generateMsg(self):
        msg = ""
        msgHeader = self.getMsgHeader()
        msgBody = self.getMsgBody()
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    # 生成一条完整的消息，针对图形界面，可传递参数
    def generateMsg_GUI(self,params):
        msg = ""
        msgBody = self.getMsgBody_GUI(params)
        msgHeader = self.getMsgHeader_GUI(params["msgID"], int(params["phoneNum"]), int(params["msgWaterCode"]),
                                          int(params["encryptionType"]), int(params["subPkg"]),msgBody)
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg
    # 生成一条完整的消息，数据随机产生
    def generateMsg_random(self):
        msg = ""
        msgID = "0200"
        phoneNum = self.getRandomStr(11, "0123456789")
        msgWaterCode = self.getRandomNum(1, 65535)
        encryptionType = 0
        # subPkg = self.getRandomNum(intArr=[0, 8192])
        subPkg = 0
        msgHeader = self.getMsgHeader_GUI(msgID,phoneNum,msgWaterCode,encryptionType,subPkg)
        msgBody = self.getMsgBody_random()
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        msg = ""
        locationBaseInfo = self.getLocationBaseInfo()           #位置基本信息
        locationExtraInfo = self.getLocationExtraInfo()         #位置附加信息
        msg = locationBaseInfo + locationExtraInfo
        return msg

    # 获取消息体，针对图形界面，可传递参数
    def getMsgBody_GUI(self,params):
        msg = ""
        locationBaseInfo = self.getLocationBaseInfo_GUI(params["baseInfo"])           #位置基本信息
        locationExtraInfo = ""
        if params["extraInfo"] == {}:
            pass
        else:
            locationExtraInfo = self.getLocationExtraInfo_GUI(params["extraInfo"])    #位置附加信息
        msg = locationBaseInfo + locationExtraInfo
        return msg
    # 获取消息体，数据随机产生
    def getMsgBody_random(self):
        msg = ""
        locationBaseInfo = self.getLocationBaseInfo_random()           #位置基本信息
        locationExtraInfo = self.getLocationExtraInfo_random()         #位置附加信息
        msg = locationBaseInfo + locationExtraInfo
        return msg

    #######################################################
    # 获取位置基本信息
    #######################################################
    def getLocationBaseInfo(self):
        msg = ""
        alarmFlag = self.getAlarmFlag()                             #报警标志
        status = self.getStatus()                                   #状态
        latitude = self.getLatitude()                               #纬度
        longtitude = self.getLongtitude()                           #经度
        elevation = self.getElevation()                             #海拔高度
        speed = self.getSpeed()                                     #速度
        directionAngle = self.getDirectionAngle()                   #获取方向角度
        infoTime = self.getInfoTime()                               #获取时间

        msg = alarmFlag + status + latitude + longtitude + elevation + speed + directionAngle + infoTime
        return msg

    # 获取位置基本信息，针对图形界面，可传递参数
    def getLocationBaseInfo_GUI(self,baseInfo):
        msg = ""
        alarmFlag = self.int2hexStringByBytes(int(baseInfo["alarmFlag"]),4)                  #报警标志
        status = self.int2hexStringByBytes(int(baseInfo["status"]),4)                        #状态
        latitude = self.getLatitude(float(baseInfo["latitude"]))                               #纬度
        longtitude = self.getLongtitude(float(baseInfo["longtitude"]))                         #经度
        elevation = self.getElevation(int(baseInfo["elevation"]))                            #海拔高度
        speed = self.getSpeed(int(baseInfo["speed"]))                                        #速度
        directionAngle = self.getDirectionAngle(int(baseInfo["directionAngle"]))             #获取方向角度
        infoTime = self.getInfoTime(baseInfo["infoTime"])                               #获取时间
        msg = alarmFlag + status + latitude + longtitude + elevation + speed + directionAngle + infoTime
        return msg
    # 获取位置基本信息，数据随机产生
    def getLocationBaseInfo_random(self):
        msg = ""
        alarmFlag = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1,2,4,8,16,32,64, \
             128,256,512,1024,2048,4096,8192,16384,262144,524288,1048576,2097152,4194304, \
             8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648],mult=29),4)        #报警标志
        status = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1,2,4,8,16,32,256, \
             512,768,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152],mult=21),4)            #状态
        latitude = self.getLatitude(self.getRandomNum(s=0,e=90000000) / 1000000)                                        #纬度
        longtitude = self.getLongtitude(self.getRandomNum(s=0,e=180000000) / 1000000)                                   #经度
        elevation = self.getElevation(self.getRandomNum(s=0,e=6000))                                                    #海拔高度
        speed = self.getSpeed(self.getRandomNum(s=0,e=150))                                                             #速度
        directionAngle = self.getDirectionAngle(self.getRandomNum(s=0,e=359))                                           #获取方向角度
        infoTime = self.getInfoTime(self.getRandomDate())                                                               #获取时间
        msg = alarmFlag + status + latitude + longtitude + elevation + speed + directionAngle + infoTime
        return msg

    #######################################################
    # 获取位置附加信息
    #######################################################
    def getLocationExtraInfo(self):
        data = ""
        # 里程，DWORD，1 / 10km，对应车上里程表读数；不支持OBD时，为基于GPS车速统计的车辆累计行驶总里程。
        extra_01 = "01" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(20202020,4)
        #油量，WORD，1/10L，对应车上油量表读数
        extra_02 = "02" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(5200,2)
        #超速报警附加信息
        extra_11 = "11" + self.int2hexStringByBytes(int(len(self.getOverSpeedAlarmExtraInfo()) / 2)) + self.getOverSpeedAlarmExtraInfo()
        #进出区域/路线报警附加信息见
        extra_12 = "12" + self.int2hexStringByBytes(6) + self.getInOutAreaAlarmExtraInfo()
        #路段行驶时间不足/过长报警附加信息见
        extra_13 = "13" + self.int2hexStringByBytes(7) + self.getDrivingLongOrShortAlarmExtraInfo()
        #IO 状态位
        extra_2A = "2A" + self.int2hexStringByBytes(2) + self.getStatusBit()
        #BYTE，无线通信网络信号强度
        extra_30 = "30" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(33)
        #BYTE，GNSS 定位卫星数
        extra_31 = "31" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(2)
        #基础数据项列表
        extra_EA = "EA" + self.int2hexStringByBytes(int(len(self.getBaseDataList()) / 2)) + self.getBaseDataList()
        #轿车 OBD 数据流
        extra_EB = "EB" + self.int2hexStringByBytes(int(len(SaloonCarOBD_data().generateSaloonCarOBDData()) / 2)) + SaloonCarOBD_data().generateSaloonCarOBDData()
        #货车 OBD 数据流
        extra_EC = "EC" + self.int2hexStringByBytes(int(len(TruckCarOBD_data().generateTruckCarOBD_data()) / 2)) + TruckCarOBD_data().generateTruckCarOBD_data()
        #新能源 OBD 数据流
        extra_ED = "ED" + self.int2hexStringByBytes(int(len(NewEnergyCar_data().generateNewEnergyCar_data()) / 2)) + NewEnergyCar_data().generateNewEnergyCar_data()
        #外设数据项列表
        extra_EE = "EE" + self.int2hexStringByBytes(int(len(Circum_data().generateCircum_data()) / 2)) + Circum_data().generateCircum_data()
        #报警事件 ID 数据项列表
        extra_FA = "FA" + self.int2hexStringByBytes(int(len(AlarmEvent_data().generateAlarmEvent_data()) / 2)) + AlarmEvent_data().generateAlarmEvent_data()

        data = extra_01 + extra_02 + extra_11 + extra_31 + extra_EA + extra_EB

        # data = extra_11 + extra_31 + extra_EA + extra_EB + extra_FA
        # data = extra_11 + extra_31 + extra_EA + extra_FA
        # data = extra_EB + extra_FA
        # data = extra_01 + extra_02 + extra_11 + extra_12 + extra_13
        # data = data + extra_2A + extra_30 + extra_31 + extra_EA + extra_EB
        # data = data +extra_FA
        return data

    def getLocationExtraInfo_GUI(self,extraInfo):
        data = ""
        if("01" in extraInfo.keys()):
            # 里程，DWORD，1 / 10km，对应车上里程表读数；不支持OBD时，为基于GPS车速统计的车辆累计行驶总里程。
            extra_01 = "01" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(extraInfo["01"]["extra_01"]),4)
            data = data + extra_01
        if ("02" in extraInfo.keys()):
            #油量，WORD，1/10L，对应车上油量表读数
            extra_02 = "02" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(extraInfo["02"]["extra_02"]),2)
            data = data + extra_02
        if ("11" in extraInfo.keys()):
            #超速报警附加信息
            overSpeedAlarmExtraInfo = self.getOverSpeedAlarmExtraInfo_GUI(extraInfo["11"])
            extra_11 = "11" + self.int2hexStringByBytes(int(len(overSpeedAlarmExtraInfo) / 2))
            data = data + extra_11
        if ("12" in extraInfo.keys()):
            #进出区域/路线报警附加信息见
            extra_12 = "12" + self.int2hexStringByBytes(6) + self.getInOutAreaAlarmExtraInfo_GUI(extraInfo["12"])
            data = data +extra_12
        if ("13" in extraInfo.keys()):
            #路段行驶时间不足/过长报警附加信息见
            extra_13 = "13" + self.int2hexStringByBytes(7) + self.getDrivingLongOrShortAlarmExtraInfo_GUI(extraInfo["13"])
            data = data + extra_13
        if ("2A" in extraInfo.keys()):
            #IO 状态位
            extra_2A = "2A" + self.int2hexStringByBytes(2) + self.getStatusBit_GUI(extraInfo["2A"])
            data = data + extra_2A
        if ("30" in extraInfo.keys()):
            #BYTE，无线通信网络信号强度
            extra_30 = "30" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(extraInfo["30"]["extra_30"]))
            data = data + extra_30
        if ("31" in extraInfo.keys()):
            #BYTE，GNSS 定位卫星数
            extra_31 = "31" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(extraInfo["31"]["extra_31"]))
            data = data + extra_31
        if ("EA" in extraInfo.keys()):
            #基础数据项列表
            baseDataList = self.getBaseDataList_GUI(extraInfo["EA"])
            extra_EA = "EA" + self.int2hexStringByBytes(int(len(baseDataList) / 2)) + baseDataList
            data = data + extra_EA
        if ("EB" in extraInfo.keys()):
            #轿车 OBD 数据流
            saloonCarOBD_data = SaloonCarOBD_data().generateSaloonCarOBDData_GUI(extraInfo["EB"])
            extra_EB = "EB" + self.int2hexStringByBytes(int(len(saloonCarOBD_data) / 2)) + saloonCarOBD_data
            data = data + extra_EB
        if ("EC" in extraInfo.keys()):
            #货车 OBD 数据流
            truckCarOBD_data = TruckCarOBD_data().generateTruckCarOBD_data()
            extra_EC = "EC" + self.int2hexStringByBytes(int(len(truckCarOBD_data) / 2)) + truckCarOBD_data
            data = data + extra_EC
        if ("ED" in extraInfo.keys()):
            #新能源 OBD 数据流
            newEnergyCar_data = NewEnergyCar_data().generateNewEnergyCar_data()
            extra_ED = "ED" + self.int2hexStringByBytes(int(len(newEnergyCar_data) / 2)) + newEnergyCar_data
            data = data + extra_ED
        if ("EE" in extraInfo.keys()):
            #外设数据项列表
            circum_data = Circum_data().generateCircum_data()
            extra_EE = "EE" + self.int2hexStringByBytes(int(len(circum_data) / 2)) + circum_data
            data = data + extra_EE
        if ("FA" in extraInfo.keys()):
            #报警事件 ID 数据项列表
            alarmEvent_data = AlarmEvent_data().generateAlarmEvent_data_GUI(extraInfo["FA"])
            extra_FA = "FA" + self.int2hexStringByBytes(int(len(alarmEvent_data) / 2)) + alarmEvent_data
            data = data + extra_FA
        return data

    # 获取位置附加信息，数据随机产生
    def getLocationExtraInfo_random(self):
        data = ""
        # 里程，DWORD，1 / 10km，对应车上里程表读数；不支持OBD时，为基于GPS车速统计的车辆累计行驶总里程。
        extra_01 = "01" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)
        #油量，WORD，1/10L，对应车上油量表读数
        extra_02 = "02" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        #超速报警附加信息
        data_11 = self.getOverSpeedAlarmExtraInfo_random()
        extra_11 = "11" + self.int2hexStringByBytes(int(len(data_11) / 2)) + data_11
        #进出区域/路线报警附加信息见
        extra_12 = "12" + self.int2hexStringByBytes(6) + self.getInOutAreaAlarmExtraInfo_random()
        #路段行驶时间不足/过长报警附加信息见
        extra_13 = "13" + self.int2hexStringByBytes(7) + self.getDrivingLongOrShortAlarmExtraInfo_ramdom()
        #IO 状态位
        extra_2A = "2A" + self.int2hexStringByBytes(2) + self.getStatusBit_random()
        #BYTE，无线通信网络信号强度
        extra_30 = "30" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        #BYTE，GNSS 定位卫星数
        extra_31 = "31" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        data_EA = self.getBaseDataList_random()
        #基础数据项列表
        extra_EA = "EA" + self.int2hexStringByBytes(int(len(data_EA) / 2)) + data_EA
        #轿车 OBD 数据流
        data_EB = SaloonCarOBD_data().generateSaloonCarOBDData_random()
        extra_EB = "EB" + self.int2hexStringByBytes(int(len(data_EB) / 2)) + data_EB
        #货车 OBD 数据流
        # extra_EC = "EC" + self.int2hexStringByBytes(int(len(TruckCarOBD_data().generateTruckCarOBD_data()) / 2)) + TruckCarOBD_data().generateTruckCarOBD_data()
        #新能源 OBD 数据流
        # extra_ED = "ED" + self.int2hexStringByBytes(int(len(NewEnergyCar_data().generateNewEnergyCar_data()) / 2)) + NewEnergyCar_data().generateNewEnergyCar_data()
        #外设数据项列表
        # extra_EE = "EE" + self.int2hexStringByBytes(int(len(Circum_data().generateCircum_data()) / 2)) + Circum_data().generateCircum_data()
        #报警事件 ID 数据项列表
        data_FA = AlarmEvent_data().generateAlarmEvent_data_random()
        extra_FA = "FA" + self.int2hexStringByBytes(int(len(data_FA) / 2)) + data_FA

        arr = []
        arr.append(extra_01)
        arr.append(extra_02)
        arr.append(extra_11)
        arr.append(extra_12)
        arr.append(extra_13)
        arr.append(extra_2A)
        arr.append(extra_30)
        arr.append(extra_31)
        arr.append(extra_EA)
        arr.append(extra_EB)
        arr.append(extra_FA)
        mult = self.getRandomNum(0,11)
        temp = []
        for i in range(0, mult):
            con = self.getRandomNum(intArr=arr,mult=1)
            if con in temp:
                con = ""
            temp.append(con)
            data = data + con
        return data


    #获取超速报警附加信息
    def getOverSpeedAlarmExtraInfo(self):
        # 0：无特定位置；
        # 1：圆形区域；
        # 2：矩形区域；
        # 3：多边形区域；
        # 4：路段
        locationType = 1
        areaId = ""                                    #若位置类型为 0，无该字段
        if locationType == 0:
            pass
        else:
            areaId = self.int2hexStringByBytes(2020,4)
        msg = self.int2hexStringByBytes(locationType) + areaId
        return msg
    def getOverSpeedAlarmExtraInfo_GUI(self,data):
        # 0：无特定位置；
        # 1：圆形区域；
        # 2：矩形区域；
        # 3：多边形区域；
        # 4：路段
        locationType = int(data["locationType_OverSpeed"])
        areaId = ""                                    #若位置类型为 0，无该字段
        if locationType == 0:
            pass
        else:
            areaId = self.int2hexStringByBytes(int(data["areaId_OverSpeed"]),4)
        msg = self.int2hexStringByBytes(locationType) + areaId
        return msg
    #获取超速报警附加信息，数据随机产生
    def getOverSpeedAlarmExtraInfo_random(self):
        locationType = self.getRandomNum(intArr=[0,1,2,3,4])
        areaId = ""                                    #若位置类型为 0，无该字段
        if locationType == 0:
            pass
        else:
            areaId = self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)
        msg = self.int2hexStringByBytes(locationType) + areaId
        return msg

    #获取进出区域/路线报警附加信息
    def getInOutAreaAlarmExtraInfo(self):
        # 0：无特定位置；
        # 1：圆形区域；
        # 2：矩形区域；
        # 3：多边形区域；
        # 4：路段
        locationType = 1
        areaId = ""
        if locationType == 0:
            areaId = "00000000"
        else:
            areaId = self.int2hexStringByBytes(2020, 4)
        direction = 0                     #0-进，1-出
        msg = self.int2hexStringByBytes(locationType) + areaId + self.int2hexStringByBytes(direction)
        return msg
    def getInOutAreaAlarmExtraInfo_GUI(self,data):
        # 0：无特定位置；
        # 1：圆形区域；
        # 2：矩形区域；
        # 3：多边形区域；
        # 4：路段
        locationType = int(data["locationType_inOut"])
        areaId = ""
        if locationType == 0:
            areaId = "00000000"
        else:
            areaId = self.int2hexStringByBytes(int(data["areaId_inOut"]), 4)
        direction = int(data["direction"])                     #0-进，1-出
        msg = self.int2hexStringByBytes(locationType) + areaId + self.int2hexStringByBytes(direction)
        return msg
    #获取进出区域/路线报警附加信息，数据随机参数
    def getInOutAreaAlarmExtraInfo_random(self):
        locationType = self.getRandomNum(intArr=[0,1,2,3,4])
        areaId = ""
        if locationType == 0:
            areaId = "00000000"
        else:
            areaId = self.int2hexStringByBytes(self.getRandomNum(1,4294967295), 4)
        direction = self.getRandomNum(intArr=[0,1])                     #0-进，1-出
        msg = self.int2hexStringByBytes(locationType) + areaId + self.int2hexStringByBytes(direction)
        return msg

    #路线行驶时间不足/过长报警附加信息消息
    def getDrivingLongOrShortAlarmExtraInfo(self):
        areaId = self.int2hexStringByBytes(2020, 4)          #路段Id
        drivingTime = self.int2hexStringByBytes(36000,2)     #路段行驶时间(单位：秒)
        result = self.int2hexStringByBytes(0)                #结果，0-不足，1-过长
        msg = areaId + drivingTime + result
        return msg
    def getDrivingLongOrShortAlarmExtraInfo_GUI(self,data):
        areaId = self.int2hexStringByBytes(int(data["areaId_road"]), 4)          #路段Id
        drivingTime = self.int2hexStringByBytes(int(data["drivingTime"]),2)     #路段行驶时间(单位：秒)
        result = self.int2hexStringByBytes(int(data["result"]))                #结果，0-不足，1-过长
        msg = areaId + drivingTime + result
        return msg
    #路线行驶时间不足/过长报警附加信息消息，数据随机产生
    def getDrivingLongOrShortAlarmExtraInfo_ramdom(self):
        areaId = self.int2hexStringByBytes(self.getRandomNum(0,4294967295), 4)          #路段Id
        drivingTime = self.int2hexStringByBytes(self.getRandomNum(0,65535),2)     #路段行驶时间(单位：秒)
        result = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]))                #结果，0-不足，1-过长
        msg = areaId + drivingTime + result
        return msg

    #获取状态位
    def getStatusBit(self):
        deepSleepStatus = 1             #1：深度休眠状态
        sleepStatus = 2                 #1：休眠状态
        retain = 0
        data = deepSleepStatus + sleepStatus + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex
    def getStatusBit_GUI(self,data):
        deepSleepStatus = int(data["deepSleepStatus"])             #1：深度休眠状态
        sleepStatus = int(data["sleepStatus"])                 #1：休眠状态
        retain = 0
        data = deepSleepStatus + sleepStatus + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex
    #获取状态位，数据随机产生
    def getStatusBit_random(self):
        dataHex = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1,2],mult=2),2)
        return dataHex

    #基础数据项列表
    def getBaseDataList(self):
        dataId_0001 = "0001" + self.int2hexStringByBytes(4) + self.getExpandStatusBit()
        dataId_0002 = "0002" + self.int2hexStringByBytes(4) + self.getExpandAlarmBit()
        dataId_0003 = "0003" + self.int2hexStringByBytes(5) + self.getTotalMileage()
        dataId_0004 = "0004" + self.int2hexStringByBytes(5) + self.getTotalOil()
        dataId_0005 = "0005" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(360000,4)
        dataId_0006 = "0006" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(72000,4)
        dataId_0007 = "0007" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(480000,4)
        dataId_0010 = "0010" + self.int2hexStringByBytes(int(len(self.getSpeedupInOneSeconds()) / 2)) + self.getSpeedupInOneSeconds()
        dataId_0011 = "0011" + self.int2hexStringByBytes(int(len(CarSafeStatusInfo().generateSecurityStatusData()) / 2)) + CarSafeStatusInfo().generateSecurityStatusData()
        dataId_0012 = "0012" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(36,2)
        dataId_0013 = "0013" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(6)
        #TODO 由于被置灰，所以没有实现
        # dataId_0015 = "0015" + self.int2hexStringByBytes(2)
        # dataId_0016 = "0016"
        #TODO 暂不支持
        # dataId_0017 = "0017" + self.int2hexStringByBytes(2)
        dataId_001D = "001D" + self.int2hexStringByBytes(1) + "01"
        data = dataId_0001 + dataId_0002 + dataId_0003 + dataId_0004 + dataId_0005
        data = data + dataId_0006 + dataId_0007 + dataId_0010 + dataId_0011 + dataId_0012
        data = data + dataId_0013 + dataId_001D
        return data
    def getBaseDataList_GUI(self,data):
        dataHex = ""
        if ("0001" in data.keys()):
            dataId_0001 = "0001" + self.int2hexStringByBytes(4) + self.getExpandStatusBit_GUI(data["0001"])
            dataHex = dataHex + dataId_0001
        if ("0002" in data.keys()):
            dataId_0002 = "0002" + self.int2hexStringByBytes(4) + self.getExpandAlarmBit_GUI(data["0002"])
            dataHex = dataHex + dataId_0002
        if ("0003" in data.keys()):
            dataId_0003 = "0003" + self.int2hexStringByBytes(5) + self.getTotalMileage_GUI(data["0003"])
            dataHex = dataHex + dataId_0003
        if ("0004" in data.keys()):
            dataId_0004 = "0004" + self.int2hexStringByBytes(5) + self.getTotalOil_GUI(data["0004"])
            dataHex = dataHex + dataId_0004
        if ("0005" in data.keys()):
            dataId_0005 = "0005" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["0005"]["dataId_0005"]),4)
            dataHex = dataHex + dataId_0005
        if ("0006" in data.keys()):
            dataId_0006 = "0006" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["0006"]["dataId_0006"]),4)
            dataHex = dataHex + dataId_0006
        if ("0007" in data.keys()):
            dataId_0007 = "0007" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(int(data["0007"]["dataId_0007"]),4)
            dataHex = dataHex + dataId_0007
        if ("0010" in data.keys()):
            speedupInOneSeconds = self.getSpeedupInOneSeconds_GUI(data["0010"])
            dataId_0010 = "0010" + self.int2hexStringByBytes(int(len(speedupInOneSeconds) / 2)) + speedupInOneSeconds
            dataHex = dataHex + dataId_0010
        if ("0011" in data.keys()):
            securityStatusData = CarSafeStatusInfo().generateSecurityStatusData_GUI(data["0011"])
            dataId_0011 = "0011" + self.int2hexStringByBytes(int(len(securityStatusData) / 2)) + securityStatusData
            dataHex = dataHex + dataId_0011
        if ("0012" in data.keys()):
            dataId_0012 = "0012" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(int(data["0012"]["dataId_0012"]),2)
            dataHex = dataHex + dataId_0012
        if ("0013" in data.keys()):
            dataId_0013 = "0013" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(int(data["0013"]["dataId_0013"]))
            dataHex = dataHex + dataId_0013
        if ("001D" in data.keys()):
            dataId_001D = "001D" + self.int2hexStringByBytes(1) + data["001D"]["dataId_001D"]
            dataHex = dataHex + dataId_001D
        return dataHex
    #基础数据项列表，数据随机产生
    def getBaseDataList_random(self):
        dataId_0001 = "0001" + self.int2hexStringByBytes(4) + self.getExpandStatusBit_random()
        dataId_0002 = "0002" + self.int2hexStringByBytes(4) + self.getExpandAlarmBit_random()
        dataId_0003 = "0003" + self.int2hexStringByBytes(5) + self.getTotalMileage_random()
        dataId_0004 = "0004" + self.int2hexStringByBytes(5) + self.getTotalOil_random()
        dataId_0005 = "0005" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)
        dataId_0006 = "0006" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)
        dataId_0007 = "0007" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)
        dataId_0010 = "0010" + self.int2hexStringByBytes(int(len(self.getSpeedupInOneSeconds_random()) / 2)) + self.getSpeedupInOneSeconds_random()
        dataId_0011 = "0011" + self.int2hexStringByBytes(int(len(CarSafeStatusInfo().generateSecurityStatusData_random()) / 2)) + CarSafeStatusInfo().generateSecurityStatusData_random()
        dataId_0012 = "0012" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(self.getRandomNum(0,65535),2)
        dataId_0013 = "0013" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(self.getRandomNum(0,255))
        dataId_001D = "001D" + self.int2hexStringByBytes(1) + self.getRandomNum(intArr=["00","01","02"])
        arr = []
        arr.append(dataId_0001)
        arr.append(dataId_0002)
        arr.append(dataId_0003)
        arr.append(dataId_0004)
        arr.append(dataId_0005)
        arr.append(dataId_0006)
        arr.append(dataId_0007)
        arr.append(dataId_0010)
        arr.append(dataId_0011)
        arr.append(dataId_0012)
        arr.append(dataId_0013)
        arr.append(dataId_001D)
        mult = self.getRandomNum(0,12)
        temp = []
        data = ""
        for i in range(0, mult):
            con = self.getRandomNum(intArr=arr)
            if con in temp:
                con = ""
            temp.append(con)
            data = data + con
        return data


    '''扩展状态标志位，见 表 C1EXT1'''
    def getExpandStatusBit(self):
        defenseUndefenseRep = 0          #0：撤防上报；1：设防上报   (1)
        retain = 0
        data = defenseUndefenseRep + retain
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex
    def getExpandStatusBit_GUI(self,data):
        defenseUndefenseRep = int(data["dataId_0001"])          #0：撤防上报；1：设防上报   (1)
        retain = 0
        data = defenseUndefenseRep + retain
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex
    def getExpandStatusBit_random(self):
        dataHex = self.int2hexStringByBytes(self.getRandomNum(intArr=[0,1]),4)
        return dataHex
    '''扩展报警标志位，见 表 C1EXT2'''
    def getExpandAlarmBit(self):
        waterTemperatureAlarm = 1                      #1:水温报警        (1)
        idlingOverlongAlarm = 2                        #1：怠速过长报警   (2)
        rapidlyAccelerateAlarm = 4                     #1：急加速报警     (4)
        sharpSlowsownAlarm = 8                         #1：急减速报警     (8)
        sharpCurve = 16                                #1：急转弯报警     (16)
        retain5_9 = 0
        insertAlarm = 1024                             #1：插入报警      (1024)
        oilExpenseNotSupportAlarm = 2048               #1:油耗不支持报警  (2048)
        OBDNotSupportAlarm = 4096                      #1:OBD 不支持报警  (4096)
        buslineNotSleepAlarm = 8192                    #1:总线不睡眠报警  (8192)
        illegalOpenDoor = 16384                        #1:非法开门       (16384)
        retain15_16 = 0
        FLASHTroubleAlarm = 131072                     #1: FLASH 故障报警   (131072)
        CANTroubleAlarm = 262144                       #1: CAN 模块故障报警  (262144)
        D3SensorTroubleAlarm = 524288                  #1：3D 传感器故障报警  (524288)
        RTCTroubleAlarm = 1048576                      #1：RTC 模块故障报警
        retain21_31 = 0
        data = waterTemperatureAlarm + idlingOverlongAlarm + rapidlyAccelerateAlarm + sharpSlowsownAlarm + sharpCurve
        data = data + retain5_9 + insertAlarm + oilExpenseNotSupportAlarm + OBDNotSupportAlarm + buslineNotSleepAlarm
        data = data + illegalOpenDoor + retain15_16 + FLASHTroubleAlarm + CANTroubleAlarm + D3SensorTroubleAlarm
        data = data + RTCTroubleAlarm + retain21_31
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex
    def getExpandAlarmBit_GUI(self,data):
        dataHex = self.int2hexStringByBytes(data["dataId_0002"], 4)
        return dataHex
    def getExpandAlarmBit_random(self):
        data = self.getRandomNum(intArr=[0,1,2,4,8,16,1024,2048, \
                                         4096,8192,16384,131072,262144,524288,1048576],mult=14)
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex
    '''行驶总里程'''
    def getTotalMileage(self):
        caculateType = "0A"
        totalMileage = self.int2hexStringByBytes(128000,4)    #行驶总里程（单位米）
        data = caculateType + totalMileage
        return data
    def getTotalMileage_GUI(self,data):
        caculateType = data["caculateType"]
        totalMileage = self.int2hexStringByBytes(int(data["totalMileage"]),4)    #行驶总里程（单位米）
        data = caculateType + totalMileage
        return data
    def getTotalMileage_random(self):
        caculateType = self.getRandomNum(intArr=["01","02","03","04","05","06","07","09","0A","0B","0C"],)
        totalMileage = self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)    #行驶总里程（单位米）
        data = caculateType + totalMileage
        return data
    '''行驶总油耗'''
    def getTotalOil(self):
        caculateType = "02"
        totalOil = self.int2hexStringByBytes(120000,4)        #总油耗（单位 mL）
        data = caculateType + totalOil
        return data
    def getTotalOil_GUI(self,data):
        caculateType = data["caculateType"]
        totalOil = self.int2hexStringByBytes(int(data["totalOil"]),4)        #总油耗（单位 mL）
        data = caculateType + totalOil
        return data
    def getTotalOil_random(self):
        caculateType = self.getRandomNum(intArr=["01","02","03","04","05","0B","0C"],)
        totalOil = self.int2hexStringByBytes(self.getRandomNum(0,4294967295),4)        #总油耗（单位 mL）
        data = caculateType + totalOil
        return data
    '''此刻 1 秒内的加速度数据，见 表 C1EXT3'''
    def getSpeedupInOneSeconds(self):
        data = ""
        pointCount = 4                                        #采集的点个数 N
        collectIntercal = 100                                 #采集间隔（单位 ms），上传值为该采集间隔时间内的加速度均值
        data = data + self.int2hexStringByBytes(pointCount,2)
        data = data + self.int2hexStringByBytes(collectIntercal,2)
        speedupVal = 1000                                     #采集点加速度均值
        for i in range(0,pointCount):
            data = data + self.int2hexStringByBytes(speedupVal + 10,2)
        return data
    def getSpeedupInOneSeconds_GUI(self,data):
        pointCount = int(data["pointCount"])                                        #采集的点个数 N
        collectIntercal = int(data["collectIntercal"])                                 #采集间隔（单位 ms），上传值为该采集间隔时间内的加速度均值
        data = ""
        data = data + self.int2hexStringByBytes(pointCount,2)
        data = data + self.int2hexStringByBytes(collectIntercal,2)
        speedupVal = 1000                                     #采集点加速度均值
        for i in range(0,pointCount):
            data = data + self.int2hexStringByBytes(speedupVal + 10,2)
        return data
    def getSpeedupInOneSeconds_random(self):
        data = ""
        pointCount = self.getRandomNum(0,50)                                        #采集的点个数 N
        collectIntercal = self.getRandomNum(0,10000)                                #采集间隔（单位 ms），上传值为该采集间隔时间内的加速度均值
        data = data + self.int2hexStringByBytes(pointCount,2)
        data = data + self.int2hexStringByBytes(collectIntercal,2)                                    #采集点加速度均值
        for i in range(0,pointCount):
            speedupVal = self.getRandomNum(0,65535)
            data = data + self.int2hexStringByBytes(speedupVal,2)
        return data


    #######################################################
    # 获取纬度信息
    #######################################################
    def getLatitude(self,data=29.40268):
        data = int(data * 1000000)
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex

    #######################################################
    # 获取经度信息
    #######################################################
    def getLongtitude(self,data=106.54041):
        data = int(data * 1000000)
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 获取海拔高度
    #######################################################
    def getElevation(self,data=521):
        dataHex = self.int2hexStringByBytes(data, 2)
        return dataHex

    #######################################################
    # 获取速度
    #######################################################
    def getSpeed(self,data=66):
        dataHex = self.int2hexStringByBytes(data, 2)
        return dataHex

    #######################################################
    # 获取方向角度
    #######################################################
    def getDirectionAngle(self,data=59):
        dataHex = self.int2hexStringByBytes(data, 2)
        return dataHex

    #######################################################
    # 获取时间
    #######################################################
    def getInfoTime(self,data="2020-02-04 18:57:04"):
        #now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = data
        data = data.replace("-","")
        data = data.replace(" ","")
        data = data.replace(":","")
        data = data[2:]
        data = self.int2BCD(int(data))
        return data

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0200"
        msgBodyProperty = self.getMsgBodyProperty(int(len(self.getMsgBody()) / 2))              #消息体属性
        phoneNum = self.int2BCD(13146201110)                     #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)            #消息流水号
        subPkgContent = ""                                       #消息包封装项
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息体属性
    def getMsgBodyProperty(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #######################################################
    # 获取报警标志
    #######################################################
    def getAlarmFlag(self):
        emergencyAlarm = 1                           #紧急报警，触动报警开关后触发
        overspeedAlarm = 2                           #超速报警
        fatigueDriving = 4                           #疲劳驾驶
        dangerAlarm = 8                              #危险预警
        GNSSTrouble = 16                             #GNSS 模块发生故障
        GNSSAntennaeLost = 32                        #GNSS 天线未接或被剪断
        GNSSAntennaeShortOut = 64                    #GNSS 天线短路
        TerminalMainPowerLackVoltage = 128           #终端主电源欠压
        TerminalMainPowerLostConnect = 256           #终端主电源掉电（设备拔出告警）
        TerMinalLCDTrouble = 512                     #终端 LCD 或显示器故障
        TTSTrouble = 1024                            #TTS 模块故障
        cameraTrouble = 2048                         #摄像头故障
        ICTrouble = 4096                             #道路运输证 IC 卡模块故障
        speedEarlyWarning = 8192                     #超速预警
        fatigueDrivingearlyWarning = 16384           #疲劳驾驶预警
        retain1 = 0
        retain2 = 0
        retain3 = 0
        drivingOverTime = 262144                     #当天累计驾驶超时
        stoppingOverTime = 524288                    #超时停车
        InOutArea = 1048576                          #进出区域
        InOutRouting = 2097152                       #进出路线
        drivingLongOrShort = 4194304                 #路段行驶时间不足/过长
        routingDivergeAlarm = 8388608                #路线偏离报警
        VSSTrouble = 16777216                        #车辆 VSS 故障
        oilException = 33554432                      #车辆油量异常
        carLost = 67108864                           #车辆被盗(通过车辆防盗器)
        illegalFire = 134217728                      #车辆非法点火
        illegalMoving = 268435456                    #车辆非法位移（拖车告警）
        collisionAlarm = 536870912                   #碰撞预警
        rollOverAlarm = 1073741824                   #侧翻预警
        illegalOpenDoor = 2147483648                 #非法开门报警（终端未设置区域时， 不判断非法开门）

        # emergencyAlarm = 0                           #紧急报警，触动报警开关后触发
        # overspeedAlarm = 0                           #超速报警
        # fatigueDriving = 0                           #疲劳驾驶
        # dangerAlarm = 0                              #危险预警
        # GNSSTrouble = 0                             #GNSS 模块发生故障
        # GNSSAntennaeLost = 0                        #GNSS 天线未接或被剪断
        # GNSSAntennaeShortOut = 0                    #GNSS 天线短路
        # TerminalMainPowerLackVoltage = 0           #终端主电源欠压
        # TerminalMainPowerLostConnect = 0           #终端主电源掉电（设备拔出告警）
        # TerMinalLCDTrouble = 0                     #终端 LCD 或显示器故障
        # TTSTrouble = 0                            #TTS 模块故障
        # cameraTrouble = 0                         #摄像头故障
        # ICTrouble = 0                             #道路运输证 IC 卡模块故障
        # speedEarlyWarning = 0                     #超速预警
        # fatigueDrivingearlyWarning = 0           #疲劳驾驶预警
        # retain1 = 0
        # retain2 = 0
        # retain3 = 0
        # drivingOverTime = 0                     #当天累计驾驶超时
        # stoppingOverTime = 0                    #超时停车
        # InOutArea = 0                          #进出区域
        # InOutRouting = 0                       #进出路线
        # drivingLongOrShort = 0                 #路段行驶时间不足/过长
        # routingDivergeAlarm = 0                #路线偏离报警
        # VSSTrouble = 0                        #车辆 VSS 故障
        # oilException = 0                      #车辆油量异常
        # carLost = 0                           #车辆被盗(通过车辆防盗器)
        # illegalFire = 0                      #车辆非法点火
        # illegalMoving = 0                    #车辆非法位移（拖车告警）
        # collisionAlarm = 0                   #碰撞预警
        # rollOverAlarm = 0                   #侧翻预警
        # illegalOpenDoor = 0                 #非法开门报警（终端未设置区域时， 不判断非法开门）

        data = emergencyAlarm + overspeedAlarm + fatigueDriving + dangerAlarm + GNSSTrouble + GNSSAntennaeLost
        data = data + GNSSAntennaeShortOut + TerminalMainPowerLackVoltage + TerminalMainPowerLostConnect + TerMinalLCDTrouble
        data = data + TTSTrouble + cameraTrouble + ICTrouble + speedEarlyWarning + fatigueDrivingearlyWarning
        data = data + retain1 + retain2 + retain3 + drivingOverTime + stoppingOverTime
        data = data + InOutArea + InOutRouting + drivingLongOrShort + routingDivergeAlarm + VSSTrouble
        data = data + oilException + carLost + illegalFire + illegalMoving + collisionAlarm
        data = data + rollOverAlarm + illegalOpenDoor
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex

    #######################################################
    # 获取状态
    #######################################################
    def getStatus(self):
        ACCStatus = 1                           #0：ACC 关；1： ACC 开  (1)
        locationStatus = 2                      #0：未定位；1：定位      (2)
        latitudeStatus = 4                      #0：北纬；1：南纬        (4)
        longitudeStatus = 0                     #0：东经；1：西经          (8)
        runStatus = 0                           #0：运营状态；1：停运状态      (16)
        isLocationEncrypt = 0                   #0：经纬度未经保密插件加密；1：经纬度已经保密插件加密 (32)
        retain6_7 = 0
        # 00：空车；01：半载；10：保留；11：满载(0 , 256 ,512 , 768)
        #（可用于客车的空、重车及货车的空载、满载状态表示，人工输入或传感器 获取）
        isFull = 256
        oilRouteStatus = 0                      #0：车辆油路正常；1：车辆油路断开  (1024)
        powerStatus = 0                         #0：车辆电路正常；1：车辆电路断开   (2048)
        doorLockStatus = 0                      #0：车门解锁；1：车门加锁    (4096)
        frontDoor = 0                           #0：门 1 关；1：门	1 开（前门）   (8192)
        middleDoor = 0                          #0：门 2 关；1：门	2 开（中门）   (16384)
        backDoor = 0                            #0：门 3 关；1：门	3 开（后门）   (32768)
        drivingDoor = 0                         #0：门 4 关；1：门	4 开（驾驶席门）   (65536)
        otherDoor = 0                           #0：门 5 关；1：门	5 开（自定义）   (131072)
        GPSStatus = 262144                      #0：未使用 GPS 卫星进行定位；1：使用 GPS 卫星进行定位  (262144)
        beidouStatus = 524288                   #0：未使用北斗卫星进行定位；1：使用北斗卫星进行定位  (524288)
        GLONSSStatus = 1048576                  #0：未使用 GLONASS 卫星进行定位；1：使用 GLONASS 卫星进行定位  (1048576)
        GalileoStatus = 0                       #0：未使用 Galileo 卫星进行定位；1：使用 Galileo 卫星进行定位   (2097152)
        retain22_31 = 0

        data = ACCStatus + locationStatus + latitudeStatus + longitudeStatus + runStatus
        data = data + isLocationEncrypt + retain6_7 + isFull + oilRouteStatus + powerStatus
        data = data + doorLockStatus + frontDoor + middleDoor + backDoor + drivingDoor
        data = data + otherDoor + GPSStatus + beidouStatus + GLONSSStatus + GalileoStatus
        data = data + retain22_31
        dataHex = self.int2hexStringByBytes(data,4)
        return dataHex



if __name__ == "__main__":
    # print(Location_msg().getAlarmFlag())
    # print(Location_msg().getInfoTime())
    # print(Location_msg().generateMsg())
    # lati = Location_msg().getLatitude(29.40268)
    # print(lati)
    # print(int("01c329ed",16) / 1000000)
    # print(int("0659dec5", 16) / 1000000)
    print(Location_msg().getLocationBaseInfo_random())



