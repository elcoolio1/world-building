#world gen

import csv
import random
import math
from PIL import Image, ImageDraw
import numpy

#races = open('races.csv','r')

seed = random.randint(100000,1000001)



#This is the random number generator. 
#To use: When you have something you want to generate values for, assign that thing a prime number (prN).
#	Initially, you can send 0 as your value for W and it will substitute the seed, but on future calls you 
#	should use the last value returned by this function.
#Behavior: Generates values (Max value  = seed). Iterates the function and returns the prN'th value generated
#	This is done so one function can be used for all calls, without creating overlap.
def xorshift(prN, W):  #prN: Prime of component. W: if continuing, previous XORshift value, else seed
	global seed
	if W == 0:
		W = seed
	for i in range(prN):  #Iterates the xorshift prN times
		X = W ^ (W >> 17) ^ (W << 12)
		W = X
	corX = X % seed #caps size of X via X mod (seed)
	return (corX)


#Generates the physical characteristics of the plane
def planeGen(): 
	global seed
	planePrN = 37

	# Size
	maxSize = 10  #Max size of Plane
	minSize = 5	  #Min size of Plane
	initW = xorshift(planePrN, 0) #Initiates xorshift()
	planeSize = (xorshift(planePrN, initW) % (maxSize + 1 - minSize)) + minSize  #iterates xorshift(), then forces it into range
	return planeSize

	# Biome(s)


def drawart():
	#creates visualization of God
	sidecount = 2 #initial number of sides per polygon
	polycount = 500 #number of layers to draw
	exacttrans = 255 #initial transparency
	mintrans = 50


	im = Image.new('RGB', (1000, 1000), (128, 128, 128))
	for i in range(polycount): #loop for every layer
		sidecount = sidecount+1 #add one side to the polygon drawn o n each layer
		
		# reduce transparency in even steps to minimum		
		if exacttrans > mintrans :
			exacttrans = exacttrans - (255 - mintrans)/polycount
			trans = round(exacttrans)

		#create random points
		coordpairs = []
		for i in range(sidecount):

			newx = numpy.random.normal(loc=500, scale=100, size=None)
			newy = numpy.random.normal(loc=500, scale=100, size=None)


			newcoord = (newx, newy)
			coordpairs.append(newcoord)

		#sort coordpairs by x coordinate low to high
		sorted(coordpairs, key = lambda xy: xy[1]) #key sets a function to be called on each iterative step of sorting. Apparently a lambda function is a small function that is defined in place. Here, it takes xy as an input (each coordinate pair) and returns just the first, x coordinate 

		#draw polygon
		draw = ImageDraw.Draw(im, 'RGBA')
		draw.polygon(coordpairs, fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255), trans) ) #draws polygon with points at each xy in coordpairs
		

	im.show() #saves image as temp file and opens with default photo program


drawart()


print(planeGen())

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

