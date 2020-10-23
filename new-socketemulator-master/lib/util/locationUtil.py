#coding:utf-8

'''
定义一个获取经纬度的辅助方法集合
'''

import json

#####################################################
#           获取文件的金纬度数据,返回一个经纬度数组
#           path：传入文件路径
#####################################################
def getLocationInfo(path):
    with open(path,"r",encoding='utf-8') as fi:
        loc_data = fi.readlines()
        strData = ""
        for lineD in loc_data:
            strData += lineD
        json_data = json.loads(strData)
        return json_data["locationInfo"]


if __name__ == "__main__":
    print(getLocationInfo("../../data/protocolTools/GPSLine_1.json"))