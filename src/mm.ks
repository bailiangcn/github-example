#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月15日 19时24分20秒
"""
构造freemind格式XML文件
"""
__revision__ = '0.1'

from xml.dom.minidom import parse

#
## 生成用于用户数统计的html 文件
#
def outputhtml():
    #写入html文件头
    htmlhead1 ='''<?xml version="1.0" encoding="utf-8"?>
    <?xml-stylesheet href="../treestyles.css" type="text/css"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xml:lang="fi" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" >
        <title>楼区派工</title>
        <link rel="stylesheet" href="../javaver.html_files/treestyles.css"
            type="text/css"/>
        <script type="text/javascript" src="../javaver.html_files/marktree.js" >
        </script>
    </head>
    <body>
        <div class="basetop">'''

            #<input type="button"  value="组1" serid ="1" onclick="countuser()" />
    htmlhead2='''<input type="button" name="reset" value="重置"  onclick="resetAll()" />
            <input type="text" id="countnum" value="0" size="5" 
                maxlength="8" readonly="readonly" />
            <a href="#" onclick="expandAll(document.getElementById('base'))"> 展开</a>
             - <a href="#" onclick="collapseAll(document.getElementById('base'))">
                 折叠</a>
        </div>
        <div id="base" class="basetext">
             <ul>
                 <li class="col" style="" id="A0">
                     <span style="">前端</span> 
                     <ul class="subexp"> 
    <!--下面由软件自动生成  -->
    '''
    print "%s%s" % (htmlhead1 , htmlhead2)
    #打开豫先存储的楼区域信息

    
    regionnum = 0
    communitynum = 0
    housenum = 0
    
    dom1 = parse(REL("../addressdata/area.xml"))
    root = dom1.documentElement
    childs= root.getElementsByTagName("regional")
    #RESPONSE['Content-Type']='text/plain'
    for child in childs:
        if child.getElementsByTagName("valid")[0].firstChild.data == "1":
            nodestr = ''
            #如果该区域有效, <valid>==1
            regionalname = child.getElementsByTagName("name")[0].firstChild.data
            regionalfilename = child.getElementsByTagName("datafile")[0].firstChild.data
            #打开相应区域的xml文件
            filename = u"../addressdata/"+ regionalfilename + u".xml"
            dom2 = parse(REL(filename))
            root2 = dom2.documentElement
            childs2 = root2.getElementsByTagName("community")

            str1 = '\n\n<!--    新的区域开始   -->\n\n <li class="exp" style="" id="B'
            str2 = '"> <span style="">'
            str3 = '</span>\n<ul class="sub">\n'
            nodestr   += str1 +str(regionnum)  + str2 + regionalname.encode('utf-8') + str3
            regionnum += 1 
            print nodestr
            for child2 in childs2: #取小区
                communityname = child2.getAttribute("name")
                nodestr = ''

                str1 = '\n<!--    新的小区开始   -->\n<li class="exp" style="" id="C'
                str2 = '"> \n\t<input type="checkbox" name="c000" value="cb'
                str3 = ('" onchange="setcheck(this.value,this.checked)" class="mycheck" '
                        '/>\n\t<span style="">')
                str4 = '</span>\n\t<ul class="sub">'
                nodestr   += str1 +str(communitynum) + str2 + str(communitynum
                        ) + str3 + communityname.encode('utf-8') + str4
                print nodestr
                houses= child2.getElementsByTagName("house")
                for house in houses: #取每栋楼
                    housename  = house.getElementsByTagName("number")[0].firstChild.data
                    if house.getElementsByTagName("service")[0].childNodes.length >0:
                        houseservice = house.getElementsByTagName(
                                "service")[0].firstChild.data
                    else:
                        houseservice = ''

                    str1 = '<input type="checkbox" name="cb'  + str(communitynum)
                    str2 = ('" value="' ' houseservice ' 
                            '" class="mycheck" id="build" onchange="checkchang(this)"'
                            '/>\n\t<span style="">')
                    str3 = '&nbsp;&nbsp;&nbsp;&nbsp;</span>\n'
                    nodestr  = str1 + str2 + housename + str3

                    print nodestr
                print "</ul> </li>"

            communitynum += 1 
            print "</ul> </li>"
    footstr = ' </li> </ul></li> </ul>  </li> </ul> </div> </body> </html>'
    print "%s" % footstr

    return

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
    #testmain()
    outputhtml()
