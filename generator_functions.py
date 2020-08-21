from opensimplex import OpenSimplex
from hex_functions import *




def ax_center_noise(axial,freq=0.1):
	pixel = ax2px(axial)
	x = pixel[0]
	y = pixel[1]
	gen = OpenSimplex()
	noise = gen.noise2d(x*freq,y*freq)/2 + 0.5 #/2+.5 moves values into 0 ... 1 from -1 ... 1
	return noise

def px_noise(pixel,freq=0.1):
	x = pixel[0]
	y = pixel[1]
	gen = OpenSimplex()
	noise = gen.noise2d(x*freq,y*freq)/2 + 0.5 #/2+.5 moves values into 0 ... 1 from -1 ... 1
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


def elev_color_sections(xy,freq=.001,break_points=[0.3,0.5,0.7,0.9]):
	e = elev(xy,freq)
	sea_level = break_points[0]
	beach_line = break_points[1]
	tree_line = break_points[2]
	snow_line = break_points[3]

	dsea = sea_level-0
	dbeach = beach_line-sea_level
	dtree = tree_line-beach_line
	drock = snow_line-tree_line
	dsnow = 1-snow_line


	dark_blue = 5,18,64
	light_blue = 45, 199, 255

	shore = 234, 210, 172
	beach = 234, 186, 107

	undergrowth= 23, 195, 103
	evergreen  = 22, 67, 35

	light_rock = 103, 98, 92
	dark_rock = 170, 167, 161

	off_white = 240, 244, 246
	pure_white = 255,255,255


	if e < sea_level:
		color = color_grad(light_blue,dark_blue,(sea_level-e)/dsea)
	elif e < beach_line:
		color = color_grad(beach,shore,(e-sea_level)/dbeach)
	elif e < tree_line:
		color = color_grad(undergrowth,evergreen,(e-beach_line)/dtree)
	elif e < snow_line:
		color = color_grad(light_rock,dark_rock,(e-tree_line)/drock)
	else:
		color = color_grad(off_white,pure_white,(e-snow_line)/dsnow)

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