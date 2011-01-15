#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月15日 19时24分20秒


"""
构造freemind格式XML文件
"""

__revision__ = '0.1'

import pickle
#
## 生成用于用户数统计的html 文件
#
def outputhtml():
    #写入html文件头
    htmlhead ='''<?xml version="1.0" encoding="utf-8"?><?xml-stylesheet href="../treestyles.css" type="text/css"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="fi" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" >
	<title>大故障用户数量统计</title>
	<link rel="stylesheet" href="../javaver.html_files/treestyles.css" type="text/css"/>
	<script type="text/javascript" src="../javaver.html_files/marktree.js" ></script>
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
    ff = open(CWD + "/dbase", 'r')
    buildlist = pickle.load(ff)
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



