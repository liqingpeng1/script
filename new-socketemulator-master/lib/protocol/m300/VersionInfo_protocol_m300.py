#encoding:utf-8

from lib.protocol.m300.M300Base import M300Base

'''
定义终端版本协议类
'''

class VersionInfo_protocol_m300(M300Base):
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0,SWVersion="VSTA000GV100",SWDate="2020-03-30",HWVersion="M1.0" \
                 ,GSMType="GSM_type_123456",carType="150",engineCode=1,VINCode="VIN_CODE_01234567890"):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.waterCode = waterCode                    #消息流水号
        self.DEV_ID = DEV_ID                          #设备Id
        self.encryptionType = encryptionType          #消息属性里面的是否加密字段

        self.SWVersion = SWVersion                    #软件版本号
        self.SWDate = SWDate                          #软件日期
        self.HWVersion = HWVersion                    #硬件版本
        self.GSMType = GSMType                        #GSM 型号
        self.carType = int(carType)                   #车系车型ID: 150D
        self.engineCode = engineCode                  #发动机编码类别
        self.VINCode = VINCode                        #汽车VIN码 或 发动机ECU编码


    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0007"                                                  #功能id
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
        SWVersion = self.str2Hex(self.SWVersion)
        SWDate = self.str2Hex(self.SWDate)
        HWVersion = self.str2Hex(self.HWVersion)
        GSMType = self.str2Hex(self.GSMType)
        carType = self.int2hexStringByBytes(self.carType,2)
        engineCode = self.int2hexStringByBytes(self.engineCode)
        VINCode = self.str2Hex(self.VINCode)
        data = SWVersion + SWDate + HWVersion + GSMType + carType + engineCode + VINCode
        return data

if __name__ == "__main__":
    print(VersionInfo_protocol_m300().generateMsg())