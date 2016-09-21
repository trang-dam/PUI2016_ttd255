import json
import urllib.request as ulr
import sys
import csv

if not len(sys.argv)==4:
    print("Invalid number of arguments. Run as: get_bus_info.py <MTA_KEY> <BUS_LINE> <BUS_LINE>.csv")
    sys.exit()

def get_jsonparsed_data(url):
	response = ulr.urlopen(url)
	data = response.read().decode("utf-8")
	return json.loads(data) 

MTA_Data = get_jsonparsed_data("http://bustime.mta.info/api/siri/vehicle-monitoring.json?key="+str(sys.argv[1])+"&VehicleMonitoringDetailLevel=calls&LineRef="+str(sys.argv[2]))

Data_1 = MTA_Data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

file = open(str(sys.argv[3]),"w+")
f = csv.writer(file)
f.writerow(['Latitude','Longitude','Stop Name','Stop Status'])
for x in Data_1:
    La = x['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
    Lo = x['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
    try:
        Name = x['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName']
    except KeyError:
        Name = ('N/A')
    try:
        Status = x['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance']
    except KeyError:
        Status = 'N/A'
    f.writerow([La,Lo,Name,Status])
file.close()

