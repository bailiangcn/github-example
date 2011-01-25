#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011-01-26 01:06:27


"""
根据网页生成数据广播需要的天气预报网页
流程:1、从getWeather*取得不同数据, 输出xml
        <source>0</source>    ＃表示0号网址信息来源
        Array(0) = "省份 地区/洲 国家名(国外)"
        Array(1) = "查询的天气预报地区名称"
        Array(2) = "查询的天气预报地区ID"
        Array(3) = "最后更新时间 格式:yyyy-MM-dd HH:mm:ss"
        Array(4) = "当前天气实况:气温、风向/风力、湿度"
        Array(5) = "第一天 空气质量、紫外线强度"
        Array(6) = "第一天 天气和生活指数"
        Array(7) = "第一天 概况 格式:M月d日 天气概况"
        Array(8) = "第一天 气温"
        Array(9) = "第一天 风力/风向"
        Array(10) = "第一天 天气图标 1"
        Array(11) = "第一天 天气图标 2"
        Array(12) = "第二天 概况 格式:M月d日 天气概况"
        Array(13) = "第二天 气温"
        Array(14) = "第二天 风力/风向"
        Array(15) = "第二天 天气图标 1"
        Array(16) = "第二天 天气图标 2"
        ......
        ......每一天的格式同:Array(12) -- Array(16)
        ......
        Array(n-4) = "最后一天 概况 格式:M月d日 天气概况"
        Array(n-3) = "最后一天 气温"
        Array(n-2) = "最后一天 风力/风向"
        Array(n-1) = "最后一天 天气图标 1"
        Array(n) = "最后一天 天气图标 2"
        如查询结果为空,输出以下结果:
        Array(0) = "查询结果为空"    

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
import xml.dom.minidom
import codecs
 
def getWeather0():
    '''
        从www.webxml.com.cn 取得天气数据(xml格式)
    '''
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################
    DAQINGID = '83'
    USERID = '92dc44c3fa1341c5b1e837f0d19d3c7b'
    URL = ''.join(("http://webservice.webxml.com.cn/", 
            "WebServices/WeatherWS.asmx/", 
            "getWeather?theCityCode=", 
            DAQINGID, "&theUserID=", USERID))
    FILENAME = "template/wea.xml"
    SOURCE = "0"
    ############################################
    try:
        # 获取网页源文件  
        sock = urllib.urlopen(URL)  
        strxml = sock.read()  
        dom=xml.dom.minidom.parseString(strxml)
        root=dom.documentElement
        #验证xml的第一个string元素是黑龙江, 如果是表示数据正常
        areastr=root.getElementsByTagName("string")[1].firstChild.data
        if  areastr== u'大庆':
            #添加数据来源标识, 增加source 元素
            soutext = dom.createTextNode(SOURCE)
            souelement = dom.createElement("source")
            souelement.appendChild(soutext)
            root.appendChild(souelement)

            #xml文件正常, 保存到template目录下的w1.xml
            #遍历nodes，删除所有空格元素
            clearSpace(dom, dom.documentElement)
            Indent(dom, dom.documentElement)
            f=file(FILENAME,'w')
            writer=codecs.lookup('utf-8')[3](f)
            dom.writexml(writer,encoding='utf-8')
            writer.close()
            f.close()
        else:
            print "nothing get"
            #print root.toxml().encode("utf-8")

    except Exception, ex:  
        #如果错误, 记入日志
        print ex
        print sys.exc_info()

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
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################

    URL = "http://qq.ip138.com/weather/heilongjiang/DaQing.htm"

    ############################################

    reWeather = re.compile(r'(?<=align\="center">天气</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    reTemperature = re.compile(r'(?<=align\="center">气温</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    reWind = re.compile(r'(?<=align\="center">风向</td>).+?(?=</tr)',
            re.I|re.S|re.U)


    try:  
        # 获取网页源文件  
        sock = urllib.urlopen(URL)  
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
    except:  
        return "There is sth wrong with the weather forecast, please inform the author. thx~" 

def xmlToHtml():
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

def transPicId(souname):
    '''
    转换不同网站的图片名称, 翻译成本地的各种图片名称
    0:www.webxml.com.cn
    1:www.weather.com.cn
    2:tool.115.com
    3:www.nmc.gov.cn
    4:tg.360.cn
    '''
    return ([0, '0'])
def getText(nodelist):
    '''
    读取一个text元素, 返回其中的内容
    '''
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def clearSpace(dom, node):
    '''
    删除xml文件中的所有空行
    '''
    children = node.childNodes[:]
    if children:
        for nd in children:
            if nd.nodeType == 3 and nd.data.isspace(): 
                node.removeChild(nd)
            else:
                clearSpace(dom,nd)

def Indent(dom, node, indent = 0):
    #美化xml 文件, 用于缩进
    # Copy child list because it will change soon
    children = node.childNodes[:]
    # Main node doesn't need to be indented
    if indent:
        text = dom.createTextNode('\n' + '\t' * indent)
        node.parentNode.insertBefore(text, node)
    if children:
        # Append newline after last child, except for text nodes
        if children[-1].nodeType == node.ELEMENT_NODE:
            text = dom.createTextNode('\n' + '\t' * indent)
            node.appendChild(text)
        # Indent children which are elements
        for n in children:
            if n.nodeType == node.ELEMENT_NODE:
                Indent(dom, n, indent + 1)

#
##自动调用测试用例，请输入测试用例名
#
def testmain():
    import unittest
    import sys
    import os

    sys.path.append(os.curdir)
    sys.path.append(os.path.join(os.curdir, 'tests'))

    from testweather import simpleTest

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(simpleTest)
    result = unittest.TextTestRunner(verbosity=3).run(suite)

if __name__=='__main__':

    testmain()


