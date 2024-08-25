import hashlib
import json
from time import time
import random

def generateHash(input_string):
    hashObject = hashlib.sha256()
    hashObject.update(input_string.encode('utf-8'))
    hashValue = hashObject.hexdigest()
    return hashValue

class BlockChain():
    def __init__(self):
        self.chain = []

    def length(self):
        return len(self.chain)
        
    def addBlock(self, currentBlock):
        if(len(self.chain) == 0):
            self.createGensisBlock()
        currentBlock.previousHash = self.chain[-1].currentHash
        isBlockMined = currentBlock.mineBlock()
        if(isBlockMined):
            self.chain.append(currentBlock)
            return True
        return False
    
    def createGensisBlock(self):
        genesisBlock = Block(0, time(), "No Previous Hash.")
        self.chain.append(genesisBlock)
    
    def printChain(self):
        for block in self.chain:
            print("Block Index", block.index)
            print("Timestamp", block.timestamp)
            print("Transactions", block.transactions)
            print( "Previous Hash",block.previousHash)
            print( "Current Hash",block.currentHash)
            print( "Is Valid Block",block.isValid)

            print("*" * 100 , "\n")

    def validateBlock(self, currentBlock):
        previousBlock = self.chain[currentBlock.index - 1]
        if(currentBlock.index != previousBlock.index + 1):
            return False
        
        previousBlockHash = previousBlock.calculateHash()
        
        if(previousBlockHash != currentBlock.previousHash):
            return False
        
        return True
        
class Block:
    def __init__(self, index, timestamp, previousHash):
        self.index = index
        self.transactions = []
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.currentHash = self.calculateHash()
        self.isValid = None
        # Create self.difficulty number to set difficulty to 3 
        self.difficulty = 3

    def calculateHash(self, randomString = "", timestamp=None):
        if(timestamp == None):
            timestamp = self.timestamp
        blockString = str(self.index) + str(timestamp) + str(self.previousHash) + json.dumps(self.transactions, default=str)+ str(randomString)
        return generateHash(blockString)

    # Define mineBlock() Method
    def mineBlock(self):
        # Define target variable and set it to a string with number '0' and multiply with difficulty
        target = "0" * self.difficulty
        # Set miningLimit to 4000 ***
        miningLimit = 40000
        # Set attemps flag variable to 1
        attempts = 1
        # Run the Loop untill programme reache the target
        while self.currentHash[:self.difficulty] != target:
            # Generate a random string
            randomString = str(random.random()).encode('utf-8')
            # Calculate hash for the block and  passs randomString to calculatehash() method
            self.currentHash = self.calculateHash(randomString)
            # Break the loope once attempts reach the mining limit
            # To prevent the mining queue blockage
            if(attempts >= miningLimit):
                # Return false to show unsuccessful mining
                return False
            
            # Increment the attemps by 1
            attempts+=1
        # Return true to show successful mining   
        return True

    def addTransaction(self, transaction):
        if transaction:
            self.transactions.append(transaction)
            if len(self.transactions) == 3:
                return "Ready"
            return "Add more transactions"


       