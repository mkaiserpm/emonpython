#!/usr/bin/python3
'''
Created on 01.04.20

@author: mario kaiser

Grafana / InfluxDb connection test

'''
metdata = "aussendata"
query_test = 'SELECT min("temp"),"name" FROM "nodes_" WHERE time > now() - 12h AND "nodeid" = 18'
#query_test = 'SELECT min("temp") FROM "nodes_" WHERE time > now() - 12h GROUP BY "name"'

from influxdb import InfluxDBClient


client = InfluxDBClient(host='localhost', port=8086)
client.switch_database(metdata)

q1_result = client.query(query_test)
print(q1_result.raw)

