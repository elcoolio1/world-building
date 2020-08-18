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



def elev_color(axial):
	freq = .001
	elev = ax_center_noise(axial,freq)

	#water to beach colors
	deep_water = (0, 129, 175)
	mid_water  = (0, 171, 231)
	shallows   = (45, 199, 255)
	shore      = (234, 210, 172)
	beach      = (234, 186, 107)

	undergrowth= (23, 195, 103)
	boreal     = (14, 125, 42)
	evergreen  = (22, 67, 35)
	rock       = (78, 103, 102)
	snow       = (249, 253, 255)

	dh = 0.1

	if elev < dh*0.75:
		color = deep_water
	elif elev < dh*1:
		color = mid_water
	elif elev < dh*1.5:
		color = shallows
	elif elev < dh*2:
		color = shore
	elif elev < dh*2.5:
		color = beach
	elif elev < dh*3.5:
		color = undergrowth
	elif elev < dh*6:
		color = boreal
	elif elev < dh*7.5:
		color = evergreen
	elif elev < dh*8.1:
		color = rock
	else:
		color = snow
		
	return color

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





