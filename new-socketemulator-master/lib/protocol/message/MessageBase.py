#encoding:utf-8
import datetime
import random
import re
import time

from lib.protocol.Base import Base

'''
定义消息协议类的基类
'''

class MessageBase(Base):

    def __init__(self):
        self.IDENTIFY = "7e"     #标识位

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


    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        msgID = self.int2hexStringByBytes(102,2)                             #消息id
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(subPkg=subPkg)             #消息体属性
        phoneNum = self.int2BCD(13146201118)                                 #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1)                          #消息流水号
        if subPkg != 8192:
            subPkgContent = ""                                               #消息包封装项
        else:
            subPkgContent = self.getMsgPackage()
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息头，针对图形界面，可传递参数
    def getMsgHeader_GUI(self,msgID,phoneNum,msgWaterCode,encryptionType,subPkg,msgBody=""):                                                        #消息id
        msgID = msgID
        subPkg = subPkg
        msgBodyProperty = self.getMsgBodyProperty_GUI(msgBodyLen=int(len(msgBody) / 2),encryptionType=encryptionType,subPkg=subPkg)  #消息体属性
        phoneNum = self.int2BCD(phoneNum)                                                                 #终端手机号
        msgWaterCode = self.int2hexStringByBytes(msgWaterCode,2)                                                        #消息流水号
        if subPkg != 8192:
            subPkgContent = ""                                                                               #消息包封装项
        else:
            subPkgContent = self.getMsgPackage()
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息体属性
    def getMsgBodyProperty(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                      #消息体长度
        encryptionType = encryptionType                              #加密方式
        subPkg = subPkg                                              #分包
        retain = 0                                                   #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #获取消息体属性，针对图形界面，可传递参数
    def getMsgBodyProperty_GUI(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                       #消息体长度
        encryptionType = encryptionType                               #加密方式
        subPkg = subPkg                                               #分包
        retain = 0                                                    #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #获取消息封装项
    def getMsgPackage(self):
        pkgCounts = 2                   #消息报包总数
        pkgCountsHex = self.int2hexStringByBytes(2,2)
        pkgNumsHex = ""
        for i in range(0,pkgCounts):
            pkgNum = i
            dataHex = self.int2hexStringByBytes(pkgNum,2)
            pkgNumsHex = pkgNumsHex + dataHex
        msgPackage = pkgCountsHex + pkgNumsHex
        return msgPackage



    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        return ""

    #######################################################
    # 获取校验码
    #######################################################
    def getCheckCode(self,data="aa"):
        if len(data) % 2 == 1:
            raise RuntimeError('数据段错误！')
        start = data[0:2]
        tmp = int(start,16)
        for i in range(2,len(data),2):
            tmp = tmp ^ int(data[i:i + 2],16)
        dataHex = self.int2hexStringByBytes(tmp)
        return dataHex

    #######################################################
    # 替换消息中的7e7d字符
    #######################################################
    def replace7e7d(self,data):
        # data = data.replace("7d","7d01")
        # data = data.replace("7e","7d02")

        tmpR = data
        tmp = tmpR[0:2]
        tmpA = tmpR[0:2]
        tmpR = tmpR[2:]
        data = ""
        while tmpA != "":
            if tmp == "7d":
                tmp = "7d01"
            elif tmp == "7e":
                tmp = "7d02"
            data = data + tmp
            tmp = tmpR[0:2]
            tmpA = tmpR[0:2]
            tmpR = tmpR[2:]
        return data

    #######################################################
    # 字符串转16进制
    #######################################################
    def str2Hex(self,data):
        dataHex = ""
        tem = ""
        for i in data:
            tem = ord(i)
            dataHex += hex(tem)[2:]
        return dataHex

    #######################################################
    # 16进制转字符串
    #######################################################
    def hex2Str(self,data):
        theStr = ""
        while data != "":
            tmp = data[:2]
            data = data[2:]
            theStr = theStr + chr(int(tmp,16))
        return theStr

    #####################################################
    # 将字符串转换为对应的ascii值数组
    #####################################################
    def str2Ascsii(self,data):
        asciiArr = []
        for i in range(0, len(data)):
            asciiValue = ord(data[i])
            asciiArr.append(asciiValue)
        return asciiArr

    ####################################################
    # 将整数转换为有符号的整数
    #####################################################
    def num2signedNum(self,num):
        return num & 0xff

    #####################################################
    # 数字转换为16进制字符串，通过传入字节数可自动补0
    # 传入数据格式所占字节数
    #####################################################
    def int2hexStringByBytes(self, num,bytescount=1):
        hexStr = hex(num)[2:]
        while len(hexStr) < (bytescount * 2):
            hexStr = "0" + hexStr
        return hexStr

    ####################################################
    # 将10进制转换位8421码
    #####################################################
    def int2BCD(self,data,bytescount=6):
        data = str(data)
        while len(data) < bytescount * 2:
            data = "0" + data
        return data

    #######################################################
    # 获取UTC时间转换位BCD格式
    #######################################################
    def getBCDTime(self,data="2020-02-04 18:57:04"):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = data
        data = data.replace("-","")
        data = data.replace(" ","")
        data = data.replace(":","")
        data = data[2:]
        data = self.int2BCD(int(data))
        return data

    #######################################################
    # 字符串转换为GBK的16进制
    #######################################################
    def GBKString2Hex(self,data):
        '''
        data = str(data.encode("gbk"))
        dataHex = self.str2Hex(data[2:len(data) - 1])
        return dataHex
        '''
        dataHex = ""
        strLen = len(data)
        for i in range(0,strLen):
            if re.search("[0-9a-zA-Z-_]",data[i]) != None:
                dataHex = dataHex + self.str2Hex(data[i])
            else:
                temp = str(data[i].encode("gbk")).replace("\\x","")
                dataHex = dataHex + temp[2:len(temp) - 1]
        return dataHex


    #######################################################
    # 16进制转换为GBK字符串
    #######################################################
    def hex2GBKString(self,dataHex):
        dataStr = self.hex2Str(dataHex)
        data = bytes(map(ord,str(dataStr)))
        data = data.decode("gbk")
        return data

    #######################################################
    # 获取一个随机数，也可以指定获取数组中的随机字符串
    #######################################################
    def getRandomNum(self,s=1,e=1,intArr=[],mult=0):
        if intArr == []:
            data = random.randint(s, e)
        else:
            if mult == 0:
                if type(intArr[0]) == int:
                    data = int(random.choice(intArr))
                elif type(intArr[0]) == str:
                    data = random.choice(intArr)
            else:
                if type(intArr[0]) == int:
                    if len(intArr) < mult:
                        raise RuntimeError('个数超过数组长度！')
                    temp = []
                    data = 0
                    for i in range(0,mult):
                        num = int(random.choice(intArr))
                        if num in temp:
                            # num = int(random.choice(intArr))
                            num = 0
                        temp.append(num)
                        data = data + num
                elif type(intArr[0]) == str:
                    if len(intArr) < mult:
                        raise RuntimeError('个数超过数组长度！')
                    temp = []
                    data = ""
                    for i in range(0,mult):
                        num = random.choice(intArr)
                        if num in temp:
                            # num = int(random.choice(intArr))
                            num = "0"
                        temp.append(num)
                        data = data + num
        return data

    #######################################################
    # 获取一个随机字符串
    #######################################################
    def getRandomStr(self,counts,strs=""):
        if strs == "":
            data = random.sample("0123456789abcdefghijkmlnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-", counts)
        else:
            data = []
            for s in range(0,counts):
                data.append(random.choice(strs))
        temp = ""
        for ch in data:
            temp = temp +ch
        return temp

    #######################################################
    # 获取随机时间
    # type：0、获取年月日时分秒 1、获取年月日 2、获取时分秒
    #######################################################
    def getRandomDate(self,s=631123200,e=1577808000,type=0):
        timeStamp = random.randint(s, e)
        timeArray = time.localtime(timeStamp)
        if type == 0:
            theTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        elif type == 1:
            theTime = time.strftime("%Y-%m-%d", timeArray)
        elif type == 2:
            theTime = time.strftime("%H:%M:%S", timeArray)
        return theTime



if __name__ == "__main__":
    # print(MessageBase().str2Hex("uvwxyz"))
    # print(MessageBase().str2Ascsii("uvwxyz"))
    # print(MessageBase().int2hexStringByBytes(220400566542345564784802,20))
    # print(MessageBase().str2Hex("a865h643gfdj64fd7432"))
    # print(MessageBase().hex2Str("d4c1423939383838"))
    # print(MessageBase().GBKString2Hex("KZP200_V201001"))
    # print(MessageBase().hex2GBKString("4b5a503230305f56323031303031"))
    # print(MessageBase().str2Hex("\xd3\xe5B23CX"))
    # print(MessageBase().getMsgBodyProperty())
    # print(MessageBase().int2BCD(13146201117))
    # print(MessageBase().getCheckCode("8001000501314620111800000000000200"))
    # print(MessageBase().getMsgHeader())
    # print(MessageBase().generateMsg())
    print(MessageBase().GBKString2Hex("渝B23CX"))
    print(MessageBase().hex2GBKString("d3e54232334358"))
    print(MessageBase().hex2GBKString("4c323030414230313032303030312c737a6c696e6779692e716963702e7669702c383838392c537a4c696e6759692c7a373254713246742c4c3230304142303130322e303030312e42494e2c2f2c"))
    # print(MessageBase().int2BCD(123456789012345,10))
    # print(MessageBase().getRandomNum(3000,5000,[2,4,6,8,10,12],4))
    # print(MessageBase().getRandomStr(10))
    print(MessageBase().replace7e7d("807d007e01314620111800000000000200"))
    print(MessageBase().replace7e7d("87d107e501314620111800000000000200"))
