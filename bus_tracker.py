import urllib
import re
import xml.etree.ElementTree as ET
import webbrowser
import time

#http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=actransit&r=210
u=urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data=u.read()
f=open('rt22.xml','wb')
f.write(data)
f.close()
tree = ET.parse('rt22.xml')

root = tree.getroot()
print root.tag
print root.attrib
nearby = 0


def calculate() :
    daves_latitude = 41.98062
    daves_longitude = -87.668
    for child in root.findall('bus'):
         direction = child.find('d')
         if "North" in direction.text:
            latitude = child.find('lat')

            lat = float(latitude.text)
            if lat > daves_latitude :
                print direction.text
                print "latitude is "+latitude.text
                longitude = child.find('lon')
                busid = child.find('id')
                print "busid is ",busid.text
                distance = 69 * abs(lat-daves_latitude)
                print "distance is ",distance
                maps_string = 'https://maps.googleapis.com/maps/api/staticmap?&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C'+latitude.text+','+longitude.text
                print maps_string
                if(distance < 0.5) :
                    webbrowser.open(maps_string)
                    return 1

    return 0
#webbrowser.open('https://maps.googleapis.com/maps/api/staticmap?&zoom=13&size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794')


while (nearby == 0) :
    nearby = calculate()
    time.sleep(10)

