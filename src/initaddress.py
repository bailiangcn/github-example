#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011-01-20 01:16:05


"""初始化xml文件，生成唯一id
"""

__revision__ = '0.1'


import xml.dom.minidom
import codecs

def initarea():
    '''
        给区域area.xml排顺序id
    '''
    filename = "../addressdata/area.xml"
    domarea=xml.dom.minidom.parse(filename)
    rootarea=domarea.documentElement
    reglist=rootarea.getElementsByTagName('regional')
    for reg in reglist: #区域nodes
        print reg.getElementsByTagName("name")[0].firstChild.data.encode("utf-8")
        print reg.getElementsByTagName("datafile")[0].firstChild.data.encode("utf-8")
        print reg.getElementsByTagName("valid")[0].firstChild.data.encode("utf-8")
        regid = reg.getElementsByTagName("id")[0]
        text = domarea.createTextNode("2000")
        print "has id :%s" % (regid.hasChildNodes())
        if regid.hasChildNodes():
            regid.firstChild.data = "1999"
        else:
            regid.appendChild(text)

    f=file(filename,'w')
    writer=codecs.lookup('utf-8')[3](f)
    domarea.writexml(writer,encoding='utf-8')
    writer.close 
    return 1

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


