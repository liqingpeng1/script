#coding: utf-8

import binascii
import os
import socket
import time


class DelaySend():
    def __init__(self,din = "M202003060520",service = None):
        self.baseUrl = "data/protocolTools/sendMsg/"
        self.din = din
        self.service = service

    def setDin(self,din):
        self.din = din

    def setServer(self,data):
        self.service = data

    #####################################################
    #               数字转换为16进制字符串
    #####################################################
    def int2hexString(self,num):
        hexStr = hex(num)[2:]
        if (len(hexStr) % 2) == 1:
            hexStr = "0" + hexStr
        return hexStr

    #####################################################
    #               数字转换为16进制字符串，通过传入字节数可自动补0
    #               传入数据格式所占字节数
    #####################################################
    def int2hexStringByBytes(self,num, bytescount=1):
        hexStr = hex(num)[2:]
        while len(hexStr) < (bytescount * 2):
            hexStr = "0" + hexStr
        return hexStr

    #####################################################
    #               设备id转换为16进制字符串
    #####################################################
    def devid2hexString(self,id):
        # 获取第一个字符的ASCII值
        ascii = ord(id[0:1])
        # 将10进制的ASCII值转换为16进制
        ascii = self.int2hexString(int(ascii))
        devid = str(ascii) + id[1:]
        return devid

    #####################################################
    #                 定义生成校验字段的函数
    #                inputStr:需要传入一个已经转换为16进制的字符串
    #####################################################
    # add crc 16 check at the end of the string
    def crc16(self,inputStr):
        inputStrByte = bytes.fromhex(inputStr)
        crc = 0xFFFF
        for i in range(0, len(inputStrByte)):
            for j in range(0, 8):
                c15 = (crc >> 15) == 1
                bit = ((inputStrByte[i] >> (7 - j)) & 1) == 1
                crc <<= 1
                crc &= 0xFFFF
                if c15 ^ bit:
                    crc ^= 0x1021
        crc = str(hex(crc))
        crc = self.leftPad(crc[2:], 4)
        # outputStr = inputStr + crc
        outputStr = crc
        return outputStr

    # pad zero to the left of the string if not long enough
    def leftPad(self,inputStr, strLen):
        if (strLen > len(inputStr)):
            outputStr = "0000000000000000000000000000000000000000" + inputStr
            outputStr = outputStr[len(outputStr) - strLen:]
            return outputStr
        else:
            return inputStr

    # pad zero to the right of the string if not long enough
    def rightPad(self,inputStr, strLen):
        if (strLen > len(inputStr)):
            outputStr = inputStr + "0000000000000000000000000000000000000000"
            outputStr = outputStr[: strLen]
            return outputStr
        else:
            return inputStr

    ##############################################################################
    def getEventPkg(self):
        if os.path.exists(self.baseUrl + self.din + '/event.txt'):
            with open(self.baseUrl + self.din + "/event.txt", "r", encoding="utf-8") as fi:
                content = fi.readlines()
                pkg = ""
                msgs = []
                pkgCounts = 0
                for i in content:
                    onePkg = i[21:].replace("\n", "")
                    onePkg = onePkg[30:][:-4]
                    onePkg = onePkg[2:]
                    pkg = pkg + onePkg
                    pkgCounts = pkgCounts + 1
                    if len(pkg) > 2000:
                        pkgCounts = self.int2hexStringByBytes(pkgCounts)
                        HEADER = "4040"
                        WATER_CODE = self.int2hexStringByBytes(1, 2)
                        DEV_ID = self.devid2hexString(self.din)
                        FUN_ID = "0021"
                        LENGTH = self.int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                        CHECK_CODE = self.crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                        msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                        msgs.append(msg)
                        pkg = ""
                        pkgCounts = 0
                pkgCounts = self.int2hexStringByBytes(pkgCounts)
                HEADER = "4040"
                WATER_CODE = self.int2hexStringByBytes(1, 2)
                DEV_ID = self.devid2hexString(self.din)
                FUN_ID = "0021"
                LENGTH = self.int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                CHECK_CODE = self.crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                msgs.append(msg)

                with open(self.baseUrl + self.din + "/event_big.txt", "w", encoding="utf-8") as fi2:
                    for txt in msgs:
                        fi2.write(txt + "\n")
                return msgs
        else:
            print("event.txt is not exist")
            return ["4040000b00034d1215010100010003f50b"]

    def getGpsPkg(self):
        if os.path.exists(self.baseUrl + self.din + '/gps.txt'):
            with open(self.baseUrl + self.din + "/gps.txt", "r", encoding="utf-8") as fi:
                content = fi.readlines()
                pkg = ""
                msgs = []
                pkgCounts = 0
                for i in content:
                    onePkg = i[21:].replace("\n", "")
                    onePkg = onePkg[30:][:-4]
                    onePkg = onePkg[2:]
                    pkg = pkg + onePkg
                    pkgCounts = pkgCounts + 1
                    if len(pkg) > 2000:
                        pkgCounts = self.int2hexStringByBytes(pkgCounts)
                        HEADER = "4040"
                        WATER_CODE = self.int2hexStringByBytes(1, 2)
                        DEV_ID = self.devid2hexString(self.din)
                        FUN_ID = "0010"
                        LENGTH = self.int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                        CHECK_CODE = self.crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                        msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                        msgs.append(msg)
                        pkg = ""
                        pkgCounts = 0
                pkgCounts = self.int2hexStringByBytes(pkgCounts)
                HEADER = "4040"
                WATER_CODE = self.int2hexStringByBytes(1, 2)
                DEV_ID = self.devid2hexString(self.din)
                FUN_ID = "0010"
                LENGTH = self.int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                CHECK_CODE = self.crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                msgs.append(msg)

                with open(self.baseUrl + self.din + "/gps_big.txt", "w", encoding="utf-8") as fi2:
                    for txt in msgs:
                        fi2.write(txt + "\n")
                return msgs
        else:
            print("gps.txt is not exist")
            return ["4040000b00034d1215010100010003f50b"]

    def getObdPkg(self):
        if os.path.exists(self.baseUrl + self.din + '/obd.txt'):
            with open(self.baseUrl + self.din + "/obd.txt", "r", encoding="utf-8") as fi:
                content = fi.readlines()
                pkg = ""
                msgs = []
                pkgCounts = 0
                for i in content:
                    onePkg = i[21:].replace("\n", "")
                    onePkg = onePkg[30:][:-4]
                    onePkg = onePkg[2:]
                    pkg = pkg + onePkg
                    pkgCounts = pkgCounts + 1
                    if len(pkg) > 2000:
                        pkgCounts = self.int2hexStringByBytes(pkgCounts)
                        HEADER = "4040"
                        WATER_CODE = self.int2hexStringByBytes(1, 2)
                        DEV_ID = self.devid2hexString(self.din)
                        FUN_ID = "0012"
                        LENGTH = self.int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                        CHECK_CODE = self.crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                        msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                        msgs.append(msg)
                        pkg = ""
                        pkgCounts = 0
                pkgCounts = self.int2hexStringByBytes(pkgCounts)
                HEADER = "4040"
                WATER_CODE = self.int2hexStringByBytes(1, 2)
                DEV_ID = self.devid2hexString(self.din)
                FUN_ID = "0012"
                LENGTH = self.int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                CHECK_CODE = self.crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                msgs.append(msg)
                with open(self.baseUrl + self.din + "/obd_big.txt", "w", encoding="utf-8") as fi2:
                    for txt in msgs:
                        fi2.write(txt + "\n")
                return msgs
        else:
            print("obd.txt is not exist")
            return ["4040000b00034d1215010100010003f50b"]

    def getLenOfFile(self):
        with open(self.baseUrl + "event_big.txt", "r", encoding="utf-8") as fi:
            data = fi.readline()
            print(len(data))

    def sendMsg(self,msgs):
        for msg in msgs:
            msg = msg.replace("\n", "")
            self.service.serviceSendMsg(msg,"0")
            time.sleep(0.05)

    def sendDelayMsgs(self):
        time.sleep(0.1)
        self.service.websocket.sendMsgToClient("-----------------------发送补报消息【开始】--------------------------",self.service.websocketId)
        msg = self.getEventPkg()
        self.sendMsg(msg)
        time.sleep(0.1)
        msg = self.getGpsPkg()
        self.sendMsg(msg)
        time.sleep(0.1)
        msg = self.getObdPkg()
        self.sendMsg(msg)
        self.service.websocket.sendMsgToClient("-----------------------发送补报消息【结束】--------------------------",self.service.websocketId)
        for fi in os.listdir(self.baseUrl + self.din):
            os.remove(self.baseUrl + self.din + "/" + fi)
        os.rmdir(self.baseUrl + self.din)

