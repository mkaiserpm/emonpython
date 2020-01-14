#!/usr/bin/python3
'''
Created on 10.01.20

@author: mario kaiser

Emontranslator

Receive messages from serial/uart
Generate JSON mqtt message
Sends data on mqtt
'''

import serial
import http.client as httpc
import time
import paho.mqtt.client as mqtt
import json


mqtt_server='localhost'
mqtt_topic='aussen/433modem'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

mqtt_connected = False

client = mqtt.Client()
client.on_connect = on_connect

def connect_mqtt():
    client.connect(mqtt_server, 1883, 60)
    client.loop_start()
    mqtt_connected = True

# Set this to the serial port of your emontx and baud rate, 9600 is standard emontx baud rate
ser = serial.Serial(port='/dev/ttyS0', baudrate = 9600, timeout = 1)

domain = "rb3met.local"
emoncmspath = "emoncms"
apikey = "2eba96e51f6b41534f52110ad063b0c8"
#conn = httpc.HTTPConnection(domain)

node_to_name = {16:"Aussen",17:"Garage",18:"Hasenstall"}

def parseLine(linestr):
    nodeid = None
    temp = 0
    humid = 0
    voltage = 0
    if "BAD-CRC" not in linestr:
        if len(linestr) > 2:
            data = linestr.split(" ")
            print(linestr)
            #print(data)
            nodeid = int(data[0])
            temp = float(data[1])
            temp = temp/ 100.
            humid = float(data[2])
            humid = humid / 100.
            voltage = float(data[3])
            voltage = voltage / 1000.
    return nodeid,temp,humid,voltage

while 1:
    try:
        if not mqtt_connected:
            connect_mqtt()
            mqtt_connected = True

        # Read in line of readings from serial / uart
        line_bytes = ser.readline()
        linestr = line_bytes.decode("utf-8").rstrip()
        nodeid,temp,humid,voltage=parseLine(linestr)
        if nodeid:
            if mqtt_connected:
                print("publishing mqtt")
                params_mqtt = {"nodeid":nodeid,"name":node_to_name[nodeid],"temp":temp,"humid":humid, "voltage":voltage, "timesend":time.time()}
                client.publish(mqtt_topic+"/{}".format(nodeid),payload=json.dumps(params_mqtt))
            params = ("{temp:%.2f,humid:%.2f,voltage:%.2f}"%(temp,humid,voltage))
            #print params
            #print "nodeid:"+str(nodeid)
            # Send to emoncms
            #conn.connect()
            #conn.request("GET", "/"+emoncmspath+"/input/post.json?&node="+str(nodeid)+"&json="+params+"&apikey="+apikey)
            #response = conn.getresponse()
            #print response.read()
            #conn2.connect()
            #conn2.request("GET", "/"+emoncmspath+"/input/post.json?&node="+str(nodeid)+"&json="+params+"&apikey="+apikey2)
            #response2 = conn2.getresponse()
            #print response2.read()


    except KeyboardInterrupt:
        raise
    
    except Exception as e:
        print(e.__doc__)
        print(e)
        pass
        
    time.sleep(1)
