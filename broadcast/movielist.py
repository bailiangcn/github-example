#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com


"""
视频播放类,具备功能: 
    初始化一个播放列表文件,输入文件名
    添加一个影片到末尾
    插入一个影片
    重新排序
    当前播放影片
    下一个播放影片
    重置当前播放影片
"""

__revision__ = '0.1'




#
##自动调用测试用例，请输入测试用例名
#
def testmain():
    import unittest
    import sys
    import os

    sys.path.append(os.curdir)
    sys.path.append(os.path.join(os.curdir, 'tests'))

    from testmovielist import simpleTest

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(simpleTest)
    result = unittest.TextTestRunner(verbosity=3).run(suite)

if __name__=='__main__':

    testmain()


