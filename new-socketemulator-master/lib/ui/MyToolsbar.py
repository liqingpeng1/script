#coding:utf-8

import wx
from lib.ui.InterfaceBase import InterfaceBase

'''
定义工具条
'''

class MyToolsbar(InterfaceBase):
    def __init__(self,frame):
        self.frame = frame

    #####################################################
    #                   创建一个工具栏,并返回该对象
    #####################################################
    # @property
    def createToolsBar(self):
        toolBar = self.frame.CreateToolBar()
        openTool = toolBar.AddTool(wx.ID_ANY, "open",
                                   wx.Bitmap(wx.Image("../../img/folder.png", "image/png").Scale(25, 25),
                                             wx.BITMAP_SCREEN_DEPTH))
        startTool = toolBar.AddTool(wx.ID_ANY, "start",
                                    wx.Bitmap(wx.Image("../../img/start.png", "image/png").Scale(25, 25),
                                              wx.BITMAP_SCREEN_DEPTH))
        stopTool = toolBar.AddTool(wx.ID_ANY, "stop",
                                   wx.Bitmap(wx.Image("../../img/stop.png", "image/png").Scale(25, 25),
                                             wx.BITMAP_SCREEN_DEPTH))
        toolBar.AddSeparator()
        infoTool = toolBar.AddTool(wx.ID_ANY, "info",
                                   wx.Bitmap(wx.Image("../../img/info.png", "image/png").Scale(25, 25),
                                             wx.BITMAP_SCREEN_DEPTH))
        helpTool = toolBar.AddTool(wx.ID_ANY, "help",
                                   wx.Bitmap(wx.Image("../../img/help.png", "image/png").Scale(25, 25),
                                             wx.BITMAP_SCREEN_DEPTH))
        toolBar.Realize()
        return toolBar