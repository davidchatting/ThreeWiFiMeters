#! /usr/bin/python
import NetworkManager as NM
#network devices - eg wlan0 - ensure that denyinterface set in dchpcd.conf otherwise will be unavailable
#import wireless as Wireless
import subprocess
import os
import pygame
import math
import time
from fontTools.ttLib import TTFont

def initNetworkScan(device):
	#for some reason have to construct command like this - doesn't work with individual arguments - denies that network interfaces exist!
	tcpdump = subprocess.Popen(('sudo tcpdump -lnt -i ' + device), stdout=subprocess.PIPE, shell=True)
	while True:
		packet=tcpdump.stdout.readline().decode("utf-8")
		parsetcpdump(packet)

	return

def parsetcpdump(packet):
  print(packet)
  
	s = 'length'
	lengthIndex = packet.find(s)
	if(lengthIndex != -1):
		length = int(packet[lengthIndex+len(s):].strip())
		print(length)

	return

def joinnetwork():
	try:
		device.RequestScan({})
		allAccessPoints = device.GetAllAccessPoints()
		allAccessPoints.sort(key=lambda ap: ap.Strength, reverse=True)

		for ap in allAccessPoints:
			info = {
				'ssid': ap.Ssid,
				'frequency': ap.Frequency,
				'level': ap.Strength
			}
			print(info)
	except:
		print("probably scanned too soon")

	device = NM.NetworkManager.GetDeviceByIpIface('wlan1')

	ssidToMonitor = 'BTHub4-W3MZ'   #will be obtained from UI using previous scan
	password = '2426adca59'

	#this step only required to ensure that the monitor is used on a network the user owns
	#Wireless.connect(ssid=ssidToMonitor, password=password)

	#if this is a 5Ghz network need to see if 2.4GHz also exists and spin up wlan0 if it does

def initDisplay():
    # disp_no = os.getenv("DISPLAY")

    # if disp_no:
    #     print("I'm running under X display = {0}".format(disp_no))

    # # Check which frame buffer drivers are available
    # # Start with fbcon since directfb hangs with composite output
    # drivers = ['fbcon', 'directfb', 'svgalib']
    # found = False
    # for driver in drivers:
    #     # Make sure that SDL_VIDEODRIVER is set
    #     if not os.getenv('SDL_VIDEODRIVER'):
    #         os.putenv('SDL_VIDEODRIVER', driver)
    #     try:
    #         pygame.display.init()
    #     except pygame.error:
    #         print('Driver: {0} failed.'.format(driver))
    #         continue
    #     found = True
    #     break

    # if not found:
    #     raise Exception('No suitable video driver found!')

    # screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    # global screen
    # screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    global screen
    screen = pygame.display.set_mode((320, 480), pygame.FULLSCREEN) 
    
    return

def update(dt):
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

def draw(screen):
  screen.fill((0, 0, 0))

  # timeMs = pygame.time.get_ticks()
  # timeSec = int((timeMs/1000) % 60)

  timeSec = time.localtime().tm_sec

  screenWidth = screen.get_width()
  screenHeight = screen.get_height()
  clockDiameter = min(screenWidth,screenHeight)-20
  cx = int(screenWidth/2)
  cy = int(screenWidth/2) #put it at the top of the screen

  pygame.draw.circle(screen, (100,100,100), (cx, cy), int(clockDiameter/2), 1)

  #pygame.draw.rect(screen,(255,255,255),(screenWidth/4,screenHeight/4,screenWidth/2,screenHeight/2))
  da = (2 * math.pi)/60.0
  
  a = (timeSec*-da)+(math.pi/2);  #0 is at 12 o'clock
  pygame.draw.arc(screen, (255,255,255), (cx-(clockDiameter/2), cy-(clockDiameter/2), clockDiameter, clockDiameter), a-(da/2), a+(da/2), 1)

  font = pygame.font.Font('HelveticaNeue-UltraLight.ttf', 22)

  label = font.render("Some text!", 1, (255,255,255))
  
  text_rect = label.get_rect(center=(cx,cy))

  screen.blit(label, text_rect)

  # gfxdraw.arc(screen, int((screenWidth/2)-(clockDiameter/2)), int((screenHeight/2)-(clockDiameter/2)), int(clockDiameter/2), int(math.degrees(a)), int(math.degrees(a+da)), (255,255,255))


    # int n = lastReadingAtSec + 1;  //draw the clock oldest values first
    # boolean finished = false;
    # do {
    #   if(n == buffer.length) n = 0;
       
      
    #   float l = (panelWidth/2)+map(buffer[n], 0, 100000, 0, maxValue);
    #   l=min(l,maxValue);
      
    #   //if(v!=0) point(100+(v*sin(a+PI)),100+(v*cos(a+PI)));
      
    #   int t=lastReadingAtSec-n;
    #   t=t<0?60+t:t;
    #   t=(int)map(t,0,60,whiteValue,blackValue);
    #   stroke(t, t, t);
    #   arc(width/2, height/2, l*2, l*2, -a-HALF_PI, -a-HALF_PI+da, PIE);
      
    #   if(n==lastReadingAtSec) finished = true;
    #   else ++n;
    # } while(!finished);

  pygame.display.flip()

def main():
  try:
    # joinnetwork()
    # initNetworkScan('eth0')

    #initDisplay()
    pygame.init()
    pygame.mouse.set_visible(False)

    fps = 60.0
    clock = pygame.time.Clock()

    dt = 1/fps

    while True:
      update(dt)
      #draw(screen)

      dt = clock.tick(fps)
  except KeyboardInterrupt:
    exit()

main()

#NM.NetworkManager.ActivateConnection('/',device, '/')

#conn = NM.Settings.ListConnections()[0]
#print(conn)

#---

# import NetworkManager
# import sys

# # Find the connection
# name = 'Wired connection 1'
# connections = NetworkManager.Settings.ListConnections()
# connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
# print(connections)
# conn = connections[name]

# # Find a suitable device
# ctype = conn.GetSettings()['connection']['type']
# if ctype == 'vpn':
#     for dev in NetworkManager.NetworkManager.GetDevices():
#         if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED and dev.Managed:
#             break
#     else:
#         print("No active, managed device found")
#         sys.exit(1)
# else:
#     dtype = {
#         '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI,
#         '802-3-ethernet': NetworkManager.NM_DEVICE_TYPE_ETHERNET,
#         'gsm': NetworkManager.NM_DEVICE_TYPE_MODEM,
#     }.get(ctype,ctype)
#     devices = NetworkManager.NetworkManager.GetDevices()

#     for dev in devices:
#         if dev.DeviceType == dtype and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
#             break
#     else:
#         print("No suitable and available %s device found" % ctype)
#         sys.exit(1)

# # And connect
# NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
