def makechange(amtchange, denoms, coinstock):
	#check if enough money is left
	if amtchange <= findTotal(denoms, coinstock):
		#find the largest coin that is smaller than amtchange
		maxCoins = findMaxCoins(denoms, coinstock, amtchange) # returns [index, maxNum]
		
		#returns None if no coin in stock is smaller than the change due
		if not maxCoins:
			return None

		numOfCoins = maxCoins[1];
		coinIndex = maxCoins[0];

		# decreasing loop which subtracts the largest coins, starting with the largest number
		for i in range(numOfCoins, -1, -1):
			#subtract the number of coins
			_amtchange = amtchange - i * denoms[coinIndex]

			# the base case
			if _amtchange == 0:
				returnArray = [0] * len(coinstock)
				returnArray[coinIndex] = i
				return returnArray

			#zero the respective field in the coinstock list
			_coinstock = coinstock[:]
			_coinstock[coinIndex] = 0

			#recursive call
			retVal = makechange(_amtchange, denoms, _coinstock)

			#check return Value
			if retVal != None:
				#amend the output array to include the coxins used in this recursive step
				retVal[coinIndex] = i
				return retVal


	else:
		#print "Error: makechange could not calculate change as the change required exceeds the stocks available."
		return None

def findTotal(denoms, coinstock):
	total = 0
	for i in range(len(denoms)):
		total += denoms[i] * coinstock[i]

	return total

# returns the index of the coin, and the maximum number thereof
# return format: [index, numOfCoins]
def findMaxCoins(denoms, coinstock, amtchange):
	#find index of first non zero element smaller than amtchange
	index = None;
	for i in range(len(coinstock)):
		if coinstock[i] != 0 and denoms[i] <= amtchange:
			index = i;
			break



	# null check, which would indicates smallest coin larger than amtchange
	if index == None:
		return None

	# find maximum number the coin fits into amtchange
	maxNum = int(amtchange / denoms[i])

	# make sure maxNum not larger than the number of coins in coinstock
	if maxNum > coinstock[index]:
		maxNum = coinstock[index]

	return [index, maxNum]

d = [25,10,5,1]
c = [2,1,2,4]
c2 = [2,4,0,0]

#import pdb
#pdb.run("makechange(55, d, c2)")