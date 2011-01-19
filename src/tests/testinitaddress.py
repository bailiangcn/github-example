#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011-01-19 21:28:37


"""
测试initaddress.py各个函数
"""

__revision__ = '0.1'




import sys
import os

sys.path.append(os.curdir)
sys.path.append(os.path.join(os.pardir, ''))

from unittest import TestCase
import initaddress


class simpleTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExample(self):
        self.assertEqual(1, 1)

    def testOther(self):
        self.assertNotEqual(0, 1)

    def testInitarea(self):
        a = initaddress.initarea()
        self.assertEqual(1, a)
        

if '__main__' == __name__:
    import unittest
    unittest.main()

