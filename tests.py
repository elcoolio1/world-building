from hex_functions import *
import pygame
import sys



screen = display_init()


while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		loc = (q,r)
		draw_hex(loc)
		draw_center(loc)
		draw_coords(loc)
		print(loc)

	pygame.display.flip()
