from hex_functions import *
import pygame
import sys




screen = display_init()


while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	for q in range(-13,14):
		for r in range(-17,18):
			loc = (q,r)
			draw_hex(loc)
			draw_center(loc)
			draw_coords(loc)

			

	pygame.display.flip()
