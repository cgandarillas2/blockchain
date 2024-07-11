from datetime import datetime
from hashlib import sha256
from uuid import uuid4

class Block:

    def __init__(self, data, previous_hash) -> None:
        # timestamps serves as a nonce but it is not enough to prevent tampering
        self.timestamp = datetime.now()
        self.data = data
        # hash pointer
        self.previous_hash = previous_hash
        # we use uuid4 to generate a random nonce that will be unique for each block
        # HIDING
        # https://docs.python.org/3/library/uuid.html
        self.nonce = uuid4().hex
        self.hash = self.calculate_hash()
        pass

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp}\nData: {self.data}\nPrevious Hash: {self.previous_hash}\nHash: {self.calculate_hash()}\nNonce: {self.nonce}\n"
        pass

    def calculate_hash(self):
        # hexdigest() returns the hash in hexadecimal format so it is easier to read
        # encode() converts the string to bytes
        return sha256(f"{self.timestamp}{self.data}{self.previous_hash}{self.nonce}".encode()).hexdigest()


class Blockchain:

    def __init__(self) -> None:
        self.genesis_block = self.create_genesis_block()
        self.genesis_block_hash = self.genesis_block.calculate_hash()
        self.chain = [self.genesis_block]
        # self.all_transactions = []
        print(f"Genesis Block has been created with hash: {self.genesis_block_hash}")
        
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
        # we call the hash function of the last block to get the previous hash
        previous_hash = self.chain[-1].calculate_hash()
        # we create a new block with the data (transaction) and the previous hash
        new_block = Block(data, previous_hash)
        self.chain.append(new_block)
        pass    

    def validate_chain(self):
        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Si se aplica esta función siempre se detectará discrepancia en el hash propio del bloque
            # pero queremos que se vea la diferencia con el anterior?
            # Esto sirve cuando se quiere detectar si alguien ha cambiado el hash del bloque antes de la creacion del siguiente
            # if(current.hash != current.calculate_hash()):
            #     print(f"The current hash of the block {i} does not equal the calculated hash of the block.")
            #     return False
            
            # This if is very important if the atacker changes all the previous hashes
            print("Verificando block:", i)
            print("current:" ,current.previous_hash)
            print("previous:" ,previous.calculate_hash(), "\n")
            if i == 1:
                # separamos porque lo guardamos especialmente en una variable
                print("Genesis hash:" ,self.genesis_block_hash, "\n")
                if(current.previous_hash != self.genesis_block_hash):
                    print(f"The previous block's {i-1} hash does not equal the previous hash value stored in the current block {i}.")
                    return False
            if(current.previous_hash != previous.calculate_hash()):
                print(f"The previous block's {i-1} hash does not equal the previous hash value stored in the current block {i}.")
                return False
        return True


new_transactions = [{'amount': '30', 'sender':'alice', 'receiver':'bob'},
               	{'amount': '55', 'sender':'bob', 'receiver':'alice'}]
transaction2 = [{'amount': '2220', 'sender':'alice', 'receiver':'bob'}, {'amount': '55', 'sender':'bob', 'receiver':'alice'}]
transaction3 = [{'amount': '400', 'sender':'alice', 'receiver':'bob'}, {'amount': '55', 'sender':'bob', 'receiver':'alice'}]
transaction4 = [{'amount': '1000', 'sender':'alice', 'receiver':'bob'}, {'amount': '55', 'sender':'bob', 'receiver':'alice'}]

# funcionamiento correcto
def test1():
    my_blockchain = Blockchain()
    my_blockchain.add_block(new_transactions)
    my_blockchain.add_block(transaction2)
    my_blockchain.add_block(transaction3)
    my_blockchain.add_block(transaction4)
    my_blockchain.print_blocks()
    print(my_blockchain.validate_chain())

# fallo en el bloque 2
def test2():
    my_blockchain = Blockchain()
    my_blockchain.add_block(new_transactions)
    my_blockchain.add_block(transaction2)
    my_blockchain.add_block(transaction3)
    my_blockchain.chain[2].data = "fake_transactions"
    my_blockchain.add_block(transaction4)
    my_blockchain.print_blocks()
    print(my_blockchain.validate_chain())

# fallo en todos los bloques. Se compara con el genesis block
def test3():
    my_blockchain = Blockchain()
    my_blockchain.add_block(new_transactions)
    my_blockchain.add_block(transaction2)
    my_blockchain.add_block(transaction3)
    my_blockchain.add_block(transaction4)
    my_blockchain.chain[0].data = "daepolnbvsi1345bsnasmkc"
    my_blockchain.chain[1].data = "lololol"
    my_blockchain.chain[2].data = "fake_hash"
    my_blockchain.chain[3].data = "xdxdxdxxdxdxdxd"
    my_blockchain.chain[4].data = "fake_hash"
    my_blockchain.print_blocks()
    print(my_blockchain.validate_chain())

# para este test descomentar la linea 17 y de 71 a 73
# correr y despues descomentar
def test4():
    my_blockchain = Blockchain()
    # my_blockchain.chain[0].data = "fake_transactions0"
    my_blockchain.add_block(new_transactions)
    my_blockchain.chain[1].data = "fake_transactions1"
    my_blockchain.add_block(transaction2)
    my_blockchain.chain[2].data = "fake_transactions2"
    my_blockchain.add_block(transaction3)
    my_blockchain.chain[3].data = "fake_transactions3"
    my_blockchain.add_block(transaction4)
    my_blockchain.chain[4].data = "fake_transactions4"

    my_blockchain.print_blocks()
    print(my_blockchain.validate_chain())

# test1()
# test2()
# test3()
test4()

