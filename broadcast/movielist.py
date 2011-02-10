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

class Mlist(object):
    '''
    影片列表类
    '''
    def __init__(self,filename=u'mainlist.xml'):
        '''
        类的初始化,读取一个xml文件,生成文件列表
        '''
        self.mlist=[]   #播出文件列表
        self.length=0   #播出文件的个数
        self.nowplay=0  #当前播放的影片号,从0开始
        dom=xml.dom.minidom.parse(filename)
        self.root=dom.documentElement
        self.length=len(self.root.getElementsByTagName('movie'))
        if self.length > 0:
            movielist = self.root.getElementsByTagName('movie')
            for eachmovie in movielist:
                self.mlist.append(getText(eachmovie))
        return 

    def append(self,moviename,order=-9):
        '''
        插入一个影片到末尾,0表示最前面,-9表示最后面,
        -1表示插入正在播放的后面
        '''
        if order == -1:
            order=self.length+1
        if order >= 0 and order <self.length:
            self.mlist.insert(order,moviename)
        else :
            self.mlist.append(moviename)
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
            data.append(''.join((u' '*4 + u'<movie>',
                eachmovie,u'</movie>')))
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
    def getnextfile(self):
        '''
        返回下一个影片的文件名
        '''
        if self.nowplay == self.length-1:
            return self.mlist[0]
        else:
            return self.mlist[self.nowplay+1]

    def makebaselist(self,path,extension=['*']):
        '''
        根据指定目录增加所有文件到播放列表,如果重复则不添加
        '''
        for eachex in extension:
            tmppath=os.path.join(path,eachex)
            for eachfile in glob.glob(tmppath):
                if eachfile not in self.mlist:
                    self.mlist.append(eachfile)
        self.length=len(self.mlist)
        


def getText(node):
    '''
    读取一个只包含text元素的node值, 返回其中的内容
    '''
    rc = ""
    
    for eachnode in node.childNodes:
        if eachnode.nodeType == eachnode.TEXT_NODE:
            rc = rc + eachnode.data
    return rc

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


