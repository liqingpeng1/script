#coding:utf-8

import wx
from lib.ui.InterfaceBase import InterfaceBase
from lib.ui.MyMenubar import MyMenubar
from lib.ui.MyToolsbar import MyToolsbar

'''
定义主窗体
'''

class MainWindow(InterfaceBase):
    def __init__(self):
        self.app = None
        self.frame = None

        self.main()

    def main(self):
        self.app = wx.App()
        self.frame = wx.Frame(None,-1, title='socketTools',size = wx.Size(800,700))

        #添加设置菜单栏
        self.frame.SetMenuBar(MyMenubar(self.frame).createMenuBar())
        #添加设置工具栏
        self.toolsBar = MyToolsbar(self.frame).createToolsBar()
        #创建主窗体布局面板，将主窗体分为几大块
        self.createPanel()

    #####################################################
    #                   显示窗体
    #####################################################
    def show(self):
        self.frame.Show()
        self.app.MainLoop()

    #####################################################
    #                   创建主窗体的布局面板
    #####################################################
    def createPanel(self):
        # 创建面板
        splitter = wx.SplitterWindow(self.frame, wx.ID_ANY)
        panel1 = wx.Panel(splitter,  wx.ID_ANY)

        treeList = wx.TreeCtrl(panel1, wx.ID_ANY, size=(wx.EXPAND, wx.EXPAND))
        item1 = treeList.AddRoot("工具汇总")
        item11 = treeList.AppendItem(item1, "终端上报报文")
        treeList.AppendItem(item1, "远程查询报文")
        treeList.AppendItem(item1, "车辆行为模拟")
        treeList.AppendItem(item1, "系统设置")

        treeList.AppendItem(item11, "GPS上报报文")
        treeList.AppendItem(item11, "OBD_CAN上报报文")
        treeList.AppendItem(item11, "其他报文")


        panel2 = wx.Panel(splitter,  wx.ID_ANY)
        panel2.SetBackgroundColour("pink")
        splitter.SplitVertically(panel1, panel2)
        splitter.SetSashPosition(200)   #设置水平分割的位置

if __name__ == "__main__":
    MainWindow().show()