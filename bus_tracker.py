import urllib
import re
import xml.etree.ElementTree as ET
import webbrowser
import time


def calculate_fremont() :
    karthik_latitude = 37.526408
    distance_near = 0
    lat_near = 0
    long_near = 0
    u=urllib.urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=actransit&r=1")
    data = u.read()
    f= open('rt1.xml','wb')
    f.write(data)
    f.close()
    tree = ET.parse('rt1.xml')
    root = tree.getroot()
    print root.tag
    print root.attrib
    nearby = 0
    for child in root:
        for children in child:
             try :
                 stopName =  children.get('title')
                 if 'Shattuck' in stopName and 'Durant' in stopName:
                    print "StopName is:",stopName
                    print "StopId is :",children.get('stopId')
                    stopId=children.get('stopId')
             except:
                continue
    stop_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&stopId="+stopId+"&routeTag=1"
    u =urllib.urlopen(stop_url)
    data = u.read()
    f= open('rt1_stop.xml','wb')
    f.write(data)
    f.close()
    vehicleId=[]
    tree = ET.parse('rt1_stop.xml')
    root = tree.getroot()
    print root.tag,root.attrib
    for child in root:
        try:
            print "child tag",child.tag,child.attrib
            for children in child:
                for prediction in children:
                    vehicleId.append(prediction.get('vehicle'))
                    print prediction.get('vehicle')
        except:
            print "exception caught"
            continue

    print "list of vehicles is ",vehicleId

    u=urllib.urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=actransit&r=1&t=0")
    data = u.read()
    f= open('rt1_long.xml','wb')
    f.write(data)
    f.close()
    tree = ET.parse('rt1_long.xml')
    root = tree.getroot()
    print root.tag
    print root.attrib
    for child in root:
        try:
            id = child.get('id')
            if id in vehicleId:
                print "id",child.get('id')
                lat = float(child.get('lat'))
                long = float(child.get('lon'))
                distance = 69 * abs(lat-karthik_latitude)
                print distance," from home"
                if distance_near == 0 or distance_near > distance :
                    distance_near = distance
                    lat_near = lat
                    long_near = long

        except:
            print "exception caught"
            print "Exception:"
            import traceback; traceback.print_exc()
            continue
    print distance_near,":",lat_near,":",long_near,":"
    maps_string = 'https://maps.googleapis.com/maps/api/staticmap?&zoom=13&size=1024x768&maptype=roadmap&markers=color:blue%7Clabel:S%7C'+str(lat_near)+','+str(long_near)
    webbrowser.open(maps_string)

    return



#http://stackoverflow.com/questions/8855212/nesting-for-loop-within-a-try-operator


def calculate_chicago() :
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

calculate_fremont()

#while (nearby == 0) :
#    nearby = calculate_chicago()
#    time.sleep(10)

