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
        self.cp=ConfigParser.ConfigParser()
        self.cp.read('schedule.conf')
        self.winx=int(self.cp.get('position','x'))
        self.winy=int(self.cp.get('position','y'))
        self.winw=int(self.cp.get('size','width'))
        self.winh=int(self.cp.get('size','height'))
        self.during = int(self.cp.get('timer', 'during'))
        self.cutclip=int(self.cp.get('timer','cutclip'))
        self.moviepath=self.cp.get('movie','moviepath')
        self.movielist=self.cp.get('movie','movielist')
        self.immediately=int(self.cp.get('movie','immediately'))
    def reload(self):
        self.immediately=int(self.cp.get('movie','immediately'))

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
            self.mplayarg = (u'-vo',u'xv', u'-af', u'volume=-200' )
        else:
            #self.mplayarg = (u'-vo',u'xv')
            self.mplayarg = (u'-vo',u'xv', u'-af', u'volume=-100' )
        self.mpc = mpc.MplayerCtrl(self, -1, u'mplayer', 
                media_file, mplayer_args=self.mplayarg,
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
            print "set timelen:",self.movielen
            self.mpc.Pause()
            self.mpc.Seek(0, 2)
            self.mpc.FrameStep()
            self.Hide()
            self.SetSize(wx.Size(mcon.winw,mcon.winh))
            self.mpc.SetSize(wx.Size(mcon.winw,mcon.winh))
        else:
            #第一个播放的节目
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
        if self.pause:
            self.SetSize(wx.Size(1, 1))
        else:
            self.SetSize(wx.Size(mcon.winw,mcon.winh))
            self.mpc.SetSize(wx.Size(mcon.winw,mcon.winh))
            
        self.Show()
        if not self.mpc.process_alive:
            print "begin a new process"
            self.mpc.Start( mplayer_args=self.mplayarg)
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
        #第一个节目暂停取消
        self.buffer0.pause=False
        self.buffer1.pause=True
        self.buffer0.loadMovie(self.ml.getnextfile())
        #定义面板
        panel = wx.Panel(self, -1)
        self.mmtime=os.stat(mcon.movielist).st_mtime
        #定义播放列表变化标志
        self.listchanged=False

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
        if not self.listchanged:
            #播放列表如果没有变化
            self.ml.beginnext()
        else:
            self.listchanged=False

        if self.nowbuffer:
            #第一视频窗口
            print "buffer1 is activeing"
            self.buffer1.Show()
            self.buffer1.mpc.Pause()
            self.buffer0.mpc.Pause()
            self.buffer0.Hide()
            self.buffer1.movietime.Start(
                    self.buffer1.movielen-mcon.cutclip,True)
            self.buffer0.loadMovie(self.ml.getnextfile(1))
        else:
            #第二视频窗口
            print "buffer0 is activeing"
            self.buffer0.Show()
            self.buffer0.mpc.Pause()
            self.buffer1.mpc.Pause()
            self.buffer1.Hide()
            self.buffer0.movietime.Start(
                    self.buffer1.movielen-mcon.cutclip,True)
            self.buffer1.loadMovie(self.ml.getnextfile(1))
        self.nowbuffer=not self.nowbuffer

    def ChangeMovie(self):
        #播放列表发生变化
        self.ml.reload()
        if mcon.immediately == 0:
            print "after this program end begin chang list"
            print self.ml.tostr().encode('utf-8') 
            print 'next pro:',self.ml.getnextfile().encode('utf-8') 

            if self.nowbuffer:
                self.buffer1.loadMovie(self.ml.getnextfile())
            else:
                self.buffer0.loadMovie(self.ml.getnextfile())
        else:
            print "now change program"

        

    def OnTimer(self, evt):
        '''
        每秒钟查询一次看看是否播出列表有变化
        '''
        #查询时间标签是否更改
        tmptime=os.stat(mcon.movielist).st_mtime
        if self.mmtime != tmptime:
            self.listchanged=True
            self.mmtime = tmptime
            mcon.reload()
            self.ChangeMovie()



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
    app = wx.App(redirect=False)
    #app = wx.App(redirect=False)
    b = MainFrame()
    app.MainLoop()



