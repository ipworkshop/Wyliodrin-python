from time import sleep
import sys
import os
import math
import serial
import thread
import select
import mpylayer

mp = mpylayer.MPlayerControl()

bufval = ''
nr = 0

def send (signal, value):
    os.write (4, signal+" "+str(value)+"\n")

def read():
    global bufval
    data = os.read (3, 100)
    #data = bufval + data
    val = data.split('\n')
    for i in range (0, len(val)):
        vl = val[i].split(' ')
        if len(vl)==2:
            try:
                return (vl[0], int(vl[1]))
            except:
                try:
                    return (vl[0], float(vl[1]))
                except:
                    return (vl[0], vl[1])
       # elif i == len (val)-1:
            #bufval = val[i]

def function():
    print "hey"
    for i in range (1,100):
        send ("temperature",i/3)
        send ("series",math.sin(i/10.0)*10+40)
        sleep (0.1)
    
    print "sleep"

def read_serial():
    global nr
    name, data = read ()
    print data
    if type(data) is int:
        print data
        srl.write (chr (data))
        nr=nr+1
        if nr == 3:
            nr = 0
            srl.write (chr(255))

srl = serial.Serial ("/dev/ttyAMA0")


def write_serial():
    read = ord(srl.read ())
    #send ("temperature",read)
    if read == 255:
        buttons = ord(srl.read ())
        send ("buttons", buttons)
        temperature = ord(srl.read ())
        send ("temperature", 100-temperature/255.0*100)
        series = ord(srl.read ())
        send ("light", 255-series)
        res = ord(srl.read ())
        send ("series", res)
        #mp.volume = (res*100)/255

mp.loadfile('I Ran Away.mp3')

epoll = select.epoll ()
epoll.register (3, select.EPOLLIN)
while True:
    events = epoll.poll (0.001)
    for fileno, event in events:
        if fileno == 3:
            read_serial()
    write_serial()

srl.close ()

