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
import os



class Frame(wx.Frame):
    '''
    节目播出窗口类
    '''
    def __init__(self, parent, id, title, mplayer, media_file,x,y):
        wx.Frame.__init__(self, None, -1, u"无边框窗口", (winx, winy) , 
                (0, 0), style = wx.FRAME_SHAPED|wx.SIMPLE_BORDER\
                |wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        #创建一个mplayerctrl实例
        self.mpc = mpc.MplayerCtrl(self, -1, mplayer, media_file,
                keep_pause=False)
        #self.mpc = mpc.MplayerCtrl(self, -1, mplayer, media_file,
        # [u'-vo',u'xv'],keep_pause=False)
        self.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)
        #设置屏幕背景为黑色
        self.mpc.SetBackgroundColour((0,0,0))
        self.Show()

    def on_media_started(self, evt):
        '''
        设置图像播放一帧后暂停
        '''
        self.mpc.Pause()
        self.Hide()
        self.SetSize(wx.Size(winw,winh))

#---------------------------------------------------------------------------

class ParFrame(wx.Frame):
    '''
    主调用窗口类,负责调度各个播出窗口
    '''

    def __init__(self):
        wx.Frame.__init__(self, None,  -1, 'Manager')
        self.win = None
        self.win1=None
        self.mmtime=0
        panel = wx.Panel(self, -1)
        b = wx.Button(panel, -1, u"打开播放窗口", (50,50))
        b.SetPosition((15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonb, b)

        c = wx.Button(panel, -1, u"播放", (50,50))
        c.SetPosition((15, 55))
        self.Bind(wx.EVT_BUTTON, self.OnButtonc, c)

        d = wx.Button(panel, -1, u"切换插播", (50,50))
        d.SetPosition((15, 95))
        self.Bind(wx.EVT_BUTTON, self.OnButtond, d)

        b1 = wx.Button(panel, -1, u"打开插播窗口", (50,50))
        b1.SetPosition((115, 15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonb1, b1)

        c1 = wx.Button(panel, -1, u"预留", (50,50))
        c1.SetPosition((115, 55))
        self.Bind(wx.EVT_BUTTON, self.OnButtonc1, c1)

        d1 = wx.Button(panel, -1, u"预留", (50,50))
        d1.SetPosition((115, 95))
        self.Bind(wx.EVT_BUTTON, self.OnButtond1, d1)

        e = wx.Button(panel, -1, u"预留", (50,50))
        e.SetPosition((15, 135))
        self.Bind(wx.EVT_BUTTON, self.OnButtone, e)

        button = wx.Button(panel, 1003, u"退出")
        button.SetPosition((215, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #创建一个定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(during)



        self.Show(True)


    def OnTimer(self, evt):
        '''
        每秒钟查询一次看看是否播出列表有变化
        '''
        tmptime=os.stat(movielist).st_mtime
        if self.mmtime != tmptime:
            print "mainlist.xml is changed!"
            self.mmtime = tmptime

    def OnButtonb(self, evt):
        self.win = Frame(None, -1, 'Hello MplayerCtrl', u'mplayer', 
                u'2.mpg',1920,0)

    def OnButtonc(self, evt):
        self.win.Show()
        self.win.mpc.Pause()

    def OnButtond(self, evt):
        if self.win.IsShown():
            self.win1.mpc.Pause()
            self.win1.Show()
            self.win.mpc.Pause()
            self.win.Hide()
        else:
            self.win.mpc.Pause()
            self.win.Show()
            self.win1.mpc.Pause()
            self.win1.Hide()

    def OnButtonb1(self, evt):
        self.win1 = Frame(None, -1, 'Hello MplayerCtrl', u'mplayer', 
                u'1.mpg',2120,0)

    def OnButtonc1(self, evt):
        print self.win.mpc.get

    def OnButtond1(self, evt):
        self.win1.mpc.keep_pause=False
        if self.win1.mpc.pause:
            self.win1.mpc.Pause()
            self.win1.mpc.keep_pause=True

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
            self.win.mpc.Quit()
            self.win.Destroy()
        if self.win1 != None:
            self.win1.mpc.Quit()
            self.win1.Destroy()

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
    during = int(cp.get('timer', 'during'))
    moviepath=cp.get('movie','moviepath')
    movielist=cp.get('movie','movielist')

    app = wx.App(redirect=False)
    b = ParFrame()
    app.MainLoop()



