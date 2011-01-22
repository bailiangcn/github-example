#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月22日 13时36分50秒


"""
用于测试mm.ks文件
"""

__revision__ = '0.1'


import sys
import os

sys.path.append(os.curdir)
sys.path.append(os.path.join(os.pardir, ''))

from unittest import TestCase
import mm

class simpleTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExample(self):
        self.assertEqual(1, 1)

    def testOther(self):
        self.assertNotEqual(0, 1)

    def testcountservice(self):
        '''测试countservice()
        '''
        mm.countservice()

if '__main__' == __name__:

    import unittest
    unittest.main()

