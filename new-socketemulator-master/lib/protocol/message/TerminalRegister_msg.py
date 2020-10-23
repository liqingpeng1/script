#encoding:utf-8

'''
定义终端注册消息
'''
from lib.protocol.message.MessageBase import MessageBase


class TerminalRegister_msg(MessageBase):
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
    def generateMsg_GUI(self,msgID="0100",phoneNum="13146201119",msgWaterCode=1,encryptionType=0,subPkg=0,provinceId=50,\
                        countyId=103,manufacturerId="11010",terminalType="a865h643gfdj64fd7432",terminalId="H6uyt08", \
                        licencePlateColor=1,carSign="渝B23CX"):
        msg = ""
        msgBody = self.getMsgBody_GUI(provinceId,countyId,manufacturerId,terminalType,terminalId,licencePlateColor,carSign)
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,msgBody)
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    # 生成一条完整的消息，数据随机产生
    def generateMsg_random(self):
        msgID = "0100"
        phoneNum = self.getRandomStr(11, "0123456789")
        msgWaterCode = self.getRandomNum(1, 65535)
        encryptionType = 0
        subPkg = self.getRandomNum(intArr=[0, 8192])
        provinceId = self.getRandomNum(10,99)
        countyId = self.getRandomNum(100,990)
        manufacturerId = self.getRandomStr(5,"0123456789")
        terminalType = self.getRandomStr(20)
        terminalId = self.getRandomStr(7)
        licencePlateColor = self.getRandomNum(intArr=[1,2,3,4,9])
        carSign = self.getRandomStr(5)
        msg = ""
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg)
        msgBody = self.getMsgBody_GUI(provinceId, countyId, manufacturerId, terminalType, terminalId, licencePlateColor,
                                      carSign)
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
        # msgNums = self.int2hexStringByBytes(1,2)
        # msgNumber = self.int2hexStringByBytes(1,2)
        #省域 ID (标示终端安装车辆所在的省域，0 保留，由平台取默认值。省 域 ID 采用 GB/T 2260 中规定的行政区划代 码六位中前两)
        provinceId = self.int2hexStringByBytes(50,2)
        #市县域 ID
        countyId = self.int2hexStringByBytes(103,2)
        #制造商 ID (5 个字节，终端制造商编码)
        manufacturerId = self.str2Hex("man03")
        #终端型号 (20 个字节，此终端型号由制造商自行定义，位数不足时，后 补“0X00”。)
        terminalType = self.str2Hex("a865h643gfdj64fd7432")
        #终端 ID (7 个字节，由大写字母和数字组成，此终端 ID 由制造商自行 定义，位数不足时，后补“0X00”)
        terminalId = self.str2Hex("H6uyt08")
        #车牌颜色 (车牌颜色，按照 JT/T415-2006 的 5.4.12。未上牌时，取值 为 0) 1：蓝色 2：黄色 3：黑色 4：白色 9：其他
        licencePlateColor = self.int2hexStringByBytes(2)
        #车辆标识 (车牌颜色为 0 时，表示车辆 VIN；否则，表示公安交通管理 部门颁发的机动车号牌)
        carSign = self.GBKString2Hex("渝B23CX")
        # msg = msg + msgNums + msgNumber
        msg = msg + provinceId + countyId + manufacturerId + terminalType + terminalId + licencePlateColor + carSign
        return msg

    # 获取消息体，针对图形界面，可传递参数
    def getMsgBody_GUI(self,provinceId=50,countyId=103,manufacturerId="11010",terminalType="a865h643gfdj64fd7432",terminalId="H6uyt08", \
                   licencePlateColor=1,carSign="渝B23CX"):
        msg = ""
        # msgNums = self.int2hexStringByBytes(1,2)
        # msgNumber = self.int2hexStringByBytes(1,2)
        #省域 ID (标示终端安装车辆所在的省域，0 保留，由平台取默认值。省 域 ID 采用 GB/T 2260 中规定的行政区划代 码六位中前两)
        provinceId = self.int2hexStringByBytes(provinceId,2)
        # 市县域 ID
        countyId = self.int2hexStringByBytes(countyId, 2)
        #制造商 ID (5 个字节，终端制造商编码)
        manufacturerId = self.str2Hex(manufacturerId)
        #终端型号 (20 个字节，此终端型号由制造商自行定义，位数不足时，后 补“0X00”。)
        terminalType = self.str2Hex(terminalType)
        #终端 ID (7 个字节，由大写字母和数字组成，此终端 ID 由制造商自行 定义，位数不足时，后补“0X00”)
        terminalId = self.str2Hex(terminalId)
        #车牌颜色 (车牌颜色，按照 JT/T415-2006 的 5.4.12。未上牌时，取值 为 0) 1：蓝色 2：黄色 3：黑色 4：白色 9：其他
        licencePlateColor = self.int2hexStringByBytes(licencePlateColor)
        #车辆标识 (车牌颜色为 0 时，表示车辆 VIN；否则，表示公安交通管理 部门颁发的机动车号牌)
        carSign = self.GBKString2Hex(carSign)
        # msg = msg + msgNums + msgNumber
        msg = msg + provinceId + countyId + manufacturerId + terminalType + terminalId + licencePlateColor + carSign
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0100"
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

    #获取消息体属性，针对图形界面，可传递参数
    def getMsgBodyProperty_GUI(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

if __name__ == "__main__":
    print(TerminalRegister_msg().generateMsg())