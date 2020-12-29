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


f = open('TokenUniqueSymbolIndex.bin', 'r')
bytecode = f.read()
f.close()

f = open('TokenUniqueSymbolIndex.json', 'r')
abi = json.load(f)
f.close()

token_address = web3.Web3.toChecksumAddress('0x' + os.urandom(20).hex())

c = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = c.constructor().transact({'from': w3.eth.accounts[0]})
r = w3.eth.getTransactionReceipt(tx_hash)
logg.debug('contract {}'.format(r.contractAddress))

c = w3.eth.contract(abi=abi, address=r.contractAddress)
d = '0x' + os.urandom(32).hex()

# Initial token will fail in any case
h =hashlib.new('sha256')
h.update('FOO'.encode('utf-8'))
z = h.digest()
foo_symbol = z.hex()

fail = False
try:
    c.functions.register(foo_symbol, token_address).transact({'from':w3.eth.accounts[0]})
except:
    fail = True
    pass

if not fail:
    raise RuntimeError('expected fail on register same token to same address')
