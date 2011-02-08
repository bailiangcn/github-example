#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""节目播出调度
"""

__revision__ = '0.1'


#导入wxPython基础模块
import MplayerCtrl as mpc
import wx



class Frame(wx.Frame):
    def __init__(self, parent, id, title, mplayer, media_file):
        wx.Frame.__init__(self, None, -1, u"无边框窗口", (0, 0) ,(1920, 1200), 
                style = wx.FRAME_SHAPED|wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)

        #self.mpc = mpc.MplayerCtrl(self, -1, mplayer, keep_pause=True)
        self.mpc = mpc.MplayerCtrl(self, -1, mplayer, media_file)


#---------------------------------------------------------------------------

class ParFrame(wx.Frame):

    def __init__(self):
        self.win = None
        wx.Frame.__init__(self, None,  -1, 'Farther')
        panel = wx.Panel(self, -1)
        b = wx.Button(panel, -1, u"打开播放窗口", (50,50))
        b.SetPosition((15, 55))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        button = wx.Button(panel, 1003, u"退出")
        button.SetPosition((15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Show(True)


    def OnButton(self, evt):
        self.win = Frame(None, -1, 'Hello MplayerCtrl', u'mplayer', u'2.mpg')
        self.win.Show(True)

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        if self.win != None:
            self.win.mpc.Stop()
        self.Destroy()

        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(redirect=False)
    b = ParFrame()
    app.MainLoop()



