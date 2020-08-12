#world gen

import csv
import random
import math

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
	# return (planeSize)

	# Biome(s)




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

