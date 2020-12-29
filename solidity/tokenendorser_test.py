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


f = open('TokenEndorser.bin', 'r')
bytecode = f.read()
f.close()

f = open('TokenEndorser.json', 'r')
abi = json.load(f)
f.close()

token_address = web3.Web3.toChecksumAddress('0x' + os.urandom(20).hex())

c = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = c.constructor().transact({'from': w3.eth.accounts[0]})
r = w3.eth.getTransactionReceipt(tx_hash)
logg.debug('contract {} initial token {}'.format(r.contractAddress, token_address))

c = w3.eth.contract(abi=abi, address=r.contractAddress)
d = '0x' + os.urandom(32).hex()

# Initial token will fail in any case
c.functions.add(token_address, d).transact({'from':w3.eth.accounts[0]})

fail = False
try:
    c.functions.add(token_address, d).transact({'from':w3.eth.accounts[0]})
except:
    fail = True
    pass

if not fail:
    raise RuntimeError('expected fail on register same token to same address')


c.functions.add(token_address, d).transact({'from':w3.eth.accounts[1]})


h = hashlib.new('sha256')
h.update(bytes.fromhex(token_address[2:]))
h.update(bytes.fromhex(w3.eth.accounts[0][2:]))
z = h.digest()

assert d[2:] == c.functions.endorsement(z.hex()).call().hex()


another_token_address = web3.Web3.toChecksumAddress('0x' + os.urandom(20).hex())
c.functions.add(another_token_address, d).transact({'from':w3.eth.accounts[0]})

assert c.functions.endorsers(w3.eth.accounts[0], 0).call() == 1
assert c.functions.endorsers(w3.eth.accounts[1], 0).call() == 1
assert c.functions.endorsers(w3.eth.accounts[0], 1).call() == 2

assert c.functions.tokens(1).call() == token_address
assert c.functions.tokens(2).call() == another_token_address

assert c.functions.tokenIndex(token_address).call() == 1
assert c.functions.tokenIndex(another_token_address).call() == 2


