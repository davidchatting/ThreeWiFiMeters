import subprocess
import _thread
import os
import sys
import pygame
from pygame import gfxdraw
import math
import time
from fontTools.ttLib import TTFont
from pathlib import Path
import random

from scapy.all import *

screenWidth = 0
screenHeight = 0
portalDiameter = 0

whiteValue = 0
blackValue = 0

apSSID = "HackMyHouse"
apMacAddress = ""

def PacketHandler(packet) :
	global apMacAddress

	if hasattr(packet, 'type') :
		# DATA packet
		if packet.type == 2 :
			iPhoneMacAddress = 'a0:d7:95:39:b4:44'

			print(packet.type)

			if hasattr(packet, 'addr1') :
				if packet.addr1 == iPhoneMacAddress or packet.addr2 == iPhoneMacAddress or packet.addr3 == iPhoneMacAddress :
					# packet.show()
					numOfBytes = 0
					if hasattr(packet, 'wepdata') : numOfBytes = len(packet.wepdata)

					sndMacAddress = packet.addr1
					recMacAddress = packet.addr2

					if recMacAddress == apMacAddress :
						drawPacket(sndMacAddress, True, numOfBytes)
					elif sndMacAddress == apMacAddress :
						drawPacket(recMacAddress, False, numOfBytes)
					print("{}	{}	{}	{}	{}".format(packet.addr1, packet.addr2, packet.addr3, numOfBytes, apMacAddress))

		# CONTROL packet
		if packet.type == 2 :
			if packet.subtype == 8 and hasattr(packet, 'info') and packet.info.decode() == apSSID :
				apMacAddress = packet.addr3

	return

def drawPacket(deviceAddress, direction, numOfBytes) :
	print("{}	{}	{}".format(deviceAddress, direction, numOfBytes))

	return

def getPositionFromMacAddress(macAddress) :
	global screenWidth
	global screenHeight
	global portalDiameter

	x = screenWidth / 2
	y = screenHeight / 2

	hex = macAddress.split(":")
	oui = int(hex[0] + hex[1] + hex[2], 16)
	device = int(hex[3] + hex[4] + hex[5], 16)

	a = ((oui & 0x00FFFF00) >> 8) / float(0xFFFF)
	d = ((oui & 0x000000FF) >> 0) / float(0x00FF)

	# but runs of devices might be quite close... so small differerence need to be visible...
	da = (device % 0xFF) / float(0xFF)

	r = portalDiameter / 2
	dr = r * 0.05

	x = (d * r * math.cos(a * math.pi * 2)) + (screenWidth/2) + (dr * math.cos(da * math.pi * 2))
	y = (d * r * math.sin(a * math.pi * 2)) + (screenHeight/2) + (dr * math.sin(da * math.pi * 2))

	return int(x), int(y)

def initNetwork() :
	# sudo airmon-ng start wlan1 1
	sniff(iface="wlan1mon", prn = PacketHandler, store=0)	#, filter="type Data"

	# t = AsyncSniffer(iface="wlan1mon", prn = PacketHandler, store=False, filter="tcp")
	# t.start()
	# time.sleep(20)
	# t.stop()

	return

def initDisplay():
	global screen
	screen = pygame.display.set_mode((320, 480), pygame.FULLSCREEN) 

	global screenWidth
	global screenHeight
	global portalDiameter

	global whiteValue
	global blackValue

	screenWidth = screen.get_width()
	screenHeight = screen.get_height()
	portalDiameter = min(screenWidth,screenHeight)-28

	whiteValue = 200
	blackValue = 15

	return

def update(dt):
	for event in pygame.event.get():
		#if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()

	return

def draw(screen):
	screen.fill((0, 0, 0))

	timeSec = time.localtime().tm_sec

	global screenWidth
	global screenHeight
	global portalDiameter

	global whiteValue
	global blackValue

	cx = int(screenWidth/2)
	cy = int(screenHeight-(screenWidth/2)) + 10 # put it at the bottom of the screen

	pygame.gfxdraw.circle(screen, cx, cy, int(portalDiameter/2),  (whiteValue,whiteValue,whiteValue))

	pygame.display.flip()

	return

def main():
	try:
		random.seed()

		initNetwork()
		initDisplay()
		# print(getPositionFromMacAddress('b0:72:bf:25:c3:41'))
		pygame.init()
		pygame.mouse.set_visible(False)

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