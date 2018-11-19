import nmap
import time
import socket
import random
import argparse

import subprocess
import _thread

from luma.core.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from numpy import ndarray

serial = spi(port=0, device=0, gpio=noop(), bus_speed_hz=16000000)
device = max7219(serial, cascaded=4)
device.contrast(0)

width, height = 16, 16
#DeviceList = [[0 for x in range(width)] for y in range(height)]
DeviceList = ndarray((256,),bool)
ActivePair = [-1,-1]

nm = nmap.PortScanner()             # instantiate nmap.PortScanner object

def getipaddress():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

def getsubnet():
    subnet=getipaddress()
    subnet=subnet[:subnet.rfind('.')-len(subnet)]
    return(subnet)

thisSubnet = getsubnet()
thisIP = getipaddress()

def dotcpdump():
    tcpdump = subprocess.Popen(('sudo', 'tcpdump', '-lnt'), stdout=subprocess.PIPE)
    while True:
        line=tcpdump.stdout.readline().decode("utf-8")

        if thisSubnet in line:
            parsetcpdump(line)
        
    return

def parsetcpdump(line):
    #if thisIP not in line:
    if True:
        line=line[:line.find(':')-len(line)]

        fromIP = line[3:line.find('>')-len(line)]
        toIP = line[line.find('>')+2:]

        if len(fromIP)>0 and len(toIP)>0:
            #remove port number...
            fromIP = fromIP[:fromIP.rfind('.')-len(fromIP)]
            toIP = toIP[:toIP.rfind('.')-len(toIP)]

            fromN=getDeviceFromIPAddress(fromIP)
            toN=getDeviceFromIPAddress(toIP)
            
            if fromN!=-1 or toN!=-1:
                ActivePair[0]=fromN
                ActivePair[1]=toN
    return

def mapnetwork():
    while True:
        print('----------------------------------------------------')

        nm.scan(hosts=getsubnet()+'.0/24', arguments='-R -sP -PE -PA21,23,80,3389')  #-O -R -sS -PE -PA21,23,80,3389
        for h in nm.all_hosts():
            ipAddress=nm[h]['addresses']['ipv4']
            print(ipAddress, nm[h]['vendor'], nm[h].hostname())    #, nm[h]['osclass']
            setDeviceFromIPAddress(ipAddress,True)
        time.sleep(60)
    return

def measurelinkquality():
    quality=0;
    while True:
        cmd = subprocess.Popen("sudo iwconfig wlan0 | grep Quality",
                             shell=True,
                             stdout=subprocess.PIPE,
                           )
        line=cmd.stdout.readline().decode("utf-8")
        line=line.lstrip()

        if 'Link Quality' in line:
            quality=int(line[line.rfind('=')+1:-6])
            quality=(quality+100)/45
            quality=max(0,min(quality,1))
            quality=int(quality*255)
            print(quality)
            device.contrast(quality)
        elif 'Not-Associated' in line:
            print('No signal')
        time.sleep(1)
    return

# def setPixel(x,y,value):
#     DeviceList[x+(y*8)]=value

#     return

def drawDisplay():
    c=canvas(device)    #luma.core.render.canvas

    #device.contrast(0)
     #for threshold in range(255,0,-1):
    with c as display:  #ImageDraw
        for n in range(0, 255):
            if DeviceList[n]==True:
                    if n!=ActivePair[0] and n!=ActivePair[1]:
                        drawDevice(n,display)

    ActivePair[0]=-1
    ActivePair[1]=-1

    # if ActivePair[0]==-1 and ActivePair[1]==-1:
    #     device.contrast(0)
    #      #for threshold in range(255,0,-1):
    #     threshold=128
    #     with c as display:  #ImageDraw
    #         for n in range(0, 255):
    #             if DeviceList[n]>threshold:
    #                     drawDevice(n,display)
    # else:
    #     device.contrast(100)

    #     with c as display:  #ImageDraw
    #         drawDevice(ActivePair[0],display)
    #         drawDevice(ActivePair[1],display)

    #         setDevice(ActivePair[0],255)
    #         setDevice(ActivePair[1],255)

    #         ActivePair[0]=-1
    #         ActivePair[1]=-1

    return

def drawDevice(n,display):
    if n>=0:
        drawPixel(n%16,int(n/16),display)

    return

def drawPixel(x,y,display):
    position=int(x/8)
    if y>=8:
        position+=2

    x=(x%8)
    y=7-(y%8)+(position*8)

    display.point((y,x), fill=1)

    return

def setDeviceFromIPAddress(ipAddress,value):
    n=int(getDeviceFromIPAddress(ipAddress))
    if n!=-1:
        setDevice(n,value)

    return

def getDeviceFromIPAddress(ipAddress):
    result=-1

    if ipAddress.startswith(thisSubnet):
        n=ipAddress[len(thisSubnet)+1:]
        if len(n)>0:
            result=int(n)

    return (result)

def setDevice(n,value):
    if n>=0:
        DeviceList[n]=value
    return

def setAllDevices(value):
    for n in range(0, 255):
        DeviceList[n]=value
    return

def main():
    setAllDevices(False)
    print(getipaddress())

    setDeviceFromIPAddress(getipaddress(),True)

    try:
        _thread.start_new_thread(mapnetwork, () )
        _thread.start_new_thread(dotcpdump, () )
        _thread.start_new_thread(measurelinkquality, () )
    except:
        print ("Error: unable to start thread")

    while 1:
        drawDisplay()
        #activeDevicesBackOn()
        #time.sleep(.1)

try:
    main()
except KeyboardInterrupt:
    exit()