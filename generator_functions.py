"""
Functions for generating based on noise gen
"""
from hex_functions import *
from noise import snoise2


def ax_center_noise(axial,freq=0.1):
	pixel = ax2px(axial)
	x = pixel[0]
	y = pixel[1]
	# gen = SimplexNoise()
	# noise = fns.Noise()
	# noise.genFromCoords((x*freq,y*freq))/2+0.5
	noise = snoise2(x*freq,y*freq)/2 + 0.5 #/2+.5 moves values into 0 ... 1 from -1 ... 1
	return noise

def px_noise(pixel,freq=0.1):
	x = pixel[0]
	y = pixel[1]
	# noise = fns.Noise()
	# noise.genFromCoords((x*freq,y*freq))/2+0.5
	# gen = SimplexNoise()
	noise = snoise2(x*freq,y*freq)/2 + 0.5 #/2+.5 moves values into 0 ... 1 from -1 ... 1
	return noise

def elev(xy,freq=0.1,octaves=3,power=3):
	elev = 0
	max_elev = 0
	for i in range(octaves):
		elev = elev + (1/2**i)*px_noise(xy,freq*(2**i))
		max_elev = max_elev + (1/2**i)
	elev = elev/max_elev
	elev = elev**power
	return elev


def elev_color_sections(e,break_points=[0.55,0.6,0.7,0.8,0.5]):
	sea_level = break_points[0]
	beach_line = break_points[1]
	tree_line = break_points[2]
	snow_line = break_points[3]
	space_level = break_points[4]

	dsea = sea_level-space_level
	dbeach = beach_line-sea_level
	# dtree = tree_line-beach_line
	dtree = tree_line-sea_level
	drock = snow_line-tree_line
	dsnow = 1-snow_line
	dspace = space_level-0

	dark_blue = 5,18,64
	light_blue = 45, 199, 255

	shore = 234, 210, 172
	beach = 234, 186, 107

	undergrowth= 12, 150, 95
	evergreen  = 22, 67, 35

	light_rock = 103, 98, 92
	dark_rock = 170, 167, 161

	off_white = 160, 205, 217
	pure_white = 255,255,255

	purple_space = 56, 4, 99
	dark_space = 0, 0, 0

	outer_rock = 87, 92, 88
	inner_rock = 119, 122, 119

	if e< space_level:
		color = color_grad(dark_space,purple_space,(e)/dspace)
	elif e < sea_level:
		color = color_grad(outer_rock,inner_rock,(e-space_level)/dsea)
	# elif e < beach_line:
	# 	color = color_grad(beach,shore,(e-sea_level)/dbeach)
	elif e < tree_line:
		color = color_grad(undergrowth,evergreen,(e-sea_level)/dtree)
	elif e < snow_line:
		color = color_grad(light_rock,dark_rock,(e-tree_line)/drock)
	else:
		color = color_grad(off_white,pure_white,(e-snow_line)*5/dsnow)
	return color

def color_grad(map1,map2,percent):
	percent = clamp(percent,0,1)
	red = map1[0]+(map2[0]-map1[0])*percent
	green = map1[1]+(map2[1]-map1[1])*percent
	blue = map1[2]+(map2[2]-map1[2])*percent

	color = int(red),int(green),int(blue)
	return color

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)