#encoding:utf-8

'''
定义外设数据项
'''
from lib.protocol.message.MessageBase import MessageBase


class Circum_data(MessageBase):
    def __init__(self):
        super().__init__()
        pass

    #####################################################
    # 创建轿车OBD数据
    #####################################################
    def generateCircum_data(self):
        data = ""
        data_1 = "3001" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(20)
        data_2 = "3002" + self.int2hexStringByBytes(1) + self.int2hexStringByBytes(21)
        data = data_1 + data_2
        return data