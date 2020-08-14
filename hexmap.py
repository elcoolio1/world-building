from generator import planeGen, xorshift
from array import *


# Manual array creation
# This will be automated for bigger map sizes

# NOTE: There is a buffer layer around the outside of each map to prevent index errors in the probabilty calculation. Working size of these
# maps is actually 4 across by 3 down

def blankGen(mapType):
	""" mapType 0 = hexMap, 1 = probMap """
	mapSize = planeGen()
	border = round(mapSize/2)
	blankMap = []
	for i in range(border):
		blankMap.append([])
		for j in range(border):
			blankMap[i].append(0)
	if mapType == 0:
		blankMap [round(border/2)][round(border/2)] = 1

	return(blankMap)

# def probMapGen(hexMap):
# 	probMap = hexMap
# 	for i in range(len(hexMap)):
# 		for(j) in range(len(hexMap[i])):
# 			if hexMap[i][j] == 1:
# 				probMap[i][j] = 7
# 	return (probMap)

hexMap = blankGen(0)  # This defines the global variables hexMap and probMap, don't delete pls
print(hexMap)
# probMap = probMapGen(hexMap)
probMap = blankGen(1)

# Calculates probability for next tile. Currently the whole board is recalculated for every call, could we make it update only locally?
def updProb():
	global hexMap, probMap
	for i in range (1,len(hexMap)-1): # Range is this way to account for the buffer layer.
		for j in range (1,len(hexMap[i])-1):
			if hexMap [i][j] == 1: #If a tile is there in hexMap, that tile in probMap is set to 7
				probMap[i][j] = 7

			# Because of the way coordinates work in a hex map, the numerical value of adjacent tiles differes in odd and even rows. This bit
			# calculates how many adjacent tiles are "full", by summing their values (since full tiles are 1 and empty are 0). The probability
			# for the next tile should be based on these values 1-6, with 7 being a tile that already exists.
			elif i%2 == 0:
				probMap [i][j] = (hexMap[i-1][j-1] + hexMap[i-1][j] + hexMap[i][j-1] + hexMap[i][j+1] + hexMap[i+1][j-1] + hexMap[i+1][j])
			else:
				probMap [i][j] = (hexMap[i-1][j] + hexMap[i-1][j+1] + hexMap[i][j-1] + hexMap[i][j+1] + hexMap[i+1][j] + hexMap[i+1][j+1])



# Picks the next tile and places it in hexMap. This function returns the next iteration of xorshift to use.
def tileGen(prevW):
	tilePrN = 23
	tileCount = 0
	addCount = 0
	global hexMap, probMap
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
	return (xorshift(tilePrN, prevW))


# Prints the arrays properly
def printProb():
	global probMap
	for i in range (len(probMap)):
		if i%2 == 0:
			print(i, " ", probMap[i])
		else:
			print(i, "  ", probMap[i])
	print("")

def printHex():
	global hexMap
	for i in range (len(hexMap)):
		if i%2 == 0:
			print(i, " ", hexMap[i])
		else:
			print(i, "  ", hexMap[i])
	print("")

def makeMap():
	global hexMap, probMap
	for i in range()

updProb()
printHex()
W = tileGen(0)
updProb()
printHex()
tileGen(W)
printHex()

# print(blankGen())