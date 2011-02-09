#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""节目播出调度
"""

__revision__ = '0.1'


#导入wxPython基础模块
import MplayerCtrl as mpc
import wx
import ConfigParser 



class Frame(wx.Frame):
    '''
    节目播出窗口类
    '''
    def __init__(self, parent, id, title, mplayer, media_file):
        wx.Frame.__init__(self, None, -1, u"无边框窗口", (winx, winy) ,(winw, winh), 
                style = wx.FRAME_SHAPED|wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)

        self.mpc = mpc.MplayerCtrl(self, -1, mplayer, keep_pause=True)


#---------------------------------------------------------------------------

class ParFrame(wx.Frame):
    '''
    主调用窗口类,负责调度各个播出窗口
    '''

    def __init__(self):
        wx.Frame.__init__(self, None,  -1, 'Farther')
        self.win = None
        panel = wx.Panel(self, -1)
        b = wx.Button(panel, -1, u"打开播放窗口", (50,50))
        b.SetPosition((15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonb, b)

        c = wx.Button(panel, -1, u"预先调入", (50,50))
        c.SetPosition((15, 55))
        self.Bind(wx.EVT_BUTTON, self.OnButtonc, c)

        d = wx.Button(panel, -1, u"开始播放", (50,50))
        d.SetPosition((15, 95))
        self.Bind(wx.EVT_BUTTON, self.OnButtond, d)

        e = wx.Button(panel, -1, u"播放新视频", (50,50))
        e.SetPosition((15, 135))
        self.Bind(wx.EVT_BUTTON, self.OnButtone, e)

        button = wx.Button(panel, 1003, u"退出")
        button.SetPosition((115, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Show(True)


    def OnButtonb(self, evt):
        self.win = Frame(None, -1, 'Hello MplayerCtrl', u'mplayer', u'2.mpg')
        self.win.Show(True)

    def OnButtonc(self, evt):
        self.win.mpc.Loadfile(u'2.mpg')
        #if not self.win.mpc.pause:
        self.win.mpc.Pause()
        self.win.mpc.Seek(0,2)

    def OnButtond(self, evt):
        self.win.mpc.keep_pause=False
        if self.win.mpc.pause:
            self.win.mpc.Pause()
            self.win.mpc.keep_pause=True

    def OnButtone(self, evt):
        self.win.mpc.Mute()
        self.win.mpc.Loadfile(u'1.mpg')
        self.win.mpc.Seek(20,2)
        self.win.mpc.Mute()
        mm=self.win.mpc.GetPosition()
        print "width=",mm[0]
        print 'height=',mm[1]

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        if self.win != None:
            self.win.Destroy()
        self.Destroy()

        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    #读取配置文件获得播放窗口的位置
    cp=ConfigParser.ConfigParser()
    cp.read('schedule.conf')
    winx=int(cp.get('position','x'))
    winy=int(cp.get('position','y'))
    winw=int(cp.get('size','width'))
    winh=int(cp.get('size','height'))

    app = wx.App(redirect=False)
    b = ParFrame()
    app.MainLoop()



