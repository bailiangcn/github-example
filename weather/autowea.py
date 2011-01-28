#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月28日 15时39分54秒


""" 
天气预报自动获取生成的调度程序
"""

__revision__ = '0.1'

import glob
import os
import sys
import weather

#生成页面的顺序
############################################
ORDER = [u'0', u'9', u'2']
############################################

#删除所有原有的wea*.xml文件
os.system('rm template/wea[0-9].xml')

#取网页生成xml文件
weather.getWeather0()
weather.getWeather2()
weather.getWeather9()


#取出所有生成的中间xml文件
allwealist = glob.glob('template/wea[0-9].xml')
if len(allwealist)==0:
    log('严重错误:未能取得任何文件')
    sys.exit()
for order in ORDER:
    filename = u'template/wea' + order + u'.xml'
    if filename in allwealist:
        weather.xmlToHtml(filename)
        print "making from %s" % filename
        break
