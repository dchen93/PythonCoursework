import MakeChange

def chkAmt(change,denoms,amt):
	total = 0
	for i in range(len(change)) :
		total = total + (denoms[i] * change[i])
	return total == amt

def main():


	denoms = [25,10,5,1]
	stock = [3,3,3,3]
	amt = 48
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 1  Works"
	else : 
		print "Test 1  Failed"


	denoms = [25,10,5,1]		
	stock = [0,2,3,3]
	amt = 48
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 2  Works"
	else : 
		print "Test 2  Failed"


	denoms = [25,10,5,1]
	stock = [1,0,3,3]
	amt = 18
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 3  Works"
	else : 
		print "Test 3  Failed"


	denoms = [25,10,5,1]		
	stock = [0,2,3,5]
	amt = 54
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 4  Works"
	else : 
		print "Test 4  Failed"



	denoms = [16,15]
	stock = [1,2]
	amt = 46
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 5  Works"
	else : 
		print "Test 5  Failed"


	denoms = [16,15]		
	stock = [1,2]
	amt = 18
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 6  Works"
	else : 
		print "Test 6  Failed"



	denoms = [12,5,3,2,1]
	stock = [1,1,3,1,1]
	amt = 27
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 7  Works"
	else : 
		print "Test 7  Failed"


	denoms = [11,10,9]		
	stock = [0,2,1]
	amt = 18
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 8  Works"
	else : 
		print "Test 8  Failed"


	denoms = [1]
	stock = [18]
	amt = 18
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 9  Works"
	else : 
		print "Test 9  Failed"


	denoms = [12,5,3]		
	stock = [0,0,0]
	amt = 18
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 10 Works"
	else : 
		print "Test 10 Failed"


	denoms = [12,5,3]
	stock = [3,3,3]
	amt = 18
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 11 Works"
	else : 
		print "Test 11 Failed"


	denoms = [12,5,3]		
	stock = [0,2,3]
	amt = 18
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 12 Works"
	else : 
		print "Test 12 Failed"


	denoms = [10,3]
	stock = [3,3]
	amt = 19
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 13 Works"
	else : 
		print "Test 13 Failed"


	denoms = [12,5,4]		
	stock = [0,2,3]
	amt = 21
	if(str(MakeChange.makechange(amt,denoms,stock)).lower() == "none"):
		print "Test 14 Works"
	else : 
		print "Test 14 Failed"



	denoms = [14,6,5]
	stock = [1,2,1]
	amt = 19
	if(chkAmt(MakeChange.makechange(amt,denoms,stock),denoms,amt)):
		print "Test 15 Works"
	else : 
		print "Test 15 Failed"


if __name__ == '__main__':
	main();