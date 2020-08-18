from opensimplex import OpenSimplex
from hex_functions import *



def ax_center_noise(axial,freq):
	pixel = ax2px(axial)
	x = pixel[0]*100
	y = pixel[1]*100
	gen = OpenSimplex()
	noise = gen.noise2d(x*freq,y*freq)/2 + 0.5 #/2+.5 moves values into 0 ... 1 from -1 ... 1
	return noise

def px_noise(pixel,freq):
	x = pixel[0]*100
	y = pixel[1]*100
	gen = OpenSimplex()
	noise = gen.noise2d(x*freq,y*freq)/2 + 0.5 #/2+.5 moves values into 0 ... 1 from -1 ... 1
	return noise

def elev_color(xy):
	freq = .001
	elev1 = px_noise(xy,freq)
	elev2 = 0.5*px_noise(xy,freq*2)
	elev3 = 0.25*px_noise(xy,freq*4)
	elev = elev1+elev2+elev3
	print(elev)

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

	if elev < dh*3:
		color = deep_water
	elif elev < dh*3.5:
		color = mid_water
	elif elev < dh*4:
		color = shallows
	elif elev < dh*4.5:
		color = shore
	elif elev < dh*5:
		color = beach
	elif elev < dh*7:
		color = undergrowth
	elif elev < dh*8:
		color = boreal
	elif elev < dh*10:
		color = evergreen
	elif elev < dh*10.5:
		color = rock
	else:
		color = snow
		
	return color