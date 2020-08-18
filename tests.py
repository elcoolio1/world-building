from hex_functions import *
import pygame
import sys
from generator_functions import *


scale = 20 #size of hexes
size = (66,66) #number of hexes

screen = display_init(scale,size)


white = 255,255,255
green = 0,255,0
blue = 0,0,255
black = 0,0,0
screen.fill(black)

cluster_points = [(0,0), (2,-5), (5,-3), (3,2), (-2,5), (-3,-2), (-5,3), (1,7), (-7,8), (-8,1), (-1,-7), (7,-8), (-6,-4), (6,4), (8,-1), (10,-6), (4,-10), (-10,6), (-4,10)]

# def random_color_range(min,max):
# 	color = (random.randint(min,max),random.randint(min,max),random.randint(min,max))
# 	# print(color)
# 	return color

# for i in range(len(cluster_points)):
# 	color = random_color_range(0,25)
# 	draw_cluster(cluster_points[i],color,2,False)
# 	draw_cluster_center(cluster_points[i],white,.5,True)





#grid
for q in range(-60,60):
	for r in range(-60,60):
		if ax_distance((q,r),(0,0)) < 30:
			loc = (q,r)
			# draw_hex_outline(loc)
			draw_hex(loc,elev_color(loc))
			# draw_hex_outline(loc,(150,150,150))


pygame.display.flip()


while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()





