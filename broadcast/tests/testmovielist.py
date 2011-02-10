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
        self.mt=Mlist('mainlist.xml')

    def tearDown(self):
        pass

    def testInit(self):
        "测试类的初始化"
        self.mt.mlist=[u'1.mpg', u'2.mpg']
        knownValues=[u'1.mpg', u'2.mpg']
        self.assertEqual(self.mt.mlist, knownValues)
        self.assertEqual(2, self.mt.length)

    def testAppend(self):
        "测试增加一个节目"
        knownValues=(
                ('3.mpg',0,[u'3.mpg',u'1.mpg', u'2.mpg']),
                ('3.mpg',1,[u'1.mpg',u'3.mpg', u'2.mpg']),
                ('3.mpg',-9,[u'1.mpg', u'2.mpg',u'3.mpg']),
                )
        for mn, od, res in knownValues:
            self.mt.mlist=[u'1.mpg', u'2.mpg']
            self.mt.length=2
            self.mt.append(mn,od)
            self.assertEqual(res,self.mt.mlist)
            self.assertEqual(3, self.mt.length)

    def testSavefile(self):
        "测试根据列表生成xml文件"
        self.mt.mlist=[u'1.mpg', u'2.mpg']
        self.mt.savefile(u'mainlist.xml')

    def testgetnextfile(self):
        "测试返回下一个播出文件"
        self.mt.mlist=[u'4.mpg', u'2.mpg']
        self.mt.nowplay=0
        self.mt.length=2
        self.assertEqual(u'2.mpg',self.mt.getnextfile())
        self.mt.nowplay=1
        self.assertEqual(u'4.mpg',self.mt.getnextfile())

    def testmakebaselist(self):
        "测试根据指定目录生成节目列表" 
        self.mt.makebaselist('',['*.py','*.xml'])
        print self.mt.mlist


if '__main__' == __name__:

    import unittest
    unittest.main()

