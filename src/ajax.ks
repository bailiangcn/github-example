#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月23日 13时41分06秒


"""
根据提交的楼号、服务组号对各组进行分工

"""

__revision__ = '0.1'

import os
import xml.dom.minidom
import codecs
initaddress= Import("initaddress")
        
def initser():
    '''
    把所有楼房的服务号置空
    '''
    areafilename = os.path.abspath(REL("../addressdata/area.xml"))
    domarea=xml.dom.minidom.parse(areafilename)
    regionallist = domarea.documentElement.getElementsByTagName('regional')
    for region in regionallist:
        filename = region.getElementsByTagName(
                'datafile')[0].firstChild.data
        regionfilename = os.path.abspath(REL(''.join(("../addressdata/"
                , filename, ".xml"))))
        #遍历各个文件
        domcomm=xml.dom.minidom.parse(regionfilename)
        rootcomm=domcomm.documentElement
        houseserlist = rootcomm.getElementsByTagName('service')
        #删除所有service文本元素
        for eachser in houseserlist:
            for node in eachser.childNodes:
                eachser.removeChild(eachser.firstChild)

        #保存xml结果到文件
        #遍历nodes，删除所有空格元素
        domcopy = domcomm.cloneNode(True)
        initaddress.clearspace(domcopy, domcopy.documentElement)
        initaddress.Indent(domcopy, domcopy.documentElement)
        f=file(regionfilename,'w')
        writer=codecs.lookup('utf-8')[3](f)
        domcopy.writexml(writer,encoding='utf-8')
        writer.close 

    print "ok"

def changeserid(filename, housedict):
    '''
    根据输入的字典对{houseid:serid}在filename文件
    当中查询更改相应的服务号
    '''
    #打开一个文件, 生成dom树
    domcomm=xml.dom.minidom.parse(filename)
    rootcomm=domcomm.documentElement
    houseidlist = rootcomm.getElementsByTagName('id')
    findone = False
    for eachhouse in housedict:
        houseid = eachhouse
        serid = housedict[houseid]
        for hid in houseidlist:
            if hid.firstChild.data == houseid:
                findone = True
                serelenode = hid.parentNode.getElementsByTagName('service')[0]
                sertext = domcomm.createTextNode(serid)
                if serelenode.hasChildNodes():
                    serelenode.firstChild.data = serid
                else:
                    serelenode.appendChild(sertext)
    if findone:
        f=file(filename,'w')
        writer=codecs.lookup('utf-8')[3](f)
        domcomm.writexml(writer,encoding='utf-8')
        writer.close 
        f.close

def ajax(xmlstr):
    '''
        修改各个楼号的服务组id
        示例xml输入
        xmlstr =('<root>' 
        '<house id="1" regid="1" serid="1"/>'
        '<house id="4" regid="3" serid="1"/>'
        '</root>')
    '''
    #RESPONSE['Content-Type']='text/plain' 
    areafilename = os.path.abspath(REL("../addressdata/area.xml"))
    domarea=xml.dom.minidom.parse(areafilename)
    regionallist = domarea.documentElement.getElementsByTagName('regional')

    dom = xml.dom.minidom.parseString(xmlstr)
    houselist = dom.documentElement.getElementsByTagName('house')
    for region in regionallist:
        housedict = {}
        regionid = region.getElementsByTagName('id')[0].firstChild.data
        for house in houselist:
            regid = house.getAttribute('regid')
            if regionid != regid:
                continue
            else:
                houseid = house.getAttribute('id')
                serid = house.getAttribute('serid')
                housedict.update({houseid:serid})
        if len(housedict)>0: 
            filename = region.getElementsByTagName(
                    'datafile')[0].firstChild.data
            regionfilename = os.path.abspath(REL(''.join(("../addressdata/"
                    , filename, ".xml"))))
            changeserid(regionfilename, housedict)
    print "ok"



#
##自动调用测试用例，请输入测试用例名
#
def testmain():
    import unittest
    import sys
    import os

    sys.path.append(os.curdir)
    sys.path.append(os.path.join(os.curdir, 'tests'))

    from testsajax import simpleTest

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(simpleTest)
    result = unittest.TextTestRunner(verbosity=3).run(suite)

if __name__=='__main__':

    testmain()


