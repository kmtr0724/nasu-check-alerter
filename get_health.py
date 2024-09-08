#!/usr/bin/python3
import time
import json
import requests
#import datetime
from datetime import datetime
from pytz import timezone,utc
from influxdb import InfluxDBClient

appsetting = json.load(open('/usr/local/etc/nasu-alerter.json', 'r'))
discord_hook_url = appsetting["discord_hook_url"]

def getHealth():

	client = InfluxDBClient('localhost', 8086, '', '', 'nasu_health')
	result = client.query('select last(temp),temp from nasu_thp limit 1;')
#l_time = resulto
	now = datetime.now()
	for k in result:
		for k2 in k:
			l_time = datetime.strptime(k2['time'],'%Y-%m-%dT%H:%M:%SZ')
			#print(l_time)
			#print(datetime.timestamp(l_time))
			time_delta = datetime.timestamp(now) - datetime.timestamp(l_time) - 32400
			#print(time_delta)
			if time_delta > 180 and time_delta <= 600:
				sendDiscord(l_time)
			break
		break
			#print ("\n")
def sendDiscord(time):
	json_body = {"content": "Nasu Offline at " + time}
	json_data = json.dumps(json_body)
	headers = {"Content-Type" : "application/json","Accept":"application/json"}
	response = requests.post(discord_hook_url,headers=headers,data=json_data,timeout=10)	

while True:
	getHealth()
	time.sleep(300)


