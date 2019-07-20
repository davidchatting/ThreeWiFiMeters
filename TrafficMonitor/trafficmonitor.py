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

import scapy.all

screenWidth = 0
screenHeight = 0
outerClockDiameter = 0
innerClockDiameter = 0

whiteValue = 0
blackValue = 0

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
	global innerClockDiameter
	global outerClockDiameter

	global whiteValue
	global blackValue

	cx = int(screenWidth/2)
	cy = int(screenHeight-(screenWidth/2)) + 10 # put it at the bottom of the screen

	pygame.gfxdraw.circle(screen, cx, cy, int(outerClockDiameter/2),  (whiteValue,whiteValue,whiteValue))
	
	pygame.display.flip()

	return

def main():
	try:
		random.seed()

		initDisplay()
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