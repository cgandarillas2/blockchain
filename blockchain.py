# We create a blockchain class that will be used to store the blockchain and perform operations on it.
# It need to have an evident tamper log

from datetime import datetime
from hashlib import sha256
from uuid import uuid4

class Block:

    def __init__(self, data, previous_hash) -> None:
        # timestamps serves as a nonce but it is not enough to prevent tampering
        self.timestamp = datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        # we use uuid4 to generate a random nonce that will be unic for each block
        # HIDING 
        self.nonce = uuid4().hex
        # self.hash = self.calculate_hash()
        pass

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp}\nData: {self.data}\nPrevious Hash: {self.previous_hash}\nHash: {self.calculate_hash()}\nNonce: {self.nonce}\n"
        pass

    def calculate_hash(self):
        return sha256(f"{self.timestamp}{self.data}{self.previous_hash}{self.nonce}".encode()).hexdigest()
    

class Blockchain:

    def __init__(self) -> None:
        self.chain = [self.create_genesis_block()]
        self.all_transactions = []
        pass

    def create_genesis_block(self):
        initial_data = "Genesis Block"
        # we could use a random hash but we use 0 for simplicity
        previous_hash = "0"
        return Block(initial_data, previous_hash)
        pass

    def print_blocks(self):
        for i in range(len(self.chain)):
            print(f"Block {i}")
            print(self.chain[i])
        pass

    def add_block(self, data):
        previous_hash = self.chain[-1].calculate_hash()
        new_block = Block(data, previous_hash)
        #self.proof_of_work(new_block)
        self.chain.append(new_block)
        pass    

    def validate_chain(self):
        for i in range(1, len(self.chain)):

            current = self.chain[i]
            #print("current:" ,current)
            previous = self.chain[i-1]
            #print("previous:" ,previous)
            # Si se aplica esta función siempre se detectará discrepancia en el hash propio del bloque
            # pero queremos que se vea la diferencia con el anterior?
            # if(current.hash != current.calculate_hash()):
            #     print(f"The current hash of the block {i} does not equal the generated hash of the block.")
            #     return False
            if(current.previous_hash != previous.calculate_hash()):
                print(f"The previous block's {i-1} hash does not equal the previous hash value stored in the current block {i}.")
                return False
        return True


new_transactions = [{'amount': '30', 'sender':'alice', 'receiver':'bob'},
               	{'amount': '55', 'sender':'bob', 'receiver':'alice'}]
transaction2 = [{'amount': '2220', 'sender':'alice', 'receiver':'bob'}, {'amount': '55', 'sender':'bob', 'receiver':'alice'}]
transaction3 = [{'amount': '400', 'sender':'alice', 'receiver':'bob'}, {'amount': '55', 'sender':'bob', 'receiver':'alice'}]
transaction4 = [{'amount': '1000', 'sender':'alice', 'receiver':'bob'}, {'amount': '55', 'sender':'bob', 'receiver':'alice'}]


my_blockchain = Blockchain()
my_blockchain.add_block(new_transactions)
my_blockchain.add_block(transaction2)
#my_blockchain.chain[2].data = "fake_transactions"
my_blockchain.add_block(transaction3)
#my_blockchain.chain[2].data = "fake_transactionesjsankjsnbdjabds"
my_blockchain.print_blocks()
# print(my_blockchain.validate_chain())
# my_blockchain.chain[1].data = "fake_transactions"
my_blockchain.add_block(transaction4)

print(my_blockchain.validate_chain())

    


