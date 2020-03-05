import pygame

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

serial = spi(port=0, device=0, gpio=noop(), bus_speed_hz=16000000)
device = max7219(serial, cascaded=4)
device.contrast(0)

width, height = 16, 16

def drawPixel(x,y,c,display):
	# translate from row of four 8x8 to 16x16
	position=(int) (x/8)
	if y>=8:
		position+=2

	x=(x%8)
	y=7-(y%8)+(position*8)

	display.point((y,x), fill=c)

	return

def main():
	try:
		pygame.init()
		pygame.mouse.set_visible(False)

		fps = 60.0
		clock = pygame.time.Clock()

		c=canvas(device)    #luma.core.render.canvas2

		frameNumber = 0
		while True:
			with c as display:  #ImageDraw
				display.rectangle((0, 0, (width * height)/8, 8), fill=0)	#clear the screen

				x = frameNumber % width
				y = (int) (frameNumber / width)
				drawPixel(x,y,1,display)

			clock.tick(fps)
			frameNumber = (frameNumber + 1) % (width * height)

	except KeyboardInterrupt:
		exit()

main()

try:
	main()
except KeyboardInterrupt:
	exit()