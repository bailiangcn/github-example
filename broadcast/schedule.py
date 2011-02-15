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
import movielist

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
        self.cutclip=int(cp.get('movie','cutclip'))

class movieFrame(wx.Frame):
    '''
    节目播出窗口类
    默认在配置文件指定大小及位置
    '''
    def __init__(self,par,media_file=None, mute=False):
        '''
        初始化一个大小为零的播放页面, 用于提前调入影片
        mute = True 会启动一个静音窗口
        '''
        wx.Frame.__init__(self, None, -1, u"mplayer", 
                (mcon.winx, mcon.winy) , (1, 1), 
                style = wx.FRAME_SHAPED|wx.SIMPLE_BORDER\
                |wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        #创建一个mplayerctrl实例
        #可以指定mplayer参数
        self.par=par
        self.movielen=0
        if mute:
            mplayarg = (u'-vo',u'gl2', u'-af', u'volume=-200' )
        else:
            mplayarg = (u'-vo',u'gl2')
        self.pause=True
        self.mpc = mpc.MplayerCtrl(self, -1, u'mplayer', 
                media_file, mplayer_args=mplayarg,
                keep_pause=True)

        #创建一个影片计时器
        self.movietime=wx.Timer(self)
        #绑定启动事件, 暂停播放
        self.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)
        self.Bind(mpc.EVT_MEDIA_FINISHED, self.on_media_finished)

        self.Bind(wx.EVT_TIMER,self.OnTimerEvent,self.movietime)
        #设置屏幕背景为黑色
        self.mpc.SetBackgroundColour((0,0,0))
        self.SetBackgroundColour((0,0,0))
        self.Show()

    def on_media_started(self, evt):
        '''
        设置图像调入后暂停, 隐藏窗口, 恢复窗口大小
        '''
        if self.pause:
            #读取节目时长
            self.movielen=self.mpc.GetTimeLength()*1000
            self.mpc.Pause()
            self.mpc.Seek(0, 2)
            self.mpc.FrameStep()
            self.Hide()
            self.SetSize(wx.Size(mcon.winw,mcon.winh))
        else:
            self.movielen=self.mpc.GetTimeLength()*1000
            self.movietime.Start(self.movielen-mcon.cutclip,True)
            print "beging play:",self.mpc.filename,self.movielen 
            self.pause=True
            self.par.PreLoad()


    def OnTimerEvent(self,evt):
        print "movie timeout"
        self.par.DoNext()

    def on_process_started(self, evt):
        print 'Process started'
    def on_media_finished(self, evt):
        print 'Media finished'
        #self.par.DoNext()
    def on_process_stopped(self, evt):
        print 'Process stopped'

    def loadMovie(self, filename):
        '''
        调入一个文件
        '''
        if not self.mpc.process_alive:
            print "begin a new process"
            self.mpc.Start()
        if self.pause:
            self.SetSize(wx.Size(1, 1))
        else:
            self.SetSize(wx.Size(mcon.winw,mcon.winh))
        self.Show()
        self.mpc.Loadfile(filename)

#---------------------------------------------------------------------------

class MainFrame(wx.Frame):
    '''
    主调用窗口类,负责调度各个播出窗口
    '''
    def __init__(self):
        wx.Frame.__init__(self, None,  -1, 'Manager')
        #定义2个播放窗口,用于切换播出
        self.nowbuffer=True
        self.buffer0 = movieFrame(self)
        self.buffer1 = movieFrame(self)
        #读取节目列表
        self.ml=movielist.Mlist(mcon.movielist)
        self.buffer0.pause=False
        self.buffer0.loadMovie(self.ml.getnextfile())
        #定义面板
        panel = wx.Panel(self, -1)
        self.mmtime=os.stat(mcon.movielist).st_mtime

        #self.win3=movieFrame(self,mute=True)

        button = wx.Button(panel, 1003, u"退出")
        button.SetPosition((215, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #创建一个定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(mcon.during)

        self.Show()

    def PreLoad(self):
        self.buffer1.loadMovie(self.ml.getnextfile(1))

    def DoNext(self):
        self.ml.beginnext()
        if self.nowbuffer:
            #第一视频窗口
            self.buffer1.Show()
            self.buffer1.mpc.Pause()
            self.buffer0.mpc.Pause()
            self.buffer0.Hide()
            self.buffer1.movietime.Start(
                    self.buffer1.movielen-mcon.cutclip,True)
            #print "pre load:",self.ml.getnextfile(1).encode('utf-8') 
            self.buffer0.loadMovie(self.ml.getnextfile(1))
        else:
            #第二视频窗口
            #self.buffer0.mpc.keep_pause=False
            self.buffer0.Show()
            self.buffer0.mpc.Pause()
            self.buffer1.mpc.Pause()
            self.buffer1.Hide()
            self.buffer0.movietime.Start(
                    self.buffer1.movielen-mcon.cutclip,True)
            #self.buffer0.mpc.keep_pause=True
            #print "beging play:",self.buffer0.mpc.filename, \
            #        self.buffer0.mpc.GetTimeLength()
            #print "pre load:",self.ml.getnextfile(1).encode('utf-8') 
            self.buffer1.loadMovie(self.ml.getnextfile(1))

        self.nowbuffer=not self.nowbuffer


        

    def OnTimer(self, evt):
        '''
        每秒钟查询一次看看是否播出列表有变化
        '''
        tmptime=os.stat(mcon.movielist).st_mtime
        if self.mmtime != tmptime:
            print "mainlist.xml is changed!"
            self.mmtime = tmptime


    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        if self.buffer0 != None:
            self.buffer0.mpc.Quit()
            self.buffer0.mpc.Destroy()
            self.buffer0.Destroy()
        if self.buffer1 != None:
            self.buffer1.mpc.Quit()
            self.buffer1.mpc.Destroy()
            self.buffer1.Destroy()

        self.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':

    #读取配置文件获得播放窗口的位置
    mcon = movieConf()
    app = wx.App(redirect=True)
    #app = wx.App(redirect=False)
    b = MainFrame()
    app.MainLoop()



