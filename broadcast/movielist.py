#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""
视频播放类,具备功能: 
    初始化一个播放列表文件,输入文件名
    添加一个影片到末尾
    插入一个影片
    重新排序
    当前播放影片
    下一个播放影片
    重置当前播放影片
"""

__revision__ = '0.1'

import xml.dom.minidom
import glob
import os
from copy import deepcopy
import sys
import datetime 

class Mlist(object):
    '''
    影片列表类
    '''
    def __init__(self,filename=u'mainlist.xml',empty=False):
        '''
        类的初始化,读取一个xml文件,生成文件列表
        '''
        self.reload(filename,empty)

    def reload(self,filename=u'mainlist.xml',empty=False):
        self.mlist=[]   #播出文件列表
        self.length=0   #播出文件的个数
        self.nowplay=0  #当前播放的影片号,从0开始
        if  empty:
            return
        try:
            dom=xml.dom.minidom.parse(filename)
            self.root=dom.documentElement
            movielist = self.root.getElementsByTagName('MOVIE')
            if len(movielist) > 0:
                mdict={}
                for eachmovie in movielist:
                    mn=eachmovie.getElementsByTagName('NAME')
                    if len(mn) > 0:
                        mdict['name']=getText(mn[0])
                        mp=eachmovie.getElementsByTagName('PATH')
                        if len(mp)>0:
                            mdict['path']=getText(mp[0])
                            if mdict['path'] != '':
                                self.mlist.append(deepcopy(mdict))
                self.length=len(self.mlist)
        except Exception, ex:  
            #如果错误, 记入日志
            print ex
        return 

    def append(self,moviename,order=-9):
        '''
        moviename是一个列表,[0]表示影片名称,[1]表示影片文件地址
        插入一个影片到末尾,0表示最前面,-9表示最后面,
        -1表示插入正在播放的后面
        '''
        moviedict={'name':moviename[0],'path':moviename[1]}
        if order == -1:
            order=self.length+1
        if order >= 0 and order <self.length:
            self.mlist.insert(order,deepcopy(moviedict))
        else :
            self.mlist.append(deepcopy(moviedict))
        self.length += 1
        return

    def savefile(self,filename):
        '''
        保存节目列表为xml文件
        '''
        data = []
        data.append(u'<?xml version="1.0" encoding="utf-8"?>')
        data.append(u'<ROOT>')
        for eachmovie in self.mlist:
            data.append(''.join((u' '*4 + u'<MOVIE>')))
            data.append(''.join((u' '*8 + u'<NAME>' +eachmovie[
                'name']+ u'</NAME>')))
            data.append(''.join((u' '*8 + u'<PATH>' +eachmovie[
                'path']+ u'</PATH>')))
            data.append(''.join((u' '*4 + u'</MOVIE>')))
        data.append(u'</ROOT>')

        try:
            f = open(filename, 'w')
            for line in data:
                line += '\n' 
                f.write(line.encode('utf-8'))
            f.close()
        except Exception, ex:  
            #如果错误, 记入日志
            print ex
            print sys.exc_info()

    def getnextfile(self,num=0):
        '''
        返回下一个影片的文件名
        '''
        nownum=self.nowplay+num
        self.length=len(self.mlist)
        #print "nownum=",nownum
        #print "length=",self.length
        if nownum > self.length-1:
            return self.mlist[0]['path']
        else:
            return self.mlist[nownum]['path']

    def beginnext(self):
        '''
        标记开始下一个影片
        '''
        self.nowplay+=1
        self.length=len(self.mlist)
        if self.nowplay>self.length-1:
            self.nowplay=0
        return self.nowplay

    def getnowplay(self):
        '''
        返回当前播放的影片,如果是-1表示停止播放
        '''
        return self.nowplay

    def makebaselist(self,path,extension=['*']):
        '''
        根据指定目录增加所有文件到播放列表,如果重复则不添加
        '''
        mdict={}
        templist=[]
        [templist.append(x['name']) for x in self.mlist]
        for eachex in extension:
            tmppath=os.path.join(path,eachex).encode('utf-8') 
            dirlist=glob.glob(tmppath)
            dirlist.sort()
            for eachfile in dirlist:
                tempmn=os.path.splitext(
                        os.path.basename(eachfile))[0]
                if tempmn not in templist:
                    mdict['name']=unicode(tempmn,'utf-8')
                    mdict['path']=unicode(os.path.abspath(eachfile),'utf-8')
                    self.mlist.append(deepcopy(mdict))
        self.length=len(self.mlist)

    def movemovie(self,oldord,neword):
        '''
        调整节目的顺序,从oldord到neword
        '''
        tempmovie=self.mlist.pop(oldord)
        self.mlist.insert(neword,tempmovie)

    def tostr(self):
        '''
        文本格式显示mlist
        '''
        resstr=u"节目列表:\n"
        for eachmovie in self.mlist:
            ts=u"name:"+eachmovie['name'
                ]+u"    path:"+eachmovie['path']+u"\n"
            resstr+=ts
        return resstr

            
        


def getText(node):
    '''
    读取一个只包含text元素的node值, 返回其中的内容
    '''
    rc = ""
    
    for eachnode in node.childNodes:
        if eachnode.nodeType == eachnode.TEXT_NODE:
            rc = rc + eachnode.data
    return rc

def errlog(modelname, ex, exc_info):
    '''
    把错误信息写入日志文件
    usage:
    try:
    except Exception, ex:
        errlog('发送邮件错误', ex, sys.exc_info())
    '''
    log(modelname + u'模块发生错误:',u'logs/error.log')
    log(unicode(ex),u'logs/error.log') 
    log(unicode(exc_info),u'logs/error.log')

def log(str, filename=u"logs/schedule.log",logs=True):
    '''
    把字符串写入日志文件
    '''
    #根据分类从配置文件选择合适的目标文件写入字符串
    if logs:
        nowtimestr = unicode(datetime.datetime.now().strftime(
            "[%Y-%m-%d %H:%M:%S]"),'utf-8')
        f = open(filename, 'a')
        if not isinstance(str,unicode):
            str = unicode(str,'utf-8')
        desstr = "%s  %s\n" % (nowtimestr, str)
        byte_out = desstr.encode('utf-8')
        f.write(byte_out)
        f.close()
        return True

#
##自动调用测试用例，请输入测试用例名
#
def testmain():
    import unittest
    import sys
    import os

    sys.path.append(os.curdir)
    sys.path.append(os.path.join(os.curdir, 'tests'))

    from testmovielist import simpleTest

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(simpleTest)
    result = unittest.TextTestRunner(verbosity=3).run(suite)

if __name__=='__main__':

    testmain()



