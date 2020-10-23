# coding:utf-8

'''
在此定义辅助函数
'''

import hashlib

#################################################
# 获取一个Md5的字符串
#################################################
def getMd5String(data):
    m = hashlib.md5()
    b = data.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5

#################################################
# 获取签名，传入一个map,
# （需要对传入的参数，按照key的升序排列）
#################################################
def getSignature(data,postData={}):
    sMd5 = ""
    if len(postData) == 0:
        keys = sorted(data.keys())
        s = ""
        for key in keys:
            s = s + key + "[" + str(data[key]) + "];"
        sMd5 = getMd5String(s)
    else:
        data["Data"] = postData
        keys = sorted(data.keys())
        s = ""
        for key in keys:
            s = s + key + "[" + str(data[key]) + "];"
        sMd5 = getMd5String(s)
    return sMd5




if __name__ == "__main__":
    # print(getSignature({"a":123,"b":"abc"}))
    print(getSignature({'ts': 1590406665, 'sid': '31e07c4a44ac439dac8931aea3704c62', 'start': 1590406665, 'uid': 'bb4d91ccc1f6461daec7a0daf1c8e8f2', 'cid': '49a92ac0f9b14ba59d91ee8debe8357d'}))
    # s=getMd5String('liqingpeng')
    # print(s)
