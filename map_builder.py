from hex_functions import *
from generator_functions import *
import pygame
import sys


scale = 20 #size of hexes
size = (66,66) #number of hexes

screen = display_init(scale,size)


# for q in range(-40,40):
# 	for r in range(-66,66):
# 		draw_line(p1,p2)
# 		if ax_distance((q,r),(0,0)) < 33:

# 			loc = (q,r)
# 			draw_cluster(q,r)


for x in range(0,1000):
	for y in range(0,1000):
		loc = x,y
		color = elev_color(loc)
		screen.set_at(loc, color)

pygame.display.flip()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
