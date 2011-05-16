#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# vim:foldmethod=indent:

"""
    用于过滤ca产生的xml文件
"""
__revision__ = '0.1'

import os  
import sys  
import xml.dom.minidom

if __name__=='__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print "开始读取文件:" + filename
        try:
            f=open(filename)
            context=f.read()
        except:
            print "文件读取错误"
        # 替换xml文件编码为utf-8
        newcontext=context.replace('encoding="GB2312"','encoding="utf-8"',1)
        dom=xml.dom.minidom.parseString(newcontext)
        root=dom.documentElement
        # 定义三个变量分别代表值等于 0 1 2
        str_0=''
        str_1=''
        str_2=''
        for node in root.childNodes:
            if node.nodeType == 1:
                # Open==0
                if node.getAttribute('Open') == u'0':
                    str_0 += node.toxml() +'\n'
                # Open==2
                if node.getAttribute('Open') == u'2':
                    str_2 += node.toxml() +'\n'
                # Open==1
                if node.getAttribute('Open') == u'1' :
                    for cnode in node.childNodes:
                        # ProductID==11 and Type==0
                        #if cnode.nodeType == 1 and cnode.getAttribute( 'ProductID'
                        #)==u'11' and cnode.getAttribute('Type')==u'0':
                        if cnode.nodeType == 1 and cnode.getAttribute('Type')==u'0':
                                str_1 += node.toxml() +'\n'
                                break

        strbegin='<?xml version="1.0" encoding="utf-8"?>\n<Info>\n'
        strcom0='<!-- Open==0 -->\n'
        strcom1='<!-- Open==1 -->\n'
        strcom2='<!-- Open==2 -->\n'
        strend='</Info>'
        strfoot='<!-- vim:foldmethod=indent: -->'
        resstr=''.join([strbegin,strcom0,str_0,strcom2,str_2,strcom1,str_1,strend,strfoot])
        newdom=xml.dom.minidom.parseString(resstr)
        newstr=newdom.toprettyxml()
        outstr=''
        i=0
        indentstr=''
        for eachline in newstr.split("\n"):
            if eachline.split():
                i+=1
                if i>2:
                    indentstr='    '
                if eachline.find('!-- Open=') >0 or eachline.find(
                        '/Info>') >0 or eachline.find('!-- vim:') >0:
                    outstr+=eachline+'\n'
                else:
                    outstr+=indentstr+eachline+'\n'

        fout=file("result_"+filename,"w+")
        fout.writelines(outstr)
        print "保存为:result_" + filename
        f.close()
        fout.close()
        

            
    else:
        print "请输入待处理的xml文件!"



