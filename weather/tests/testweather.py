#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月26日 20时53分11秒


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

    def testgetWeather0(self):
        '''
        测试从www.webxml.com.cn 取得天气数据(xml格式)
        '''
        #weather.getWeather0()
        pass

    def testlistToxml(self):
        '''
        测试根据列表变量生成xml文件
        listToxml(soulist)
        '''
        soulist = [u'0', u'2011/01/25 22:11:52',u'1月26日 多云', 
                u'-28℃/-18℃', u'北风微风转西风微风', u'1.gif',
                u'1月27日 晴', u'-28℃/-18℃', u'0.gif',
                u'1月28日 晴', u'-29℃/-18℃', u'0.gif']
        weather.listToxml(soulist)

    def testxmlToHtml(self):
        '''
        测试读取xml文件生成html文件
        xmlToHtml()
        '''
        weather.xmlToHtml('./template/wea.xml')

    def testinsertBar(self):
        '''
        测试输入超长字符串自动断行
        '''
        knownValues= ((u'西风微风转西北风微风', 
            u'西风微风转<br>西北风微风'), 
            (u'西风转西北风', u'西风转<br>西北风'), 
            (u'西风', u'西风'), 
            (u'西风转西北微风', u'西风转<br>西北微风'), 
            )
        for soustr, resstr in knownValues:
            wishres=weather.insertBr(soustr)
            self.assertEqual(wishres, resstr)

    def testdiffDayAndWeather(self):
        '''
        测试diffDayAndWeather()能否正常返回元组
        '''
        knownValues= ((u'1月26日 多云', 
            [u'1月', u'26日',u'多云', u'星期三']), 
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

