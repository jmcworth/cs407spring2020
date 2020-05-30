# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:53:26 2020

@author: mille
"""
import os
blockchain=[]
file="blockchain.txt"
	
def startMenu():
	print("Welcome to your blockchain. Select from the following options: ")
	print("\t* Enter 'n' to create a new blockchain. (This will erase any existing blockchain).")
	print("\t* Enter 'e' to see existing blockchain.")
	userInput=input()
	if(userInput=='n' or userInput=='N'):
		InitializeBlockchain()
		WillContinue()
	elif(userInput=='e' or userInput=='E'):
		PrintBlockchain()
		WillContinue()
	else:
		print("Invalid Selection")
		return startMenu()
	
def menu():
	print("What would you like to do?")
	print("1. Add a new transaction.")
	print("2. Print current blockchain")
	print("3. Manipulate existing data")
	print("4. Save and exit")
	selection=int(input("Your selection:"))
	if(selection==1):
		AddValue()
	elif(selection==2):
		PrintBlockchain()
		WillContinue()
	elif(selection==3):
		ManipulateData()
	elif(selection==4):
		Save()
		WillContinue(False)
	else:
		print("Invalid selection.")
		return menu()
	
def Save():
	fileBlockchain=open(file,"w")
	fileBlockchain.write(str(blockchain))
	
	
def PrintBlockchain():
	if os.stat(file).st_size==0:
		print("No blockchain exists yet.")
		return startMenu()
	else:
		fileBlockchain=open(file,"r")
		blockchain.append(fileBlockchain.read())
		print(blockchain)
		return menu()

def InitializeBlockchain():
	#if blockchain txt file isn't empty, then empty it
	if os.stat(file).st_size!=0:
		fileBlockchain=open(file,"r+")
		fileBlockchain.truncate(0)
		fileBlockchain.close()
	print("Enter the starting value for your genesis block: ")
	blockchain.append([(GetUserInput())])
	
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
	
def GetLastBlockchainVal():
	if len(blockchain)==0:
		print("Your blockchain is empty.")
		return menu()
	elif len(blockchain)==1:#return lone element
		return blockchain[0]
	else:
		return blockchain[-1]

def AddValue():
	transactionAmt=GetUserInput()
	blockchain.append([GetLastBlockchainVal(),transactionAmt])
	if(IsValidBlockchain):
		print("Value successfully added.")
	else:
		print("Value not accepted. Maintaining original blockchain")
		blockchain.pop()
	
def IsValidBlockchain(arr):
	return True

def ManipulateData(val):
	if len(blockchain)==0:
		print("Cannot alter empty blockchain.")
		return menu()
	blockchain[0]=val
	if IsValidBlockchain:
		("")

def GetUserInput():
	return float(input("Your transaction amount: "))

startMenu()

