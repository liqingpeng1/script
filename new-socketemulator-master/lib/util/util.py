#coding:utf-8

#########################################
# 字符串自动补空格函数
# num 字符串期望的长度
#########################################
def strAddSpace(str,num):
    data = str
    if len(str) < num:
        for i in range(0,num - len(str)):
            data = data + " "
    return data