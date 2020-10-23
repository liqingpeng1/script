#coding: utf-8
import time

from testCase.MainCase import MainCase


###########################################################
# 使用html 报告模板输出
###########################################################
def run():
    caseObj = MainCase()
    caseObj.startTest()

###########################################################
# 只在控制台输出测试结果
###########################################################
def txtRun():
    caseObj = MainCase()
    caseObj.startTxtTest()

###########################################################
# 通过服务方式启动拨测服务
###########################################################
def runService():
    caseObj = MainCase()
    caseObj.set_from_addr("optest@vandyo.com")                             # 设置发件箱
    caseObj.set_password("123qweQWE!@#AaA")                                # 设置邮箱登录密码
    caseObj.add_to_addr("749880966@qq.com")                           # 添加收件箱
    #
    # caseObj.add_to_addr("yuzhanyong@vandyo.com")                           # 添加收件箱
    # caseObj.add_to_addr("jiaxiantao@vandyo.com")                           # 添加收件箱
    # caseObj.add_to_addr("liyujia@vandyo.com")                              # 添加收件箱
    # caseObj.add_to_addr("zouyang@vandyo.com")                              # 添加收件箱
    # caseObj.add_to_addr("zhanchengtao@vandyo.com")                         # 添加收件箱
    # caseObj.add_to_addr("huangshu@vandyo.com")                             # 添加收件箱

    # caseObj.add_to_addr("908963295@qq.com")                              # 添加收件箱
    # caseObj.add_to_cc("jiaxiantao@vandyo.com")                             # 添加抄送
    # caseObj.add_to_cc("langang@vandyo.com")                              # 添加抄送
    caseObj.setDurTime(1 * 1 * 60)                                         # 设置多久执行一次拨测程序
    caseObj.startTestService()


if __name__ == "__main__":
    # runService()
    run()
    # txtRun()