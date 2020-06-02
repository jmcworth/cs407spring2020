"""
Brittany Miller-Burt
Joe Collinsworth
Maksim Stoyanov
CS 407 Intro to Blockchain

SOURCE: https://blockgeeks.com/guides/python-blockchain-2/
"""
import os
import hashlib
import json
import sys

'''###############################################################
	Genesis block and empty arrays. 
	Goal is to write to the file to keep track of the blockchain. 
###############################################################'''
genesisBlock = {
	"previousHash":"",
	"index":0,
	"transaction":[],
	"nonce":23		
}

blockchain=[]

openTransactions=[]

file="blockchain.txt"

owner="EliteHacker"

'''####################################################################
	Menus to provide user interaction
	Start menu is what's created on start up. Once users
	make a selection here, they are taken to a different menu
####################################################################'''	
def startMenu():
	print("Welcome to your blockchain. Select from the following options: ")
	print("\t* Enter 'n' to create a new blockchain. (This will erase any existing blockchain).")
	print("\t* Enter 'e' to see existing blockchain.")
	userInput=input()
	if(userInput=='n' or userInput=='N'):
		InitializeBlockchain()
	elif(userInput=='e' or userInput=='E'):
		print("Loading existing blockchain")
		PrintBlockchain()
		print("")
	else:
		print("Invalid Selection")
		return startMenu()
	
'''####################################################################
	Regular menu that leads to further interaction
####################################################################'''	
def menu():
	print("What would you like to do?")
	print("  1. Add a new transaction.")
	print("  2. Print current blockchain")
	print("  3. Manipulate existing data")
	print("  4. Mine for a block.")
	print("  5. Check if chain has been altered")
	print("  6. Create a new block chain. (This will delete any existing one.)")
	print("  7. Save and Exit")
	selection=int(input("Your selection:"))
	if(selection==1):
		AddValue()
	elif(selection==2):
		PrintBlockchain()
		Continue()
	elif(selection==3):
		ManipulateData()
		Continue()
	elif(selection==4):
		MineBlock()
		Continue()
	elif(selection==5):
		IsChainValid()
	elif(selection==6):
		InitializeBlockchain()
	elif(selection==7):
		Save()
		sys.exit		
	else:
		print("Invalid selection.")
		return menu()
	
'''####################################################################
	opening and reading file and stripping any unnecessary characters out
####################################################################'''
def OpenFile():	
	fileBlockchain=open(file,"r")
	fileInfo=fileBlockchain.read()
	fileInfo=json.loads(json.dumps(fileInfo))
	fileInfo=fileInfo.replace('\\','')
	fileBlockchain.close()
	blockchain.append(fileInfo)
	

'''####################################################################
	Used for creating block to add to transaction info
####################################################################'''	
def GetTransactionInfo():
	recipient=input('Enter the recipient of the transaction: ')
	amount=float(input('Enter the amount: '))
	return recipient, amount

'''####################################################################
	Writes to file before closing
####################################################################'''
def Save():
	fileBlockchain=open(file,"w")
	fileBlockchain.write(str(blockchain))
	fileBlockchain.close()
	print("Blockchain saved.")
	
'''####################################################################
	Allows user to see their blockchain so far saved to the file.
	May want this to just print existing blockchain but would need to read
	to an array from the file so it's kind of a pain in the ass
####################################################################'''
def PrintBlockchain():
	if os.stat(file).st_size==0:
		print("Blockchain hasn't been saved yet.")
		print("Checking local memory...")
		if(len(blockchain)==0):
			print("No blockchain exists")
			return Continue()
	else:
		print(blockchain)
		return Continue()

'''####################################################################
	If users want to create a whole new block chain this function clears
	out what's already in the file and then adds the default genesis block
####################################################################'''
def InitializeBlockchain():
	#if blockchain txt file isn't empty, then empty it
	if os.stat(file).st_size!=0:
		fileBlockchain=open(file,"r+")
		fileBlockchain.truncate(0)
		fileBlockchain.close()
	blockchain.append(genesisBlock)
	print("Blockchain intialized...")
	Continue()

'''####################################################################
	Lets users quit or not, still behaves strangely
####################################################################'''	
def Continue():
	input("Press 'Enter' to continue...")
	return menu()

