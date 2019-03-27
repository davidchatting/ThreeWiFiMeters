
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
from random import randint

screenWidth = 0
screenHeight = 0
outerClockDiameter = 0
innerClockDiameter = 0

whiteValue = 0
blackValue = 0

def initMapNetwork(intervalSec):
	try:
		_thread.start_new_thread(mapnetworkThread, (intervalSec,) )
	except:
		print ("Error: unable to start thread for speed test")

	return

def mapnetworkThread(intervalSec):
	while True:
		print("mapnetworkThread")
		time.sleep(intervalSec)
		
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

	global whiteValue
	global blackValue

	cx = int(screenWidth/2)
	cy = int(screenHeight-(screenWidth/2)) + 10 #put it at the bottom of the screen

	pygame.draw.circle(screen, (0,0,0), (cx, cy), int(innerClockDiameter/2)-2, 0)
	pygame.draw.circle(screen, (blackValue,blackValue,blackValue), (cx, cy), int(innerClockDiameter/2)-2, 1)

	pygame.display.flip()

	return

def main():
	try:
		initDisplay()
		pygame.init()
		pygame.mouse.set_visible(False)

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