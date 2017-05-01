'''
Created on 01.05.2017

@author: mario

Emontranslator

Receive messages from serial/uart
Generate JSON Emon Input Messages
Insert via EMON API / APIKEY to emoncms on locahost (running on pi)
'''

import serial
import httplib
import time

domain = "localhost"
emoncmspath = "emoncms"
apikey = "2eba96e51f6b41534f52110ad063b0c8"

nodeid = 10
conn = httplib.HTTPConnection(domain)

# Set this to the serial port of your emontx and baud rate, 9600 is standard emontx baud rate
ser = serial.Serial('/dev/ttyS0', 9600)

def parseLine(linestr):
    nodeid = None
    temp = 0
    humid = 0
    voltage = 0
    return nodeid,temp,humid,voltage

while 1:
    # Read in line of readings from serial / uart
    linestr = ser.readline()
    linestr = linestr.rstrip()
    print linestr

    nodeid,temp,humid,voltage=parseLine(linestr)
    if nodeid:
        params = ("{temp:%d,humid:%d,voltage:%d}"%(nodeid,temp,humid,voltage))
        print params
        # Send to emoncms
        #conn.request("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&json="+params)
        #response = conn.getresponse()
        #print response.read()
    time.sleep()