from generator import planeGen, xorshift
from array import *
import time
import math



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
def updProb(hexMap, probMap):
	""" returns updated probMap"""
	for i in range (1,len(hexMap)-1): # Range is this way to account for the buffer layer.
		for j in range (1,len(hexMap[i])-1):
			if hexMap [i][j] == 1: #If a tile is there in hexMap, it skips it
				pass
			# Because of the way coordinates work in a hex map, the numerical value of adjacent tiles differes in odd and even rows. This bit
			# calculates how many adjacent tiles are "full", by summing their values (since full tiles are 1 and empty are 0). The probability
			# for the next tile should be based on these values 1-6, with 7 being a tile that already exists.
			elif i%2 == 0:
				probMap [i][j] = (hexMap[i-1][j-1] + hexMap[i-1][j] + hexMap[i][j-1] + hexMap[i][j+1] + hexMap[i+1][j-1] + hexMap[i+1][j])
			else:
				probMap [i][j] = (hexMap[i-1][j] + hexMap[i-1][j+1] + hexMap[i][j-1] + hexMap[i][j+1] + hexMap[i+1][j] + hexMap[i+1][j+1])
	return (probMap)



# Picks the next tile and places it in hexMap. This function returns the next iteration of xorshift to use.
def tileGen(hexMap, probMap, prevW):
	""" returns updated in the same order """
	tilePrN = 23
	tileCount = 0
	addCount = 0
	for i in range(len(probMap)):  # sums the total probabilities for the spaces that could get a new tile
		for j in range (len(probMap[i])):
			if probMap [i][j] == 7:
				pass
			else:
				tileCount = tileCount + probMap [i][j]
	
	newTile = (xorshift(tilePrN, prevW))%tileCount # Iterates xorshift, then uses the tileCount to force it into the range we want
	# print(tileCount)    vestigial checking code
	# print("NEW TILE: ", newTile)
	for i in range(len(probMap)): # Counts up to the newTile value, then places a tile there
		for j in range (len(probMap[i])):
			if probMap [i][j] == 7:
				pass
			elif probMap[i][j] == 0:
				pass
			else:
				addCount = addCount + probMap [i][j]
				if addCount > newTile:
					hexMap[i][j] = 1
					probMap[i][j] = 7
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

def printHex(hexMap):
	niceMap = []
	for i in range (len(hexMap)):
		niceMap.append([])
		for j in range (len(hexMap[i])):
			if hexMap[i][j] == 0:
				niceMap[i].append(".")
			elif hexMap[i][j] == 1:
				niceMap[i].append("M")
		if i%2 == 0:
			print(" ", niceMap[i])
		else:
			print("    ", niceMap[i])
	print("")


def makeMap():
	W = 0
	planeSize = planeGen(0)
	hexMap = blankGen(0, planeSize) 
	probMap = blankGen(1, planeSize)
	for i in range(planeSize):
		probMap = updProb(hexMap, probMap)
		hexMap, probMap, W = tileGen(hexMap, probMap, W)
		printHex (hexMap)
		time.sleep(.05)

makeMap()