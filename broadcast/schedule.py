#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""
节目播出调度主程序
"""

__revision__ = '0.1'


#导入wxPython基础模块
import MplayerCtrl as mpc
import wx
import ConfigParser 
import os
import sys
import time

class movieConf(object):
    """
    设置配置文件类
    """
    def __init__(self, filename=u'schedule.conf'):
        cp=ConfigParser.ConfigParser()
        cp.read('schedule.conf')
        self.winx=int(cp.get('position','x'))
        self.winy=int(cp.get('position','y'))
        self.winw=int(cp.get('size','width'))
        self.winh=int(cp.get('size','height'))
        self.during = int(cp.get('timer', 'during'))
        self.moviepath=cp.get('movie','moviepath')
        self.movielist=cp.get('movie','movielist')

class movieFrame(wx.Frame):
    '''
    节目播出窗口类
    默认在配置文件指定大小及位置
    '''
    def __init__(self,media_file=None, mute=False):
        '''
        初始化一个大小为零的播放页面, 用于提前调入影片
        mute = True 会启动一个静音窗口
        '''
        wx.Frame.__init__(self, None, -1, u"mplayer", 
                (mcon.winx, mcon.winy) , (0, 0), 
                style = wx.FRAME_SHAPED|wx.SIMPLE_BORDER\
                |wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        #创建一个mplayerctrl实例
        #可以指定mplayer参数
        if mute:
            mplayarg = (u'-vo',u'xv', u'-af', u'volume=-200' )
        else:
            mplayarg = (u'-vo',u'xv')
        self.mpc = mpc.MplayerCtrl(self, -1, u'mplayer', 
                media_file, mplayer_args=mplayarg,
                keep_pause=True)
        self.mpc.SetBackgroundColour((0,0,0))
        #绑定启动事件, 暂停播放
        self.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)

        #设置屏幕背景为黑色
        self.Show()

        #if media_file != '':
        #    self.mpc.Loadfile(media_file)

    def on_media_started(self, evt):
        '''
        设置图像调入后暂停, 隐藏窗口, 恢复窗口大小
        '''
        print self.mpc.filename
        self.mpc.Pause()
        self.mpc.Seek(0, 2)
        self.Hide()
        self.SetSize(wx.Size(mcon.winw,mcon.winh))

    def on_process_started(self, evt):
        print 'Process started'
    def on_media_finished(self, evt):
        print 'Media finished'
        self.mpc.Quit()
    def on_process_stopped(self, evt):
        print 'Process stopped'

    def pauseMovie(self):
        pass

    def getPause(self):
        '''
        获得影片是否暂停的状态
        '''
        return self.mpc.playing

    def loadMovie(self, filename):
        '''
        调入一个文件
        '''
        if not self.mpc.process_alive:
            print "begin a new process"
            self.mpc.Start()
        self.SetSize(wx.Size(0, 0))
        self.Show()
        self.mpc.Loadfile(filename)
        #print "stream_length:%s" % self.mpc.GetTimeLength()
        #print "stream_pos:%s" % self.mpc.GetTimePos()
        #print "Pause stat is:%s" % self.mpc.pause

#---------------------------------------------------------------------------

class MainFrame(wx.Frame):
    '''
    主调用窗口类,负责调度各个播出窗口
    '''

    def __init__(self):
        wx.Frame.__init__(self, None,  -1, 'Manager')
        self.win = None
        self.win1=None
        self.win3=movieFrame(mute=True)
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

        c1 = wx.Button(panel, -1, u"测试暂停状态", (50,50))
        c1.SetPosition((115, 55))
        self.Bind(wx.EVT_BUTTON, self.OnButtonc1, c1)

        button = wx.Button(panel, 1003, u"退出")
        button.SetPosition((215, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #创建一个定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(mcon.during)

        self.Show()


    def OnTimer(self, evt):
        '''
        每秒钟查询一次看看是否播出列表有变化
        '''
        tmptime=os.stat(mcon.movielist).st_mtime
        if self.mmtime != tmptime:
            print "mainlist.xml is changed!"
            self.mmtime = tmptime

    def OnButtonb(self, evt):
        self.win = movieFrame( u'2.mpg')

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
        self.win1 = movieFrame( u'1.mpg')

    def OnButtonc1(self, evt):
        self.win3.loadMovie(u'视频片段/002.mpg')
        #print self.win.mpc.filename
        #print "stream_length:%s" % self.win.mpc.GetTimeLength()
        #print "stream_pos:%s" % self.win.mpc.GetTimePos()
        #print "Pause stat is:%s" % self.win.mpc.pause
        #self.win.mpc.Seek(0, 2)

    def OnButtond1(self, evt):
        self.win1.mpc.keep_pause=False
        if self.win1.mpc.pause:
            self.win1.mpc.Pause()
            self.win1.mpc.keep_pause=True

    def OnButtone(self, evt):
        self.win.mpc.Loadfile(u'1.mpg')
        self.win.mpc.Seek(20,2)
        mm=self.win.mpc.GetPosition()
        print "width=",mm[0]
        print 'height=',mm[1]

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        if self.win != None:
            self.win.mpc.Quit()
            self.win.mpc.Destroy()
            self.win.Destroy()
        if self.win1 != None:
            self.win1.mpc.Quit()
            self.win1.mpc.Destroy()
            self.win1.Destroy()
        if self.win3 != None:
            self.win3.mpc.Quit()
            self.win3.mpc.Destroy()
            self.win3.Destroy()


        self.Destroy()

        
#---------------------------------------------------------------------------

if __name__ == '__main__':

    #读取配置文件获得播放窗口的位置
    mcon = movieConf()
    app = wx.App(redirect=False)
    b = MainFrame()
    app.MainLoop()



