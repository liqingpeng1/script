#coding: utf-8

'''
用户接口相关用例
'''
import json
import time
import unittest

import requests
from config import config
from testCase.common import utils


class User_interface_cases(unittest.TestCase):

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
        # 获取car_id
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
        result = json.loads(resObj.text)
        print("\n请求地址：" + url)
        print("-------------------------返回结果：-------------------------")
        print(resObj.text)
        config.CAR_ID = result["result"][0]["cid"]
        config.CAR_ID = result["result"][0]["din"]

    ##########################################################
    # 商品列表
    ##########################################################
    def test_user_mall_goods_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/mall/goods/list"
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
        postData = {}
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
    # 第三方应用列表
    ##########################################################
    def test_user_third_party_app_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/third/party/app/list"
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
    # 查询商务合作信息
    ##########################################################
    def test_user_business_cooperation_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/business/cooperation/get"
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
    # 测试获取用户基本信息
    ##########################################################
    def test_user_info_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/info/get"
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
    # 获取弹框广告
    ##########################################################
    def test_user_pop_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/pop/list"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        params["psl"] = 1
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
    # banner图片列表
    ##########################################################
    def test_user_banner_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/banner/list"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["sid"] = config.SID
        params["ts"] = ts
        params["uid"] = config.UID
        postData = {}
        postData["type"] = 1
        temp = dict(params, **postData)
        cs = utils.getSignature(temp)
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
    # 获取闪屏广告
    ##########################################################
    def test_user_flash_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/flash/list"
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
    # 获取车消息开关
    ##########################################################
    def test_user_car_msg_config_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/car_msg/config/get"
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
    # 获取用户推送消息开关
    ##########################################################
    def test_user_user_msg_config_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/user_msg/config/get"
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
    # 版本更新
    ##########################################################

    def test_user_config_version_update_get(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/config/version/update/get"
        ts = int(time.time())
        headers = {"Accept-Encoding": "gzip",
                   "Content-Type": "application/json; charset=UTF-8"}
        params = {}
        params["ts"] = ts
        params["uid"] = config.UID
        params["version"] = "1.1.1"
        params["appid"] = "com.vandyo.app.android"
        params["os"] = 2
        cs = utils.getSignature(params)
        params["cs"] = cs
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
    # 用户菜单列表
    ##########################################################
    def test_user_menu_list(self):
        url = config.HTTP_PREFIX + config.HOST + "/user/menu/list"
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
        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == "__main__":
    # Login_case().getData()
    # Login_case().login()
    User_interface_cases().startTest()
