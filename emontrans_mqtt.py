#!/usr/bin/python
'''
Created on 01.05.2017

@author: mario

Emontranslator

Receive messages from serial/uart
Generate JSON Emon Input Messages
Insert via EMON API / APIKEY to emoncms on locahost (running on pi)

Sends data on mqtt
'''

import serial
import httplib
import time
import paho.mqtt.client as mqtt
import json

domain = "localhost"
emoncmspath = "emoncms"
apikey = "2eba96e51f6b41534f52110ad063b0c8"

domain2 ="piboxmet.local"
apikey2 = "1ed78821a7e18f9b1b41ab30c3ffad0b"

nodeid = 10
conn = httplib.HTTPConnection(domain)
conn2 = httplib.HTTPConnection(domain2)

mqtt_server='piboxmet.local'
mqtt_topic='aussen/433modem'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_server, 1883, 60)

client.loop_start()

# Set this to the serial port of your emontx and baud rate, 9600 is standard emontx baud rate
ser = serial.Serial('/dev/ttyS0', 9600)

def parseLine(linestr):
    nodeid = None
    temp = 0
    humid = 0
    voltage = 0
    if "BAD-CRC" not in linestr:
        if len(linestr) > 2:
                data = linestr.split(" ")
                print linestr
                print data
                nodeid = int(data[0])
                temp = float(data[1])
                temp = temp/ 100.
                humid = float(data[2])
                humid = humid / 100.
                voltage = float(data[3])
                voltage = voltage / 100.
    return nodeid,temp,humid,voltage

while 1:
    try:
        # Read in line of readings from serial / uart
        linestr = ser.readline()
        linestr = linestr.rstrip()
        #print linestr
    
        nodeid,temp,humid,voltage=parseLine(linestr)
        if nodeid:
            params = ("{temp:%.2f,humid:%.2f,voltage:%.2f}"%(temp,humid,voltage))
            #print params
            print "nodeid:"+str(nodeid)
            # Send to emoncms
            conn.connect()
            conn.request("GET", "/"+emoncmspath+"/input/post.json?&node="+str(nodeid)+"&json="+params+"&apikey="+apikey)
            response = conn.getresponse()
            print response.read()
            conn2.connect()
            conn2.request("GET", "/"+emoncmspath+"/input/post.json?&node="+str(nodeid)+"&json="+params+"&apikey="+apikey2)
            response2 = conn2.getresponse()
            print response2.read()
 	    print("publishing mqtt")
  	    params_mqtt = {"temp":temp,"humid":humid, "voltage":voltage, "timesend":time.time()}
  	    client.publish(mqtt_topic+"/{}".format(nodeid),payload=json.dumps(params_mqtt))


    except KeyboardInterrupt:
        raise
    except Exception as e:
        print e.__doc__
        print e.message
        pass
        
    time.sleep(1)
