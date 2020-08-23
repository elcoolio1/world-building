#world gen

import csv
import random
import math
from array import *
import time
import os

#races = open('races.csv','r')
seed = 0

def NewSeed():
	global seed
	seed = random.randint(100000,1000001)
	# seed = 12345678
	return seed



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
	maxSize = 3  #Max size of Plane
	minSize = 110  #Min size of Plane
	planeSize = (xorshift(planePrN, W) % (maxSize + 1 - minSize)) + minSize  #iterates xorshift(), then forces it into range
	return planeSize

	# Biome(s)


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
			if probMap [i][j] <= 7:
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
					updProb(i, j, probMap)
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
	niceMap = []
	for i in range (len(probMap)):
		niceMap.append([])
		for j in range (len(probMap[i])):
			if probMap[i][j] <= 6: # == 0 for border probability
				niceMap[i].append(".")
			# elif 0 < probMap[i][j] <= 6:
			# 	niceMap[i].append(str(probMap[i][j]))
			elif probMap[i][j] >= 7:
				niceMap[i].append("M")
		if i%2 == 0:
			print(" ", niceMap[i])
		else:
			print("    ", niceMap[i])
	print("")


def makeMap():
	init_time = time.clock()
	W = 0
	planeSize = planeGen(0)
	hexMap = blankGen(0, planeSize) 
	probMap = blankGen(1, planeSize)
	probMap = initProb(hexMap, probMap)
	for i in range(planeSize):
		# probMap = initProb(hexMap, probMap)
		hexMap, probMap, W = tileGen(hexMap, probMap, W)
		# printHex (probMap)
		# print("\n"*100, i+1, "/", planeSize)
		# time.sleep(.01)
	printHex (probMap)
	print("time in ms: ", round(1000*(time.clock() - init_time), 2),"\nSeed:		", seed)


# makeMap()
