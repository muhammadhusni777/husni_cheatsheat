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
            audio = r.listen(source, timeout= 3, phrase_time_limit =5)
    
            try:
                text = r.recognize_google(audio,language = "ID")
                #print('you says : {}'.format(text))
                
                if (text == "burung"):
                    print('hurung')
                    ser.write('hurung'.encode())
                elif (text == "parem"):
                    print('pareum')
                    ser.write('pareum'.encode())
                elif (text == "haarp"):
                    print('hareup')
                    ser.write('hareup'.encode())
                else:
                    print('you says : {}'.format(text))
                    ser.write(text.encode())
                
            except:
                print('')
                #a = 'no'

def disconnect():
    ser.close()

def led_off():
    #message = 'L'
    #ser.write(message.encode())
    enable = 0
    a = 'yes'
    print(enable)
    

def my_mainloop():
    print ("sisteum aktip")
    master.after(1000, my_mainloop)

def transmit():
    print("hoho")
    

master = tk.Tk()
master.after(1000, my_mainloop)

port_select = tk.StringVar()


master.title("SUNDANESE TO MACHINE TRANSLATOR")
master.geometry('400x200')

#port_select = tk.StringVar()
#send_string = tk.StringVar()


label1 = tk.Label(master, text = 'UART PORT : ', font = "BOLD")
label1.place(x=0, y=0)

form_port = tk.Entry(master, textvariable = port_select)
form_port.place(x=140, y=5)

connect_button = tk.Button(master, text='connect', command=connect , width=10, height=1)
connect_button.place(x=100, y=50)
disconnect_button = tk.Button(master, text='disconnect', command=disconnect, width=10, height=1)
disconnect_button.place(x=200, y=50)


label2 = tk.Label(master, text = 'REKAM SUARA : ', font = "BOLD")
label2.place(x=0, y=100)

led_on_button = tk.Button(master, text='HAYANG REKAM', command=led_on, width = 20, height=1)
led_on_button.place(x = 50, y=150)

led_off_button = tk.Button(master, text='EREUN REKAM', command=led_off, width=20, height=1)
led_off_button.place (x=200, y = 150)




master.mainloop()



    
