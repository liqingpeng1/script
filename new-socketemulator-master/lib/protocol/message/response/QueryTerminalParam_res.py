#encoding:utf-8

'''
定义查询终端参数应答消息
'''
from lib.protocol.message.MessageBase import MessageBase


class QueryTerminalParam_res(MessageBase):
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

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        msg = ""
        resWaterCode = self.int2hexStringByBytes(1004,2)             #应答流水号,对应的终端参数查询消息的流水号
        resParamCounts = self.int2hexStringByBytes(10)                 #应答参数个数
        paramList = self.getParamList()                                #参数项列表
        msg = resWaterCode + paramList
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0104"
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(msgBodyLen=int(len(self.getMsgBody()) / 2),subPkg=subPkg)  #消息体属性
        phoneNum = self.int2BCD(13146201119)                                                                 #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                                                        #消息流水号
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
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex
    #######################################################
    # 获取参数项列表
    #######################################################
    def getParamList(self):
        #终端心跳发送间隔，单位为秒（s）
        param_0001 = "0001" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(10,4)
        #TCP 消息应答超时时间，单位为秒（s）
        param_0002 = "0002" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(10,4)
        #TCP 消息重传次数
        param_0003 = "0003" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(5,4)
        #主服务器 APN，无线通信拨号访问点。若网络制式为 CDMA，则该处为 PPP 拨号号码
        param_0010 = "0010" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("CDMA_0123")) / 2)) + self.GBKString2Hex("CDMA_0123")
        #主服务器无线通信拨号用户名
        param_0011 = "0011" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("user007")) / 2)) + self.GBKString2Hex("user007")
        #主服务器无线通信拨号密码
        param_0012 = "0012" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("password_123")) / 2)) + self.GBKString2Hex("password_123")
        #主服务器地址,IP 或域名
        param_0013 = "0013" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("www.test.com")) / 2)) + self.GBKString2Hex("www.test.com")
        #备份服务器 APN，无线通信拨号访问点
        param_0014 = "0014" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("192.168.1.3")) / 2)) + self.GBKString2Hex("192.168.1.3")
        #备份服务器无线通信拨号用户名
        param_0015 = "0015" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("user123")) / 2)) + self.GBKString2Hex("user123")
        #备份服务器无线通信拨号密码
        param_0016 = "0016" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("pass1234")) / 2)) + self.GBKString2Hex("pass1234")
        #备份服务器地址,IP 或域名
        param_0017 = "0017" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("www.test2.com")) / 2)) + self.GBKString2Hex("www.test2.com")
        #服务器 TCP 端口/主服务器端口
        param_0018 = "0018" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(53762,4)
        #服务器 UDP 端口/备份服务器端口
        param_0019 = "0019" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(53673,4)
        #位置汇报策略，0：定时汇报；1：定距汇报；2：定时和定距汇报
        param_0020 = "0020" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(0,4)
        #休眠时汇报时间间隔，单位为秒（s），>0
        param_0027 = "0027" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(20,4)
        #缺省时间汇报间隔，单位为秒（s），>0
        param_0029 = "0029" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(30,4)
        #缺省距离汇报间隔，单位为米（m），>0
        param_002C = "002C" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(1000,4)
        #拐点补传角度，<180
        param_0030 = "0030" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(60,4)
        #电子围栏半径（非法位移阈值），单位为米
        param_0031 = "0031" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(100,2)
        #报警屏蔽字，与位置信息汇报消息中的报警标志相对应，相应位为 1 则相应报警被屏蔽
        param_0050 = "0050" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(1,4)
        #最高速度，单位为公里每小时（km/h）
        param_0055 = "0055" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(240000,4)
        #超速持续时间，单位为秒（s）
        param_0056 = "0056" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(1200,4)
        #连续驾驶时间门限，单位为秒（s）
        param_0057 = "0057" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(18000,4)
        #当天累计驾驶时间门限，单位为秒（s）
        param_0058 = "0058" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(19000,4)
        #最小休息时间，单位为秒（s）
        param_0059 = "0059" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3600,4)
        #最长停车时间，单位为秒（s）
        param_005A = "005A" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(4800,4)
        #超速报警预警差值，单位为 1/10Km/h
        param_005B = "005B" + self.int2hexStringByBytes(2) +self.int2hexStringByBytes(50,2)
        #疲劳驾驶预警差值，单位为秒（s），>0
        param_005C = "005C" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(10,2)
        #碰撞报警参数设置：
        # b7-b0：碰撞时间，单位 4ms；
        # b15-b8：碰撞加速度，单位 0.1g，设置范围在：0-79 之间，默认为 10
        param_005D = "005D" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(10 + (30 + 255),2)
        #侧翻报警参数设置：
        # 侧翻角度，单位 1 度，默认为 30 度。
        param_005E = "005E" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(30,2)
        #车辆里程表读数，1/10km
        param_0080 = "0080" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(320000,4)
        #车辆所在的省域 ID
        param_0081 = "0081" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(50,2)
        #车辆所在的市域 ID
        param_0082 = "0082" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(100,2)
        #公安交通管理部门颁发的机动车号牌
        param_0083 = "0083" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("CX3B")) / 2)) + self.GBKString2Hex("CX3B")
        #车牌颜色，按照 JT/T415-2006 的 5.4.12 未上牌时，取值 为 0) 1：蓝色 2：黄色 3：黑色 4：白色 9：其他
        param_0084 = "0084" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(1)
        #GNSS 定位模式，定义如下：
        #bit0，0：禁用 GPS 定位， 1：启用	GPS 定位；
        # bit1，0：禁用北斗定位，	1：启用北斗定位；
        # bit2，0：禁用 GLONASS 定位， 1：启用 GLONASS 定位；
        # bit3，0：禁用 Galileo 定位， 1：启用 Galileo 定位。
        param_0085 = "0085" + self.int2hexStringByBytes(1) + self.getGNSSMode()
        #清零故障码，0x01:清空
        param_2001 = "2001" + self.int2hexStringByBytes(1) + "01"
        #清空设备车辆数据，0x01:清空
        param_2002 = "2002" + self.int2hexStringByBytes(1) + "01"
        #清空驾驶行程数据，0x01:清空
        param_2003 = "2003" + self.int2hexStringByBytes(1) + "01"
        #总油耗（单位 ml）
        param_2004 = "2004" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(5000000,4)
        #水温报警参数（单位℃）
        param_2006 = "2006" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(70,4)
        #急加速参数附表（无）：0-关闭；1-低灵敏；2-中灵敏；3-高灵敏；
        param_2007 = "2007" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(3)
        #急减速参数附表（无）：0-关闭；1-低灵敏；2-中灵敏；3-高灵敏；
        param_2008 = "2008" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(3)
        #急转弯参数附表（无）：0-关闭；1-低灵敏；2-中灵敏；3-高灵敏；
        param_2009 = "2009" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(3)
        #车辆类型，详细见厂家车型表
        param_200A = "200A" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(30,2)
        #车辆电瓶低电压报警阈值（单位 0.1V）
        param_200B = "200B" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(3,4)
        #怠速时间过长报警（单位 S）
        param_200C = "200C" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(6000,4)
        #定位时间过长报警（单位 S）
        param_200D = "200D" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(60,4)
        #拖车报警参数附表（无）
        param_200E = "200E" + self.int2hexStringByBytes(int(len(self.GBKString2Hex("Alarm003")) / 2)) + self.GBKString2Hex("Alarm003")
        #碰撞报警参数附表（无）：0-关闭；1-低灵敏；2-中灵敏；3-高灵敏；
        param_200F = "200F" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(1)
        #点火门限电压,单位 0.1V
        param_200F = "200F" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(2200,4)
        #里程类型(高位字节)，油耗类型(低位字节)
        # 里程类型：
        # 0x00: 取消强制设置
        # 0x01: GPS
        # 0x02: J19391； 0x03: J19392； 0x04: J19393；
        # 0x05: J19394； 0x06: J19395； 0x07: OBD 仪表；
        # 0x08: OBD/私有协议；
        # 0x09: J1939A； 0x0A: J1939B； 0x0B: J1939C；0x0C: J1939D
        # …
        # 0xFF: 不改变强制类型
        #
        # 油耗类型：
        # 0x00: 取消强制设置
        # 0x01: J19391； 0x02: J19392； 0x03: J19393； 0x04: J19394
        # 0x05: J19395； 0x06: OBD1；	0x07: OBD2
        # …
        # 0xFF: 不改变强制类型
        param_2012 = "2012" + self.int2hexStringByBytes(2) + "0001"
        #里程系数：设置值/1000，例如：1020 -> 1.02
        param_2013 = "2013" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(2000,2)
        #油耗系数：设置值/1000，例如：1020 -> 1.02
        param_2014 = "2014" + self.int2hexStringByBytes(2) + self.int2hexStringByBytes(2000,2)
        #00：关闭 OBD 功能（禁止终端设备访问汽车 ECU）
        # 01：开启 OBD 功能（允许终端设备访问汽车 ECU）
        param_2017 = "2017" + self.int2hexStringByBytes(1) + "01"
        #发送位置数据方式，设备默认采用先进先出
        # 0x00:先进先出（默认）
        # 0x01:实时优先
        param_2018 = "2018" + self.int2hexStringByBytes(1) + "00"
        #三急报警需要增加前后几秒的数据包（增加的数据主要是针对 0200） 0x00-0x0A,最大是 10 秒，默认是 0 秒，即是关闭该功能。
        param_2019 = "2019" + self.int2hexStringByBytes(1) + "02"
        #读取故障码指令：
        # 0x01:读取 OBD 故障码，通过 0900 上报 F2 上报。
        # 0x00:不读取故障码。
        param_201A = "201A" + self.int2hexStringByBytes(1) + "01"
        #单位秒，休眠唤醒时长最低 5 分钟，即是 300 秒
        param_201C = "201C" + self.int2hexStringByBytes(4) + self.int2hexStringByBytes(300,4)
        #数据加密使能
        # 00：不加密
        # 01：加密算法 1
        # 02：加密算法 2
        param_FF01 = "FF01" + self.int2hexStringByBytes(1) + "00"

        data = param_0001 + param_0002 + param_0003 + param_0010 + param_0011
        data = data + param_0012 + param_0013 + param_0014 + param_0015 + param_0016
        data = data + param_0017 + param_0018 + param_0019 + param_0020 + param_0027
        data = data + param_0029 + param_002C + param_0030 + param_0031 + param_0050
        data = data + param_0055 + param_0056 + param_0057 + param_0058 + param_0059
        data = data + param_005A + param_005B + param_005C + param_005D + param_005E
        data = data + param_0080 + param_0081 + param_0082 + param_0083 + param_0084
        data = data + param_0085 + param_2001 + param_2002 + param_2003 + param_2004
        data = data + param_2006 + param_2007 + param_2008 + param_2009 + param_200A
        data = data + param_200B + param_200C + param_200D + param_200E + param_200F
        data = data + param_2012 + param_2013 + param_2014 + param_2017 + param_2018
        data = data + param_2019 + param_201A + param_201C + param_FF01
        return data




    #获取GNSS 定位模式
    # bit0，0：禁用 GPS 定位， 1：启用	GPS 定位；
    # bit1，0：禁用北斗定位，	1：启用北斗定位；
    # bit2，0：禁用 GLONASS 定位， 1：启用 GLONASS 定位；
    # bit3，0：禁用 Galileo 定位， 1：启用 Galileo 定位
    def getGNSSMode(self):
        bit0 = 1
        bit1 = 2
        bit2 = 0
        bit3 = 0
        data = bit0 + bit1 + bit2 + bit3
        dataHex = self.int2hexStringByBytes(data)
        return dataHex






if __name__ == "__main__":
    print(QueryTerminalParam_res().generateMsg())