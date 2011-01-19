import xml.dom.minidom
dom=xml.dom.minidom.parse('addressdata/addresslist_ln.xml')
dom
dom.toxml()
_ip.magic("who ")
root=dom.documentElement
root.toxml()
root.nodeName
root.getElementsByTagName('community')
root.getElementsByTagName('community').childNodes
root.getElementsByTagName('community')[0].childNodes
comm0=root.getElementsByTagName('community')[0]
comm0.nodeName
comm0.getAttribute('name')
print comm0.getAttribute('name')
comm0.toxml()
comm0.getElementsByTagName('house')
houselist=comm0.getElementsByTagName('house')
houselist.length
_ip.magic("who ")
comm0.childNodes.length
for node in comm0.childNodes:
    print node.nodeName
    

_ip.magic("who ")
houselist
houselist[0].toxml()
house0=houselist[0]
house0.getElementsByTagName('number')
house0.getElementsByTagName('number').toxml()
house0.getElementsByTagName('number')[0].toxml()
house0.getElementsByTagName('number')[0].data
number0=house0.getElementsByTagName('number')[0]
number0.nodeValue
number0.nodeName
number0.firstChild.data
text=dom.createTextNode('id')
text=dom.createTextNode('1')
text.toxml 
text.toxml()
item=dom.createElement('id')
item.appendChild(text)
item.toxml()
_ip.magic("who ")
house0.appendChild(item)
house0.toxml()
print house0.toxml()
root.getElementsByTagName('community')[0].getElementsByTagName('house')[0]
root.getElementsByTagName('community')[0].getElementsByTagName('house')[0].toxml()
f=file('test.xml','w')
dom.writexml(f,encoding='utf-8')
import codecs
writer=codecs.lookup('utf-8')[3](f)
dom.writexml(writer,encoding='utf-8')
writer.close 
writer=codecs.lookup('utf-8')[3](f)
f=file('test.xml','w')
writer=codecs.lookup('utf-8')[3](f)
print writer
