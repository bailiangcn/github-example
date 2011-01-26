#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月26日 16时03分05秒


"""
用于测试weather.py各模块
"""

__revision__ = '0.1'



import sys
import os

sys.path.append(os.curdir)
sys.path.append(os.path.join(os.pardir, ''))

from unittest import TestCase
import weather

class simpleTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExample(self):
        self.assertEqual(1, 1)

    def testOther(self):
        self.assertNotEqual(0, 1)
    def testgetWeather0(self):
        pass
        #weather.getWeather0()
    def testxmlToHtml(self):
        '''
        测试读取xml文件生成html文件
        xmlToHtml()
        '''
        weather.xmlToHtml('./template/w1.xml')

    def testdiffDayAndWeather(self):
        '''
        测试diffDayAndWeather()能否正常返回元组
        '''
        knownValues= ((u'1月26日 多云', [u'1月', u'26日',u'多云']), 
                )
        for temstr, wishres in knownValues:
            result = weather.diffDayAndWeather(temstr)
            self.assertEqual(wishres, result)
    def testdiffTem(self):
        '''
        测试diffTem()能否正常返回元组
        '''
        knownValues= (('-28℃/-18℃', ['-28℃','-18℃']), 
                )
        for temstr, wishres in knownValues:
            result = weather.diffTem(temstr)
            self.assertEqual(wishres, result)

    def testtransPicId(self):
        '''
        测试transPicId能否正确转换为本地图片名称
        '''
        knownValues= (('d00.png',  '0.png'),
                ('d00.gif',  '0.png'), 
                ('d00.png',  '0.png'), 
                ('d0.gif',  '0.png'), 
                ('0.gif',  '0.png'), 
                ('a_0.gif',  '0.png'), 
                ('b_0.gif',  '0.png'), 
                ('d10.png',  '10.png'),
                ('d10.gif',  '10.png'), 
                ('d10.png',  '10.png'), 
                ('d10.gif',  '10.png'), 
                ('10.gif',  '10.png'), 
                ('a_10.gif',  '10.png'), 
                ('b_10.gif',  '10.png'), 
                )
        for souname, wishres in knownValues:
            result = weather.transPicId(souname)
            self.assertEqual(wishres, result)

if '__main__' == __name__:
    import unittest
    unittest.main()

