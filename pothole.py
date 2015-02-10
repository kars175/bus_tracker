#https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Pot-Holes-Reported/7as2-ds3y

#with open('example.csv', 'rb') as csvfile:
#    dialect = csv.Sniffer().sniff(csvfile.read(1024))
#    csvfile.seek(0)
#    reader = csv.reader(csvfile, dialect)
    
    
import csv
import re
import operator

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


pot_hole = open("pot_hole.csv")
pot_hole_open = open("pot_hole_open.csv",'w') #write the header for the csv file
line=pot_hole.readline()
pot_hole_open.write(line)

#step 1 remove all completed pot holes. We want to know only the open pot holes while (1):
    line=pot_hole.readline()

    if(line==''):
        break
    completed = re.search(r'Completed',line)
    if completed :
        continue
    else :
        pot_hole_open.write(line)
       
pot_hole_open.close()
pot_hole.close()

pot_hole_open = open("pot_hole_open.csv")
i=0
dict_pot_hole= csv.DictReader(pot_hole_open);
#{'STATUS': 'Open - Dup', 'X COORDINATE': '1161660.25738822', 'COMPLETION DATE': '', 'ZIP': '60645', 'STREET ADDRESS': '7413 N DAMEN AVE', 'CREATION DATE': '02/08/2015', 'TYPE OF SERVICE REQUEST': 'Pothole in Street', 'SERVICE REQUEST NUMBER': '15-00237470', 'LONGITUDE': '-87.68032240344158', 'Police District': '24', 'Y COORDINATE': '1949311.76000709', 'MOST RECENT ACTION': '', 'LATITUDE': '42.017069883363384', 'NUMBER OF POTHOLES FILLED ON BLOCK': '', 'Community Area': '1', 'Ward': '49', 'SSA': '', 'CURRENT ACTIVITY': '', 'LOCATION': '(42.017069883363384, -87.68032240344158)'} pot_hole_zip ={}

for row in dict_pot_hole :   
    print row['STREET ADDRESS'],row['NUMBER OF POTHOLES FILLED ON BLOCK'],row['ZIP']
    if row['ZIP'] in pot_hole_zip :
            pot_hole_zip[row['ZIP']] += 1
    else:
         pot_hole_zip[row['ZIP']]=1
    i=i+1
    if(i==500) :
        break

for zip in pot_hole_zip :
    print zip," has ",pot_hole_zip[zip]

max_pot_hole_zip = keywithmaxval(pot_hole_zip)

print "zip with max pot holes is ",max_pot_hole_zip," has ", pot_hole_zip[max_pot_hole_zip]
    


