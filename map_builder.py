from hex_functions import *
import pygame
import sys


scale = 20 #size of hexes
size = (66,66) #number of hexes

screen = display_init(scale,size)
white = 255,255,255
green = 0,255,0
blue = 0,0,255
p1 = (0,0)
p2 = (12,-4)

for q in range(-40,40):
	for r in range(-66,66):
		draw_line(p1,p2)
		if ax_distance((q,r),(0,0)) < 33:

			loc = (q,r)
			draw_cluster(q,r)



pygame.display.flip()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
