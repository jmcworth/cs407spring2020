# -*- coding: utf-8 -*-
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

'''###############################################################
	Genesis block and empty arrays. 
	Goal is to write to the file to keep track of the blockchain. 
###############################################################'''
genesisBlock = {
	'previousHash':'',
	'index':0,
	'transaction':[],
	'nonce':23		
}

blockchain=[]

openTransactions=[]

file="blockchain.txt"

owner='EliteHacker'

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
		print("Blockchain intialized...")
		WillContinue()
	elif(userInput=='e' or userInput=='E'):
		print("")
		PrintBlockchain()
		print("")
		WillContinue()
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
	print("  5. Save and exit")
	selection=int(input("Your selection:"))
	if(selection==1):
		AddValue()
	elif(selection==2):
		PrintBlockchain()
		WillContinue()
	elif(selection==3):
		ManipulateData()
		WillContinue()
	elif(selection==4):
		MineBlock()
		WillContinue()
	elif(selection==5):
		Save()
	else:
		print("Invalid selection.")
		return menu()

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
	
'''####################################################################
	Allows user to see their blockchain so far saved to the file.
	May want this to just print existing blockchain but would need to read
	to an array from the file so it's kind of a pain in the ass
####################################################################'''
def PrintBlockchain():
	if os.stat(file).st_size==0:
		print("No blockchain exists yet.")
		return startMenu()
	else:
		fileBlockchain=open(file,"r")
		blockchain.append(fileBlockchain.read())
		print(blockchain)
		return menu()

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
	hashBlock=hashlib.sha256(json.dumps(genesisBlock).encode()).hexdigest()
	blockchain.append(hashBlock)

'''####################################################################
	Lets users quit or not, still behaves strangely
####################################################################'''	
def WillContinue(cont=True):
	if cont is True:
		print("Continue? 'y' or 'n'")
		doContinue=input()
		if(doContinue=='y' or doContinue=='Y'):
			return menu()
		elif(doContinue=='n' or doContinue=='N'):
			exit
		else:
			print("Invalid selection.")
			return WillContinue()
	else:
		exit

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
def AddValue(recipient,amount,sender=owner):
	recipient,amount=GetTransactionInfo()
	transaction={
		'sender':owner,
		'recipient':recipient,
		'amount':amount
	}
	openTransactions.append(transaction)
	
'''####################################################################
	Checks to see if miner's POW result is valid. Might want to simplify this and
	add some functionality to ProofOfWork() instead
####################################################################'''	
def IsValidProof(transactions,prevHash,nonce):
	guess=(str(transactions)+str(prevHash)+str(nonce)).encode()
	guessHash=hashlib.sha256(guess).hexdigest()
	print(guessHash)
	return guessHash[0:2]=='00'

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
def ManipulateData(val):
	if len(blockchain)==0:
		print("Cannot alter empty blockchain.")
		return menu()
	blockchain[0]=val
	if IsValidProof:
		("")

'''####################################################################
	Creates a new block. Currently just used in MineBlock() but I don't think
	that's quite right
####################################################################'''
def CreateBlock(openTransactions,lastBlockHash,nonce):
	block={
		'previousHash':lastBlockHash,
		'index':len(blockchain),
		'transaction':openTransactions,
		'nonce':nonce
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
		'sender':'MINING',
		'recipient': owner,
		'amount':10.0		
	}
	openTransactions.append(rewardTransaction)
	block=CreateBlock(openTransactions,hashedBlock,nonce)
	blockchain.append(block)


'''####################################################################
	Program entry point
####################################################################'''
startMenu()

