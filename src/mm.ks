#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月15日 19时24分20秒
"""
通过xml文件构造地址，用于给各楼进行分工
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
        <script type="text/javascript" 
        src="../javaver.html_files/marktree.js" >
        </script>
    </head>
    <body>
        <div class="basetop"><input type="checkbox" name="showall" />
        <span id="showall">显示所有组</span>
    '''

    htmlhead2='''
            <a href="#" onclick="resetAll()" > 重置</a> - <a href="#" 
            <a href="#" onclick="expandAll(document.getElementById('base'))" >
            展开</a> - <a href="#" 
            onclick="collapseAll(document.getElementById('base'))"
            > 折叠</a>
        </div>
        <div id="base" class="basetext">
             <ul>
                 <li class="col" style="" id="A0">
                     <span style="">前端</span> 
                     <ul class="subexp"> 
    <!--下面由软件自动生成  -->
    '''

    #读入有多少个组xml
    print "%s" % htmlhead1 
    #打开豫先存储的楼区域信息
    #RESPONSE['Content-Type']='text/plain'
    dom0 = parse(REL("../addressdata/service.xml"))
    root = dom0.documentElement
    childs= root.getElementsByTagName("team")
    str1 = '<input type="button"  value="组'
    str2 = '" serid ="'
    str3 = '" id="serid'
    str4 = '" onclick="dividework(this)" />'

    for child in childs:
        serid = child.getAttribute("id").encode("utf-8")
        print "%s%s%s%s%s%s%s\r\n" % (str1,  
                 serid,str2, serid, str3, serid, str4)
    print "%s" % htmlhead2 

    
    regionnum = 0
    communitynum = 0
    housenum = 0
    
    dom1 = parse(REL("../addressdata/area.xml"))
    root = dom1.documentElement
    childs= root.getElementsByTagName("regional")
    for child in childs:
        if child.getElementsByTagName("valid")[0].firstChild.data == "1":
            nodestr = ''
            #如果该区域有效, <valid>==1
            regionalname = child.getElementsByTagName("name"
                    )[0].firstChild.data
            regionalfilename = child.getElementsByTagName("datafile"
                    )[0].firstChild.data
            #打开相应区域的xml文件
            filename = u"../addressdata/"+ regionalfilename + u".xml"
            dom2 = parse(REL(filename))
            root2 = dom2.documentElement
            childs2 = root2.getElementsByTagName("community")

            str1 = ('\n\n<!--    新的区域开始   -->\n\n '
                    '<li class="exp" style="" id="B')
            str2 = '"> <span style="">'
            str3 = '</span>\n<ul class="sub">\n'
            nodestr += str1 +str(regionnum) + str2 + regionalname.encode(
                    'utf-8') + str3
            regionnum += 1 
            print nodestr
            for child2 in childs2: #取小区
                communityname = child2.getAttribute("name")
                nodestr = ''

                str1 = ('\n<!--    新的小区开始   -->\n'
                    '<li class="exp" style="" id="C')
                str2 = '"> \n\t<input type="checkbox" name="c000" value="cb'
                str3 = ('" onchange="setcheck(this.value,this.checked)" '
                    'class="mycheck" />\n\t<span style="">')
                str4 = '</span>\n\t<ul class="sub">'
                nodestr   += ''.join((str1, str(communitynum), str2, 
                    str(communitynum), str3, communityname.encode('utf-8'), str4))
                print nodestr
                houses= child2.getElementsByTagName("house")
                for house in houses: #取每栋楼
                    housename  = house.getElementsByTagName("number"
                            )[0].firstChild.data
                    if house.getElementsByTagName("service"
                            )[0].childNodes.length >0:
                        houseservice = house.getElementsByTagName(
                                "service")[0].firstChild.data
                    else:
                        houseservice = ''

                    str1 = ('<span style=display:inline-block>'
                            '<input type="checkbox" name="cb' )
                    str2 = str(communitynum) + '" value="'    
                    str3 =  ('" class="mycheck" id="build')
                    str4 = ('" onchange="checkchang(this)"'
                            '/>\n\t<span style="">')
                    str5 = '</span><span id="house'
                    str6 = '">&nbsp;&nbsp;&nbsp;&nbsp;</span></span>\n'
                    nodestr = ''.join((str1,str2,houseservice,
                        str3,str(housenum), str4, housename, str5, 
                        str(housenum), str6))

                    print nodestr
                    housenum  += 1 
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
