#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月15日 10时07分57秒


"""
测试mm.py
"""

__revision__ = '0.1'

import sys, os

sys.path.append(os.curdir)
sys.path.append(os.pardir)

from unittest import TestCase
from mm import  * 

class simpleTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #def testmakemm(self):
    #    "测试makemm函数"
    #    makemm()
    #    self.assertEqual(1, 1)

    #def testmakehtml(self):
    #    "测试makehtml 函数"
    #    makehtml()
    #    self.assertEqual(1, 1)

    def testtranscode(self):
        knowvalues= (('前端', '&#x524d;&#x7aef;'),('1-7', '1-7'), ('\n', '&#xa;') )
        for src, knowres in knowvalues:
            res = transcode(src)
        self.assertEqual(knowres, res)

    def testoutputhtml(self):
        "测试outputhtml 函数"
        outputhtml()
        self.assertEqual(1, 1)

if '__main__' == __name__:
    import unittest
    unittest.main()

