import logging
import os
import json
import hashlib

import web3
import eth_tester

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


eth_params = eth_tester.backends.pyevm.main.get_default_genesis_params({
    'gas_limit': 9000000,
    })
backend = eth_tester.PyEVMBackend(eth_params)
instance = eth_tester.EthereumTester(backend)
provider = web3.Web3.EthereumTesterProvider(instance)
w3 = web3.Web3(provider)


f = open('AddressDeclarator.bin', 'r')
bytecode = f.read()
f.close()

f = open('AddressDeclarator.json', 'r')
abi = json.load(f)
f.close()

#token_address = web3.Web3.toChecksumAddress('0x' + os.urandom(20).hex())

c = w3.eth.contract(abi=abi, bytecode=bytecode)
#tx_hash = c.constructor().transact({'from': w3.eth.accounts[0]})

declarations = [
    ['0x' + os.urandom(32).hex(), '0x' + os.urandom(32).hex()],
    ['0x' + os.urandom(32).hex(), '0x' + os.urandom(32).hex()],
    ['0x' + os.urandom(32).hex(), '0x' + os.urandom(32).hex()],
    ['0x' + os.urandom(32).hex(), '0x' + os.urandom(32).hex()],
        ]

# Deployment is a self-signed declaration
tx_hash = c.constructor(declarations[0][0]).transact({'from': w3.eth.accounts[0]})
r = w3.eth.getTransactionReceipt(tx_hash)
logg.debug('contract {}'.format(r.contractAddress))

c = w3.eth.contract(abi=abi, address=r.contractAddress)

r = c.functions.declaratorCount(w3.eth.accounts[0]).call()
assert r == 1

r = c.functions.declaratorAddressAt(w3.eth.accounts[0], 0).call()
assert r == w3.eth.accounts[0]

r = c.functions.declaration(w3.eth.accounts[0], w3.eth.accounts[0]).call()
assert r[0].hex() == declarations[0][0][2:]


# Add first declaration for 0 by 2
c.functions.addDeclaration(w3.eth.accounts[0], declarations[1][0]).transact({'from': w3.eth.accounts[2]})

r = c.functions.declaratorCount(w3.eth.accounts[0]).call()
assert r == 2

r = c.functions.declaratorAddressAt(w3.eth.accounts[0], 1).call()
assert r == w3.eth.accounts[2]

r = c.functions.declaration(w3.eth.accounts[2], w3.eth.accounts[0]).call()
assert r[0].hex() == declarations[1][0][2:]


# Add second declaration for 0 by 2
c.functions.addDeclaration(w3.eth.accounts[0], declarations[1][1]).transact({'from': w3.eth.accounts[2]})

r = c.functions.declaratorCount(w3.eth.accounts[0]).call()
assert r == 2


r = c.functions.declaration(w3.eth.accounts[2], w3.eth.accounts[0]).call()
assert r[0].hex() == declarations[1][0][2:]
assert r[1].hex() == declarations[1][1][2:]


# Add first declaration for 1 by 2
c.functions.addDeclaration(w3.eth.accounts[1], declarations[2][0]).transact({'from': w3.eth.accounts[2]})

r = c.functions.declaratorCount(w3.eth.accounts[0]).call()
assert r == 2

r = c.functions.declaratorCount(w3.eth.accounts[1]).call()
assert r == 1

r = c.functions.declaratorAddressAt(w3.eth.accounts[1], 0).call()
assert r == w3.eth.accounts[2]

r = c.functions.declaration(w3.eth.accounts[2], w3.eth.accounts[1]).call()
assert r[0].hex() == declarations[2][0][2:]


# Add declaration for 0 by 3
c.functions.addDeclaration(w3.eth.accounts[0], declarations[3][0]).transact({'from': w3.eth.accounts[3]})


# 0 declared itself and 1
r = c.functions.declarationCount(w3.eth.accounts[0]).call()
assert r == 1

# 0 was declared by itself, 1 and 3
r = c.functions.declaratorCount(w3.eth.accounts[0]).call()
assert r == 3

# 1 declared noone
r = c.functions.declarationCount(w3.eth.accounts[1]).call()
assert r == 0

# 1 was declared by 2
r = c.functions.declaratorCount(w3.eth.accounts[1]).call()
assert r == 1

# 2 declared 0 and 1
r = c.functions.declarationCount(w3.eth.accounts[2]).call()
assert r == 2

# 2 was declared by noone
r = c.functions.declaratorCount(w3.eth.accounts[2]).call()
assert r == 0

# 3 declared 0
r = c.functions.declarationCount(w3.eth.accounts[3]).call()
assert r == 1

# 3 was declared by noone
r = c.functions.declaratorCount(w3.eth.accounts[3]).call()
assert r == 0
