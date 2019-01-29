#!/usr/bin/python
import os
import sys
import time
import pygame

os.environ['SDL_VIDEODRIVER'] = 'Allwinner A10/A13 FBDEV'
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ["SDL_MOUSEDEV"] = "/dev/input/event2"

pygame.init()
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
gpos =(0,0)
bgimage = pygame.image.load('bg0003.jpg')
bgimage = pygame.transform.scale(bgimage, (320,240))
screen = pygame.display.set_mode((320,240))

screen.fill (black)
screen.blit(bgimage, (0,0))
myfont = pygame.font.SysFont("Computerfont",40)
prglabel  = myfont.render('Test cheapo TFT', 1, white)
pygame.draw.rect(screen, blue, (0,0,480,40),)
screen.blit(prglabel, (40, 5))
pygame.display.update()
while True:
   for event in pygame.event.get():
      if event.type == 6:
         cpos = pygame.mouse.get_pos()
         if (cpos <> gpos):
            print cpos
            gpos = cpos
