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
        f = open(os.path.join(testdir, '../eth_token_endorser/data/TokenEndorser.bin'), 'r')
        bytecode = f.read()
        f.close()

        f = open(os.path.join(testdir, '../eth_token_endorser/data/TokenEndorser.json'), 'r')
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


    def tearDown(self):
        pass


    def test_basic(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        d = '0x' + os.urandom(32).hex()
        c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[0]})

        with self.assertRaises(Exception):
            c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[0]})

        c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.add(self.address_token_two, d).transact({'from': self.w3.eth.accounts[0]})
        c.functions.add(self.address_token_two, d).transact({'from': self.w3.eth.accounts[1]})

    def test_endorsement(self):

        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        d = '0x' + os.urandom(32).hex()
        c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[0]})
        c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})


        h = hashlib.new('sha256')
        h.update(bytes.fromhex(self.address_token_one[2:]))
        h.update(bytes.fromhex(self.w3.eth.accounts[0][2:]))
        z = h.digest()

        assert d[2:] == c.functions.endorsement(z.hex()).call().hex()

        #another_token_address = web3.Web3.toChecksumAddress('0x' + os.urandom(20).hex())
        c.functions.add(self.address_token_two, d).transact({'from': self.w3.eth.accounts[0]})

        assert c.functions.endorsers(self.w3.eth.accounts[0], 0).call() == 1
        assert c.functions.endorsers(self.w3.eth.accounts[1], 0).call() == 1
        assert c.functions.endorsers(self.w3.eth.accounts[0], 1).call() == 2

        assert c.functions.tokens(1).call() == self.address_token_one
        assert c.functions.tokens(2).call() == self.address_token_two

        assert c.functions.tokenIndex(self.address_token_one).call() == 1
        assert c.functions.tokenIndex(self.address_token_two).call() == 2



    def test_symbol_index(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)
        d = '0x' + os.urandom(32).hex()
        c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[0]})
        c.functions.add(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.add(self.address_token_two, d).transact({'from': self.w3.eth.accounts[1]})



if __name__ == '__main__':
    unittest.main()
