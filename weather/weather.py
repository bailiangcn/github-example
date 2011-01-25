#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月25日 16时52分28秒


"""根据网页生成数据广播需要的天气预报网页
流程:1、从getWeather*取得不同数据, 输出xml
2、检验xml格式的正确性
3、输入xml文件, 输出字典
3、对比各种输入的结果, 输出合格的xml格式
4、根据xml文件和模板生成html文件

"""

__revision__ = '0.1'


import os  
import re  
import urllib  
import sys  
import time  
from string import Template
 
def getWeather0():
    '''
        从www.webxml.com.cn 取得天气数据(xml格式)
    '''
    pass
def getWeather1():
    '''
        从http://www.weather.com.cn/html/weather/101050901.shtml
        取得天气数据(xml格式)
    '''
    pass

def getWeather2():  
    '''
        从qq.ip138.com 取得天气数据
    '''
    reWeather = re.compile(r'(?<=align\="center">天气</td>).+?(?=</tr)', re.I|re.S|re.U)
    reTemperature = re.compile(r'(?<=align\="center">气温</td>).+?(?=</tr)', re.I|re.S|re.U)
    reWind = re.compile(r'(?<=align\="center">风向</td>).+?(?=</tr)', re.I|re.S|re.U)


    try:  
        # 获取网页源文件  
        sock = urllib.urlopen("http://qq.ip138.com/weather/heilongjiang/DaQing.htm")  
        strhtml = sock.read()  
        strhtml = unicode(strhtml, 'gb2312','ignore').encode('utf-8','ignore')  
        #print strhtml
        # 正则表达式取得各段
        weatherPara = re.findall(reWeather, strhtml)
        temperaturePara = re.findall(reTemperature, strhtml)
        windPara = re.findall(reWind, strhtml)

        # 获取温度信息
        # [0] 当前温度 [1]明日最高 [2]明日最低[3]后日最高[4]后日最低
        theGrades = re.findall('(-?\d+)℃', temperaturePara[0])  
        nowtime = 0
        if int(theGrades[0]) < int(theGrades[1]):
            nowtime = 1

        # 获取天气描述信息  
        # [0] 当前天气描述 [1]明日 [2]后日
        weathers = re.findall(r'(?<=br/>).+?(?=</td)',weatherPara[0])  
        #获取风向
        # [0] 当前风向 [1]明日 [2]后日
        wind = re.findall(r'(?<=td>).+?(?=</td>)', windPara[0])

        # 定义时间格式  
        this_date = str(time.strftime("%Y/%m/%d %a"))  
        now = int(time.time())  
        sec = 24*60*60 
        day_today = "今天(%s号)" % str(time.strftime("%d", time.localtime(now+0*sec)))  
        day_tommo = "明天(%s号)" % str(time.strftime("%d", time.localtime(now+1*sec)))  
        day_aftom = "后天(%s号)" % str(time.strftime("%d", time.localtime(now+2*sec)))  
        # 定义短信正文  
        sms = [this_date]  
        sms.append("大庆天气")  
        if nowtime ==  0:
            sms.append("%s:%s,%s, %s-%s℃" % (day_today, weathers[0],wind[0], theGrades[1], theGrades[0]))  
        else:
            sms.append("%s:%s,%s, %s℃" % (day_today, weathers[0],wind[0], theGrades[0]))  

        sms.append("%s:%s,%s, %s-%s℃" % (day_tommo, weathers[1], wind[1],theGrades[3 - nowtime], theGrades[2 - nowtime]))  
        sms.append("%s:%s,%s, %s-%s℃" % (day_aftom, weathers[2], wind[2],theGrades[5 - nowtime], theGrades[4 - nowtime]))  
        smscontent = '\n'.join(sms)  

        #写入html文件
        filesou = open("./template/temp.htm", "r")
        filedes = open("./html/index.htm", "w")
        for eachline in filesou:
            s  = Template(eachline).substitute(
                    MAXTEM=theGrades[0], #最高温度
                    MINTEM=('中庆' + 'ss').decode('utf8').encode('gb2312'), 
                    )
            filedes.write('%s\n' % s)

        filesou.close()
        filedes.flush()
        filedes.close()
        return smscontent  #.decode('utf-8').encode('gb2312')  

    except:  
        return "There is sth wrong with the weather forecast, please inform the author. thx~" 


def main():  
    print "getting out the weather code..." 
    msg = getWeather2()  
    print "\n", msg  
    print "Done." 
 
if __name__ == "__main__":  
    sys.exit(main()) 

