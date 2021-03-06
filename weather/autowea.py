#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@163.com
# vim:ts=4:sw=4:ft=python:expandtab:set fdm=indent:


"""
天气预报自动获取生成的调度程序
"""

__revision__ = '0.1'

import glob
import os
import sys
import weather
from weather import zhLjust
import time

import ConfigParser
#生成页面的顺序, 可以调整ORDER的顺序,
#表示生成的优先选用顺序
############################################

cf = ConfigParser.ConfigParser()
cf.read("config.ini")
ORDER = cf.get("host", "order").decode('utf-8').split(' ')

#ORDER = [u'0', u'9', u'1', u'2']
#管理员邮箱, 可自行添加(但注意可能出现126认为是垃圾邮件)
MAILLIST = ['bailiangcn@163.com', 'test2011@126.com']
############################################

#删除所有原有的wea*.xml文件
os.system('rm template/wea[0-9].xml')

mess = u'信息采集开始:\n\n'
for order in ORDER:
    cmdstr = u'weather.getWeather'+order+u'()'
    weafilename = u'template/wea'+order+u'.xml'
    i = 0
    #如果网页链接出错,等待5秒钟后重新采集三次
    while i < 3:
        exec cmdstr
        if os.path.isfile(weafilename):
            mess = ''.join((mess, u' '*4, u'信息源', order, u'号成功\n'))
            i = 9
        else:
            time.sleep(5)
            i += 1
    if i < 9:
        mess = ''.join((mess, u' '*4, u'信息源', order, u'号失败\n'))

#取出所有生成的中间xml文件
allwealist = glob.glob('template/wea[0-9].xml')
if len(allwealist) == 0:
    weather.log('严重错误:未能取得任何文件')
    weather.sendsimplemail(MAILLIST,
                           '天气预报严重错误', '未能取得任何文件,请尽快检查系统')
    sys.exit()
else:
    #生成采集信息报告
    mess = ''.join((mess, u'\n采集报告结果报告:\n', u'='*16))
    for order in ORDER:
        filename = u'template/wea' + order + u'.xml'
        if filename in allwealist:
            nowlist = weather.xmlToList(filename)
            mess = ''.join((mess, u'\n\n系统采集正常,信息来源:', nowlist[0], u'\n'))
            mess = ''.join((mess, u'\n', u' '*4, nowlist[1]))
            tempstr = "| ".join((
                zhLjust(nowlist[2], 20), zhLjust(nowlist[3], 20),
                zhLjust(nowlist[5], 20), zhLjust(nowlist[4], 40),
            ))
            mess = ''.join((mess, u'\n', u' '*4, tempstr))
            tempstr = "| ".join((
                zhLjust(nowlist[6], 20), zhLjust(nowlist[7], 20),
                zhLjust(nowlist[8], 20),
            ))
            mess = ''.join((mess, u'\n', u' '*4, tempstr))
            tempstr = "| ".join((
                zhLjust(nowlist[9], 20),
                zhLjust(nowlist[10], 20), zhLjust(nowlist[11], 20)
            ))
            mess = ''.join((mess, u'\n', u' '*4, tempstr))
for order in ORDER:
    filename = u'template/wea' + order + u'.xml'
    if filename in allwealist:
        mess = ''.join((mess, u'\n\n', u'='*16,
                        u'\n\n系统采集正常,生成页面采用信息来源: ', filename))
        weather.xmlToHtml(filename)
        weather.sendattachmail('bailiangcn@163.com',
                               u'天气预报运行报告',
                               mess.encode('utf-8'))
        break
