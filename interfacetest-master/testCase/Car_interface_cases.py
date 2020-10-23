#coding: utf-8

'''
汽车接口相关用例
'''
import json
import random
import time
import unittest

import requests
from config import config
from testCase.common import utils


class Car_interface_cases(unittest.TestCase):
    ##########################################################
    # 登录，用户手机密码登录
    # 单元测试的同时获取uid 和sid
    # 必须是第一个执行的单元测试用例
    ##########################################################
    def test_user_authorize_pwd_login(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/authorize/pwd/login"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["ts"] = ts
        postData = {}
        postData["mobile"] = config.USER_NAME
        postData["password"] = utils.getMd5String(config.PASSWORD)
        resObj = requests.post(
            url,
            headers=headers,
            params=params,
            data=json.dumps(postData),
            verify=config.SSL_VERIFY)
        print("原始结果：" + resObj.text)
        result = json.loads(resObj.text)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        config.SID = result["result"]["sid"]
        config.UID = result["result"]["uid"]
        self.baseAssert(resObj)

    ##########################################################
    # 查询人车对话
    ##########################################################
    def test_car_man_speak(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/man/speak"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        postData = {}
        postData["cid"] = config.CAR_ID
        postData["message"] = random.choice(
            ['车辆位置', '即时速度', '发动机转速', '剩余油量', '电瓶电压'])
        cs = utils.getSignature(params, json.dumps(postData))
        params["cs"] = cs
        params.pop("sid")
        print(postData)
        resObj = requests.post(
            url,
            headers=headers,
            params=params,
            data=json.dumps(postData),
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

#######################################  车相关  ############################
    ##########################################################
    # 车品牌列表
    ##########################################################
    def test_car_brand_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/brand/list"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

        ##########################################################
        # 车款年款列表
        ##########################################################
        def test_car_model_list_year(self):
            # todo
            url = config.HTTP_PREFIX + config.HOST + "/car/model/list/year"
            ts = int(time.time())
            headers = {"Accept-Encoding": "gzip",
                       "Content-Type": "application/json; charset=UTF-8"}
            params = {}
            params["sid"] = config.SID
            params["ts"] = ts
            params["uid"] = config.UID
            cs = utils.getSignature(params)
            params["cs"] = cs
            params.pop("sid")
            resObj = requests.get(
                url,
                headers=headers,
                params=params,
                verify=config.SSL_VERIFY)
            print("\n请求地址：" + url)
            print("-------------------------返回结果：-------------------------")
            print(resObj.text)
            self.baseAssert(resObj)

    ##########################################################
    # 查询车列表
    ##########################################################
    def test_car_my_car_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/my_car/list"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("原始结果：" + resObj.text)
        result = json.loads(resObj.text)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        config.CAR_ID = result["result"][0]["cid"]
        self.baseAssert(resObj)

    ##########################################################
    # 查询车信息
    ##########################################################
    def test_car_my_car_info(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/my_car/info"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 查询日报告
    ##########################################################
    def test_car_api_reprt_reportDay_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/api/reprt/reportDay/get"
        ts = int(time.time())
        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=UTF-8",
            "ver": "2.0.0.01"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        postData = {}
        postData["cid"] = config.CAR_ID
        cs = utils.getSignature(params, json.dumps(postData))
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.post(
            url,
            headers=headers,
            params=params,
            data=json.dumps(postData),
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 查询历史轨迹列表
    ##########################################################
    def test_car_api_locus_list_page(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/api/locus/list/page"
        ts = int(time.time())
        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=UTF-8",
            "ver": "2.0.0.01"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["start"] = ts
        params["sort"] = 1
        params["size"] = 10
        params["uid"] = config.UID
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 查询轨迹点
    ##########################################################
    def test_car_api_locus_points_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/api/locus/points/list"
        ts = int(time.time())
        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=UTF-8",
            "ver": "2.0.0.01"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["start"] = ts
        params["end"] = ts - 86400
        params["uid"] = config.UID
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测
    ##########################################################
    def test_car_car_health(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health"
        ts = int(time.time())
        headers = {
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=UTF-8",
            "ver": "2.0.0.01"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        params["cid"] = config.CAR_ID
        params["type"] = 2
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测-电瓶检测结果
    ##########################################################
    def test_car_car_health_battery(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health_battery"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测-刹车系统检测结果
    ##########################################################
    def test_car_car_health_brake(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health_brake"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测-发动机检测结果
    ##########################################################
    def test_car_car_health_engine(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health_engine"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测-变速箱检测结果
    ##########################################################
    def test_car_car_health_gearbox(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health_gearbox"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测-油箱检测结果
    ##########################################################
    def test_car_car_health_oilbox(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health_oilbox"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 车辆健康检测总用户数
    ##########################################################
    def test_car_car_health_total_user(self):
        url = config.HTTP_PREFIX + config.HOST + "/car/car_health_total_user"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(
            url,
            headers=headers,
            params=params,
            verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 接口基本断言，需要传入一个返回结果对象
    ##########################################################
    def baseAssert(self, resObj):
        statusCode = int(resObj.status_code)  # 响应状态码
        resTime = int(resObj.elapsed.total_seconds() * 1000)  # 获取接口相应时间(毫秒)
        result = json.loads(resObj.text)
        error = result["error"]
        self.assertEqual(statusCode, 200, "响应状态码为：" + str(statusCode))
        self.assertTrue(resTime < config.TIME_OUT, "响应时间大于" +
                        str(int(config.TIME_OUT /
                                1000)) +
                        "秒，响应时间为：" +
                        str(resTime) +
                        "毫秒")
        self.assertTrue(error in config.WHITE_LIST_ERROR, "接口返回错误")
        print("接口响应时间：" + str(resTime) + "毫秒")

    def startTest(self):
        suite = unittest.TestSuite()
        suite.addTest(Car_interface_cases("test_user_authorize_pwd_login"))
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
        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == "__main__":
    Car_interface_cases().startTest()
