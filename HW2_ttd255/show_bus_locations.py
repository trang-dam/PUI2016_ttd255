import json
import urllib.request as ulr
import sys
import pandas as pd
from pandas import Series, DataFrame

if not len(sys.argv) == 3:
	print('Invalid number of arguments. Run as: show_bus_locations.py <MTA_KEY> <BUS_LINE>')
	sys.exit()

def get_jsonparsed_data(url):
	response = ulr.urlopen(url)
	data = response.read().decode("utf-8")
	return json.loads(data)

MTA_Data = get_jsonparsed_data("http://bustime.mta.info/api/siri/vehicle-monitoring.json?key="+str(sys.argv[1])+"&VehicleMonitoringDetailLevel=calls&LineRef="+str(sys.argv[2]))

Data_1 = MTA_Data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

info_keys = ['VehicleLocation','ProgressRate']

Active_buses = 0
print('Number of Active Buses : %d' %sum(rec['MonitoredVehicleJourney']['ProgressRate'] == "normalProgress" for rec in Data_1))
for rec in Data_1:
	if rec['MonitoredVehicleJourney']['ProgressRate'] == "normalProgress":
		Active_buses += 1
		print('Bus %d is at latitude %s and longitude %s' %((Active_buses-1), 
        	str(rec['MonitoredVehicleJourney']['VehicleLocation']['Latitude']), 
        	str(rec['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])))
