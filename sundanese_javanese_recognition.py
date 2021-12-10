'''
SUNDANESE TRANSMITTER .PY
WRITTEN BY MUHAMMAD HUSNI WHEN HE IS GABUT
RUN USE THONNY IDE AND PYTHON 3.8.2
I HOPE THIS HELP YOU FOR MAKING SUNDANESE TKINTER INTERFACE FOR ARDUINO
'''


import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import *
import speech_recognition as sr


ser = serial.Serial()

ser.baudrate = 9600

enable = 0

r = sr.Recognizer()
global a

def connect():
    ser.port = port_select.get()
    ser.open()
    print(port_select.get())
    
def led_on():
    #message = 'H'
    #ser.write(message.encode())
    enable = 1
    a = 'yes'
    print(enable)

    if (a == 'yes'):  
        with sr.Microphone() as source:
            print('speak please:')
            #r.pause_threshold = 1
            r.energy_threshold = 400
            #r.duration = 1
            #r.adjust_for_ambient_noise(source,duration=1)
            audio = r.listen(source,phrase_time_limit=1)
            
            try:
                print('recognition')
                text = r.recognize_google(audio,language = "ID")
                #print('you says : {}'.format(text))
                
                if (text == "burung" or text =="huruf"): #murup in javanese hurung in sundanese
                    print('hurung')
                    ser.write('hurung'.encode())
                elif (text == "parem"or text == "mate"):
                    print('pareum')
                    ser.write('pareum'.encode())
                elif (text == "haarp" or text =="Arab" or text == "harap" or text =="ngarep"):
                    print('hareup')
                    ser.write('hareup'.encode())
                elif (text == "genggam" or text == "genggem" or text == "gem"):
                    print('nyapit')
                    ser.write('nyapit'.encode())
                
                elif (text == "buka"):
                    print('lepas')
                    ser.write('lepas'.encode())
                elif (text == "buri"):
                    print('tukang')
                    ser.write('tukang'.encode()) 
                else:
                    print('you says : {}'.format(text))
                    ser.write(text.encode())
                
            except:
                print('')
                #a = 'no'

def disconnect():
    ser.close()
'''
def led_off():
    #message = 'L'
    #ser.write(message.encode())
    enable = 0
    a = 'yes'
    print(enable)
'''    

def my_mainloop():
    print ("aktip")
    master.after(500, my_mainloop)

def transmit():
    print("hoho")
    

master = tk.Tk()
master.after(500, my_mainloop)

port_select = tk.StringVar()


master.title("SUNDANESE TO ROBOT LANGUAGE TRANSLATOR")
master.geometry('410x200')

#port_select = tk.StringVar()
#send_string = tk.StringVar()


label1 = tk.Label(master, text = 'UART PORT : ', font = "BOLD")
label1.place(x=0, y=30)

form_port = tk.Entry(master, textvariable = port_select)
form_port.place(x=100, y=30)

connect_button = tk.Button(master, text='konek', command=connect , width=10, height=1)
connect_button.place(x=100, y=80)
disconnect_button = tk.Button(master, text='teu konek', command=disconnect, width=10, height=1)
disconnect_button.place(x=200, y=80)


label2 = tk.Label(master, text = 'REKAM SORA : ', font = "BOLD")
label2.place(x=0, y=120)

led_on_button = tk.Button(master, text='HAYANG REKAM', command=led_on, width = 60, height=1)
led_on_button.place(x = 0, y=150)

#led_off_button = tk.Button(master, text='EREUN REKAM', command=led_off, width=20, height=1)
#led_off_button.place (x=200, y = 150)

label2 = tk.Label(master, text = 'nu nyien : muhammadhusni777. ig na husni : husnimuttaqin', font = "BOLD")
label2.place(x=0, y=0)


master.mainloop()    
