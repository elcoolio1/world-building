from hex_functions import *
import pygame
import time

import sys
pygame.init()

hex_scale = 50 #hex R in pixels
hex_size = hex_width, hex_height= 20, 20 #number of hexagons hor/vert to fit in window
size = width, height = (hex_width+2)*hex_scale, (hex_height+2)*hex_scale
center_x = int(width/2)
center_y = int(height/2)
origin = (center_x,center_y)
grid_thickness = int(0.1)

red = 255, 0, 0
white = 255,255,255

screen = pygame.display.set_mode(size)
print(width)

while 1:
	pygame.draw.circle(screen,white,origin,5)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	for i in range(-10,10):
		for j in range(-10,10):
			pygame.draw.aalines(
				screen, 
				red,
				True,
				draw_px_hx(
					ax2px((i,j)),
					hex_scale,
					origin
				),
				grid_thickness
			)
			print(i,j)
			print(ax2px((i,j)))
	
	pygame.display.flip()
