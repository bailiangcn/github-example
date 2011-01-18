#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月18日 17时57分29秒


"""
用于测试mm.ks文件
"""

__revision__ = '0.1'




from unittest import TestCase

class simpleTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExample(self):
        self.assertEqual(1, 1)

    def testOther(self):
        self.assertNotEqual(0, 1)

if '__main__' == __name__:

    import unittest
    unittest.main()

