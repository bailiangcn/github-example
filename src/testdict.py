#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AUTHOR:  BaiLiang , bailiangcn@gmail.com
# Last Change:  2011年01月22日 17时21分03秒


"""docstring
"""

__revision__ = '0.1'




from xml.dom.minidom import parse


serfilename = "../addressdata/service.xml"
domser=parse(serfilename)
rootser=domser.documentElement
serlist=rootser.getElementsByTagName('team')
#countres为最终的统计结果
countres= {}
for team in serlist: #服务组node
    #teamid表示当前处理的服务组号
    teamid = team.getAttribute("id")
    countres[teamid] ={} 




#打开区域area.xml
areafilename = "../addressdata/area.xml"
domarea=parse(areafilename)
rootarea=domarea.documentElement
reglist=rootarea.getElementsByTagName('regional')
regdict = {}


#生成一个包含所有区域的字典
for reg in reglist: #区域nodes
    regname = reg.getElementsByTagName("id"
            )[0].firstChild.data + "numbuild"
    regdict[regname] = 0
#根据各组和区域生成空白二维字典
    #{服务组：{区域：统计值}}
for key in countres:
    countres[key] = regdict

    #开始遍历各区、楼号
reg  =  reglist[0] #区域nodes
regname = reg.getElementsByTagName("id"
        )[0].firstChild.data + "numbuild"
communityfilename = reg.getElementsByTagName("datafile"
        )[0].firstChild.data.encode("utf-8")
commfilename = ''.join(("../addressdata/", 
communityfilename, ".xml"))
        #遍历各楼
domcomm=parse(commfilename)
rootcomm=domcomm.documentElement
houselist = rootcomm.getElementsByTagName('house')
house  =  houselist[0]
houseidlist = house.getElementsByTagName('id')
houseservicelist = house.getElementsByTagName('service')