'''####################################################################
	Gets last block in chain. Returns to the menu if it's empty,
	returns the only element if all that's there is the genesis block,
	and finally, returns the last block if there's more than one
####################################################################'''	
def GetLastBlock():
	if len(blockchain)==0:
		print("Your blockchain is empty.")
		return menu()
	elif len(blockchain)==1:#return lone element
		return blockchain[0]
	else:
		return blockchain[-1]

'''####################################################################
	Takes information from GetTransactionInfo() and adds this to the 
	existing transactions
####################################################################'''
def AddValue(sender=owner):
	recipient,amount=GetTransactionInfo()
	transaction={
		"sender":owner,
		"recipient":recipient,
		"amount":amount
	}
	openTransactions.append(transaction)
	newBlock=CreateBlock(openTransactions,HashBlock(GetLastBlock()),ProofOfWork())
	blockchain.append(newBlock)
	print("Transaction added to blockchain.")
	Continue()
	
'''####################################################################
	Checks to see if miner's POW result is valid. Might want to simplify this and
	add some functionality to ProofOfWork() instead
####################################################################'''	
def IsValidProof(transactions,prevHash,nonce):
	guess=(str(transactions)+str(prevHash)+str(nonce)).encode()
	guessHash=hashlib.sha256(guess).hexdigest()
	print(guessHash)
	return guessHash[0:2]=="00"

'''####################################################################
	Hashes a given block that has already been created
####################################################################'''
def HashBlock(block):
	return hashlib.sha256(json.dumps(block).encode()).hexdigest()

'''####################################################################
	Returns number of attempts to get valid proof of work.
	This function comes from the website cited at the top and I'm not
	fully sure what it's doing here yet. 
####################################################################'''
def ProofOfWork():
	lastBlock=blockchain[-1]
	lastBlockHash=HashBlock(lastBlock)
	nonce=0
	while not IsValidProof(openTransactions,lastBlockHash,nonce):
		nonce+=1
	return nonce

'''####################################################################
	Function not quite right. It's meant to simulate how a block is 
	rendered invalid if someone tries to mess with the data. However, I haven't 
	finished it yet
####################################################################'''
def ManipulateData():
	if len(blockchain)==0:
		print("Cannot alter empty blockchain.")
		menu()
	print("Current value of the genesis block nonce is 23.")
	genesisBlockHashOriginal=HashBlock(genesisBlock)
	val=float(input("Enter a number to alter the nonce of the genesis block:"))
	genesisBlock["nonce"]=val
	genesisBlockManipulated=HashBlock(genesisBlock)
	if genesisBlockHashOriginal==genesisBlockManipulated:
		print("You've entered 23. Please enter a different number.")
		ManipulateData()
	else:
		print("Original Hash: ",str(genesisBlockHashOriginal))
		print("New Hash: ",str(genesisBlockManipulated))
		input("Press enter to continue...")
		IsChainValid()
		

'''####################################################################
	Creates a new block. Currently just used in MineBlock() but I don't think
	that's quite right
####################################################################'''
def CreateBlock(openTransactions,lastBlockHash,nonce):
	block={
		"previousHash":lastBlockHash,
		"index":len(blockchain),
		"transaction":openTransactions,
		"nonce":nonce
	}
	return block

'''####################################################################
	Lets miners try to mine for a block. Creates and appends a block to the chain
####################################################################'''
def MineBlock():
	lastBlock=GetLastBlock()
	hashedBlock=HashBlock(lastBlock)
	nonce=ProofOfWork()
	rewardTransaction={
		"sender":"MINING",
		"recipient": owner,
		"amount":10.0		
	}
	openTransactions.append(rewardTransaction)
	block=CreateBlock(openTransactions,hashedBlock,nonce)
	blockchain.append(block)
	Continue()

'''####################################################################
	Check if Chain is valid
####################################################################'''
def IsChainValid():
	isValid=True
	copyChain=blockchain
	hashOrig=hashlib.sha256(str(copyChain).encode())
	blockchain.clear()
	OpenFile()
	hashNew=hashlib.sha256(str(blockchain).encode())
	if hashOrig.hexdigest()==hashNew.hexdigest():
		print("Chain is not compromised.")
		Continue()
		isValid=False;
		print("Chain has been tampered.")
		blockchain.clear()
		blockchain.append(copyChain)
		Continue()
	else:
		isValid=False;
		print("Chain has been tampered.")
		blockchain.clear()
		blockchain.append(copyChain)
		Continue()
	return isValid
		

'''####################################################################
	Program entry point
####################################################################'''
OpenFile()
PrintBlockchain()






