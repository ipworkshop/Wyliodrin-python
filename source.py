from time import sleep
import sys
import os
import math
import serial
import thread
import select
import mpylayer

mp = mpylayer.MPlayerControl()

def send (signal, value):
    os.write (4, signal+" "+str(value)+"\n")

def read():
    data = os.read (3, 10)
    val = data.split('\n')
    for va in val:
        vl = va.split(' ')
        if len(vl)==2:
            try:
                return (vl[0], int(vl[1]))
            except:
                try:
                    return (vl[0], float(vl[1]))
                except:
                    return (vl[0], vl[1])

def function():
    print "hey"
    for i in range (1,100):
        send ("temperature",i/3)
        send ("series",math.sin(i/10.0)*10+40)
        sleep (0.1)
    
    print "sleep"

def read_serial():
    nr=0;
    epoll = select.epoll ()
    epoll.register (3, select.EPOLLIN)
    events = epoll.poll (0.5)
    epoll = select.epoll ()
    epoll.register (3, select.EPOLLIN)
    events = epoll.poll (0.5)
    for fileno, event in events:
        if fileno == 3:
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
    while True:
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
            mp.volume = (res*100)/255
            sleep (0.001)

#thread.start_new_thread (read_serial, ())
mp.loadfile('I Ran Away.mp3')
write_serial ()

srl.close ()

