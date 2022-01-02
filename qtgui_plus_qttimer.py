#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import datetime as dt

import sys
import math
import utm
from math import sin, cos, sqrt, atan2, radians, acos, degrees
import random  

from math import pow
phi = math.pi
import PyQt5.QtCore
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, QTimer,QTime, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine
import threading 

#from PyQt5 import QtCore

import time
import paho.mqtt.client as paho
#broker="123.45.0.10"
broker="127.0.0.1"
port = 1883

pubdelay = 2 #delay publish to all wind and engine box
counter = 0


compass = 0

val_latitude = -6.859444  #centre
val_longitude = 107.590695  #centre
knot = 0
meter = 0

get_lat_GUI = val_latitude + 0.002
get_lon_GUI = val_longitude + 0.002

lat_error = 0
long_error = 0

deg_error = 0
meter_error_GUI = 0

degree_error_GUI = 0

#get_lat_GUI1 = 0
#get_lon_GUI1 = 0
get_lat_GUI_last = 0
get_lon_GUI_last = 0
counter_distance_mea = 0
dst_bw_line = 0
distance =0

knot = 0
sensor2 = 0
meter = 0

depth = 0

message_time = 0
message_time_prev = 0

current_time = dt.datetime.now()
title = str(current_time.day)+str(current_time.month)+str(current_time.year) + str(".csv")
fields = ['time', 'lat', 'long', 'wind speed', 'wave speed']
filename = title

with open(filename, 'a') as csvfile:
	# creating a csv writer object
	csvwriter = csv.writer(csvfile)
	# writing the fields
	csvwriter.writerow(fields)



def reMap(value, maxInput, minInput, maxOutput, minOutput):

	value = maxInput if value > maxInput else value
	value = minInput if value < minInput else value

	inputSpan = maxInput - minInput
	outputSpan = maxOutput - minOutput

	scaledThrust = float(value - minInput) / float(inputSpan)


	return minOutput + (scaledThrust * outputSpan)

class MQTTValue(QObject):   
	def __init__(self):
		super(MQTTValue,self).__init__()
	

	
	@pyqtSlot(result=float)
	def get_knot(self):  return knot 

	@pyqtSlot(result=float)
	def get_meter(self):  return sensor2
		


	@pyqtSlot(result=float)
	def lat(self):  return val_latitude

	@pyqtSlot(result=float)
	def long(self):  return val_longitude

	@pyqtSlot(float)
	def get_lat (self, lat_GUI):
		global get_lat_GUI
		get_lat_GUI = round(float(lat_GUI),6)
		#print("Lat target = ", get_lat_GUI)

	@pyqtSlot(float)
	def get_lon (self, lon_GUI):
		global get_lon_GUI
		get_lon_GUI = round(float(lon_GUI),6)
		

	
	@pyqtSlot(float)
	def get_lat1 (self, lat_GUI1):
		global get_lat_GUI1
		get_lat_GUI1 = float(lat_GUI1)
		print("Lat 1= ", get_lat_GUI1)

	@pyqtSlot(float)
	def get_lon1 (self, lon_GUI1):
		global get_lon_GUI1
		get_lon_GUI1 = float(lon_GUI1)
		global delta_lat
		global delta_lon
		global distance
		delta_lat = (get_lat_GUI - get_lat_GUI1)*111000
		delta_lon = (get_lon_GUI - get_lon_GUI1)*111000
		distance = sqrt(pow(delta_lat, 2) +  pow(delta_lon, 2))
		print("Lon 1= ", get_lon_GUI1)
		print("delta lat= ", delta_lat)
		print("delta lon= ", delta_lon)
		print("distance= ", distance)
		
		
		
		
        
	@pyqtSlot(result=float)
	def distance_bw_line(self):return distance 	
	
	
	@pyqtSlot(result=float)
	def lat_target(self):return get_lat_GUI 	
	
	
	@pyqtSlot(result=float)
	def long_target(self):return get_lon_GUI
	
	
	@pyqtSlot(result=float)
	def meter_error(self):return meter_error_GUI
	
	@pyqtSlot(result=float)
	def degree_error(self):return degree_error_GUI
	
	@pyqtSlot(result=float)
	def ship_compass(self):return compass
	
	@pyqtSlot(result=float)
	def get_depth(self):return depth

