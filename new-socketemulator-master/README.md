# 模拟程序说明文档

#### （一）、框架结构说明  
config：存放项目配置文件  
dada：存放项目需要的数据和产生的数据  
doc：项目帮助文档，markdown格式编写  
lib：车机协议实现的类，以及各种业务逻辑  
static：存放网页端图形操作界面的静态文件，包含：js，css，图片等  
templates：存放网页模板文件 html  
views：存放网页端操作的后台处理逻辑，以及页面的展示逻辑  
run.py：启动项目图形操作界面主程序，访问：127.0.0.1:5000 即可（本机运行）   
requirements.txt：设置项目需要的依赖库  

---
### (二)、安装部署
1、机器上安装了python3 和 pip包管理工具   
2、使用 ：pip install -r requirements.txt  安装依赖库  
3、python3 run.py 运行项目  
4、访问 host:5000 即可进入模拟器页面  

---
### （三）、文档目录
[1、lib使用库说明](doc/lib_details.md)  
