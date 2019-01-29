#! /usr/bin/python
import NetworkManager as NM
#network devices - eg wlan0 - ensure that denyinterface set in dchpcd.conf otherwise will be unavailable
#import wireless as Wireless
import speedtest
import subprocess
import _thread
import os
import pygame
import math
import time
from fontTools.ttLib import TTFont
from pathlib import Path
from numpy import interp
from random import randint

import nmap
nmapPortScanner = nmap.PortScanner()             # instantiate nmap.PortScanner object
import socket

from numpy import ndarray 
DeviceList = ndarray((256,),bool)

def getipaddress():
    return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

thisIP = getipaddress()

def getsubnet():
    subnet=getipaddress()
    subnet=subnet[:subnet.rfind('.')-len(subnet)]
    return(subnet)

thisSubnet = getsubnet()


def getDeviceFromIPAddress(ipAddress):
    result=-1

    if ipAddress.startswith(thisSubnet):
        n=ipAddress[len(thisSubnet)+1:]
        if len(n)>0:
            result=int(n)

    return (result)


downMbps = 0
upMbps = 0

capFile = Path() / 'capture-01.cap'
previousCapFileSize = 0

trafficArray = [0] * 60

screenWidth = 0
screenHeight = 0
outerClockDiameter = 0
innerClockDiameter = 0

whiteValue = 0
blackValue = 0

lastReadingAtSec = 0

def utils_wifi_freq_to_channel(mhz):
	return {
		2412: 1,
		2417: 2,
		2422: 3,
		2427: 4,
		2432: 5,
		2437: 6,
		2442: 7,
		2447: 8,
		2452: 9,
		2457: 10,
		2462: 11,
		2467: 12,
		2472: 13,
		2484: 14,
		5180: 36,
		5190: 38,
		5200: 40,
		5210: 42,
		5220: 44,
		5230: 46,
		5240: 48,
		5260: 52,
		5280: 56,
		5300: 60,
		5320: 64
	}.get(mhz)


def initNetwork():
	#joinnetwork()

	# connectionInterface = 'wlan0'
	# scannerInterface = 'wlan1'

	# connection = NM.NetworkManager.GetDeviceByIpIface(connectionInterface)
	# scanner = NM.NetworkManager.GetDeviceByIpIface(scannerInterface)

	# homeSSID = connection.ActiveAccessPoint.Ssid

	# scanner.RequestScan({})
	# allAccessPoints = scanner.GetAllAccessPoints()	#returns array of NetworkManager.AccessPoint objects
	# allAccessPoints.sort(key=lambda ap: ap.Strength, reverse=True)

	# for ap in allAccessPoints:
	# 	#potentially more than one match (wifi repeaters 2.4 vs 5g networks etc)
	# 	if ap.Ssid == homeSSID:
	# 		#subprocess.Popen('sudo airmon-ng stop ' + scannerInterface + 'mon', shell=False)	#, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
	# 		#subprocess.Popen('sudo airmon-ng start ' + scannerInterface, shell=False)	#, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT

	# 		cmd = 'sudo airodump-ng --bssid "' + ap.HwAddress + '" --channel ' + str(utils_wifi_freq_to_channel(ap.Frequency)) + ' -w capture ' + scannerInterface + 'mon' + ' --write-interval 1 --output-format pcap'
	# 		print(cmd)
	# 		airodump = subprocess.Popen(cmd, shell=True) #, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
	# 		break
	
	cmd = 'sudo airodump-ng --bssid "' + '00:25:BC:8D:2D:BC' + '" --channel ' + str(36) + ' -w capture ' + 'wlan1' + 'mon' + ' --write-interval 1 --output-format pcap'
	print(cmd)
	#airodump = subprocess.Popen(cmd, shell=True) #, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT

def initMapNetwork(intervalSec):
	try:
		_thread.start_new_thread(mapnetworkThread, (intervalSec,) )
	except:
		print ("Error: unable to start thread for speed test")

	return

def mapnetworkThread(intervalSec):
	global DeviceList

	while True:
		print('----------------------------------------------------')

		nmapPortScanner.scan(hosts=getsubnet()+'.0/24', arguments='-R -sP -PE -PA21,23,80,3389')  #-O -R -sS -PE -PA21,23,80,3389

		for n in range(0, 255):
			DeviceList[n]=False

		for h in nmapPortScanner.all_hosts():
			ipAddress=nmapPortScanner[h]['addresses']['ipv4']

			DeviceList[getDeviceFromIPAddress(ipAddress)]=True
			print(getDeviceFromIPAddress(ipAddress), ipAddress, nmapPortScanner[h]['vendor'], nmapPortScanner[h].hostname())    #, nm[h]['osclass']
		
		time.sleep(intervalSec)
	return

