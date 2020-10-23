#coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

'''
发送邮件的类
'''
class EmailTool():
    def __init__(self):
        self.from_addr = 'optest@vandyo.com'                  # 发件箱
        self.password = '123qweQWE!@#AaA'                     # 发件箱密码
        self.to_addr = "liyuanhong@vandyo.com"                # 收件箱
        self.to_cc = ""                                       # 抄送
        self.smtp_server = "smtp.exmail.qq.com"               # 发信服务器
        self.title = "车安优拨测反馈"                         # 邮件标题
        self.msg_obj = MIMEMultipart("mixed")

    def set_from_addr(self,data):
        self.from_addr = data
    def set_password(self,data):
        self.password = data
    def set_to_addr(self,data):
        self.to_addr = data
    def set_to_cc(self,data):
        self.to_cc = data
    def set_smtp_server(self,data):
        self.smtp_server = data
    def set_title(self,data):
        self.title = data
    def set_email_type(self,data):
        self.email_type = data

    #########################################################
    # 添加收件人
    #########################################################
    def add_to_addr(self,data):
        if self.to_addr == "":
            self.to_addr = data
        else:
            self.to_addr = self.to_addr + "," + data

    #########################################################
    # 添加抄送
    #########################################################
    def add_to_cc(self,data):
        if self.to_cc == "":
            self.to_cc = data
        else:
            self.to_cc = self.to_cc + "," + data

    #########################################################
    # 添加邮件内容: plain为纯文本，html：为html格式
    #########################################################
    def addContent(self,msg="",type="plain"):
        mime = MIMEText(msg, type, 'utf-8')
        self.msg_obj.attach(mime)

    #########################################################
    # 发送邮件
    #########################################################
    def send(self):
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        self.msg_obj['From'] = Header(self.from_addr)
        self.msg_obj['To'] = Header(self.to_addr)                                                 # 收信人
        if self.to_cc != "":
            self.msg_obj['Cc'] = Header(self.to_cc)                                               # 添加抄送
        self.msg_obj['Subject'] = Header(self.title)
        server = smtplib.SMTP_SSL(host=self.smtp_server)
        server.connect(self.smtp_server, 465)
        server.login(self.from_addr, self.password)
        if self.to_cc == "":
            server.sendmail(self.from_addr, self.to_addr.split(',') ,self.msg_obj.as_string())   # 发送邮件
        else:
            server.sendmail(self.from_addr, self.to_addr.split(',') + self.to_cc.split(","), self.msg_obj.as_string())  # 发送邮件
        server.quit()                                                                            # 关闭服务器

    #########################################################
    # 设置附件内容
    ########################################################
    def set_attachment(self,file_path,file_name):
        txt = ""
        with open(file_path, "r", encoding="utf-8") as fi:
            content = fi.read()
            txt = content
        part = MIMEText(txt, "plain", 'utf-8')
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        self.msg_obj.attach(part)

    #########################################################
    # 读取并返回文件内容
    #########################################################
    def read_from_file(self,file_name):
        txt = ""
        with open(file_name, "r", encoding="utf-8") as fi:
            content = fi.read()
            txt = content
        return txt


if __name__ == "__main__":
    obj = EmailTool()
    obj.set_to_addr("liyuanhong@vandyo.com")
    obj.add_to_addr("908963295@qq.com")
    obj.add_to_cc("langang@vandyo.com")
    obj.addContent("这是一个测试邮件，请忽略...")
    obj.set_attachment("../../result/2020-05-22/2020-05-22 13_50_21.html", "2020-05-22 13_50_21.html")
    obj.send()


