#coding: utf-8

'''
车动态接口相关用例
'''
import json
import time
import unittest

import requests
from config import config
from testCase.common import utils


class CarDynamic_interface_cases(unittest.TestCase):
    ##########################################################
    # 登录，用户手机密码登录
    # 单元测试的同时获取uid 和sid
    # 必须是第一个执行的单元测试用例
    ##########################################################
    def test_user_authorize_pwd_login(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/authorize/pwd/login"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["ts"] = ts
        postData = {}
        postData["mobile"] = config.USER_NAME
        postData["password"] = utils.getMd5String(config.PASSWORD)
        resObj = requests.post(url, headers=headers, params=params, data=json.dumps(postData),verify=config.SSL_VERIFY)
        print("原始结果：" + resObj.text)
        result = json.loads(resObj.text)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        config.SID = result["result"]["sid"]
        config.UID = result["result"]["uid"]
        self.baseAssert(resObj)
        #获取car_id
        url = config.HTTP_PREFIX + config.HOST + "/car/my_car/list"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(url, headers=headers, params=params,verify=config.SSL_VERIFY)
        print("原始结果：" + resObj.text)
        result = json.loads(resObj.text)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        config.CAR_ID = result["result"][0]["cid"]

    ##########################################################
    # 车辆动态信息
    ##########################################################
    def test_carDynamic_api_status_car_state_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/carDynamic/api/status/car/state/get"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["start"] = ts
        params["uid"] = config.UID
        params["cid"] = config.CAR_ID
        cs = utils.getSignature(params)
        params["cs"] = cs
        params.pop("sid")
        resObj = requests.get(url, headers=headers, params=params,verify=config.SSL_VERIFY)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        self.baseAssert(resObj)

    ##########################################################
    # 接口基本断言，需要传入一个返回结果对象
    ##########################################################
    def baseAssert(self,resObj):
        statusCode = int(resObj.status_code)  # 响应状态码
        resTime = int(resObj.elapsed.total_seconds() * 1000)  # 获取接口相应时间(毫秒)
        result = json.loads(resObj.text)
        error = result["error"]
        self.assertEqual(statusCode, 200, "响应状态码为：" + str(statusCode))
        self.assertTrue(resTime < config.TIME_OUT, "响应时间大于" + str(int(config.TIME_OUT/1000)) + "秒，响应时间为：" + str(resTime) + "毫秒")
        self.assertTrue(error in config.WHITE_LIST_ERROR,"接口返回错误")
        print("接口响应时间：" + str(resTime) + "毫秒")

    def startTest(self):
        suite = unittest.TestSuite()
        suite.addTest(CarDynamic_interface_cases("test_user_authorize_pwd_login"))
        suite.addTest(CarDynamic_interface_cases("test_carDynamic_api_status_car_state_get"))                 # 车辆动态信息
        runner = unittest.TextTestRunner()
        runner.run(suite)

if __name__ == "__main__":
    CarDynamic_interface_cases().startTest()