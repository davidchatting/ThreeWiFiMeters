#! /usr/bin/python
import NetworkManager as NM
#network devices - eg wlan0 - ensure that denyinterface set in dchpcd.conf otherwise will be unavailable
#import wireless as Wireless
import subprocess
import os
import pygame

def dotcpdump(device):
	#for some reason have to construct command like this - doesn't work with individual arguments - denies that network interfaces exist!
	tcpdump = subprocess.Popen(('sudo tcpdump -lnt -i ' + device), stdout=subprocess.PIPE, shell=True)
	while True:
		packet=tcpdump.stdout.readline().decode("utf-8")
		parsetcpdump(packet)

	return

def parsetcpdump(packet):
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
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        print("I'm running under X display = {0}".format(disp_no))

    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib']
    found = False
    for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print('Driver: {0} failed.'.format(driver))
            continue
        found = True
        break

    if not found:
        raise Exception('No suitable video driver found!')

    screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    global screen
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    return

def update(dt):
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

def draw(screen):
  screen.fill((0, 0, 0))

  timeMs = pygame.time.get_ticks()

  screenWidth = screen.get_width()
  screenHeight = screen.get_height()

  pygame.draw.rect(screen,(255,255,255),(screenWidth/4,screenHeight/4,screenWidth/2,screenHeight/2))

  pygame.display.flip()

def main():
	try:
		# joinnetwork()
		# dotcpdump('eth0')

		pygame.init()
		pygame.mouse.set_visible(False)
		initDisplay()
		
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
