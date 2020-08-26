#world gen

import copy
import csv
import random
import math
from array import *
import time
import os

#races = open('races.csv','r')

def NewSeed():
	seed = random.randint(100000,1000001)
	# seed = 12345678
	return seed

seed = NewSeed()



#This is the random number generator. 
#To use: When you have something you want to generate values for, assign that thing a prime number (prN).
#	Initially, you can send 0 as your value for W and it will substitute the seed, but on future calls you 
#	should use the last value returned by this function.
#Behavior: Generates values (Max value  = seed). Iterates the function and returns the prN'th value generated
#	This is done so one function can be used for all calls, without creating overlap.
def xorshift(prN, W):  
	""" prN: Prime of component. W: if continuing, previous XORshift value, else seed """
	# print("IN XORSHIFT", W)
	global seed
	if W == 0:
		W = seed
	for i in range(prN):  #Iterates the xorshift prN times
		X = W ^ (W >> 17) ^ (W << 12)
		W = X
	corX = W % seed #caps size of X via X mod (seed)
	return (corX)

#Generates the physical characteristics of the plane
def planeGen(W): 
	""" W is the current working step  of W for your function. Pass 0 for init """
	global seed
	planePrN = 37

	# Size
	maxSize = 10  #Max size of Plane
	minSize = 1000  #Min size of Plane
	planeSize = (xorshift(planePrN, W) % (maxSize + 1 - minSize)) + minSize  #iterates xorshift(), then forces it into range
	return planeSize

	# Biome(s)

planeSize = planeGen(0)

# Manual array creation
# This will be automated for bigger map sizes

# NOTE: There is a buffer layer around the outside of each map to prevent index errors in the probabilty calculation. blankGen by default
# produces maps that are the length of the generated fragment size on each side 

def blankGen(mapType, mapSize):
	""" mapType 0 = hexMap, 1 = probMap 
	mapSize can be manual, but usually the result of planeGen()"""
	border = round(mapSize*(math.log(10)/math.log(mapSize)**1.4))
	blankMap = []
	for i in range(border):
		blankMap.append([])
		for j in range(border):
			blankMap[i].append(0)
	if mapType == 0:
		blankMap [round(border/2)][round(border/2)] = 1
	if mapType == 1:
		blankMap [round(border/2)][round(border/2)] = 7

	return(blankMap)

# Calculates probability for next tile. Currently the whole board is recalculated for every call, could we make it update only locally?
def initProb(hexMap, probMap):
	""" returns updated probMap"""
	for i in range (1,len(hexMap)-1): # Range is this way to account for the buffer layer.
		for j in range (1,len(hexMap[i])-1):
			if hexMap [i][j] == 1: #If a tile is there in hexMap, it skips it
				continue
			# Because of the way coordinates work in a hex map, the numerical value of adjacent tiles differes in odd and even rows. This bit
			# calculates how many adjacent tiles are "full", by summing their values (since full tiles are 1 and empty are 0). The probability
			# for the next tile should be based on these values 1-6, with 7 being a tile that already exists.
			elif i%2 == 0:
				probMap [i][j] = (
					hexMap[i-1][j-1] + 
					hexMap[i-1][j] + 
					hexMap[i][j-1] + 
					hexMap[i][j+1] + 
					hexMap[i+1][j-1] + 
					hexMap[i+1][j])
			else:
				probMap [i][j] = (
					hexMap[i-1][j] + 
					hexMap[i-1][j+1] + 
					hexMap[i][j-1] + 
					hexMap[i][j+1] + 
					hexMap[i+1][j] + 
					hexMap[i+1][j+1])
	return (probMap)

def updProb(i, j, probMap):
	a = max(i, j)
	if 0 < a < len(probMap)+1:
		if i%2 == 0:
			probMap[i-1][j-1] = probMap[i-1][j-1] + 1
			probMap[i-1][j] = probMap[i-1][j] + 1
			probMap[i][j-1] =  probMap[i][j-1] + 1
			probMap[i][j+1] = probMap[i][j+1] + 1
			probMap[i+1][j-1] = probMap[i+1][j-1] + 1
			probMap[i+1][j] = probMap[i+1][j] + 1
		else:
			probMap[i-1][j] = probMap[i-1][j] + 1
			probMap[i-1][j+1] = probMap[i-1][j+1] + 1
			probMap[i][j-1] = probMap[i][j-1] + 1
			probMap[i][j+1] = probMap[i][j+1] + 1
			probMap[i+1][j] = probMap[i+1][j] + 1
			probMap[i+1][j+1] = probMap[i+1][j+1] + 1
	return(probMap)

