#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月30日 16时53分33秒

"""
根据网页生成数据广播需要的天气预报网页
流程:
1、从getWeather9取得数据, 输出xml格式
    <source>0</source>    ＃表示0号网址信息来源
    Array(0) = "省份 地区/洲 国家名(国外)"
    Array(1) = "查询的天气预报地区名称"
    Array(2) = "查询的天气预报地区ID"
    Array(3) = "最后更新时间 格式:yyyy/MM/dd HH:mm:ss"
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
    Array(17) = "第3天 概况 格式:M月d日 天气概况"
    Array(18) = "第3天 气温"
    Array(19) = "第3天 风力/风向"
    Array(20) = "第3天 天气图标 1"
    Array(21) = "第3天 天气图标 2"
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

2、从其他网页取得数据, 输出为列表格式, 调用listToxml(filename)生成xml文件
    listToxml(weadata, filename)输入要求如下:
    weadata [0]    "信息来源"
    weadata [1]    "更新时间 格式:yyyy-MM-dd HH:mm:ss"
    weadata [2]    "第一天 概况 格式:M月d日 天气概况"
    weadata [3]    "第一天 气温"  
    weadata [4]    "第一天 风力/风向"
    weadata [5]    "第一天 天气图标 1"                
    weadata [6]    "第二天 概况 格式:M月d日 天气概况"
    weadata [7]    "第二天 气温"  
    weadata [8]    "第二天 天气图标 1"                
    weadata [9]    "第三天 概况 格式:M月d日 天气概况"
    weadata [10]   "第三天 气温"  
    weadata [11]   "第三天 天气图标 1"

    filename要求为相对于本脚本的相对路径名

3、检验xml格式的正确性(待完善)
4、输入xml文件, 输出列表(待完善)
4、对比各种输入的结果, 输出合格的xml格式(待完善)
5、根据xml文件和模板生成html文件
"""
__revision__ = '0.1'

import os  
import re  
import urllib  
import sys  
import time  
import datetime
from string import Template
import xml.dom.minidom
import codecs

import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart

############################################################ 
#                                                          #
#              网页读取部分                                #
#                                                          #
############################################################

def getWeather0():
    '''
    从www.webxml.com.cn 取得天气数据(xml格式)
    直接保存为xml格式
    来源格式说明: 
    String(0) 到 String(4)：省份0，城市1，城市代码2，城市图片名称3，最后更新时间4。
    String(5) 到 String(11)：当天的 气温5，概况6，风向和风力7，天气趋势开始图片
        名称(以下称：图标一)8，天气趋势结束图片名称(以下称：图标二)9，现在的天
        气实况10，天气和生活指数11。 
    String(12) 到 String(16)：第二天的 气温12，概况13，风向和风力14，
            图标一15，图标二16。
    String(17) 到 String(21)：第三天的 气温17，概况18，风向和风力19，
            图标一20，图标二21。
    String(22) 被查询的城市或地区的介绍 
    输出格式说明:(参见listToxml()输入要求)
    '''
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################
    DAQINGID = '50842'
    URL = ''.join(("http://webservice.webxml.com.cn/", 
            "WebServices/Weatherwebservice.asmx/", 
            "getWeatherbyCityName?theCityName=", 
            DAQINGID))
    FILENAME = "template/wea0.xml"
    SOURCE = "0"
    ############################################
    try:
        # 获取网页源文件  
        sock = urllib.urlopen(URL)  
        strxml = sock.read()  
        dom=xml.dom.minidom.parseString(strxml)
        root=dom.documentElement
        #验证xml的第二个string元素是大庆, 如果是表示数据正常
        strlist=root.getElementsByTagName("string")
        if strlist[1].hasChildNodes():
            areastr=strlist[1].firstChild.data
        else:
            log('weather0获取xml文件失败')
            log(strxml)
            return False
        if  areastr== u'大庆':
            #生成一个包含所有天气字符串的列表
            weatherlist = []
            for eachstr in strlist:
                weatherlist.append(getText(eachstr))
            resultlist = [u'0', weatherlist[4].replace("-", "/"), 
                    weatherlist[6], weatherlist[5], weatherlist[7], 
                    weatherlist[8], weatherlist[13],weatherlist[12],
                    weatherlist[15],weatherlist[18],weatherlist[17],
                    weatherlist[20]]
            listToxml(resultlist, "template/wea0.xml")
            log('weather0获取天气信息成功', 'logs/running.log')
        else:
            log('weather0获取xml文件失败')
            log(strxml)
            log('weather0获取xml文件失败', 'logs/running.log')
            return False
    except Exception, ex:  
        #如果错误, 记入日志
        log('严重错误:weather0获取xml文件失败')
        errlog('getWeather0', ex, sys.exc_info())
        return False
    return True