def getTraffic():
	traffic = 0

	capFileSize = 0

	global previousCapFileSize
	global capFile

	if(capFile.exists()):
		capFileSize = capFile.stat().st_size
		traffic = (capFileSize - previousCapFileSize)
		previousCapFileSize = capFileSize

	return traffic

def initSpeedTest(intervalSec):
	try:
		_thread.start_new_thread(speedtestThread, (intervalSec,) )
	except:
		print ("Error: unable to start thread for speed test")

	return

def speedtestThread(intervalSec):
	speedtestDueAtSec = 0

	while True:
		nowSec = time.time()
		if(nowSec > speedtestDueAtSec):
			speedtestDueAtSec = nowSec + intervalSec
			doSpeedtest()
		else:
			time.sleep(intervalSec)

	return

def doSpeedtest():
	global downMbps
	global upMbps

	print("start speed test")
	#takes about 1 minute to complete
	servers = []
	# If you want to test against a specific server
	# servers = [1234]

	s = speedtest.Speedtest()
	s.get_servers(servers)
	s.get_best_server()
	s.download()
	s.upload()
	s.results.share()

	results_dict = s.results.dict()

	
	downMbps = results_dict['download'] / 1000000
	upMbps = results_dict['upload'] / 1000000

	print('{0:.2f}'.format(downMbps))
	print('{0:.2f}'.format(upMbps))

	return

def joinnetwork():
	ssidToMonitor = 'BTHub4-W3MZ' #will be obtained from UI using previous scan
	password = ''

	#this step only required to ensure that the monitor is used on a network the user owns
	#Wireless.connect(ssid=ssidToMonitor, password=password)

	#if this is a 5Ghz network need to see if 2.4GHz also exists and spin up wlan0 if it does

	return

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
		trafficArray[sec] = getTraffic()	#randint(0, 10000)
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

def draw(screen):
	screen.fill((0, 0, 0))

	# timeMs = pygame.time.get_ticks()
	# timeSec = int((timeMs/1000) % 60)

	timeSec = time.localtime().tm_sec

	global screenWidth
	global screenHeight
	global innerClockDiameter
	global outerClockDiameter
	global trafficArray

	global whiteValue
	global blackValue

	global DeviceList

	cx = int(screenWidth/2)
	cy = int(screenHeight-(screenWidth/2)) + 10 #put it at the bottom of the screen

	da = (2 * math.pi)/60.0

	n = lastReadingAtSec + 1
	while True:
		if n == 60:
			n = 0
		
		a = (n*da)+(math.pi/2);	#0 is at 12 o'clock
		r = interp(trafficArray[n], [0,25000], [innerClockDiameter/2,outerClockDiameter/2]) #32768
		
		dt=lastReadingAtSec-n;
		if dt < 0:
			dt = 60 + dt
		fillValue = interp(dt, [0,59], [whiteValue,blackValue])

		startAngleRad = a-(da/2)
		stopAngleRad = a+(da/2)
		drawArc(screen, fillValue, cx, cy, r, startAngleRad, stopAngleRad)

		if n == lastReadingAtSec:
			break

		n += 1

	pygame.draw.circle(screen, (0,0,0), (cx, cy), int(innerClockDiameter/2)-2, 0)
	pygame.draw.circle(screen, (blackValue,blackValue,blackValue), (cx, cy), int(innerClockDiameter/2)-2, 1)

	font = pygame.font.Font('data/SempliceRegular.ttf', 11)

	global downMbps
	global upMbps

	numberOfDevices = 0
	deviceRingRadiusMin = int(256/math.pi)/2
	for n in range(0, 255):
		if DeviceList[n] == True:
			a = ((2 * math.pi)/256)*n

			pygame.draw.circle(screen, (255,255,255), (cx + int(deviceRingRadiusMin*math.cos(a)), cy + int(deviceRingRadiusMin*math.sin(a))), 3, 1)
    		#point(cx+(deviceRingDiameterMin/2)*cos(a),cy+(deviceRingDiameterMin/2)*sin(a))
			#print('device',n)
			numberOfDevices = numberOfDevices + 1
	
	downLabel = font.render('{0:.2f}'.format(numberOfDevices), 1, (whiteValue,whiteValue,whiteValue))
	#downLabel = font.render('{0:.2f}'.format(downMbps), 1, (whiteValue,whiteValue,whiteValue))
	#downLabel = font.render('00:25:BC:8D:2D:BC', False, (whiteValue,whiteValue,whiteValue))

	text_rect = downLabel.get_rect(center=(cx,cy))

	screen.blit(downLabel, text_rect)

	pygame.display.flip()

	return

def main():
	try:
		initDisplay()
		pygame.init()
		pygame.mouse.set_visible(False)

		#initNetwork()
		#initSpeedTest(900)	#900 seconds is a 15 minute interval
		initMapNetwork(60)

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



#mapnetwork()