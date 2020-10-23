#coding: utf-8

'''
测试套件类，用来组织所有的测试用例
'''
import os
import platform
import time
import unittest

from testCase.CarDynamic_interface_cases import CarDynamic_interface_cases
from testCase.Car_interface_cases import Car_interface_cases
from testCase.DemoCar_case import DemoCar_case
from testCase.User_interface_cases import User_interface_cases
from testCase.common import HTMLTestRunnerNew
from testCase.common.EmailTool import EmailTool
from testCase.common.HTMLTestRunner import HTMLTestRunner


class MainCase():
    def __init__(self):
        self.sucessCount = 0
        self.failureCount = 0
        self.errorCount = 0
        self.testReport = ""  # 测试报告名
        self.testDate = ""  # 测试日期
        self.from_addr = 'optest@vandyo.com'                  # 发件箱
        self.password = '123qweQWE!@#AaA'                     # 发件箱密码
        # self.to_addr = "liyuanhong@vandyo.com"                # 收件箱
        self.to_addr = "749880966@qq.com"                # 收件箱
        self.to_cc = ""                                       # 抄送
        self.msg = "邮件内容"                                 # 邮件正文
        self.smtp_server = "smtp.exmail.qq.com"               # 发信服务器
        self.title = "车安优拨测报告"                         # 邮件标题
        self.durTime = 1 * 5 * 60                             # 多久执行一次拨测程序（秒）

    def getSucessCount(self):
        return self.sucessCount

    def getFailCount(self):
        return self.failureCount

    def getErrorCount(self):
        return self.errorCount

    def getTestReport(self):
        return self.testReport

    def getTestDate(self):
        return self.testDate

    def set_from_addr(self, data):
        self.from_addr = data

    def set_password(self, data):
        self.password = data

    def set_to_addr(self, data):
        self.to_addr = data

    def set_title(self, data):
        self.title = data

    def set_msg(self, data):
        self.msg = data

    def setDurTime(self, data):
        self.durTime = data

    #########################################################
    # 添加收件人
    #########################################################
    def add_to_addr(self, data):
        if self.to_addr == "":
            self.to_addr = data
        else:
            self.to_addr = self.to_addr + "," + data
    #########################################################
    # 添加抄送
    #########################################################

    def add_to_cc(self, data):
        if self.to_cc == "":
            self.to_cc = data
        else:
            self.to_cc = self.to_cc + "," + data

    ###########################################################
    # 使用html 报告模板输出
    ###########################################################
    def startTest(self):
        suite = unittest.TestSuite()
        suite.addTest(User_interface_cases(
            "test_user_authorize_pwd_login"))            # 用户手机密码登录
        suite.addTest(User_interface_cases(
            "test_user_mall_goods_list"))                # 商品列表
        suite.addTest(User_interface_cases(
            "test_user_third_party_app_list"))           # 第三方应用列表
        suite.addTest(User_interface_cases(
            "test_user_business_cooperation_get"))       # 查询商务合作信息
        suite.addTest(User_interface_cases("test_user_info_get")
                      )                       # 获取用户基本信息
        suite.addTest(User_interface_cases("test_user_pop_list")
                      )                       # 获取弹框广告
        suite.addTest(User_interface_cases("test_user_banner_list")
                      )                    # banner图片列表
        suite.addTest(User_interface_cases("test_user_flash_list")
                      )                     # 获取闪屏广告
        suite.addTest(User_interface_cases(
            "test_user_car_msg_config_get"))             # 获取车消息开关
        suite.addTest(User_interface_cases(
            "test_user_user_msg_config_get"))            # 获取用户推送消息开关
        suite.addTest(User_interface_cases(
            "test_user_config_version_update_get"))      # 版本更新
        suite.addTest(User_interface_cases("test_user_menu_list")
                      )                      # 用户菜单列表

        suite.addTest(Car_interface_cases("test_car_brand_list")
                      )                             # 车品牌列表
        suite.addTest(Car_interface_cases("test_car_my_car_list")
                      )                            # 查询车列表
        suite.addTest(Car_interface_cases("test_car_my_car_info")
                      )                            # 查询车信息
        suite.addTest(Car_interface_cases("test_car_man_speak")
                      )                              # 查询人车对话
        suite.addTest(Car_interface_cases(
            "test_car_api_reprt_reportDay_get"))                # 查询日报告
        suite.addTest(Car_interface_cases(
            "test_car_api_locus_list_page"))                    # 查询历史轨迹列表
        suite.addTest(Car_interface_cases(
            "test_car_api_locus_points_list"))                  # 查询轨迹点
        suite.addTest(Car_interface_cases("test_car_car_health")
                      )                             # 车辆健康检测
        # 车辆健康检测-电瓶检测结果
        suite.addTest(Car_interface_cases("test_car_car_health_battery"))
        # 车辆健康检测-刹车系统检测结果
        suite.addTest(Car_interface_cases("test_car_car_health_brake"))
        # 车辆健康检测-发动机检测结果
        suite.addTest(Car_interface_cases("test_car_car_health_engine"))
        # 车辆健康检测-变速箱检测结果
        suite.addTest(Car_interface_cases("test_car_car_health_gearbox"))
        # 车辆健康检测-油箱检测结果
        suite.addTest(Car_interface_cases("test_car_car_health_oilbox"))
        suite.addTest(Car_interface_cases(
            "test_car_car_health_total_user"))                  # 车辆健康检测总用户数

        suite.addTest(DemoCar_case("test_user_authorize_pwd_login")
                      )                          # demo车登录接口
        suite.addTest(DemoCar_case("test_car_my_car_list")
                      )                                   # demo车，查询车列表
        # demo车,辆动态信息
        suite.addTest(DemoCar_case("test_carDynamic_api_status_car_state_get"))
        suite.addTest(DemoCar_case("test_car_api_locus_list_page")
                      )                           # 判断 demo车是否正常行驶

        suite.addTest(CarDynamic_interface_cases(
            "test_carDynamic_api_status_car_state_get"))                 # 车辆动态信息

        ts = time.time()
        timeArray = time.localtime(ts)
        curTime = ""
        curDate = ""
        sys = platform.system()
        if sys == "Windows":
            curTime = time.strftime("%Y-%m-%d %H_%M_%S", timeArray)
            curDate = time.strftime("%Y-%m-%d", timeArray)
        else:
            curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            curDate = time.strftime("%Y-%m-%d", timeArray)
        fdir = "result/" + curDate
        if not os.path.exists(fdir):
            os.mkdir(fdir)
        filePath = fdir + "/" + curTime + ".html"
        self.testReport = curTime + ".html"
        self.testDate = curDate
        fp = open(filePath, 'wb')

        # 生成报告的Title,描述
        runner = HTMLTestRunner(
            stream=fp,
            title='车安优App接口测试',
            description='车安优App拨测程序测试报告...')
        # runner = HTMLTestRunnerNew.HTMLTestRunner(stream=fp, title='车安优App接口测试', description='车安优App拨测程序测试报告...')
        result = runner.run(suite)
        self.sucessCount = result.success_count
        self.failureCount = result.failure_count
        self.errorCount = result.error_count
        self.msg = "【" + curTime + "】 测试简要结果如下：\n"
        self.msg = self.msg + "\n 用例总数：" + \
            str(self.sucessCount + self.failureCount + self.errorCount)
        self.msg = self.msg + "\n 成功个数：" + str(self.sucessCount)
        self.msg = self.msg + "\n 失败个数：" + str(self.failureCount)
        self.msg = self.msg + "\n 错误个数：" + str(self.errorCount)
        if len(result.failures) > 0:
            self.msg = self.msg + \
                "\n\n------------------------------------失败详情----------------------------------------------"
            for i in range(0, len(result.failures)):
                logs = result.failures[i][1].split("\n")
                log = str(result.failures[i][0]) + "\n" + \
                    logs[len(logs) - 3] + "\n" + logs[len(logs) - 2]
                self.msg = self.msg + \
                    "\n失败(" + str(i + 1) + "):>>>>>>>>>>>>>>>>>>>:"
                self.msg = self.msg + "\n" + log

        if len(result.errors) > 0:
            self.msg = self.msg + \
                "\n\n------------------------------------错误详情----------------------------------------------"
            for i in range(0, len(result.errors)):
                logs = result.errors[i][1].split("\n")
                log = str(result.errors[i][0]) + "\n" + \
                    logs[len(logs) - 3] + "\n" + logs[len(logs) - 2]
                self.msg = self.msg + \
                    "\n错误(" + str(i + 1) + "):>>>>>>>>>>>>>>>>>>>:"
                self.msg = self.msg + "\n" + log
        self.msg = self.msg + "\n\n测试报告详情，详见附件..."

        print(self.msg)
        fp.close()

    ###########################################################
    # 使用html 报告模板输出
    ###########################################################

    def startTxtTest(self):
        suite = unittest.TestSuite()
        suite.addTest(User_interface_cases(
            "test_user_authorize_pwd_login"))  # 用户手机密码登录
        suite.addTest(User_interface_cases(
            "test_user_mall_goods_list"))  # 商品列表
        suite.addTest(User_interface_cases(
            "test_user_third_party_app_list"))  # 第三方应用列表
        suite.addTest(User_interface_cases(
            "test_user_business_cooperation_get"))  # 查询商务合作信息
        suite.addTest(User_interface_cases("test_user_info_get"))  # 获取用户基本信息
        suite.addTest(User_interface_cases("test_user_pop_list"))  # 获取弹框广告
        suite.addTest(User_interface_cases("test_user_banner_list")
                      )                    # banner图片列表
        suite.addTest(User_interface_cases("test_user_flash_list")
                      )                     # 获取闪屏广告
        suite.addTest(User_interface_cases(
            "test_user_car_msg_config_get"))             # 获取车消息开关
        suite.addTest(User_interface_cases(
            "test_user_user_msg_config_get"))            # 获取用户推送消息开关
        suite.addTest(User_interface_cases(
            "test_user_config_version_update_get"))      # 版本更新
        suite.addTest(User_interface_cases("test_user_menu_list"))  # 用户菜单列表

        suite.addTest(Car_interface_cases("test_car_my_car_list")
                      )                      # 查询车列表
        runner = unittest.TextTestRunner()
        runner.run(suite)

    ###########################################################
    # 定时测试服务，如果有失败用例，会自动发送邮件通知
    ###########################################################
    def startTestService(self):
        self.startTest()
        if self.failureCount > 0 or self.errorCount > 0:
            self.sendEmail()
        startTime = int(time.time())
        while True:
            endTime = int(time.time())
            if endTime - startTime >= self.durTime:
                self.startTest()
                if self.failureCount > 0 or self.errorCount > 0:
                    self.sendEmail()
                startTime = int(time.time())
            else:
                time.sleep(1)

    ###########################################################
    # 发送邮件
    ###########################################################
    def sendEmail(self):
        email_obj = EmailTool()
        # 设置邮件内容
        email_obj.addContent(self.msg)

        ts = time.time()
        timeArray = time.localtime(ts)
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # 设置邮件标题
        email_obj.set_title(curTime + " 拨测报告")
        curDate = time.strftime("%Y-%m-%d", timeArray)
        time.sleep(2)
        email_obj.set_attachment(
            "result/" + curDate + "/" + self.testReport,
            self.testReport)         # 设置附件
        # 设置抄送
        email_obj.set_to_addr(self.to_addr)
        # 设置收信人
        email_obj.set_to_cc(self.to_cc)
        email_obj.send()
