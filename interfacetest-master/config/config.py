# coding: utf-8

#################### 全局参数设置 ##################
SSL_VERIFY = True                                                          # 是否开启SSL验证，默认设置为True；需要抓包调试的时候，改为False
TIME_OUT = 2000                                                            # 设置最大响应超时时间(毫秒)
#################### 测试用户参数设置 ##################
# USER_NAME = "13146201116"                                                   # 用户名
# PASSWORD = "Lyh123456"                                                      # 密码
# CAR_DIN = "M202003060518"                                                   # 车机号
# HOST = "api-test.vandyo.com"                                                # 域名
USER_NAME = "18883284712"                                                     # 用户名
PASSWORD = "123456abcdA"                                                      # 密码
CAR_DIN = "M502744004592"                                                     # 车机号(可以不用配置)
HOST = "api.vandyo.com"                                                       # 域名
# 请求头公共参数
HEADER = {"Accept-Encoding": "gzip", "Content-Type": "application/json; charset=UTF-8"}
SID = ""
UID = ""
CAR_ID = ""                                                                  # 车机id （区别于硬件的车机号）
HTTP_PREFIX = "https://"                                                     # http url前缀
WHITE_LIST_ERROR = [0,99,3022]                                               # 白名单错误码（在白名单里面的错误码不会断言失败）

#################### 体验模式参数设置 ##################
EX_HOST = "api.vandyo.com"                                                  # 体验模式域名
# 请求头公共参数
EX_HEADER = {"Accept-Encoding": "gzip", "Content-Type": "application/json; charset=UTF-8"}
EX_USER_NAME = "guest"                                                      # 用户名
EX_PASSWORD = "fcf41657f02f88137a1bcf068a32c0a3"                            # 密码
EX_SID = ""
EX_UID = ""
EX_HTTP_PREFIX = "https://"                                                 # http url前缀
EX_CAR_ID = ""                                                              # 车机id （区别于硬件的车机号）


