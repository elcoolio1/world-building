#world gen

import csv
import random
import math
from PIL import Image, ImageDraw #for drawart()
import numpy #for gaussian random in drawart()

#races = open('races.csv','r')

seed = random.randint(100000,1000001)
# seed = 12345678


#This is the random number generator. 
#To use: When you have something you want to generate values for, assign that thing a prime number (prN).
#	Initially, you can send 0 as your value for W and it will substitute the seed, but on future calls you 
#	should use the last value returned by this function.
#Behavior: Generates values (Max value  = seed). Iterates the function and returns the prN'th value generated
#	This is done so one function can be used for all calls, without creating overlap.
def xorshift(prN, W):  
	""" prN: Prime of component. W: if continuing, previous XORshift value, else seed """
	global seed
	if W == 0:
		W = seed
	for i in range(prN):  #Iterates the xorshift prN times
		X = W ^ (W >> 17) ^ (W << 12)
		W = X
	corX = X % seed #caps size of X via X mod (seed)
	return (corX)


#Generates the physical characteristics of the plane
def planeGen(W): 
	""" W is the current working step  of W for your function. Pass 0 for init """
	global seed
	planePrN = 37

	# Size
	maxSize = 27  #Max size of Plane
	minSize = 27  #Min size of Plane
	planeSize = (xorshift(planePrN, W) % (maxSize + 1 - minSize)) + minSize  #iterates xorshift(), then forces it into range
	return planeSize

	# Biome(s)


def drawart():
	#creates visualization of God
	sidecount = 2 #initial number of sides per polygon
	polycount = 1000 #number of layers to draw
	exacttrans = 255 #initial transparency (0-255)
	mintrans = 50 #minimum transparency (0-255)
	bar = [] #list for loading bar
	barcounter = 0 #counts for 1% of cycles, then adds to loading bar
	tencounter = 1

	im = Image.new('RGB', (1000, 1000), (128, 128, 128))
	for i in range(polycount): #loop for every layer

		#progressbar
		barcounter = barcounter +1

		if barcounter >= polycount/100:

			#makes loading bar longer for each 1% of cycles in loop
			if tencounter >= 10:
				bar.append('*')
				tencounter = 0
			else:
				bar.append('|')
			print ("\n" * 100) #shitty way of clearing terminal. just fill it with empty lines
			print(''.join(bar)) #prints list with loading bar elements as one string with no spaces or commas
			barcounter = 0
			tencounter = tencounter +1

		sidecount = sidecount+1 #add one side to the polygon drawn o n each layer
		
		# reduce transparency in even steps to minimum		
		if exacttrans > mintrans :
			exacttrans = exacttrans - (255 - mintrans)/polycount
			trans = round(exacttrans)

		#create random points
		coordpairs = []
		for i in range(sidecount):

			newx = numpy.random.normal(loc=500, scale=100, size=None) #generates random point following gaussian distribution centered on 500 (middle of 1000x1000 image) 
			newy = numpy.random.normal(loc=500, scale=100, size=None)
			newcoord = (newx, newy)
			coordpairs.append(newcoord)

		#sort coordpairs by x coordinate low to high
		sorted(coordpairs, key = lambda xy: xy[1]) #key sets a function to be called on each iterative step of sorting. Apparently a lambda function is a small function that is defined in place. Here, it takes xy as an input (each coordinate pair) and returns just the first, x coordinate 

		#draw polygon
		draw = ImageDraw.Draw(im, 'RGBA')
		draw.polygon(coordpairs, fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255), trans) ) #draws polygon with points at each xy in coordpairs
		
	im.show() #saves image as temp file and opens with default photo program


# drawart()


def races():
	global seed
	#races and their weights
	HumanW = 100
	DwarfW = 100
	ElfW = 100
	GnomeW = 100
	DragonbornW = 100
	HalflingW = 100
	TieflingW = 100



# l = 0
# for i in range(18):
# 	l = xorshift(37,l)
# 	print(l)

# print (xorshift(5, 0))
# print(planeGen(3))

