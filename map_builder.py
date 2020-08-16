from hex_functions import *
import pygame
import sys


scale = 20 #size of hexes
size = (66,66) #number of hexes

screen = display_init(scale,size)
white = 255,255,255
green = 0,255,0
blue = 0,0,255

# while 1:


# for q in range(-40,40):
# 	for r in range(-66,66):
# 		if ax_distance((q,r),(0,0)) < 33:

# 			loc = (q,r)
# 			draw_hex(loc,white)
# 			draw_hex_outline(loc)

# 		else:
# 			loc = (q,r)
# 			draw_hex_outline(loc,white)
# 			# draw_hex(loc)
# 			# draw_center(loc)
for q in range(-40,40):
	for r in range(-66,66):
		if ax_distance((q,r),(0,0)) < 33:

			loc = (q,r)
			draw_hex(loc,white)
			draw_hex_outline(loc)

			

			if q%4==0:
				if r%4==0:
					draw_hex(loc,green)
					draw_coords(loc)








pygame.display.flip()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
