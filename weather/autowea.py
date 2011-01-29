#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月29日 10时07分57秒


""" 
天气预报自动获取生成的调度程序
"""

__revision__ = '0.1'

import glob
import os
import sys
import weather

#生成页面的顺序, 可以调整ORDER的顺序, 
#表示生成的优先选用顺序
############################################
ORDER = [u'0', u'9', u'2']
#管理员邮箱, 可自行添加(但注意可能出现126认为是垃圾邮件)
MAILLIST = ['bailiangcn@gmail.com','test2011@126.com']
############################################

#删除所有原有的wea*.xml文件
os.system('rm template/wea[0-9].xml')

##取网页生成xml文件
weather.getWeather0()
weather.getWeather2()
weather.getWeather9()


#取出所有生成的中间xml文件
allwealist = glob.glob('template/wea[0-9].xml')
if len(allwealist)==0:
    weather.log('严重错误:未能取得任何文件')
    weather.sendsimplemail(MAILLIST, 
            '天气预报严重错误', '未能取得任何文件,请尽快检查系统')
    sys.exit()
for order in ORDER:
    filename = u'template/wea' + order + u'.xml'
    if filename in allwealist:
        mess= ''.join((u'系统采集正常,信息来源:', filename)) 
        weather.xmlToHtml(filename)
        weather.sendattachmail('bailiangcn@gmail.com',u'天气预报运行报告',
                mess.encode('utf-8'))
        break
