#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月22日 13时27分39秒


"""初始化xml文件，生成唯一id
"""

__revision__ = '0.1'


import xml.dom.minidom
import codecs

def initarea():
    '''
        给区域area.xml排顺序id
    '''
    areafilename = "../addressdata/area.xml"
    domarea=xml.dom.minidom.parse(areafilename)
    rootarea=domarea.documentElement
    reglist=rootarea.getElementsByTagName('regional')
    regionalnum = 0
    housenum = 0
    for reg in reglist: #区域nodes
        regionalnum += 1 
        #给各个区域进行编码id = regionalnum
        regid = reg.getElementsByTagName("id")[0]
        text = domarea.createTextNode(str(regionalnum))
        if regid.hasChildNodes():
            regid.firstChild.data = str(regionalnum)
        else:
            regid.appendChild(text)
        communityfilename = reg.getElementsByTagName("datafile"
                )[0].firstChild.data.encode("utf-8")
        commfilename = ''.join(("../addressdata/", 
            communityfilename, ".xml"))
        housenum = inithouse(commfilename, housenum)

    f=file(areafilename,'w')
    writer=codecs.lookup('utf-8')[3](f)
    domarea.writexml(writer,encoding='utf-8')
    writer.close 
    f.close
    return 1

def inithouse(commfilename, housenum):
    '''
        根据输入的filename进行楼号Id的重新编排
    '''
    domcomm=xml.dom.minidom.parse(commfilename)
    rootcomm=domcomm.documentElement
    commlist=rootcomm.getElementsByTagName('community')
    commnum = 0
    for comm in commlist:
        commnum += 1 
        houselist = comm.getElementsByTagName('house')
        for house in houselist:
            housenum += 1
            houseidlist = house.getElementsByTagName('id')
            idtext = domcomm.createTextNode(str(housenum))
            idelement = domcomm.createElement("id")
            idelement.appendChild(idtext)
            if houseidlist.length>0:  #如果有id元素
                houseid = houseidlist[0]
                if houseid.hasChildNodes():
                    houseid.firstChild.data = str(housenum)
                else:
                    houseid.appendChild(idtext)
            else:   #如果没有Id元素
                house.appendChild(idelement)

    #保存xml结果到文件
    #遍历nodes，删除所有空格元素
    domcopy = domcomm.cloneNode(True)
    clearspace(domcopy, domcopy.documentElement)
    Indent(domcopy, domcopy.documentElement)
    f=file(commfilename,'w')
    writer=codecs.lookup('utf-8')[3](f)
    domcopy.writexml(writer,encoding='utf-8')
    writer.close 

    return housenum

def clearspace(dom, node):
    '''
    删除xml文件中的所有空行
    '''
    children = node.childNodes[:]
    if children:
        for nd in children:
            if nd.nodeType == 3 and nd.data.isspace(): 
                node.removeChild(nd)
            else:
                clearspace(dom,nd)

def Indent(dom, node, indent = 0):
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

    from testinitaddress import simpleTest

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(simpleTest)
    result = unittest.TextTestRunner(verbosity=3).run(suite)

if __name__=='__main__':

    testmain()


