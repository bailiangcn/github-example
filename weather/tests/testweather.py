#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


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
import filecmp


class simpleTest(TestCase):

    def testgetWeather0(self):
        '''
        测试从www.webxml.com.cn 取得天气数据(xml格式)
        '''
        soufile = './tests/data/weather_0_20140729.xml'
        weather.getWeather0(soufile)
        self.assertTrue(filecmp.cmp('./template/wea0.xml',
                                    './tests/data/weares_0_20140729.xml'))

    def testgetWeather1(self):
        '''
        测从 weather_1
        http://www.weather.com.cn/html/weather/101050901.shtml
        取得天气数据(html格式)
        '''
        soufile = './tests/data/weather_1_20140729.html'
        weather.getWeather1(soufile)
        #weather.getWeather1()
        outfile = './template/wea1.xml'
        self.assertTrue(os.path.exists(outfile), "output error found")
        self.assertTrue(filecmp.cmp('./template/wea1.xml',
                                './tests/data/weares_1_20140729.xml'))

    def testgetWeather2(self):
        '''
        测试从qq.ip138.com 取得天气数据(html格式)
        '''
        soufile = './tests/data/weather_2_20140730.html'
        weather.getWeather2(soufile)
        #weather.getWeather2()
        outfile = './template/wea2.xml'
        self.assertTrue(os.path.exists(outfile), "output error found")
        correct_res = './tests/data/weares_2_20140730.xml'
        if not filecmp.cmp(outfile, correct_res):
            commstr = 'diff %s %s' % (outfile, correct_res)
            os.system(commstr)
            self.fail("result have error!")

    def getWeather9(self):
        '''
        测试从www.webxml.com.cn 取得天气数据(xml格式)
        '''
        weather.getWeather9()

    def testlistToxml(self):
        '''
        测试根据列表变量生成xml文件
        listToxml(soulist)
        '''
        soulist = [u'0', u'2011/01/25 22:11:52', u'1月26日 多云',
                   u'-28℃/-18℃', u'北风微风转西风微风', u'1.gif',
                   u'1月27日 晴', u'-28℃/-18℃', u'0.gif',
                   u'1月28日 晴', u'-29℃/-18℃', u'0.gif']
        weather.listToxml(soulist, 'template/testwea.xml')

    def testxmlToList(self):
        '''
        测试读取xml文件生成html文件
        xmlToList()
        '''
        wishvalue = [u'0', u'2011/01/25 22:11:52', u'1月26日 多云',
                     u'-28℃/-18℃', u'北风微风转西风微风', u'1.gif',
                     u'1月27日 晴', u'-28℃/-18℃', u'0.gif',
                     u'1月28日 晴', u'-29℃/-18℃', u'0.gif']
        resvalue = weather.xmlToList('./template/testwea0.xml')
        self.assertEqual(wishvalue, resvalue)

    def xmlToHtml(self):
        '''
        测试读取xml文件生成html文件
        xmlToHtml()
        '''
        weather.xmlToHtml('./template/wea2.xml')

    def testinsertBar(self):
        '''
        测试输入超长字符串自动断行
        '''
        knownValues = ((u'西风微风转西北风微风',
                       u'西风微风'),
                      (u'西风转西北风', u'西风'),
                      (u'西风', u'西风'),
                      (u'西风西北微风', u'西风西<br>北微风'),
                      (u'西风西北微风西风西北微风西风转西北微风',
                       u'西风西北微<br>风西风西北'),
                       )
        for soustr, resstr in knownValues:
            wishres = weather.insertBr(soustr)
            self.assertEqual(wishres, resstr)

    def testdiffDayAndWeather(self):
        '''
        测试diffDayAndWeather()能否正常返回元组
        '''
        knownValues = ((u'1月26日 多云',
                       [u'1月', u'26日', u'多云', u'星期三']),
                       )
        for temstr, wishres in knownValues:
            result = weather.diffDayAndWeather(temstr, True)
            self.assertEqual(wishres, result)

    def testdiffTem(self):
        '''
        测试diffTem()能否正常返回元组
        '''
        knownValues = (('-28℃/-18℃', ['-28℃', '-18℃']),
                       )
        for temstr, wishres in knownValues:
            result = weather.diffTem(temstr)
            self.assertEqual(wishres, result)

    def testlog(self):
        '''
        测试log函数记录日志功能
        '''
        res = weather.log('开始日志记录')
        self.assertEqual(res, True)

    def testtransPicId(self):
        '''
        测试transPicId能否正确转换为本地图片名称
        '''
        knownValues = (('d00.png',  '0.png'),
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
                      ('d01',  '1.png'),
                      ('n01',  '1.png'),
                       )
        for souname, wishres in knownValues:
            result = weather.transPicId(souname)
            self.assertEqual(wishres, result)

    def testisChinese(self):
        '''
        测试isChinese()能否判断汉字
        '''
        knownValues = ((u'中', True), ('e', False),
                       ('中', False))
        for souchr, wishres in knownValues:
            result = weather.isChinese(souchr)
            self.assertEqual(wishres, result)

    def testzhLjust(self):
        '''
        测试zhLjust()能否正确根据中文填充空格
        '''
        knownValues = (
            ((u'中', 4), u'中 '),
            ((u'e中f  ', 6), u'e中f '),
        )
        for souchr, wishres in knownValues:
            result = weather.zhLjust(souchr[0], souchr[1])
            self.assertEqual(wishres, result)

    def testsendsimplemail(self):
        '''
        测试sendsimplemail()发送邮件功能
        '''
        weather.sendsimplemail(
            ['bailiangcn@gmail.com', 'bailiangcn@163.com'],
            '群发邮件测试', '兔年吉祥\n新年快乐')

    def testsendattachmail(self):
        weather.sendattachmail('bailiangcn@163.com',
                               '测试附件', '希望顺利')

    def testreverseTemp(self):
        '''
        测试 reverseTemp()
        '''
        knownValues = (
            (u'27℃～20℃', u'20℃/27℃'),
        )
        for souchr, wishres in knownValues:
            result = weather.reverseTemp(souchr)
            self.assertEqual(wishres, result)

if '__main__' == __name__:
    import unittest
    unittest.main()
