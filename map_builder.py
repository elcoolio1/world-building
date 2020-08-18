from hex_functions import *
from generator_functions import *
import arcade
import sys


scale = 20 #size of hexes
size = (66,66) #number of hexes

display_init(scale,size)
arcade.start_render()


for q in range(-40,40):
	for r in range(-66,66):
		if ax_distance((q,r),(0,0)) < 33:

			loc = (q,r)
			draw_hex(loc)


# for x in range(0,1000):
# 	for y in range(0,1000):
# 		loc = x,y
# 		color = elev_color(loc)

arcade.finish_render()
arcade.run()
