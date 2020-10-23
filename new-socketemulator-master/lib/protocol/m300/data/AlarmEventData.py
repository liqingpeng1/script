#encoding:utf-8

from lib.protocol.m300.M300Base import M300Base

'''
定义报警事件需要的数据包
'''

class AlarmEventData(M300Base):
    def __init__(self):
        pass

    ########################################################
    # 获取CAN状态数据包
    ########################################################
    def getCANStatusData(self,safeStatus=0,doorStatus=0,lockStatus=0,windowStatus=0,lightStatus=0,swichStatusA=0,swichStatusB=0):
        statusMask = "ffffffffffffffffffff"                                       # 状态掩码
        safeStatus = self.int2hexStringByBytes(safeStatus)                        # 安全状态
        doorStatus = self.int2hexStringByBytes(doorStatus)                        # 门状态
        lockStatus = self.int2hexStringByBytes(lockStatus)                        # 锁状态
        windowStatus = self.int2hexStringByBytes(windowStatus)                    # 窗户状态
        lightStatus = self.int2hexStringByBytes(lightStatus)                      # 灯状态
        swichStatusA = self.int2hexStringByBytes(swichStatusA)                    # 开关状态A
        swichStatusB = self.int2hexStringByBytes(swichStatusB)                    # 开关状态B
        retain1 = "00"                                                              # 预留
        retain2 = "00"                                                              # 预留
        retain3 = "00"                                                              # 预留
        data = statusMask + safeStatus + doorStatus + lockStatus + windowStatus + lightStatus
        data = data + swichStatusA + swichStatusB + retain1 + retain2 + retain3
        return data



if __name__ == "__main__":
    print(AlarmEventData().getCANStatusData())