#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月21日 12时43分05秒


"""docstring
"""

__revision__ = '0.1'




import sys
import os

sys.path.append(os.curdir)
sys.path.append(os.path.join(os.pardir, ''))

from unittest import TestCase
import ajax

class simpleTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExample(self):
        self.assertEqual(1, 1)

    def testOther(self):
        self.assertNotEqual(0, 1)

    def testajax(self):
        '''测试ajax方法'''
        xmlstr =('<root>' 
        '<house id="1" regid="1" serid="7"/>'
        '<house id="4" regid="3" serid="1"/>'
        '<house id="5" regid="2" serid="1"/>'
        '<house id="6" regid="1" serid="4"/>'
        '<house id="2" regid="1" serid="5"/>'
        '</root>')

        ajax.ajax(xmlstr)
        self.assertEqual(1, 1)


if '__main__' == __name__:
    import unittest
    unittest.main()