def timerEvent():
	global time
	global message_time
	global message_time_prev
	#time = time.addSecs(0.1)
	message_time = time.time() - message_time_prev
	if message_time > 5:
		print(time.time())
		message_time_prev = time.time()
		
		with open(filename, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				rows = [ [str(current_time), str(val_latitude), str(val_longitude),str(knot), str(sensor2)]]
				csvwriter.writerows(rows)


'''
timer = QTimer()
time = QTime(0, 0, 0)
timer.timeout.connect(timerEvent)
timer.start(1000)
'''

	
def on_message(client, userdata, message):
		msg = str(message.payload.decode("utf-8"))
		t = str(message.topic)

		if(msg[0] == 'c'):
			val =  1
		else:
			val = float(msg)

			
		if (t == "get_knot"):
			global knot
			knot = float(msg)
					
		if (t == "get_meter"):
			global sensor2
			sensor2 = float(msg)
					
		if (t == "GPS/lat"):
			global val_latitude
			val_latitude = round(float(msg),6)


		if (t == "GPS/long"):
			global val_longitude
			val_longitude = round(float(msg),6)

		if (t=="save"):
			print(val_longitude)
			with open(filename, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				rows = [ [str(current_time), str(val_latitude), str(val_longitude),str(knot), str(sensor2)]]
				csvwriter.writerows(rows)
		if(t=="compass"):
			global compass
			compass = float(msg)
			
		global meter_error_GUI
		global degree_error_GUI
		global lat_error
		global long_error
		
		#print("Lon target = ", get_lon_GUI)
		lat_error = round((val_latitude - get_lat_GUI)*111000 , 3)    #euclian distance equation (B)
		long_error = round((val_longitude - get_lon_GUI)*111000 , 3)  
		#print(str(lat_error) + str(" ") + str(long_error))
		meter_error_GUI = round(math.sqrt(pow(lat_error,2) + pow (long_error,2)) , 2) #euclian distance equation (C)
		if meter_error_GUI < 0.1:
			meter_error_GUI = 0.1
		
		
		if long_error >= 0 :
			degree_error_GUI = -1*round((math.degrees(math.acos(-1*lat_error/meter_error_GUI))) , 0) - compass
			#print("a")
		else :
			degree_error_GUI = round((math.degrees(math.acos(-1*lat_error/meter_error_GUI))) , 0) - compass
			#print("b")
		#print(long_error)



if __name__ == "__main__":
	'''     
	timer = QTimer()
	time = QTime(0, 0, 0)
	timer.timeout.connect(timerEvent)
	timer.start(1000)
	'''
	##Mosquitto Mqtt Configuration
	client= paho.Client("GUI")
	client.on_message=on_message

	print("connecting to broker ",broker)
	client.connect(broker,port)#connect
	print(broker," connected")

	
	
	client.loop_start()
	print("Subscribing")

    #subscribe	
	client.subscribe("get_knot")
	client.subscribe("get_meter")
	client.subscribe("GPS/lat")	
	client.subscribe("GPS/long")	
	client.subscribe("save")
	client.subscribe("compass")

	
	client.publish("MainControl", "active")#publish

	## QT5 GUI
	print("Graphical User Interface ")
	app = QGuiApplication(sys.argv)
	#app = QtCore.QCoreApplication(sys.argv)

	view = QQuickView()
	view.setSource(QUrl('main.qml'))

	mqttvalue = MQTTValue()

	timer = QTimer()
	timer.timeout.connect(timerEvent)
	timer.start(10)


	context = view.rootContext()
	context.setContextProperty("mqttvalue", mqttvalue)



	root = view.rootObject()
	timer.timeout.connect(root.updateValue) ##Call function update in GUI QML

	engine = QQmlApplicationEngine(app) 
	engine.quit.connect(app.quit) ## Quit Button Respon
		
	view.show()
	
    
    

	sys.exit(app.exec_())