# Picks the next tile and places it in hexMap. This function returns the next iteration of xorshift to use.
def tileGen(hexMap, probMap, prevW):
	""" returns updated in the same order """
	tilePrN = 23
	tileCount = 0
	addCount = 0
	for i in range(len(probMap)):  # sums the total probabilities for the spaces that could get a new tile
		for j in range (len(probMap[i])):
			if probMap [i][j] < 7:
				tileCount = tileCount + probMap [i][j]
	
	newTile = (xorshift(tilePrN, prevW))%tileCount # Iterates xorshift, then uses the tileCount to force it into the range we want
	# print(tileCount)    # vestigial checking code
	# print("NEW TILE: ", newTile)
	for i in range(len(probMap)): # Counts up to the newTile value, then places a tile there
		for j in range (len(probMap[i])):
			if 0 < probMap [i][j] < 7:
				addCount = addCount + probMap [i][j]
				if addCount > newTile:
					hexMap[i][j] = 1
					probMap[i][j] = 7
					# print("Before updProb", probMap)
					# print(i, j)
					try:
						updProb(i, j, probMap)
					except IndexError:
						continue

					# print("after updProb", probMap)

					break
		if addCount > newTile:
			break
	return (hexMap, probMap, xorshift(tilePrN, prevW))

# Prints the arrays properly
def printProb(probMap):
	for i in range (len(probMap)):
		if i%2 == 0:
			print(i, " ", probMap[i])
		else:
			print(i, "   ", probMap[i])
	print("")

def printHex(probMap):
	print("")
	kplsth = []
	kplstv = []
	midMap = []
	niceMap = []
	# decides what horizontal rows to keep
	for i in range(len(probMap)-1): 
		for j in range(len(probMap)):
			if 7 <= probMap[i][j]:
				kplsth.append(i)
				break
	for x in kplsth:
		midMap.append(probMap[x])

	# decides what vertical lines to keep
	for i in range(len(probMap)-1):
		for j in range(len(probMap[i])-1):
			if 7 <= probMap[j][i]:
				kplstv.append(i)
				break
	for i in range(len(midMap)-1):
		niceMap.append([])
		for x in kplstv:
			niceMap[i].append(midMap[i][x])


	#prints Map
	for i in range (len(niceMap)):
		if i%2 == 0:
			print("", end=" ")
		else:
			print(" ", end=" ")
		for j in range (len(niceMap[i])):
			if niceMap[i][j] <= 6: # == 0 for border probability
				print(" ", end=" ")
			elif niceMap[i][j] >= 7:
				print("0", end=" ")
		print("")
	print("")

def makeMap():
	init_time = time.clock()
	W = 0
	global planeSize
	planeSize = planeGen(0)
	hexMap = blankGen(0, planeSize) 
	probMap = blankGen(1, planeSize)
	probMap = initProb(hexMap, probMap)
	for i in range(1,planeSize):
		# probMap = initProb(hexMap, probMap)
		hexMap, probMap, W = tileGen(hexMap, probMap, W)
		# print (i)
		# printHex (probMap)
		# print("\n"*100, i+1, "/", planeSize)
		# time.sleep(.01)
	print("time in ms: ", round(1000*(time.clock() - init_time), 2),"\nSeed:	", seed)
	printHex (probMap)

def weighted_pick(weight_matrix, prN, W):
	""" Returns weighted pick where HIGH values are more common.
	weight_matrix is a list formatted [['Item0', weight0], ['Item1', weight1]] etc.. prN is the prime of the given spec, W is current xorshift.
	Returns choice as (Item, position, W)"""
	# GENERAL NOTES ON FUNCTION OF THIS TYPE OF CALL
	# The general way this type of call works is by picking a "random" seed-generated number, then bounding it into a usable range to choose an option.
	# First the weights of all options are summed, X. Then, xorshift is called to generate a number, W. W mod X gives a number Z, where 0 =< Z < X. 
	# The weights are then added again one by one, and once the running sum of the weights > Z, the item attached to the most recently added weight
	# is selected as the choice.
	Weight_total = 0
	count = 0
	for i in range (len(weight_matrix)): #sums for the total weight of the values
		Weight_total = Weight_total + weight_matrix[i][1]
	W = xorshift(prN, W) 	# Picks a random number based on the seed and the prime value of the trait
	choice = W%Weight_total # Bounds the value to the range of usable values
	for i in range (len(weight_matrix)): # adds weights one by one
		count = count + weight_matrix[i][1]
		if count > choice: # when the running total surpasses the target, the selection is made
			return (weight_matrix[i][0], i, W)

