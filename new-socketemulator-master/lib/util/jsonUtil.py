#coding:utf-8

'''
处理json辅助类
'''


#####################################################
# 判断json中是否有值为空的项
#####################################################
def hasJsonDataIsNone(data):
    for key,value in data.items():
        if value == None or value == "":
            return True
    return False



if __name__ == "__main__":
    data = {"a":1,"b":"bb","c":"s","d":123}
    print(hasJsonDataIsNone(data))