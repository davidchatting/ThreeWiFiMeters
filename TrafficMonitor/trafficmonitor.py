import subprocess
import _thread
import os
import sys
import pygame
import math
import time
from fontTools.ttLib import TTFont
from pathlib import Path
from numpy import interp
import random

import nmap
import socket

import scapy.all
import ipaddress

screenWidth = 0
screenHeight = 0
outerClockDiameter = 0
innerClockDiameter = 0

whiteValue = 0
blackValue = 0

localRouter = ""
internetGateway = ""
remoteServer = "1.1.1.1"   #use rather than ip address so no DNS resolution required (which obvs needs network)

nm = nmap.PortScanner()
devices = ["" for x in range(256)]

connectivity = [False, False, False]

trafficArray = [0] * 60
lastReadingAtSec = 0

def initTestNetwork(intervalSec):
	try:
		_thread.start_new_thread(testNetworkThread, (intervalSec,) )
	except:
		print ("Error: unable to start thread for speed test")
	
	return

def testNetworkThread(intervalSec):
	time.sleep(random.randint(0, 60))	#attempt to unsync threads to spread the load
	while True:
		testNetwork()
		time.sleep(intervalSec)
	return

def testNetwork():
	print("testNetwork")

	global localRouter, internetGateway, remoteServer
	if len(localRouter) == 0:
		locateNetwork()

	connectivity[0] = ping(localRouter)
	connectivity[1] = ping(internetGateway)
	connectivity[2] = ping(remoteServer)

	return

def locateNetwork():
	global localRouter, internetGateway, remoteServer
	
	try:
		for i in range(1, 28):
			reply = traceroute(remoteServer,depth = i)

			if reply is not None:
				if len(localRouter) == 0:
					localRouter = reply.src

				# some gateways (at least the BT ones) don't always reply to direct pings - so are useless waypoints - so test that they do ping
				if len(internetGateway) == 0 and not ipaddress.ip_address(reply.src).is_private and ping(reply.src):
					internetGateway = reply.src

				if reply.type == 3:
					# destination reached
					break
	except socket.gaierror:
		print("can't resolve hostname")

	print("localRouter: " + localRouter)
	print("internetGateway: " + internetGateway)
	print("remoteServer:    " + remoteServer)

def ping(ipAddress):
	result = False

	reply = traceroute(ipAddress,28)
	if reply is not None:
		result = True

	return result

def traceroute(ipAddress,depth):
    pkt = scapy.all.IP(dst = ipAddress, ttl = depth) / scapy.all.UDP(dport=33434)
    # Send the packet and get a reply
    reply = scapy.all.sr1(pkt, verbose=0, timeout=2)

    return reply

def initMapNetwork(intervalSec):
	try:
		_thread.start_new_thread(mapNetworkThread, (intervalSec,) )
	except:
		print ("Error: unable to start thread for speed test")

	return

def mapNetworkThread(intervalSec):
	time.sleep(random.randint(0, 60))	#attempt to unsync threads to spread the load
	while True:
		mapNetwork()
		time.sleep(intervalSec)
		
	return

def mapNetwork():
	print("mapNetwork")
	nm.scan(hosts=getsubnet(getipaddress())+'.0/24', arguments='-R -sP -PE -PA21,23,80,3389')  #-O -R -sS -PE -PA21,23,80,3389

	for d in devices:
		d = ""
	for h in nm.all_hosts():
		ipAddress=nm[h]['addresses']['ipv4']
		# print(getDeviceFromIPAddress(ipAddress), nm[h].hostname())    #, nm[h]['osclass']    nm[h]['vendor'], 
		devices[getDeviceFromIPAddress(ipAddress)] = nm[h].hostname()
	return

def getsubnet(ipAddress):
    subnet=ipAddress[:ipAddress.rfind('.')-len(ipAddress)]
    return(subnet)

def getipaddress():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


def getDeviceFromIPAddress(ipAddress):
    result=-1

    thisSubnet = getsubnet(getipaddress())
    if ipAddress.startswith(thisSubnet):
        n=ipAddress[len(thisSubnet)+1:]
        if len(n)>0:
            result=int(n)

    return (result)

def initDisplay():
	global screen
	screen = pygame.display.set_mode((320, 480), pygame.FULLSCREEN) 

	global screenWidth
	global screenHeight
	global innerClockDiameter
	global outerClockDiameter

	global whiteValue
	global blackValue

	screenWidth = screen.get_width()
	screenHeight = screen.get_height()
	outerClockDiameter = min(screenWidth,screenHeight)-28
	innerClockDiameter = outerClockDiameter/2

	whiteValue = 200
	blackValue = 15

	return

def update(dt):
	global innerClockDiameter
	global outerClockDiameter
	global trafficArray
	global lastReadingAtSec

	sec = time.localtime().tm_sec
	if(sec != lastReadingAtSec):
		trafficArray[sec] = random.randint(0, 25000)
		lastReadingAtSec = sec

	for event in pygame.event.get():
		#if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()

	return

