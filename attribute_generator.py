from hexmap import *

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
