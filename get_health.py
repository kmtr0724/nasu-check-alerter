#!/usr/bin/python3
import time
import json
import requests
#import datetime
from datetime import datetime
from datetime import timedelta
from pytz import timezone,utc
from influxdb import InfluxDBClient

appsetting = json.load(open('/usr/local/etc/nasu-alerter.json', 'r'))
discord_hook_url = appsetting["discord_hook_url"]
alerted_flag = 0

def getHealth():
	global alerted_flag

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
			if time_delta > 180 and alerted_flag == 0:
				o_time = l_time + timedelta(hours=9)
				sendDiscord("Nasu Offline at " + o_time.strftime('%Y/%m/%d %H:%M:%S'))
				alerted_flag = 1
			elif time_delta <= 60 and alerted_flag == 1:
				o_time = l_time + timedelta(hours=9)
				sendDiscord("Nasu Recovered at " + o_time.strftime('%Y/%m/%d %H:%M:%S'))
				alerted_flag = 0
			break
		break
			#print ("\n")
def sendDiscord(content_str):
	json_body = {"content": content_str}
	json_data = json.dumps(json_body)
	headers = {"Content-Type" : "application/json","Accept":"application/json"}
	response = requests.post(discord_hook_url,headers=headers,data=json_data,timeout=10)	

while True:
	getHealth()
	time.sleep(300)

