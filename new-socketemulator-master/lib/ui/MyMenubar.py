#coding:utf-8

import wx
from lib.ui.InterfaceBase import InterfaceBase

'''
定义菜单栏
'''

class MyMenubar(InterfaceBase):

    def __init__(self,frame):
        self.frame = frame

    #####################################################
    #                   wxpython定义菜单栏
    #####################################################
    def createMenuBar(self):
        menuBar = wx.MenuBar()

        #《------------------       开始菜单编码start      ---------------------》
        #first_ 代表一级菜单，即menubar上显示的菜单
        first_menuStart = wx.Menu()

        menuItemOpen = first_menuStart.Append(wx.ID_ANY, u"打开    ")
        menuItemExit = first_menuStart.Append(wx.ID_ANY, u"退出    ")
        self.frame.Bind(wx.EVT_MENU, self.myExit, menuItemExit)

        # 《------------------       开始菜单编码end      ---------------------》

        menuBar.Append(first_menuStart, u"文件")
        return menuBar

    def myExit(self,evt):
        print(evt)
        wx.Exit()