def inv_weighted_pick(weight_matrix, prN, W):
	""" Returns weighted pick where LOW values are more common.
	weight_matrix is a list formatted [['Item0', weight0], ['Item1', weight1]] etc.. prN is the prime of the given spec, W is current xorshift.
	Returns choice as (Item, position, W)"""
	# GENERAL NOTES ON FUNCTION OF THIS TYPE OF CALL
	# The general way this type of call works is by picking a "random" seed-generated number, then bounding it into a usable range to choose an option.
	# First the weights of all options are summed, X. Then, xorshift is called to generate a number, W. W mod X gives a number Z, where 0 =< Z < X. 
	# The weights are then added again one by one, and once the running sum of the weights > Z, the item attached to the most recently added weight
	# is selected as the choice.
	Weight_total = 0
	count = 0
	for i in range (len(weight_matrix)): #sums for the total weight of the values
		Weight_total = Weight_total + 1/(weight_matrix[i][1])
	W = xorshift(prN, W) 	# Picks a random number based on the seed and the prime value of the trait
	choice = W%Weight_total # Bounds the value to the range of usable values
	for i in range (len(weight_matrix)): # adds weights one by one
		count = count + 1/(weight_matrix[i][1])
		if count > choice: # when the running total surpasses the target, the selection is made
			return (weight_matrix[i][0], i, W)

def pickAttribute(atrib:str, weight_matrix, dom, none, prN, W): 
	""" atrib is str, name of attribute. weight_matrix is the weighted matrix (see weighted_pick() for formatting), dom is the number of 
	dominant attributes from the matrix, none is the number of nonexistant attributes from the matrix, prN is the prime of the attribute 
	and W is the most recent W call 0 if none """
	if len(weight_matrix) < dom + none:
		print ("Dom + None attributes are more than options available")
		return (0)
	domChoice = []
	noneChoice = []				# Lists needs to be declared before use
	while len(domChoice) < dom: # rolls for an attribute, then removes it from the available options
		choice, pos, W = weighted_pick(weight_matrix, prN, W)
		domChoice.append(choice)
		weight_matrix.pop(pos)

	while len(noneChoice) < none: # rolls for an attribute, then removes it from the available options
		choice, pos, W = inv_weighted_pick(weight_matrix, prN, W)
		noneChoice.append(choice)
		weight_matrix.pop(pos)

	print("Dominant {0}:		".format(atrib), domChoice)
	print("Nonexistant {0}:	".format(atrib), noneChoice)
	return domChoice, noneChoice

def attribAmnt(prN, maxim, minim):
	global planeSize, seed
	x = (xorshift(2*prN,0)%(planeSize-maxim+1)) + maxim
	y = round(abs(math.log(maxim*x/(planeSize))/math.log(maxim/2.01)))
	if y > maxim:
		y = maxim
	elif y < minim:
		y = minim
	return(y)

def noneAmnt(prN, maxim, minim):
	global planeSize, seed
	x = (xorshift(prN,0)%(planeSize-maxim+1)) + maxim
	y = round(abs(math.log(maxim*x/(planeSize))/math.log(maxim/2.01)))
	if y > maxim:
		y = maxim
	elif y < minim:
		y = minim - 1
	z = maxim - y + 1
	return(z)
	
def pickRace():

	# Declarations
	racePrN = 11				# prime for this attribute
	race_weight_matrix = [['Human', 10], ['Dwarf', 10], ['Elf', 10],['Gnome', 10],['Dragonborn', 10], ['Halfling', 10],['Tiefling', 10]]
	races_dominant = attribAmnt(racePrN,3,1)
	races_none = noneAmnt(racePrN,3,1)
	races = pickAttribute('races', race_weight_matrix, races_dominant, races_none, racePrN, 0)
	return(races)

def pickResources():

	resourcePrN = 7
	resource_weight_matrix = [['Water', 30], ['Ore', 7], ['Wood', 10],['Stone', 20],['Ancient Tech', 3], ['Fertile Soil', 10], ['Magic Essence', 10]]
	domRes = attribAmnt(resourcePrN,2,1)
	noneRes = noneAmnt(resourcePrN,2,1)
	resources = pickAttribute('resources', resource_weight_matrix, domRes, noneRes, resourcePrN, 0)
	return (resources)

def pickMagic():
	pass
	magicPrn = 13
	magic_weight_matrix = ([['Necromancy', 10],['Conjuration', 10],['Evocation', 10],['Abjuration', 10],['Transmutation', 10],
		['Divination', 10],['Enchantment', 10],['Illusion', 10]])
	domMagic = attribAmnt(magicPrn,4,1)
	noneMagic = noneAmnt(magicPrn,2,0)
	magic = pickAttribute('magic', magic_weight_matrix, domMagic, noneMagic, magicPrn, 0)
	return (magic)

def Island():
	makeMap()
	# print("\n", planeSize, '\n')
	pickRace()
	print("")
	pickResources()
	print("")
	pickMagic()

def NewIsland():
	global seed
	seed = NewSeed()
	Island()

def NewLoop():
	while True:
		x = input()
		print('\n'*50)
		NewIsland()

NewLoop()