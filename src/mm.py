#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月15日 10时46分58秒


"""
构造freemind格式XML文件
"""

__revision__ = '0.1'

import pickle

#
## 转换中文为mm编码格式
#
def transcode(src):
    res= ''
    temsrc = src
    if isinstance(src, str):
        temsrc = unicode(src, 'utf-8')
    for i in temsrc:
        tempi = repr(i)
        a = ord(i)
        if a ==  10:
            s= '&#xa;'
        else:
            if len(tempi) > 4:
                s  = '&#x' + tempi[4:-1] + ';'
            else:
                s  = i
        res  += s
    return res

#
## 读取base文件，构建mm文件
#
def makemm():
    "构造mm 文件"
    #写入mm文件头
    filename  = "mytest.mm" 
    fp = open(filename, 'w')
    mmhead = ('<map version="0.8.1">\n' + 
            '<!-- To view this file, download free mind mapping ' + 
            'software FreeMind from http://freemind.sourceforge.net -->\n' +
            '<node ID="A01" TEXT="' + transcode('前端') + '">\n' )
    fp.write(mmhead)
    #打开豫先存储的楼区域信息
    buildlist = pickle.load(open('dbase', 'r'))
    loopnum = len(buildlist)
    #loopnum = 9     #调试用，之后删除
    oldregion = ''
    oldcommunity = ''
    oldbuildid = ''
    regionnum = 0 
    communitynum = 0
    buildingnum = 0
    for i in  range(loopnum):
        region = buildlist[i][0]     #区域
        community = buildlist[i][1]  #小区
        building = buildlist[i][2]   #楼号
        buildid = buildlist[i][3]    #楼号id
        capacity = buildlist[i][4]   #用户数
        nodestr = ''
        if region != oldregion: 
            if regionnum > 0:
                nodestr = '</node>\n</node>\n</node>\n'
            else:
                nodestr = ''
            nodestr  += ('<node FOLDED="true" ID="B' + str(regionnum) + '" POSITION="right" TEXT="' + 
                    transcode(region)  + '">\n')
            regionnum += 1
            communitynum = 0
            buildingnum = 0
            oldregion = region
            fp.write(nodestr)

        if community != oldcommunity:
            if communitynum > 0:
                nodestr = '</node>\n</node>\n'
            else:
                nodestr = ''
            nodestr  += ('<node FOLDED="true" ID="C' + str(communitynum) + 
                    '" POSITION="right" TEXT="' + transcode(community) + '">\n')
            communitynum += 1
            buildingnum = 0
            oldcommunity = community
            fp.write(nodestr)

        if buildingnum > 0:
            nodestr = '</node>\n'
        else:
            nodestr = ''
        nodestr  += ('<node ID="H' + str(buildingnum) + 
                '" POSITION="right" TEXT="' + transcode(building) + '">\n' +
                '<hook NAME="accessories/plugins/NodeNote.properties">\n<text>'  + 
                transcode('id=' + buildid + '\nnum=')  + str(capacity)+  '</text>\n</hook>')
        buildingnum += 1
        oldbuildid = buildid
        fp.write(nodestr)
 
 
        #print region, community, building, buildid, capacity
        #print repr(region)
    fp.write('</node>\n</node>\n</node>\n</node>\n</map>\n')
    fp.close()


#
## 生成用于用户数统计的html 文件
#
def makehtml():
    #写入html文件头
    filename  = "myhtml.html" 
    fp = open(filename, 'w')
    htmlhead ='''<?xml version="1.0" encoding="utf-8"?><?xml-stylesheet href="treestyles.css" type="text/css"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="fi" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" >
	<title>大故障用户数量统计</title>
	<link rel="stylesheet" href="javaver.html_files/treestyles.css" type="text/css"/>
	<script type="text/javascript" src="javaver.html_files/marktree.js" ></script>
</head>

<body>
	<div class="basetop">
		<input type="button"  value="统计" onclick="countuser()" />
		<input type="button" name="reset" value="重置"  onclick="resetAll()" />
		<input type="text" id="countnum" value="0" size="5" maxlength="8" readonly="readonly" />
		<a href="#" onclick="expandAll(document.getElementById('base'))"> 展开</a>
		 - <a href="#" onclick="collapseAll(document.getElementById('base'))"> 折叠</a>
	</div>
	<div id="base" class="basetext">
		 <ul>
			 <li class="col" style="" id="A0">
				 <span style="">前端</span> 
                <ul class="subexp"> 
    <!--下面由软件自动生成  -->
    '''
    fp.write(htmlhead)
    #打开豫先存储的楼区域信息
    buildlist = pickle.load(open('dbase', 'r'))
    loopnum = len(buildlist)
    #loopnum = 290     #调试用，之后删除
    oldregion = ''
    oldcommunity = ''
    oldbuildid = ''
    regionnum = 0 
    communitynum = 0
    communityid = ''
    buildingnum = 0
    for i in  range(loopnum):
        region = buildlist[i][0]     #区域
        community = buildlist[i][1]  #小区
        building = buildlist[i][2]   #楼号
        buildid = buildlist[i][3]    #楼号id
        capacity = buildlist[i][4]   #用户数
        nodestr = ''
        if region != oldregion: 
            if regionnum > 0:
                nodestr = '</ul></li></ul></li>'
            else:
                nodestr = ''
            str1 = '\n\n<!--    新的区域开始   -->\n\n <li class="exp" style="" id="B'
            str2 = '"> <span style="">'
            str3 = '</span>\n<ul class="sub">\n'
            nodestr   += str1 +str(i)  + str2 + region.encode('utf-8') + str3
            regionnum += 1
            communitynum = 0
            buildingnum = 0
            oldregion = region
            fp.write(nodestr)

        if community != oldcommunity:
            communityid = str(i)
            if communitynum > 0:
                nodestr = '</ul>\n</li>\n'
            else:
                nodestr = ''
            str1 = '\n<!--    新的小区开始   -->\n<li class="exp" style="" id="C'
            str2 = '"> \n\t<input type="checkbox" name="c000" value="cb'
            str3 = '" onchange="setcheck(this.value,this.checked)" class="mycheck" />\n\t<span style="">'
            str4 = '</span>\n\t<ul class="sub">'
            nodestr   += str1 +str(i)  + str2 + communityid + str3 + community.encode('utf-8') + str4
            communitynum += 1
            buildingnum = 0
            oldcommunity = community
            fp.write(nodestr)

        str1 = '<input type="checkbox" name="cb'  + communityid
        str2 = '" value="' + str(capacity) + '" class="mycheck" id="build" onchange="checkchang(this)"/><span style="">'
        str3 = '&nbsp;&nbsp;&nbsp;&nbsp;</span>\n'
        
        nodestr  = str1 + str2 + building + str3
        buildingnum += 1
        oldbuildid = buildid
        fp.write(nodestr)
 