#keep everything on the "grid"
def quantiseAngle(a):
	da = (2 * math.pi) / 720	#resolution of 0.5 degree
	
	n = math.ceil(a/da)
	result = n * da

	return result

def drawArc(screen, fill, cx, cy, radius, startAngleRad, stopAngleRad):
	p = [(cx, cy)]

	a = quantiseAngle(startAngleRad)
	da = (2 * math.pi) / 360	#resolution of 1 degree
	while True:
		x = cx + int(radius*math.cos(a))
		y = cy + int(radius*math.sin(a))
		p.append((x, y))

		if a >= stopAngleRad:
			break

		a = quantiseAngle(a + da)
	p.append((cx, cy))

	if len(p) > 2:
	    pygame.draw.polygon(screen, (fill, fill, fill), p, 1)

def drawDevices(cx, cy, bandWidth, screen):
	radius = int(3.5 * bandWidth)
	circumference = 2 * radius * math.pi
	deviceRadius = int((circumference/256)/2 - 2)

	# pygame.draw.circle(screen, (blackValue,blackValue,blackValue), (cx, cy), radius, 1)

	da = (2 * math.pi) / 255
	for i, d in enumerate(devices):
		if len(d) != 0:
			a = i * da
			x = int(cx + radius * math.cos(a))
			y = int(cy + radius * math.sin(a))
			pygame.draw.circle(screen, (whiteValue,whiteValue,whiteValue), (x, y), deviceRadius, 0)

	return

def drawConnectivity(cx, cy, bandWidth, screen):
	connectedWidth = int(bandWidth)
	disconnectedWidth = int(connectedWidth/3)
	
	localWidth = disconnectedWidth
	gatewayWidth = disconnectedWidth
	remoteWidth = disconnectedWidth
	if(connectivity[0]):
		localWidth = connectedWidth
		if(connectivity[1]):
			gatewayWidth = connectedWidth
			if(connectivity[2]):
				remoteWidth = connectedWidth

	pygame.draw.circle(screen, (whiteValue,whiteValue,whiteValue), (cx, cy), localWidth + gatewayWidth + remoteWidth, 0)
	pygame.draw.circle(screen, (blackValue,blackValue,blackValue), (cx, cy), localWidth + gatewayWidth, 0)
	pygame.draw.circle(screen, (whiteValue,whiteValue,whiteValue), (cx, cy), localWidth, 0)

	return

def drawActivity(cx, cy, bandWidth, screen):
	radius = int(4 * bandWidth)

	# pygame.draw.circle(screen, (whiteValue,whiteValue,whiteValue), (cx, cy), radius, 1)
	da = (2 * math.pi)/60.0

	n = lastReadingAtSec + 1

	while True:
		if n == 60:
			n = 0

		a = (n*da)+(math.pi/2);	# 0 is at 12 o'clock
		r = interp(trafficArray[n], [0,25000], [radius, radius + bandWidth]) #32768
		# r = radius
		
		dt=lastReadingAtSec-n
		if dt < 0:
			dt = 60 + dt
		fillValue = interp(dt, [0,59], [whiteValue,blackValue])

		startAngleRad = a-(da/2)
		stopAngleRad = a+(da/2)
		drawArc(screen, fillValue, cx, cy, r, startAngleRad, stopAngleRad)

		if n == lastReadingAtSec:
			break

		n += 1

	return

def drawArc(screen, fill, cx, cy, radius, startAngleRad, stopAngleRad):
	# p = [(cx, cy)]
	p = []

	a = quantiseAngle(startAngleRad)
	da = (1 * math.pi) / 360	#resolution of 0.5 degree
	while True:
		x = cx + int(radius*math.cos(a))
		y = cy + int(radius*math.sin(a))
		p.append((x, y))

		if a >= stopAngleRad:
			break

		a = quantiseAngle(a + da)
	# p.append((cx, cy))

	if len(p) > 2:
		pygame.draw.polygon(screen, (fill, fill, fill), p, 1)

	return

def draw(screen):
	screen.fill((0, 0, 0))

	timeSec = time.localtime().tm_sec

	global screenWidth
	global screenHeight
	global innerClockDiameter
	global outerClockDiameter

	global whiteValue
	global blackValue

	cx = int(screenWidth/2)
	cy = int(screenHeight-(screenWidth/2)) + 10 # put it at the bottom of the screen

	pygame.draw.circle(screen, (blackValue,blackValue,blackValue), (cx, cy), int(outerClockDiameter/2), 1)

	bandWidth = (outerClockDiameter/2)/6	# the interface is drawn in bands

	drawConnectivity(cx, cy, bandWidth, screen)
	drawDevices(cx, cy, bandWidth, screen)
	drawActivity(cx, cy, bandWidth, screen)

	pygame.display.flip()

	return

def main():
	try:
		random.seed()

		initDisplay()
		pygame.init()
		pygame.mouse.set_visible(False)

		initMapNetwork(60)
		initTestNetwork(60)

		fps = 60.0
		clock = pygame.time.Clock()

		dt = 1/fps

		while True:
			update(dt)
			draw(screen)

			dt = clock.tick(fps)

	except KeyboardInterrupt:
		exit()

main()