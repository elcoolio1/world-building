from hex_functions import *
import pygame
import sys



screen = display_init()
p1 = (0,0)
p2 = (12,-4)
screen.fill((255,255,255))
white = 255,255,255
green = 0,255,0
blue = 0,0,255

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

		# loc = (q,r)
		# draw_hex(loc)
		# draw_center(loc)
		# draw_coords(loc)
		# print(loc)

	flipped = px2ax(ax2px(p2))
	print('original',p2)
	print('converted',flipped)

	draw_hex(flipped,blue)
	draw_hex(p2,green)
	draw_line(p1,p2)
	draw_coords(p1)
	draw_coords(p2)

	pygame.display.flip()



