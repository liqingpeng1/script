#coding:utf-8

from lib.protocol.report.ProtocolBase import ProtocolBase

'''
终端上报故障码数据包
'''
class TroubleCode_protocol(ProtocolBase):

    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",UTCTime="2020-01-09 18:19:38",troubleCodeNum=2,troubleCode=[{"systemId":"00","content1":"00","content2":"01","status":0},{"systemId":"00","content1":"00","content2":"02","status":0}],MILStatus=1):
        super().__init__()
        self.msgCount = int(msgCount)                             # 设置默认要发送的GPS数据包个数
        self.WATER_CODE = int(WATER_CODE);                        # 设置默认消息流水号
        self.DEV_ID = DEV_ID                                      # 设置默认设备id

        self.UTCTime = UTCTime                                    # 设置默认UTC时间
        self.troubleCodeNum = int(troubleCodeNum)                 # 故障码个数
        self.troubleCode = troubleCode                            # 故障码内容
        self.MILStatus = int(MILStatus)                           # MIL状态

    #####################################################
    #               生成故障码消息
    #####################################################
    def generateMsg(self):
        info = ""
        HEADER = "4040"                                                         #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                         #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                              #设备id
        FUN_ID = "001A"                                                         # 功能id(GPS功能id)
        data = ""                                                               #数据段
        for i in range(0,self.msgCount):
            data += self.generateData()
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data)/2))        # 消息长度

        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)                                              # 校验字段
        info += CHECK_CODE
        return info

    #####################################################
    #               创建故障码包数据段
    #####################################################
    def generateData(self):
        data = ""
        # UTCTime = self.getUTCTime("2020-01-03 13:05:13")
        UTCTime = self.getUTCTime(self.UTCTime)                                      #时间信息
        troubleCodeNum = self.int2hexStringByBytes(self.troubleCodeNum)              #故障码个数
        troubleCodeContent = ""
        for i in range(0,len(self.troubleCode)):
            troubleCodeContent = troubleCodeContent + self.troubleCode[i]["systemId"]
            troubleCodeContent = troubleCodeContent + self.troubleCode[i]["content1"]
            troubleCodeContent = troubleCodeContent + self.troubleCode[i]["content2"]
            troubleCodeContent = troubleCodeContent + self.int2hexStringByBytes(int(self.troubleCode[i]["status"]))
        MILStatus = self.int2hexStringByBytes(self.MILStatus)
        data = data + UTCTime + troubleCodeNum + troubleCodeContent + MILStatus
        return data

    #####################################################
    #               将UTC时间转换为16进制，
    #        例如：2020-01-02   20:30:00 （年取后面2字节）则将20,01，02,20,30,00 转换为对应的6个字节
    #        theTime:传入一个类似：2020-01-03 13:05:13的一个字符串
    #####################################################
    def getUTCTime(self,theTime):
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
        UTCTime = ""
        for i in range(0, len(timeArr)):
            UTCTime += self.int2hexString(int(timeArr[i]))
        return UTCTime