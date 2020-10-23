#coding: utf-8

'''
车模拟程序测试用例
'''
import json
import random
import time
import unittest

import requests
from config import config
from testCase.common import utils


class DemoCar_case(unittest.TestCase):
    ##########################################################
    # demo车登录接口
    ##########################################################
    def test_user_authorize_pwd_login(self):
        url = config.EX_HTTP_PREFIX + config.EX_HOST + "/user/authorize/pwd/login"
        ts = int(time.time())
        headers = config.EX_HEADER
        params = {}
        params["ts"] = ts
        postData = {}
        postData["mobile"] = config.EX_USER_NAME
        postData["password"] = config.EX_PASSWORD
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
        config.EX_SID = result["result"]["sid"]
        config.EX_UID = result["result"]["uid"]
        self.baseAssert(resObj)

    ##########################################################
    # demo车，查询车列表
    ##########################################################
    def test_car_my_car_list(self):
        url = config.EX_HTTP_PREFIX + config.EX_HOST + "/car/my_car/list"
        ts = int(time.time())
        headers = config.EX_HEADER
        params = {}
        params["sid"] = config.EX_SID
        params["ts"] = ts
        params["uid"] = config.EX_UID
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
        config.EX_CAR_ID = result["result"][0]["cid"]
        self.baseAssert(resObj)

    ##########################################################
    # demo车,辆动态信息
    ##########################################################
    def test_carDynamic_api_status_car_state_get(self):
        url = config.EX_HTTP_PREFIX + config.EX_HOST + \
              "/carDynamic/api/status/car/state/get"
        ts = int(time.time())
        headers = config.EX_HEADER
        params = {}
        params["sid"] = config.EX_SID
        params["ts"] = ts
        params["start"] = ts
        params["uid"] = config.EX_UID
        params["cid"] = config.EX_CAR_ID
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
    # 判断 demo车是否正常行驶
    ##########################################################
    def test_car_api_locus_list_page(self):
        url = config.EX_HTTP_PREFIX + config.EX_HOST + "/car/api/locus/list/page"
        ts = int(time.time())
        headers = config.EX_HEADER
        params = {}
        params["sid"] = config.EX_SID
        params["ts"] = ts
        params["start"] = ts
        params["uid"] = config.EX_UID
        params["cid"] = config.EX_CAR_ID
        params["size"] = 10
        params["sort"] = 1
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
        # 车机最近一次轨迹的开始时间
        lastTime = int(result["result"][0]["sti"])
        self.baseAssert(resObj)
        url = config.EX_HTTP_PREFIX + config.EX_HOST + \
            "/carDynamic/api/status/car/state/get"
        ts2 = int(time.time())
        headers = config.EX_HEADER
        params = {}
        params["sid"] = config.EX_SID
        params["ts"] = ts2
        params["start"] = ts2
        params["uid"] = config.EX_UID
        params["cid"] = config.EX_CAR_ID
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
        accStatus = int(result["result"]["acc"])
        self.baseAssert(resObj)
        durTime = ts - lastTime
        # self.assertTrue(durTime < 11000, "demo车机已经有超过3小时未启动，请检查是否出现问题")
        self.assertTrue(
            durTime < 11000 or accStatus == 1,
            "demo车机已经有超过3小时未启动，请检查是否出现问题")

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
        suite.addTest(DemoCar_case("test_user_authorize_pwd_login")
                      )                      # demo车登录接口
        suite.addTest(DemoCar_case("test_car_my_car_list")
                      )                               # demo车，查询车列表
        # demo车,辆动态信息
        suite.addTest(DemoCar_case("test_carDynamic_api_status_car_state_get"))
        suite.addTest(DemoCar_case("test_car_api_locus_list_page")
                      )                       # 判断 demo车是否正常行驶
        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == "__main__":
    DemoCar_case().startTest()