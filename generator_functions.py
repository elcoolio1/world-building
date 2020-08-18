from opensimplex import OpenSimplex
from hex_functions import *



def ax_center_noise(axial,freq):
	pixel = ax2px(axial)
	x = pixel[0]*100
	y = pixel[1]*100
	gen = OpenSimplex()
	noise = abs(gen.noise2d(x*freq,y*freq))
	return noise
