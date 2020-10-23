#coding:utf-8

'''
定义一个心跳协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

'''
终端心跳协议数据包
'''
class HeartBeatReport_protocol(ProtocolBase):
    def __init__(self,WATER_CODE = "0003",DEV_ID = "M121501010001"):
        super().__init__()
        self.WATER_CODE = int(WATER_CODE);  # 设置默认消息流水号
        self.DEV_ID = DEV_ID  # 设置默认设备id

    #####################################################
    #               生成心跳消息
    #####################################################
    def generateHeartBeatMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"      # 消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)   # 消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)   # 设备id
        FUN_ID = "0003"         # 功能id(心跳功能id)
        data = ""          # 数据段
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data) / 2))   # 消息长度

        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)    # 校验字段
        info += CHECK_CODE
        return info

if __name__ == "__main__":
    pass