def getWeather1():
    '''
        从http://www.weather.com.cn/html/weather/101050901.shtml
        取得天气数据(html格式), 输出为xml格式
    '''
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################

    URL = "http://www.weather.com.cn/html/weather/101050901.shtml"

    ############################################

    reDay = re.compile(r'(?<=class="weatherYubaoBox">).*?(?=id\="weatherYubao2")', 
            re.I|re.S|re.U)

    reWeather = re.compile(r'(?<=align\="center">天气</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    reTemperature = re.compile(r'(?<=align\="center">气温</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    reWind = re.compile(r'(?<=align\="center">风向</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    rePic = reWeather
    reEachDay = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})',re.I|re.S|re.U)
    
    weadata = []
    for i in range(12):
        weadata.append(u'')
    try:  
        # 获取网页源文件  
        sock = urllib.urlopen(URL)  
        strhtml = sock.read()  
        # 正则表达式取得各段
        dayPara = re.findall(reDay, strhtml)
        weatherPara = re.findall(reWeather, strhtml)
        temperaturePara = re.findall(reTemperature, strhtml)
        windPara = re.findall(reWind, strhtml)
        picPara = re.findall(rePic, strhtml)
        #获取日期
        #print len(dayPara)
        #print dayPara[0]
        return

    except Exception, ex:  
        #如果错误, 记入日志
        errlog('getWeather1', ex, sys.exc_info())

def getWeather2():  
    '''
        从qq.ip138.com 取得天气数据(html格式), 输出为xml格式
    '''
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################

    URL = "http://qq.ip138.com/weather/heilongjiang/DaQing.htm"

    ############################################

    reDay = re.compile(r'(?<=日期).*星期.+?(?=</tr>)', 
            re.I|re.S|re.U)
    reWeather = re.compile(r'(?<=align\="center">天气</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    reTemperature = re.compile(r'(?<=align\="center">气温</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    reWind = re.compile(r'(?<=align\="center">风向</td>).+?(?=</tr)',
            re.I|re.S|re.U)
    rePic = reWeather
    reEachDay = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})',re.I|re.S|re.U)
    
    weadata = []
    for i in range(12):
        weadata.append(u'')
    try:  
        #获取网页源文件  
        sock = urllib.urlopen(URL)  
        strhtml = sock.read()  
        strhtml = unicode(strhtml, 'gb2312','ignore').encode('utf-8','ignore')  

        # 正则表达式取得各段
        dayPara = re.findall(reDay, strhtml)
        weatherPara = re.findall(reWeather, strhtml)
        temperaturePara = re.findall(reTemperature, strhtml)
        windPara = re.findall(reWind, strhtml)
        picPara = re.findall(rePic, strhtml)
        #获取日期
        theDays= re.findall(reEachDay, dayPara[0]) 
        firstDay = datetime.datetime.strptime(theDays[1],'%Y-%m-%d')
        nextDay = firstDay + datetime.timedelta(1)
        lastDay = firstDay + datetime.timedelta(2)
        weadata[0] = u'2'
        weadata[1] = unicode(theDays[0].replace('-', '/'))
        weadata[2] = unicode(firstDay.month)+u'月'+unicode(firstDay.day)+u'日 '
        weadata[6] = unicode(nextDay.month)+u'月'+unicode(nextDay.day)+u'日 '
        weadata[9] = unicode(lastDay.month)+u'月'+unicode(lastDay.day)+u'日 '

        #获取天气概况
        theWeathers= re.findall(r'(?<=br/>).+?(?=</td)',weatherPara[0])  
        weadata[2] += unicode(theWeathers[1].decode('utf-8')) 
        weadata[6] += unicode(theWeathers[2] .decode('utf-8'))
        weadata[9] += unicode(theWeathers[3] .decode('utf-8'))
        # 获取温度信息
        # [0] 当前温度 [1]明日最高 [2]明日最低[3]后日最高[4]后日最低
        theGrades = re.findall('(-?\d+℃)', temperaturePara[0])  
        weadata[3] = unicode(theGrades[2].decode('utf-8')
                ) + u'/' +unicode(theGrades[3].decode('utf-8')) 
        weadata[7] = unicode(theGrades[4].decode('utf-8')
                ) + u'/' +unicode(theGrades[5].decode('utf-8')) 
        weadata[10] = unicode(theGrades[6].decode('utf-8')
                ) + u'/' +unicode(theGrades[7].decode('utf-8')) 
        #获取风向
        # [0] 当前风向 [1]明日 [2]后日
        theWinds = re.findall(r'(?<=td>).+?(?=</td>)', windPara[0])
        weadata[4] = unicode(theWinds[1].decode('utf-8'))
        #获取天气图标
        thePics = re.findall(r'/image/(..\.gif)"', picPara[0])
        weadata[5] = unicode(thePics[1].decode('utf-8'))
        weadata[8] = unicode(thePics[2].decode('utf-8'))
        weadata[11] = unicode(thePics[3].decode('utf-8'))

        listToxml(weadata, "template/wea2.xml")
        log('weather2获取天气信息成功', 'logs/running.log')
    except Exception, ex:  
        #如果错误, 记入日志
        log('严重错误:weather2获取xml文件失败')
        errlog('getWeather2', ex, sys.exc_info())
        log('weather2获取xml文件失败', 'logs/running.log')
        return False
    return True

def GetWeather8():
    url = 'http://php.weather.sina.com.cn/search.php?city='+city+'&dpc=1'
    response = urllib2.urlopen(url)
    result=response.read() #.decode('utf-8').encode("gbk")
    mathes = re.findall(r'<!-- box begin-->([\s\S]+?)<!-- box end-->',result)
    if len(mathes) == 0:
        print '没有找到'
        return
    data = []
 
    #找城市名
    cityname = re.findall(r'<div class="nav21">([\s\S]+?)<\/div>',result)
    if len(cityname) > 0:
        city = filterHtmlTags(cityname[0])
    #天气
    try:
        data.append(re.findall(r'<h2>([\s\S]+?)<\/h2>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
    #温度
    try:
        data.append(re.findall(r'<div class="w-number">([\s\S]+?)<\/div>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
    #风向
    try:
        data.append(re.findall(r'<li>风向：([\s\S]+?)<\/li>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
    #风力
    try:
        data.append(re.findall(r'<li>风力：([\s\S]+?)<\/li>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
    #紫外线
    try:
        data.append(re.findall(r'<li>紫外线：([\s\S]+?)<\/li>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
    #舒适度
    try:
        data.append(re.findall(r'<li>舒适度：([\s\S]+?)<\/li>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
    #防晒指数
    try:
        data.append(re.findall(r'<li>防晒指数：([\s\S]+?)<\/li>',mathes[0])[0])
    except IndexError:
        data.append('暂无数据')
 
    #明天
    t = []
    t.append(re.findall(r'<p>天气：([\s\S]+?)<\/p>',mathes[1])[0])
    t.append(re.findall(r'<p>温度：([\s\S]+?)<\/p>',mathes[1])[0])
    t.append(re.findall(r'<p>风力：([\s\S]+?)<\/p>',mathes[1])[0])
    data.append(t)
    #后天
    t = []
    t.append(re.findall(r'<p>天气：([\s\S]+?)<\/p>',mathes[2])[0])
    t.append(re.findall(r'<p>温度：([\s\S]+?)<\/p>',mathes[2])[0])
    t.append(re.findall(r'<p>风力：([\s\S]+?)<\/p>',mathes[2])[0])
    data.append(t)
 
    for a in range(len(data)):
        data[a] = filterHtmlTags(data[a])
 
    result =  "城市:\t%s\n----今日天气----\n天气:\t%s\n温度:\t%s\n风向:\t%s\n风力:\t%s\n紫外线:\t%s\n舒适度:\t%s\n防晒指数:\t%s\n----明日天气----\n天气:\t%s\n温度:%s\n风力:%s\n----后天天气----\n天气:%s\n温度:%s\n风力:%s\n" % (city,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7][0],data[7][1],data[7][2],data[8][0],data[8][1],data[8][2])
    print result
 
def filterHtmlTags(a):
    if isinstance(a,basestring) :
        a = re.sub(r'<[^>]+>','',a)
        a = re.sub(r'\s+','',a)
    if isinstance(a,list):
        for i in range(len(a)):
            a[i] = filterHtmlTags(a[i])
    return a
def getWeather9():
    '''
        从www.webxml.com.cn 取得天气数据(xml格式)
        直接保存为xml格式
    '''
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################
    DAQINGID = '83'
    USERID = '92dc44c3fa1341c5b1e837f0d19d3c7b'
    URL = ''.join(("http://webservice.webxml.com.cn/", 
            "WebServices/WeatherWS.asmx/", 
            "getWeather?theCityCode=", 
            DAQINGID, "&theUserID=", USERID))
    FILENAME = "template/wea9.xml"
    SOURCE = "9"
    ############################################
    try:
        # 获取网页源文件  
        sock = urllib.urlopen(URL)  
        strxml = sock.read()  
        dom=xml.dom.minidom.parseString(strxml)
        root=dom.documentElement
        #验证xml的第二个string元素是大庆, 如果是表示数据正常
        strlist = root.getElementsByTagName("string")
        if strlist[1].hasChildNodes():
            areastr=strlist[1].firstChild.data
        else:
            log('weather9获取xml文件失败')
            log(strxml)
            return False
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
            log('weather9获取天气信息成功', 'logs/running.log')
        else:
            log('weather9获取xml文件失败')
            log(strxml)
            log('weather9获取xml文件失败', 'logs/running.log')
            return False

    except Exception, ex:  
        #如果错误, 记入日志
        log('严重错误:weather9获取xml文件失败')
        errlog('getWeather9', ex, sys.exc_info())
        return False
    return True
############################################################ 
#                                                          #
#              对数据进行进一步处理部分                    #
#                                                          #
############################################################

def listToxml(weadata, FILENAME="template/wea.xml"):
    '''
    输入一个天气列表, 生成xml文件
    weadata [0]  -->   source[0]        "信息来源"
    weadata [1]  -->   weatherlist[3]   "更新时间 格式:yyyy-MM-dd HH:mm:ss"
    weadata [2]  -->   weatherlist[7]   "第一天 概况 格式:M月d日 天气概况"
    weadata [3]  -->   weatherlist[8]   "第一天 气温"  
    weadata [4]  -->   weatherlist[9]   "第一天 风力/风向"
    weadata [5]  -->   weatherlist[10]  "第一天 天气图标 1"                
    weadata [6]  -->   weatherlist[12]  "第二天 概况 格式:M月d日 天气概况"
    weadata [7]  -->   weatherlist[13]  "第二天 气温"  
    weadata [8]  -->   weatherlist[15]  "第二天 天气图标 1"                
    weadata [9]  -->   weatherlist[17]  "第三天 概况 格式:M月d日 天气概况"
    weadata [10]  -->  weatherlist[18]  "第三天 气温"  
    weadata [11] -->   weatherlist[20]  "第三天 天气图标 1"
    '''
    #相应参数:如果参数发生变化, 修改以下部分
    ############################################
    ############################################
    if len(weadata) > 0:
        data = []
        wlist = [3, 7, 8, 9, 10, 12, 13, 15, 17, 18, 20]
        i = 0
        data.append(u'<?xml version="1.0" encoding="utf-8"?>')
        data.append(u' '*4 + u'<ArrayOfString>')
        data.append(''.join((u' '*8 + u'<source>',weadata[0],u'</source>')))
        #根据上面的列表, 填充空白的string元素
        for j in range(wlist[-1] + 1):
            if wlist[i] > j:
                data.append(u' '*8 + u'<string/>')
                continue
            i += 1 
            data.append(''.join((u' '*8 + u'<string>', 
                weadata[i], u'</string>')))
        data.append(u' '*4 + u'</ArrayOfString>')

        try:
            f = open(FILENAME, 'w')
            for line in data:
                line += '\n' 
                f.write(line.encode('utf-8'))
            f.close()
        except Exception, ex:  
            #如果错误, 记入日志
            print ex
            print sys.exc_info()

def xmlToHtml(xmlfilename):
    '''
    打开xml文件, 根据TEMPFILENAME模板替换相应字段
    ${SOURCE}   数据来源
    ${DAY0}     当天日期
    ${MAXTEM0}  当日最高温度
    ${MINTEM0}  当日最低温度
    ${WEATHER0} 当日天气
    ${WIND0}    当日风力
    ${LAPIC0}   当日天气图标(大)
    ${PIC0}     当日天气图标
    ${TEM0}     当日最高温度至最低温度

    ${DAY1}     次日日期
    ${TEM1}     次日最高温度至最低温度
    ${PIC1}     次日天气图标
    
    ${DAY2}     第三天日期
    ${TEM2}     第三最高温度至最低温度
    ${PIC2}     第三日天气图标
    '''
    #相应参数:如果网址参数发生变化, 修改以下部分
    ############################################
    TEMPFILENAME = "template/temp.htm"
    RESULTFILENAME ="html/index.htm" 
    ############################################

    #读入天气预报xml文件
    dom=xml.dom.minidom.parse(xmlfilename)
    root=dom.documentElement
    sourcelist = root.getElementsByTagName('source')[0]
    source = getText(sourcelist)
    strlist=root.getElementsByTagName('string')
    weatherlist = []
    for eachstr in strlist:
        weatherlist.append(getText(eachstr))
        
    #写入html文件
    filesou = open(TEMPFILENAME, "r")
    filedes = open(RESULTFILENAME, "w")
    for eachline in filesou:
        s  = Template(eachline).substitute(
            SOURCE = source.encode('gb2312'), 
            MAXTEM0=diffTem(weatherlist[8])[1].encode('gb2312'),  
            MINTEM0=diffTem(weatherlist[8])[0].encode('gb2312'), 
            WEATHER0 =diffDayAndWeather(weatherlist[7]
                )[2] .encode('gb2312'), 
            WIND0 =insertBr(weatherlist[9]).encode('gb2312'), 
            LONGDAY0 =''.join((diffDayAndWeather(weatherlist[7])[0],
               diffDayAndWeather(weatherlist[7])[1],'&nbsp;&nbsp;', 
               diffDayAndWeather(weatherlist[7])[3], )
                ).encode('gb2312'), 
            DAY0 =diffDayAndWeather(weatherlist[7])[1].encode('gb2312'), 
            LAPIC0 = "".join(("../image/a", 
                transPicId(weatherlist[10]))).encode('gb2312'),
            PIC0 = "".join(("../image/b", 
                transPicId(weatherlist[10]))).encode('gb2312'),
            PIC1 = "".join(("../image/b", 
                transPicId(weatherlist[15]))).encode('gb2312'),
            PIC2 = "".join(("../image/b", 
                transPicId(weatherlist[20]))).encode('gb2312'),
            DAY1 =diffDayAndWeather(weatherlist[12])[1].encode('gb2312'), 
            DAY2 =diffDayAndWeather(weatherlist[17])[1].encode('gb2312'), 
            TEM0 = weatherlist[8].replace("/", u"至").encode('gb2312'), 
            TEM1 = weatherlist[13].replace("/", u"至").encode('gb2312'), 
            TEM2 = weatherlist[18].replace("/", u"至").encode('gb2312'), 
            )
        filedes.write('%s\n' % s)

    filesou.close()
    filedes.flush()
    filedes.close()
    return weatherlist[3].encode('utf-8')

def insertBr(str):
    '''
    输入超长字符串自动断行
    '''
    resstr = str.strip()
    if len(resstr)>16:
        resstr = resstr[0:16]
    if len(resstr)>5:
        resstr = resstr[:len(resstr)//2] + "<br>" +resstr[len(resstr)//2:] 
    return resstr
def transPicId(souname):
    '''
    转换不同网站的图片名称, 翻译成本地的各种图片名称
    0:www.webxml.com.cn
    1:www.weather.com.cn
    2:tool.115.com
    3:www.nmc.gov.cn
    4:tg.360.cn
    '''
    name=souname.split(".")[0]
    while not name.isdigit():
        name = name[1:]
    num = int(name)
    resname = "".join((str(num), ".png"))
    return (resname)

def diffDayAndWeather(temstr):
    '''
    输入一个日期天气的字符串, 返回一个日期天气的列表
    例子 输入 '1月26日 多云',  返回 ['1月', '26日','多云', '星期三'] 
    '''
    restem0 = temstr.split(" ")
    restem1 = restem0[0].split(u"月")
    month = int(restem1[0])
    day = int(restem1[1][0:-1])
    year = datetime.date.today().year
    week = datetime.date(year, month, day).isoweekday()
    weekdict = {1:u'一', 2:u'二', 3:u'三', 
            4:u'四', 5:u'五', 6:u'六',7:u'日'}
    restem1[0]=restem1[0] + u"月"
    return ([restem1[0], restem1[1], restem0[1], u'星期' + weekdict[week]])

def diffTem(temstr):
    '''
    输入一个最低温度最高温度的字符串, 返回一个最低最高温度的列表
    例子 输入 -28℃/-18℃ 返回 [-28℃, -18℃]
    '''
    restem = temstr.split("/")
    return (restem)

def getText(node):
    '''
    读取一个只包含text元素的node值, 返回其中的内容
    '''
    rc = ""
    
    for eachnode in node.childNodes:
        if eachnode.nodeType == eachnode.TEXT_NODE:
            rc = rc + eachnode.data
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
    '''美化xml 文件, 用于缩进
     Copy child list because it will change soon
    '''
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

def errlog(modelname, ex, exc_info):
    '''
    把错误信息写入日志文件
    '''
    log(modelname + '模块发生错误:')
    log(unicode(ex)) 
    log(unicode(exc_info))

def log(str, filename="logs/weatherlog.txt"):
    '''
    把字符串写入日志文件
    '''
    #根据分类从配置文件选择合适的目标文件写入字符串
    nowtimestr = unicode(datetime.datetime.now().strftime(
        "[%Y-%m-%d %H:%M:%S]"),'utf-8')
    f = open(filename, 'a')
    if not isinstance(str,unicode):
        str = unicode(str,'utf-8')
    desstr = "%s  %s\n" % (nowtimestr, str)
    byte_out = desstr.encode('utf-8')
    f.write(byte_out)
    f.close()
    return True
############################################################ 
#                                                          #
#                 发送邮件                                 #
#                                                          #
############################################################

def sendsimplemail (address, sub, mailstr ):
    '''
    发送不带附件的邮件。参数说明:
    address 邮件的目的地址[列表] 
    例如:['one@163.com','two@163.com', ] 
    sub 邮件的主题 
    mailstr 邮件的内容
    '''
    mailuser = 'test2011'
    mailpwd = 'password2011'

    msg = MIMEText(mailstr, _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = '系统监控服务中心<test2011@126.com>'
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.126.com')
        smtp.login(mailuser, mailpwd)
        smtp.sendmail('test2011@126.com',
                address, msg.as_string())
        smtp.close()
    except Exception, ex:
        errlog('发送邮件错误', ex, sys.exc_info())


def sendattachmail (address, sub, mailstr):

    '''
    发送带附件的邮件。参数说明:
    address 邮件的目的地址[列表] 
    例如:['one@163.com','two@163.com', ] 
    sub 邮件的主题 
    mailstr 邮件的内容
    '''

    mailuser = 'test2011'
    mailpwd = 'password2011'

    msg = MIMEMultipart()
    att = MIMEText(open(r'html/index.htm', 'rb').read(),
            'base64', 'utf-8')
    att['content-type'] = 'application/octet-stream'
    att['content-disposition'] = 'attachment;filename="index.htm"'
    msg.attach(att)

    body = MIMEText(mailstr, _charset='utf-8')
    msg.attach(body)

    msg['to'] = address
    msg['From'] = '系统监控服务中心<test2011@126.com>'
    msg['subject'] = sub

    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.126.com')
        smtp.login(mailuser, mailpwd)
        smtp.sendmail('test2011@126.com',
                address, msg.as_string())
        smtp.close()
    except Exception, ex:
        errlog('发送带附件邮件错误', ex, sys.exc_info())
   

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

def main():
    '''
    调用主程序, 生成html页面
    '''
    getWeather2()

if __name__=='__main__':

    testmain()
    #main()


