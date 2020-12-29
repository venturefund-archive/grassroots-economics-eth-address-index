import os
import unittest
import json
import logging
import hashlib

import web3
import eth_tester
import eth_abi

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('eth.vm').setLevel(logging.WARNING)

testdir = os.path.dirname(__file__)


class Test(unittest.TestCase):

    contract = None

    def setUp(self):
        eth_params = eth_tester.backends.pyevm.main.get_default_genesis_params({
            'gas_limit': 9000000,
            })

        # create store of used accounts
        #f = open(os.path.join(testdir, '../eth_token_index/data/TokenUniqueSymbolIndex.bin'), 'r')
        f = open(os.path.join(testdir, '../../solidity/TokenUniqueSymbolIndex.bin'), 'r')
        bytecode = f.read()
        f.close()

        #f = open(os.path.join(testdir, '../eth_token_index/data/TokenUniqueSymbolIndex.json'), 'r')
        f = open(os.path.join(testdir, '../../solidity/TokenUniqueSymbolIndex.json'), 'r')
        self.abi = json.load(f)
        f.close()


        backend = eth_tester.PyEVMBackend(eth_params)
        self.eth_tester =  eth_tester.EthereumTester(backend)
        provider = web3.Web3.EthereumTesterProvider(self.eth_tester)
        self.w3 = web3.Web3(provider)
        c = self.w3.eth.contract(abi=self.abi, bytecode=bytecode)
        tx_hash = c.constructor().transact({'from': self.w3.eth.accounts[0]})

        r = self.w3.eth.getTransactionReceipt(tx_hash)

        self.address = r.contractAddress


        # create token
        f = open(os.path.join(testdir, '../eth_token_endorser/data/GiftableToken.bin'), 'r')
        bytecode = f.read()
        f.close()

        f = open(os.path.join(testdir, '../eth_token_endorser/data/GiftableToken.json'), 'r')
        self.abi_token = json.load(f)
        f.close()

        t = self.w3.eth.contract(abi=self.abi_token, bytecode=bytecode)
        tx_hash = t.constructor('Foo Token', 'FOO', 18).transact({'from': self.w3.eth.accounts[0]})

        r = self.w3.eth.getTransactionReceipt(tx_hash)

        self.address_token_one = r.contractAddress

        t = self.w3.eth.contract(abi=self.abi_token, bytecode=bytecode)
        tx_hash = t.constructor('Bar Token', 'BAR', 18).transact({'from': self.w3.eth.accounts[0]})

        r = self.w3.eth.getTransactionReceipt(tx_hash)

        self.address_token_two = r.contractAddress

        t = self.w3.eth.contract(abi=self.abi_token, bytecode=bytecode)
        tx_hash = t.constructor('Bar Token Duplicate', 'BAR', 18).transact({'from': self.w3.eth.accounts[0]})

        r = self.w3.eth.getTransactionReceipt(tx_hash)

        self.address_token_three = r.contractAddress


    def tearDown(self):
        pass


    def test_basic(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        h = hashlib.new('sha256')
        h.update('FOO'.encode('utf-8'))
        z = h.digest()

        # owner text
        with self.assertRaises(Exception):
            c.functions.register(z.hex(), self.address_token_one).transact({'from': self.w3.eth.accounts[1]})

        logg.debug('using identifier {}'.format(z.hex()))
        # Register FOO symbol
        c.functions.register(z.hex(), self.address_token_one).transact({'from': self.w3.eth.accounts[0]})

        # Raise on duplicate FOO symbol
        with self.assertRaises(Exception):
            c.functions.register(z.hex(), self.address_token_one).transact({'from': self.w3.eth.accounts[0]})

        # Raise on mismatch between supplied symbol and token symbol reported by ERC20
        with self.assertRaises(Exception):
            c.functions.register(z.hex(), self.address_token_two).transact({'from': self.w3.eth.accounts[0]})

        h = hashlib.new('sha256')
        h.update('BAR'.encode('utf-8'))
        z = h.digest()

        # Register BAR symbol
        c.functions.register(z.hex(), self.address_token_two).transact({'from': self.w3.eth.accounts[0]})

        # Raise on duplicate BAR symbol (with different token contract address)
        with self.assertRaises(Exception):
            c.functions.register(z.hex(), self.address_token_three).transact({'from': self.w3.eth.accounts[0]})


if __name__ == '__main__':
    unittest.main()
