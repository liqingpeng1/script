#encoding:utf-8

'''
定义数据上行透传消息
'''
import datetime

from lib.protocol.message.MessageBase import MessageBase


class DataUpstreamTransport_msg(MessageBase):
    def __init__(self):
        super().__init__()          #不执行该方法，无法使用父类里面定义的属性
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
    def generateMsg_GUI(self,msgID="0900",phoneNum="13146201119",msgWaterCode=1,encryptionType=0,subPkg=0,msgType="F3",data={"infoTime":"2020-02-06 11:31:56"}):
        msg = ""
        msgBody = self.getMsgBody_GUI(msgType,data)
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,msgBody)
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
        #透传消息类型
        #0xF1	驾驶行程数据（熄火发送）
        # 0xF2	故障码数据（状态改变发送）
        # 0xF3	休眠进入(进入休眠模式发送)
        # 0xF4	休眠唤醒（退出休眠模式发送）
        msgType = "F2"
        msgContent = ""
        if msgType == "F1":
            msgContent = self.getDrivingData()              #驾驶行程数据（熄火发送）
        elif msgType == "F2":
            msgContent = self.getTroubleCodeData()      #故障码数据（状态改变发送）
        elif msgType == "F3":
            msgContent = self.getIntoSleepData()          #休眠进入(进入休眠模式发送)
        elif msgType == "F4":
            msgContent = self.getOutSleepData()                #休眠唤醒（退出休眠模式发送）
        msg = msgType + msgContent
        return msg

    # 获取消息体，针对图形界面，可传递参数
    def getMsgBody_GUI(self,msgType="F3",data={"infoTime":"2020-02-06 11:31:56"}):
        msg = ""
        # 透传消息类型
        # 0xF1	驾驶行程数据（熄火发送）
        # 0xF2	故障码数据（状态改变发送）
        # 0xF3	休眠进入(进入休眠模式发送)
        # 0xF4	休眠唤醒（退出休眠模式发送）
        msgType = msgType
        msgContent = ""
        if msgType == "F1":
            # 驾驶行程数据（熄火发送）
            msgContent = self.getDrivingData_GUI(data["time_1"],data["time_2"],data["fireLatitude"],data["fireLongitude"],data["unFireLatitude"], \
                           data["unFireLongitude"],data["drivingCircleLabel"],data["drivingCircleTotalMileageType"],data["drivingCircleTotalMileage"], \
                           data["drivingCircleTotalOil"],data["drivingCircleTotalTime"],data["drivingCircleOverSpeedTotalTime"], \
                           data["drivingCircleOverSpeedTotalTimes"],data["drivingCircleAverageSpeed"],data["drivingCircleMaxSpeed"], \
                           data["drivingCircleIdlingTime"],data["drivingCircleFootBrakeIsSupport"],data["drivingCircleFootBrakeTatalTimes"], \
                           data["drivingCircleRapidlyAccelerateTimes"],data["drivingCircleSharpSlowdownTimes"],data["drivingCircleSharpCurveTimes"], \
                           data["speedIn20"],data["speedIn20_40"],data["speedIn40_60"],data["speedIn60_80"],data["speedIn80_100"],data["speedIn100_120"], \
                           data["speedOut120"],data["rapidlyAccelerateTimes"],data["rapidlySharpSlowdownTimes"],data["sharpCurveTimes"])
        elif msgType == "F2":
            # 故障码数据（状态改变发送）
            msgContent = self.getTroubleCodeData_GUI(data["infoTime"],data["latitude"],data["longitude"],data["troubleCodeNums"],data["systemId"])
        elif msgType == "F3":
            # 休眠进入(进入休眠模式发送)
            msgContent = self.getIntoSleepData_GUI(data["infoTime"])
        elif msgType == "F4":
            # 休眠唤醒（退出休眠模式发送）
            msgContent = self.getOutSleepData_GUI(data["infoTime"],data["outSleepType"],data["carVoltage"],data["vibrateOutSleepSpeedUpVal"])
        msg = msgType + msgContent
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0900"
        msgBodyProperty = self.getMsgBodyProperty(int(len(self.getMsgBody()) / 2))              #消息体属性
        phoneNum = self.int2BCD(13146201119)                     #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                           #消息流水号
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
    # 获取驾驶行程数据
    #######################################################
    def getDrivingData(self):
        time_1 = "0001" + self.int2hexStringByBytes(6) + self.getBCDTime("2020-02-05 22:07:30")
        time_2 = "0002" + self.int2hexStringByBytes(6) + self.getBCDTime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        fireLatitude = "0003" + self.int2hexStringByBytes(4) + self.getFireLatitude(29.40268)            #点火纬度
        fireLongitude = "0004" + self.int2hexStringByBytes(4) + self.getFireLongitude(106.54041)          #点火经度
        unFireLatitude = "0005" + self.int2hexStringByBytes(4) + self.getUnFireLatitude(29.40268)        #熄火纬度
        unFireLongitude = "0006" + self.int2hexStringByBytes(4) + self.getUnFireLongitude(106.54041)      # 熄火经度
        drivingCircleLabel = "0007" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(123,2)  #驾驶循环标签
        #一个驾驶循环总里程类型：
        # 0x01：GPS 总里程(累计)
        # 0x02：J1939 里程算法 1
        # 0x03：J1939 里程算法 2
        # 0x04：J1939 里程算法 3
        # 0x05：J1939 里程算法 4
        # 0x06：J1939 里程算法 5
        # 0x07：OBD 仪表里程
        # 0x08：OBD 速度里程
        # 0x09：J1939 里程算法 6
        # 0x0A：J1939 里程算法 7
        # 0x0B：J1939 里程算法 8
        # 0x0C：J1939 里程算法 9
        drivingCircleTotalMileageType = "0008" + self.int2hexStringByBytes(1) + "01"
        #一个驾驶循环总里程，单位米
        drivingCircleTotalMileage = "0009" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(38090,4)
        #一个驾驶循环总耗油，单位毫升(ml)
        drivingCircleTotalOil = "000A" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(75400,4)
        #一个驾驶循环总时长，单位秒
        drivingCircleTotalTime = "000B" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(726000,4)
        #一个驾驶循环超速累计时长，单位秒
        drivingCircleOverSpeedTotalTime = "000C" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(54000,2)
        #一个驾驶循环超速次数，单位次
        drivingCircleOverSpeedTotalTimes = "000D" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(101,2)
        #一个驾驶循环平均车速，单位 KM/H
        drivingCircleAverageSpeed = "000E" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(65)
        #一个驾驶循环最大车速，单位 KM/H
        drivingCircleMaxSpeed = "000F" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(123)
        #一个驾驶循环怠速时长，单位秒
        drivingCircleIdlingTime = "0010" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(12600000,4)
        #一个驾驶循环脚刹次数支持与否，1 为支持
        drivingCircleFootBrakeIsSupport = "0011" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(1)
        #一个驾驶循环脚刹总次数，单位次
        drivingCircleFootBrakeTatalTimes = "0012" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(32,2)
        #一个驾驶循环急加速次数
        drivingCircleRapidlyAccelerateTimes = "0013" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(79,4)
        #一个驾驶循环急减速次数
        drivingCircleSharpSlowdownTimes = "0014" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(10,4)
        #一个驾驶循环急转弯次数
        drivingCircleSharpCurveTimes = "0015" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(33,4)
        #速度为-20Km/H 的里程,单位:m
        speedIn20 = "0016" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(1068,4)
        #速度为 20-40Km/H 的里程,单位:m
        speedIn20_40 = "0017" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(2020,4)
        #速度为 40-60Km/H 的里程,单位:m
        speedIn40_60 = "0018" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(30400,4)
        #速度为 60-80Km/H 的里程,单位:m
        speedIn60_80 = "0019" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(37000,4)
        #速度为 80-100Km/H 的里程,单位:m
        speedIn80_100 = "001A" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(10400,4)
        #速度为 100-120Km/H 的里程,单位:m
        speedIn100_120 = "001B" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(5000,4)
        #速度为 120Km/H 以上的里程,单位:m
        speedOut120 = "001C" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3200,4)
        #急加速总次数
        rapidlyAccelerateTimes = "001D" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3000,4)
        #急减速总次数
        rapidlySharpSlowdownTimes = "001E" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3507,4)
        #急转弯总次数
        sharpCurveTimes = "001F" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(580,4)

        data = time_1 + time_2 + fireLatitude + fireLongitude + unFireLatitude
        data = data + unFireLongitude + drivingCircleLabel + drivingCircleTotalMileageType + drivingCircleTotalMileage + drivingCircleTotalOil
        data = data + drivingCircleTotalTime + drivingCircleOverSpeedTotalTime + drivingCircleOverSpeedTotalTimes + drivingCircleAverageSpeed + drivingCircleMaxSpeed
        data = data + drivingCircleIdlingTime + drivingCircleFootBrakeIsSupport + drivingCircleFootBrakeTatalTimes + drivingCircleRapidlyAccelerateTimes + drivingCircleSharpSlowdownTimes
        data = data + drivingCircleSharpCurveTimes + speedIn20 + speedIn20_40 + speedIn40_60 + speedIn60_80
        data = data + speedIn80_100 + speedIn100_120 + speedOut120 + rapidlyAccelerateTimes + rapidlySharpSlowdownTimes
        data = data + sharpCurveTimes
        return data

    # 获取驾驶行程数据，针对图形界面，可传递参数
    def getDrivingData_GUI(self,time_1="2020-02-05 22:07:30",time_2="2020-02-08 22:07:30",fireLatitude=29.40268,fireLongitude=106.54041, \
                           unFireLatitude=29.40268,unFireLongitude=106.54041,drivingCircleLabel=123,drivingCircleTotalMileageType="01", \
                           drivingCircleTotalMileage=38090,drivingCircleTotalOil=75400,drivingCircleTotalTime=726000, \
                           drivingCircleOverSpeedTotalTime=54000,drivingCircleOverSpeedTotalTimes=101,drivingCircleAverageSpeed=65, \
                           drivingCircleMaxSpeed=123,drivingCircleIdlingTime=12600000,drivingCircleFootBrakeIsSupport=1, \
                           drivingCircleFootBrakeTatalTimes=32,drivingCircleRapidlyAccelerateTimes=79,drivingCircleSharpSlowdownTimes=10, \
                           drivingCircleSharpCurveTimes=33,speedIn20=1068,speedIn20_40=2020,speedIn40_60=30400,speedIn60_80=37000, \
                           speedIn80_100=10400,speedIn100_120=5000,speedOut120=3200,rapidlyAccelerateTimes=3000, \
                           rapidlySharpSlowdownTimes=3507,sharpCurveTimes=580):
        time_1 = "0001" + self.int2hexStringByBytes(6) + self.getBCDTime(time_1)
        time_2 = "0002" + self.int2hexStringByBytes(6) + self.getBCDTime(time_2)
        fireLatitude = "0003" + self.int2hexStringByBytes(4) + self.getFireLatitude(fireLatitude)            #点火纬度
        fireLongitude = "0004" + self.int2hexStringByBytes(4) + self.getFireLongitude(fireLongitude)          #点火经度
        unFireLatitude = "0005" + self.int2hexStringByBytes(4) + self.getUnFireLatitude(unFireLatitude)        #熄火纬度
        unFireLongitude = "0006" + self.int2hexStringByBytes(4) + self.getUnFireLongitude(unFireLongitude)      # 熄火经度
        drivingCircleLabel = "0007" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(drivingCircleLabel,2)  #驾驶循环标签
        #一个驾驶循环总里程类型：
        drivingCircleTotalMileageType = "0008" + self.int2hexStringByBytes(1) + drivingCircleTotalMileageType
        #一个驾驶循环总里程，单位米
        drivingCircleTotalMileage = "0009" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleTotalMileage,4)
        #一个驾驶循环总耗油，单位毫升(ml)
        drivingCircleTotalOil = "000A" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleTotalOil,4)
        #一个驾驶循环总时长，单位秒
        drivingCircleTotalTime = "000B" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleTotalTime,4)
        #一个驾驶循环超速累计时长，单位秒
        drivingCircleOverSpeedTotalTime = "000C" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(drivingCircleOverSpeedTotalTime,2)
        #一个驾驶循环超速次数，单位次
        drivingCircleOverSpeedTotalTimes = "000D" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(drivingCircleOverSpeedTotalTimes,2)
        #一个驾驶循环平均车速，单位 KM/H
        drivingCircleAverageSpeed = "000E" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(drivingCircleAverageSpeed)
        #一个驾驶循环最大车速，单位 KM/H
        drivingCircleMaxSpeed = "000F" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(drivingCircleMaxSpeed)
        #一个驾驶循环怠速时长，单位秒
        drivingCircleIdlingTime = "0010" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleIdlingTime,4)
        #一个驾驶循环脚刹次数支持与否，1 为支持
        drivingCircleFootBrakeIsSupport = "0011" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(drivingCircleFootBrakeIsSupport)
        #一个驾驶循环脚刹总次数，单位次
        drivingCircleFootBrakeTatalTimes = "0012" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(drivingCircleFootBrakeTatalTimes,2)
        #一个驾驶循环急加速次数
        drivingCircleRapidlyAccelerateTimes = "0013" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleRapidlyAccelerateTimes,4)
        #一个驾驶循环急减速次数
        drivingCircleSharpSlowdownTimes = "0014" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleSharpSlowdownTimes,4)
        #一个驾驶循环急转弯次数
        drivingCircleSharpCurveTimes = "0015" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(drivingCircleSharpCurveTimes,4)
        #速度为-20Km/H 的里程,单位:m
        speedIn20 = "0016" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedIn20,4)
        #速度为 20-40Km/H 的里程,单位:m
        speedIn20_40 = "0017" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedIn20_40,4)
        #速度为 40-60Km/H 的里程,单位:m
        speedIn40_60 = "0018" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedIn40_60,4)
        #速度为 60-80Km/H 的里程,单位:m
        speedIn60_80 = "0019" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedIn60_80,4)
        #速度为 80-100Km/H 的里程,单位:m
        speedIn80_100 = "001A" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedIn80_100,4)
        #速度为 100-120Km/H 的里程,单位:m
        speedIn100_120 = "001B" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedIn100_120,4)
        #速度为 120Km/H 以上的里程,单位:m
        speedOut120 = "001C" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(speedOut120,4)
        #急加速总次数
        rapidlyAccelerateTimes = "001D" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(rapidlyAccelerateTimes,4)
        #急减速总次数
        rapidlySharpSlowdownTimes = "001E" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(rapidlySharpSlowdownTimes,4)
        #急转弯总次数
        sharpCurveTimes = "001F" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(sharpCurveTimes,4)

        data = time_1 + time_2 + fireLatitude + fireLongitude + unFireLatitude
        data = data + unFireLongitude + drivingCircleLabel + drivingCircleTotalMileageType + drivingCircleTotalMileage + drivingCircleTotalOil
        data = data + drivingCircleTotalTime + drivingCircleOverSpeedTotalTime + drivingCircleOverSpeedTotalTimes + drivingCircleAverageSpeed + drivingCircleMaxSpeed
        data = data + drivingCircleIdlingTime + drivingCircleFootBrakeIsSupport + drivingCircleFootBrakeTatalTimes + drivingCircleRapidlyAccelerateTimes + drivingCircleSharpSlowdownTimes
        data = data + drivingCircleSharpCurveTimes + speedIn20 + speedIn20_40 + speedIn40_60 + speedIn60_80
        data = data + speedIn80_100 + speedIn100_120 + speedOut120 + rapidlyAccelerateTimes + rapidlySharpSlowdownTimes
        data = data + sharpCurveTimes
        return data


    #######################################################
    # 获取点火纬度，单位：0.000001 度，Bit31=0/1	北纬/南纬
    #######################################################
    def getFireLatitude(self,data=29.40268):
        orientation = 0                  #0:北纬  1：南纬  （2147483648）
        data = int(data * 1000000)
        data = data + orientation
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 点火经度，单位：0.000001 度，Bit31=0/1	东经/西经
    #######################################################
    def getFireLongitude(self,data=106.54041):
        orientation = 0                  #0:东经  1：西经  （2147483648）
        data = int(data * 1000000)
        data = data + orientation
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 获取熄火纬度，单位：0.000001 度，Bit31=0/1	北纬/南纬
    #######################################################
    def getUnFireLatitude(self,data=29.40268):
        orientation = 0                  #0:北纬  1：南纬  （2147483648）
        data = int(data * 1000000)
        data = data + orientation
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 熄火经度，单位：0.000001 度，Bit31=0/1	东经/西经
    #######################################################
    def getUnFireLongitude(self,data=106.54041):
        orientation = 0                  #0:东经  1：西经  （2147483648）
        data = int(data * 1000000)
        data = data + orientation
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 获取故障码数据
    #######################################################
    def getTroubleCodeData(self):
        infoTime = self.getBCDTime("2020-02-06 11:31:56")
        #单位：0.000001 度，Bit31=0/1	北纬/南纬
        latitude = self.getLatitude(29.40268)
        #单位：0.000001 度，Bit31=0/1	东经/西经
        longitude = self.getLongitude(106.54041)
        #为 0 表示无故障码，非 0 为故障码个数
        troubleCodeNums = 6
        troubleCodeNumsHex = self.int2hexStringByBytes(troubleCodeNums)
        #故障码
        troubleCode = ""
        for i in range(0,troubleCodeNums):
            # tbc0 = self.int2hexStringByBytes(i)
            tbc0 = "00"
            # tbc1 = self.int2hexStringByBytes(1)
            tbc1 = self.int2hexStringByBytes(0)
            # tbc2 = self.int2hexStringByBytes(2)
            tbc2 = self.int2hexStringByBytes(i)
            # tbc3 = self.int2hexStringByBytes(3)
            tbc3 = self.int2hexStringByBytes(0)
            troubleCode = troubleCode + tbc0 + tbc1 + tbc2 + tbc3
        data = infoTime + latitude + longitude + troubleCodeNumsHex + troubleCode
        return data

    # 获取故障码数据，针对图形界面，可传递参数
    def getTroubleCodeData_GUI(self,infoTime="2020-02-06 11:31:56",latitude=29.40268,longitude=106.54041,troubleCodeNums=3,systemId="00"):
        infoTime = self.getBCDTime(infoTime)
        #单位：0.000001 度，Bit31=0/1	北纬/南纬
        latitude = self.getLatitude(latitude)
        #单位：0.000001 度，Bit31=0/1	东经/西经
        longitude = self.getLongitude(longitude)
        #为 0 表示无故障码，非 0 为故障码个数
        troubleCodeNums = troubleCodeNums
        troubleCodeNumsHex = self.int2hexStringByBytes(troubleCodeNums)
        #故障码
        troubleCode = ""
        for i in range(0,troubleCodeNums):
            # troubleCode = troubleCode + self.int2hexStringByBytes(i,4)
            tbc0 = systemId
            tbc1 = self.int2hexStringByBytes(0)
            tbc2 = self.int2hexStringByBytes(i)
            tbc3 = self.int2hexStringByBytes(0)
            troubleCode = troubleCode + tbc0 + tbc1 + tbc2 + tbc3
        data = infoTime + latitude + longitude + troubleCodeNumsHex + troubleCode
        return data
    #获取维度
    def getLatitude(self,data=29.40268):
        orientation = 0                  #0:北纬  1：南纬  （2147483648）
        data = int(data * 1000000)
        data = data + orientation
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex
    #获取经度
    def getLongitude(self,data=106.54041):
        orientation = 0                  #0:东经  1：西经  （2147483648）
        data = int(data * 1000000)
        data = data + orientation
        dataHex = self.int2hexStringByBytes(data, 4)
        return dataHex

    #######################################################
    # 获取进入休眠数据包
    #######################################################
    def getIntoSleepData(self):
        infoTime = self.getBCDTime("2020-02-06 11:31:56")
        msg = infoTime
        return msg
    # 获取进入休眠数据包，针对图形界面，可传递参数
    def getIntoSleepData_GUI(self,infoTime="2020-02-06 11:31:56"):
        infoTime = self.getBCDTime(infoTime)
        msg = infoTime
        return msg

    #######################################################
    # 获取休眠唤醒数据包
    #######################################################
    def getOutSleepData(self):
        infoTime = self.getBCDTime("2020-02-06 11:31:56")
        #休眠唤醒类型
        # 0x01：休眠定时唤醒
        # 0x02：CAN1
        # 0x04：CAN2
        # 0x08：gSensor 0x10：电压变
        outSleepType = "01"
        #车辆电压，单位 0.1V
        carVoltage = self.int2hexStringByBytes(360,2)
        #振动唤醒加速度值，单位 mg
        vibrateOutSleepSpeedUpVal = self.int2hexStringByBytes(3700,2)

        data = infoTime + outSleepType + carVoltage + vibrateOutSleepSpeedUpVal
        return data

    #获取休眠唤醒数据包，针对图形界面，可传递参数
    def getOutSleepData_GUI(self,infoTime="2020-02-06 11:31:56",outSleepType="01",carVoltage=360,vibrateOutSleepSpeedUpVal=3700):
        infoTime = self.getBCDTime(infoTime)
        #休眠唤醒类型
        # 0x01：休眠定时唤醒
        # 0x02：CAN1
        # 0x04：CAN2
        # 0x08：gSensor 0x10：电压变
        outSleepType = outSleepType
        #车辆电压，单位 0.1V
        carVoltage = self.int2hexStringByBytes(carVoltage,2)
        #振动唤醒加速度值，单位 mg
        vibrateOutSleepSpeedUpVal = self.int2hexStringByBytes(vibrateOutSleepSpeedUpVal,2)
        data = infoTime + outSleepType + carVoltage + vibrateOutSleepSpeedUpVal
        return data




if __name__ == "__main__":
    print(DataUpstreamTransport_msg().generateMsg())
