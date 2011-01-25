#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011-01-26 01:26:42


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
        weather.getWeather0()
    def testtransPicId(self):
        '''
        测试transPicId能否正确转换为本地图片名称
        '''
        knownValues= (('d00.png', [0, '0']),
                ('d00.gif', [1, '0']), 
                ('d00.png', [2, '0']), 
                ('d0.gif', [3, '0']), 
                ('0.gif', [4, '0']), 
                )
        for souname, wishres in knownValues:
            result = weather.transPicId(souname)
            self.assertEqual(wishres, result)

if '__main__' == __name__:
    import unittest
    unittest.main()

