from generator import planeGen
from array import *


# Manual array creation
# This will be automated for bigger map sizes

# NOTE: There is a buffer layer around the outside of each map to prevent index errors in the probabilty calculation. Working size of these
# maps is actually 4 across by 3 down

A = [0,0,0,0,0,0]
B =  [0,0,0,0,0,0]
C = [0,0,0,1,0,0]
D =  [0,0,0,0,0,0]
E = [0,0,0,0,0,0]

hexMap = [A,B,C,D,E]

probA = [0,0,0,0,0,0]
probB =  [0,0,0,0,0,0]
probC = [0,0,0,0,0,0]
probD =  [0,0,0,0,0,0]
probE = [0,0,0,0,0,0]
probMap = [probA,probB,probC,probD,probE]


# Calculates probability for next tile. Currently the whole board is recalculated for every call, could we make it update only locally?
def initProb():
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


# Picks the next tile
def nextTile():
	tileCount = 0
	global hexMap, probMap
	for i in range(len(probMap)):
		for j in range (len(probMap[i])):
			if probMap [i][j] == 7:
				pass
			else:
				tileCount = tileCount + probMap [i][j]






# TODO: something that uses the xorshift function to decide what tile to place, somehow wieghted by the value 1-6 of the array probMap

initProb()
# Prints the arrays properly
def printMaps():
	for i in range (len(probMap)):
		if i%2 == 0:
			print(i, " ", probMap[i])
		else:
			print(i, "  ", probMap[i])

	print("")

	for i in range (len(hexMap)):
		if i%2 == 0:
			print(i, " ", hexMap[i])
		else:
			print(i, "  ", hexMap[i])

nextTile()