# 
 #       #print region, community, building, buildid, capacity
 #       #print repr(region)
    footstr = ' </li> </ul></li> </ul>  </li> </ul> </div> </body> </html>'
    fp.write(footstr)
    fp.close()

#
## 生成用于用户数统计的html 文件
#
def outputhtml():
    #写入html文件头
    htmlhead ='''<?xml version="1.0" encoding="utf-8"?><?xml-stylesheet href="treestyles.css" type="text/css"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="fi" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" >
	<title>大故障用户数量统计</title>
	<link rel="stylesheet" href="javaver.html_files/treestyles.css" type="text/css"/>
	<script type="text/javascript" src="javaver.html_files/marktree.js" ></script>
</head>

<body>
	<div class="basetop">
		<input type="button"  value="统计" onclick="countuser()" />
		<input type="button" name="reset" value="重置"  onclick="resetAll()" />
		<input type="text" id="countnum" value="0" size="5" maxlength="8" readonly="readonly" />
		<a href="#" onclick="expandAll(document.getElementById('base'))"> 展开</a>
		 - <a href="#" onclick="collapseAll(document.getElementById('base'))"> 折叠</a>
	</div>
	<div id="base" class="basetext">
		 <ul>
			 <li class="col" style="" id="A0">
				 <span style="">前端</span> 
                <ul class="subexp"> 
    <!--下面由软件自动生成  -->
    '''
    print "%s" % htmlhead
    #打开豫先存储的楼区域信息
    buildlist = pickle.load(open('dbase', 'r'))
    loopnum = len(buildlist)
    #loopnum = 290     #调试用，之后删除
    oldregion = ''
    oldcommunity = ''
    oldbuildid = ''
    regionnum = 0 
    communitynum = 0
    communityid = ''
    buildingnum = 0
    for i in  range(loopnum):
        region = buildlist[i][0]     #区域
        community = buildlist[i][1]  #小区
        building = buildlist[i][2]   #楼号
        buildid = buildlist[i][3]    #楼号id
        capacity = buildlist[i][4]   #用户数
        nodestr = ''
        if region != oldregion: 
            if regionnum > 0:
                nodestr = '</ul></li></ul></li>'
            else:
                nodestr = ''
            str1 = '\n\n<!--    新的区域开始   -->\n\n <li class="exp" style="" id="B'
            str2 = '"> <span style="">'
            str3 = '</span>\n<ul class="sub">\n'
            nodestr   += str1 +str(i)  + str2 + region.encode('utf-8') + str3
            regionnum += 1
            communitynum = 0
            buildingnum = 0
            oldregion = region
            print "%s" % nodestr

        if community != oldcommunity:
            communityid = str(i)
            if communitynum > 0:
                nodestr = '</ul>\n</li>\n'
            else:
                nodestr = ''
            str1 = '\n<!--    新的小区开始   -->\n<li class="exp" style="" id="C'
            str2 = '"> \n\t<input type="checkbox" name="c000" value="cb'
            str3 = '" onchange="setcheck(this.value,this.checked)" class="mycheck" />\n\t<span style="">'
            str4 = '</span>\n\t<ul class="sub">'
            nodestr   += str1 +str(i)  + str2 + communityid + str3 + community.encode('utf-8') + str4
            communitynum += 1
            buildingnum = 0
            oldcommunity = community
            print "%s" % nodestr

        str1 = '<input type="checkbox" name="cb'  + communityid
        str2 = '" value="' + str(capacity) + '" class="mycheck" id="build" onchange="checkchang(this)"/><span style="">'
        str3 = '&nbsp;&nbsp;&nbsp;&nbsp;</span>\n'
        
        nodestr  = str1 + str2 + building + str3
        buildingnum += 1
        oldbuildid = buildid
        print "%s" % nodestr
 
# 
 #       #print region, community, building, buildid, capacity
 #       #print repr(region)
    footstr = ' </li> </ul></li> </ul>  </li> </ul> </div> </body> </html>'
    print "%s" % footstr

    



#
##自动调用测试用例，请输入测试用例名
#
def testmain():
    import unittest
    import sys
    import os

    sys.path.append(os.curdir)
    sys.path.append(os.path.join(os.curdir, 'tests'))

    from testmm import simpleTest

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(simpleTest)
    result = unittest.TextTestRunner(verbosity=3).run(suite)

if __name__=='__main__':

    testmain()

outputhtml()


