#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""
测试movielist.py
"""

__revision__ = '0.1'



import sys
import os

sys.path.append(os.curdir)
sys.path.append(os.path.join(os.pardir, ''))

from unittest import TestCase
from movielist import *

class simpleTest(TestCase):
    def setUp(self):
        self.mt=Mlist('testlist.xml')

    def tearDown(self):
        pass

    def testInit(self):
        "测试类的初始化"
        knownValues=[
                {'name':u'1.mpg','path':u'1.mpg'},
                {'name':u'2.mpg','path':u'2.mpg'},
                ]
        self.assertEqual(self.mt.mlist, knownValues)
        self.assertEqual(2, self.mt.length)

    def testAppend(self):
        "测试增加一个节目到不同顺序"
        knownValues=(
                (['3.mpg','3.mpg'],0, [
                        {'name':u'3.mpg','path':u'3.mpg'},
                        {'name':u'1.mpg','path':u'1.mpg'},
                        {'name':u'2.mpg','path':u'2.mpg'},
                        ]),
                (['3.mpg','3.mpg'],1, [
                        {'name':u'1.mpg','path':u'1.mpg'},
                        {'name':u'3.mpg','path':u'3.mpg'},
                        {'name':u'2.mpg','path':u'2.mpg'},
                        ]),
                (['3.mpg','3.mpg'],-9, [
                        {'name':u'1.mpg','path':u'1.mpg'},
                        {'name':u'2.mpg','path':u'2.mpg'},
                        {'name':u'3.mpg','path':u'3.mpg'},
                        ]),)
        for mn, od, res in knownValues:
            self.mt=Mlist('testlist.xml')
            self.mt.append(mn,od)
            self.assertEqual(res,self.mt.mlist)
            self.assertEqual(3, self.mt.length)

    def Savefile(self):
        "测试根据列表生成xml文件"
        self.mt.mlist=[
                {'name':u'1.mpg','path':u'1.mpg'},
                {'name':u'2.mpg','path':u'2.mpg'},
                ]
        self.length=2
        self.mt.savefile(u'testlist.xml')

    def testgetnextfile(self):
        "测试返回下一个播出文件"
        self.mt.nowplay=0
        self.mt.mlist=[
                        {'name':u'1.mpg','path':u'1.mpg'},
                        {'name':u'2.mpg','path':u'2.mpg'},
                        {'name':u'3.mpg','path':u'3.mpg'},
                        {'name':u'4.mpg','path':u'4.mpg'},
                        ]
        print self.mt.tostr().encode('utf-8') 
        print self.mt.getnextfile()
        self.assertEqual(u'1.mpg',self.mt.getnextfile())
        print self.mt.getnextfile(2)
        self.assertEqual(u'3.mpg',self.mt.getnextfile(2))

    def testmakebaselist(self):
        "测试根据指定目录生成节目列表" 
        mt=Mlist('mainlist.xml')
        mt.makebaselist(u'/home/bl/www/broadcast/视频片段'
                ,[u'*'])
        mt.savefile(u'mainlist.xml')

    def testmovemovie(self):
        "测试移动节目顺序" 
        knownValues=[
                {'name':u'2.mpg','path':u'2.mpg'},
                {'name':u'1.mpg','path':u'1.mpg'},
                ]
        mt=Mlist('testlist.xml')
        mt.movemovie(1,0)
        self.assertEqual(mt.mlist, knownValues)
        


if '__main__' == __name__:

    import unittest
    unittest.main()

