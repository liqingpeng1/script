# coding: utf-8
import binascii
import socket
import time
import os

din = "M202008270021"
#####################################################
#               数字转换为16进制字符串
#####################################################
def int2hexString(num):
    hexStr = hex(num)[2:]
    if (len(hexStr) % 2) == 1:
        hexStr = "0" + hexStr
    return hexStr


#####################################################
#               数字转换为16进制字符串，通过传入字节数可自动补0
#               传入数据格式所占字节数
#####################################################
def int2hexStringByBytes(num, bytescount=1):
    hexStr = hex(num)[2:]
    while len(hexStr) < (bytescount * 2):
        hexStr = "0" + hexStr
    return hexStr


#####################################################
#               设备id转换为16进制字符串
#####################################################
def devid2hexString(id):
    # 获取第一个字符的ASCII值
    ascii = ord(id[0:1])
    # 将10进制的ASCII值转换为16进制
    ascii = int2hexString(int(ascii))
    devid = str(ascii) + id[1:]
    return devid


#####################################################
#                 定义生成校验字段的函数
#                inputStr:需要传入一个已经转换为16进制的字符串
#####################################################
# add crc 16 check at the end of the string
def crc16(inputStr):
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
    crc = leftPad(crc[2:], 4)
    # outputStr = inputStr + crc
    outputStr = crc
    return outputStr


# pad zero to the left of the string if not long enough
def leftPad(inputStr, strLen):
    if (strLen > len(inputStr)):
        outputStr = "0000000000000000000000000000000000000000" + inputStr
        outputStr = outputStr[len(outputStr) - strLen:]
        return outputStr
    else:
        return inputStr


# pad zero to the right of the string if not long enough
def rightPad(inputStr, strLen):
    if (strLen > len(inputStr)):
        outputStr = inputStr + "0000000000000000000000000000000000000000"
        outputStr = outputStr[: strLen]
        return outputStr
    else:
        return inputStr


##############################################################################
def getEventPkg():
    if os.path.exists('event.txt'):
        with open("event.txt", "r", encoding="utf-8") as fi:
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
                    pkgCounts = int2hexStringByBytes(pkgCounts)
                    HEADER = "4040"
                    WATER_CODE = int2hexStringByBytes(1, 2)
                    DEV_ID = devid2hexString(din)
                    FUN_ID = "0021"
                    LENGTH = int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                    CHECK_CODE = crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                    msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                    msgs.append(msg)
                    pkg = ""
                    pkgCounts = 0
            pkgCounts = int2hexStringByBytes(pkgCounts)
            HEADER = "4040"
            WATER_CODE = int2hexStringByBytes(1, 2)
            DEV_ID = devid2hexString(din)
            FUN_ID = "0021"
            LENGTH = int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
            CHECK_CODE = crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
            msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
            msgs.append(msg)

        with open("event_big.txt", "w", encoding="utf-8") as fi2:
            for txt in msgs:
                fi2.write(txt + "\n")
        return msgs
    else:
        print("event.txt is not exist")
        return ["4040000b00034d1215010100010003f50b"]


def getGpsPkg():
    if os.path.exists('gps.txt'):
        with open("gps.txt", "r", encoding="utf-8") as fi:
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
                    pkgCounts = int2hexStringByBytes(pkgCounts)
                    HEADER = "4040"
                    WATER_CODE = int2hexStringByBytes(1, 2)
                    DEV_ID = devid2hexString(din)
                    FUN_ID = "0010"
                    LENGTH = int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                    CHECK_CODE = crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                    msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                    msgs.append(msg)
                    pkg = ""
                    pkgCounts = 0
            pkgCounts = int2hexStringByBytes(pkgCounts)
            HEADER = "4040"
            WATER_CODE = int2hexStringByBytes(1, 2)
            DEV_ID = devid2hexString(din)
            FUN_ID = "0010"
            LENGTH = int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
            CHECK_CODE = crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
            msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
            msgs.append(msg)

        with open("gps_big.txt", "w", encoding="utf-8") as fi2:
            for txt in msgs:
                fi2.write(txt + "\n")
        return msgs
    else:
        print("gps.txt is not exist")
        return ["4040000b00034d1215010100010003f50b"]


def getObdPkg():
    if os.path.exists('obd.txt'):
        with open("obd.txt", "r", encoding="utf-8") as fi:
            content = fi.readlines()
            pkg = ""
            msgs = []
            pkgCounts = 0
            for i in content:
                onePkg = i[21:].replace("\n", "")
                onePkg = onePkg[30:][:-4]
                onePkg = onePkg[2:]
                print(onePkg)
                pkg = pkg + onePkg
                pkgCounts = pkgCounts + 1
                if len(pkg) > 2000:
                    pkgCounts = int2hexStringByBytes(pkgCounts)
                    HEADER = "4040"
                    WATER_CODE = int2hexStringByBytes(1, 2)
                    DEV_ID = devid2hexString(din)
                    FUN_ID = "0012"
                    LENGTH = int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
                    CHECK_CODE = crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
                    msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
                    msgs.append(msg)
                    pkg = ""
                    pkgCounts = 0
            pkgCounts = int2hexStringByBytes(pkgCounts)
            HEADER = "4040"
            WATER_CODE = int2hexStringByBytes(1, 2)
            DEV_ID = devid2hexString(din)
            FUN_ID = "0012"
            LENGTH = int2hexStringByBytes(int(len(WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg) / 2), 2)
            CHECK_CODE = crc16(HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg)
            msg = HEADER + LENGTH + WATER_CODE + DEV_ID + FUN_ID + pkgCounts + pkg + CHECK_CODE
            msgs.append(msg)
            with open("obd_big.txt", "w", encoding="utf-8") as fi2:
                for txt in msgs:
                    fi2.write(txt + "\n")
            return msgs
    else:
        print("obd.txt is not exist")
        return ["4040000b00034d1215010100010003f50b"]


def getLenOfFile():
    with open("event_big.txt", "r", encoding="utf-8") as fi:
        data = fi.readline()
        print(len(data))


def sendMsg(msgs):
    host = "172.19.7.13"
    port = 49008
    BUF_SIZE = 1024

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(2)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳
    client.connect((host, port))
    for msg in msgs:
        print(msg)
        msg = msg.replace("\n", "")
        client.send(binascii.a2b_hex(msg))
        data = client.recv(BUF_SIZE)
        print(data)
        print(binascii.b2a_hex(data))
    client.close()


if __name__ == "__main__":
    msg = getEventPkg()
    sendMsg(msg)
    time.sleep(1)
    msg = getGpsPkg()
    sendMsg(msg)
    time.sleep(1)
    msg = getObdPkg()
    sendMsg(msg)

    # getLenOfFile()



