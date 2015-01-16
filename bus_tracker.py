import urllib
import re
import xml.etree.ElementTree as ET

u=urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data=u.read()
f=open('rt22.xml','wb')
f.write(data)
f.close()
tree = ET.parse('rt22.xml')

root = tree.getroot()
print root.tag
print root.attrib

for child in root.findall('bus'):
     direction = child.find('d')
     print direction.text
