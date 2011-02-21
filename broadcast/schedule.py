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
from movielist import log
from movielist import errlog


#------------------------------------------------------------
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
        self.logs=(self.cp.get('logs','log')=='1')
    def reload(self):
        self.logs=(self.cp.get('logs','log')=='1')

#------------------------------------------------------------
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
        wx.Frame.__init__(self, par, -1, u"mplayer", 
                (mcon.winx, mcon.winy) , (1, 1), 
                style = wx.FRAME_SHAPED|wx.SIMPLE_BORDER\
                |wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        #创建一个mplayerctrl实例
        #可以指定mplayer参数
        self.par=par
        self.movielen=0
        #当前播放的影片名字
        self.moviename=''
        if mute:
            self.mplayarg = (u'-vo',u'xv', u'-af', u'volume=-200' )
        else:
            self.mplayarg = (u'-vo',u'xv', u'-fs')
            #self.mplayarg = (u'-vo',u'xv', u'-af', u'volume=-50' )
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
            log(u'媒体播放事件开始',logs=mcon.logs)
            self.moviename = ''
            try:
                self.moviename=self.mpc.filename
            except Exception, ex:
                errlog(u'开始取播放文件名称出现错误', ex, sys.exc_info())
            log(u'媒体播放事件开始'+self.moviename,logs=mcon.logs)
            self.mpc.Pause()
            self.mpc.Osd(0)
            log(u'开始取播放文件时长',logs=mcon.logs)
            self.movielen=0
            try:
                self.movielen=self.mpc.GetTimeLength()*1000
                #如果模拟测试节目非正常停止取消注释
                #self.movielen+=1000000
            except Exception, ex:
                errlog(u'开始取播放文件时长出现错误', ex, sys.exc_info())

            log(u'影片长度:'+unicode(str(self.movielen)) ,logs=mcon.logs)
            self.mpc.Seek(0, 2)
            self.mpc.FrameStep()
            self.Hide()
            self.SetSize(wx.Size(mcon.winw,mcon.winh))

        else:
            #第一个播放的节目
            log(u'第一个播放的节目 ',logs=mcon.logs)
            self.movielen=self.mpc.GetTimeLength()*1000
            self.movietime.Start(self.movielen-mcon.cutclip,True)
            self.moviename=self.mpc.filename
            log(u'开始播放影片:'+self.moviename ,logs=mcon.logs)
            log(u'影片长度:'+unicode(str(self.movielen)) ,logs=mcon.logs)
            self.pause=True
            self.par.PreLoad()

    def OnTimerEvent(self,evt):
        log(u'影片计时器时间到,开始准备调用DoNext()',logs=mcon.logs)
        self.par.curprogramid += 1
        log(u"curprogramid:"+unicode(self.par.curprogramid),logs=mcon.logs)
        log(u"oldprogramid:"+unicode(self.par.oldprogramid),logs=mcon.logs)
        self.par.DoNext()

    def on_process_started(self, evt):
        log(u'mplayer 进程开始',logs=mcon.logs)

    def on_media_finished(self, evt):
        #log(u'媒体停止播放事件',logs=mcon.logs)
        #如果没有正常取得视频文件的长度, 
        #或者媒体非正常停止
        #在视频文件停止播放后切换到下一个影片
        log(u'媒体停止播放事件',logs=mcon.logs)
        log(u"in media finish curprogramid:"+unicode(
            self.par.curprogramid),logs=mcon.logs)
        log(u"in media finish oldprogramid:"+unicode(
            self.par.oldprogramid),logs=mcon.logs)
        if not self.par.listchanged:
            if self.movielen ==0 or (
                    self.par.oldprogramid == self.par.curprogramid):
                log(u'媒体非正常停止播放'+self.moviename,logs=mcon.logs)
                log(u'媒体非正常停止播放:  '+self.moviename +u"    取得时长:"+unicode(
                    self.movielen), filename=u'logs/error.log',logs=mcon.logs)
                self.par.curprogramid += 1
                self.par.DoNext()
        #保存当前播放节目id
        self.par.oldprogramid=self.par.curprogramid

    def on_process_stopped(self, evt):
        log(u'mplayer 进程停止',logs=mcon.logs)

    def loadMovie(self, filename):
        '''
        调入一个文件
        '''
        log(u'loadMovie 开始',logs=mcon.logs)
        if self.pause:
            log(u'设置窗口最小尺寸',logs=mcon.logs)
            self.SetSize(wx.Size(1, 1))
        else:
            log(u'设置窗口全屏尺寸',logs=mcon.logs)
            self.SetSize(wx.Size(mcon.winw,mcon.winh))
            
        self.Show()
        if not self.mpc.process_alive:
            log(u'开始一个新mplayer进程',logs=mcon.logs)
            self.mpc.Start( mplayer_args=self.mplayarg)
        self.mpc.Loadfile(filename)

#---------------------------------------------------------------------------

class MainFrame(wx.Frame):
    '''
    主调用窗口类,负责调度各个播出窗口
    '''
    def __init__(self):
        wx.Frame.__init__(self, None,  -1, 'Manager')
        #定义播放列表变化标志
        self.listchanged=False
        #定义紧急切换节目标识

        #定义2个播放窗口,用于切换播出
        log(u'定义2个播放窗口,用于切换播出',logs=mcon.logs)
        #self.curbuffer表示当前播放窗口是否是0号窗口
        self.curbuffer=True
        self.buffer0 = movieFrame(self)
        self.buffer1 = movieFrame(self)
        #读取节目列表
        self.ml=movielist.Mlist(mcon.movielist)
        #设置当前播放的节目临时ID
        self.curprogramid=0
        self.oldprogramid=self.curprogramid
        #取配置文件的时间标签
        self.mmtime=os.stat(mcon.movielist).st_mtime
        #第一个节目暂停取消
        self.buffer0.pause=False
        self.buffer1.pause=True
        log(u'0缓冲区开始调入影片'+self.ml.getnextfile(),logs=mcon.logs)
        self.buffer0.loadMovie(self.ml.getnextfile())
        #定义面板
        panel = wx.Panel(self, -1)

        #创建一个检测配置文件更改和退出的定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(mcon.during)

        self.Show(False)

    def PreLoad(self):
        "预读文件"
        log(u'开始 PreLoad()',logs=mcon.logs)
        log(u'预读文件:'+self.ml.getnextfile(1),logs=mcon.logs)
        self.buffer1.loadMovie(self.ml.getnextfile(1))

    def DoNext(self):
        "播放下一个影片"
        log(u'开始 DoNext()',logs=mcon.logs)
        if self.listchanged:
            self.listchanged=False
        else:
            #播放列表如果变化
            log(u'播放列表未变化,调用ml.beginnext()',logs=mcon.logs)
            self.ml.beginnext()

        if self.curbuffer:
            #第一视频窗口
            log(u'1 号缓冲区激活,0 号隐藏',logs=mcon.logs)
            self.buffer1.Show()
            self.buffer1.mpc.Pause()
            self.buffer0.mpc.Pause()
            self.buffer0.Hide()
            log(u"影片长度:"+unicode(self.buffer1.movielen),
                    logs=mcon.logs)
            self.buffer1.movietime.Start(
                    self.buffer1.movielen-mcon.cutclip,True)
            log(u'0 号缓冲区准备预读文件:'+self.ml.getnextfile(1),
                    logs=mcon.logs)
            self.buffer0.loadMovie(self.ml.getnextfile(1))
        else:
            #第二视频窗口
            log(u'0 号缓冲区激活,1 号隐藏',logs=mcon.logs)
            self.buffer0.Show()
            self.buffer0.mpc.Pause()
            self.buffer1.mpc.Pause()
            self.buffer1.Hide()
            log(u"影片长度:"+unicode(self.buffer0.movielen),
                    logs=mcon.logs)
            self.buffer0.movietime.Start(
                    self.buffer0.movielen-mcon.cutclip,True)
            log(u'1 号缓冲区准备预读文件:'+self.ml.getnextfile(1),
                    logs=mcon.logs)
            self.buffer1.loadMovie(self.ml.getnextfile(1))
        self.curbuffer=not self.curbuffer

    def ChangeMovie(self):
        #播放列表发生变化
        log(u'开始 ChangeMovie()',  logs=mcon.logs)
        self.ml.reload()
        if self.curbuffer:
            self.buffer1.mpc.Stop()
            log(u'节目单发生变化, 1号缓冲区准备预读文件:'+self.ml.getnextfile(),
                    logs=mcon.logs)
            self.buffer1.loadMovie(self.ml.getnextfile())
        else:
            self.buffer0.mpc.Stop()
            log(u'节目单发生变化, 0号缓冲区准备预读文件:'+self.ml.getnextfile(),
                    logs=mcon.logs)
            self.buffer0.loadMovie(self.ml.getnextfile())
        self.curprogramid += 1

        

    def OnTimer(self, evt):
        '''
        每秒钟查询一次看看是否播出列表有变化
        '''
        #查询时间标签是否更改
        tmptime=os.stat(mcon.movielist).st_mtime
        if self.mmtime != tmptime  and not self.listchanged:
            log(u'节目单发生变化 OnTimer()内部', logs=mcon.logs)
            self.listchanged=True
            self.mmtime = tmptime
            mcon.reload()
            self.ChangeMovie()
        #检查是否存在exit 文件, 如果有退出系统
        if os.path.isfile('exit'):
            os.remove('exit')
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
    try :
        mcon = movieConf()
    except Exception, ex:
        errlog(u'配置文件错误', ex, sys.exc_info())
    log(u"\n\n***************开始运行程序***************\n\n",logs=mcon.logs)
    app = wx.App(redirect=False)
    b = MainFrame()
    app.MainLoop()




