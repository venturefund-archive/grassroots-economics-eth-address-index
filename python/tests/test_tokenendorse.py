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

description = '0x{:<064s}'.format(b'foo'.hex())

class Test(unittest.TestCase):

    contract = None

    def setUp(self):
        eth_params = eth_tester.backends.pyevm.main.get_default_genesis_params({
            'gas_limit': 9000000,
            })

        # create store of used accounts
        f = open(os.path.join(testdir, '../eth_address_declarator/data/AddressDeclarator.bin'), 'r')
        bytecode = f.read()
        f.close()

        f = open(os.path.join(testdir, '../eth_address_declarator/data/AddressDeclarator.json'), 'r')
        self.abi = json.load(f)
        f.close()
        
        backend = eth_tester.PyEVMBackend(eth_params)
        self.eth_tester =  eth_tester.EthereumTester(backend)
        provider = web3.Web3.EthereumTesterProvider(self.eth_tester)
        self.w3 = web3.Web3(provider)
        c = self.w3.eth.contract(abi=self.abi, bytecode=bytecode)
        tx_hash = c.constructor(description).transact({'from': self.w3.eth.accounts[0]})

        r = self.w3.eth.getTransactionReceipt(tx_hash)

        self.address = r.contractAddress


        # create token
        f = open(os.path.join(testdir, '../eth_address_declarator/data/GiftableToken.bin'), 'r')
        bytecode = f.read()
        f.close()

        f = open(os.path.join(testdir, '../eth_address_declarator/data/GiftableToken.json'), 'r')
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
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[0]})
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_two, d).transact({'from': self.w3.eth.accounts[0]})

        self.assertEqual(c.functions.declaratorCount(self.address_token_one).call(), 2)
        self.assertEqual(c.functions.declaratorCount(self.address_token_two).call(), 1)


    def test_declaration(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        d = '0x' + os.urandom(32).hex()
        d_two = '0x' + os.urandom(32).hex()
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_one, d_two).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[2]})
        c.functions.addDeclaration(self.address_token_two, d).transact({'from': self.w3.eth.accounts[2]})

        proofs = c.functions.declaration(self.w3.eth.accounts[1], self.address_token_one).call()
        self.assertEqual(proofs[0].hex(), d[2:])
        self.assertEqual(proofs[1].hex(), d_two[2:])


    def test_declaration_count(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        d = '0x' + os.urandom(32).hex()
        d_two = '0x' + os.urandom(32).hex()
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_one, d_two).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[2]})
        c.functions.addDeclaration(self.address_token_two, d).transact({'from': self.w3.eth.accounts[2]})

        self.assertEqual(c.functions.declarationCount(self.w3.eth.accounts[1]).call(), 1)
        self.assertEqual(c.functions.declarationCount(self.w3.eth.accounts[2]).call(), 2)

    
    def test_declarator_to_subject(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        d = '0x' + os.urandom(32).hex()
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[2]})
        c.functions.addDeclaration(self.address_token_two, d).transact({'from': self.w3.eth.accounts[1]})


        self.assertEqual(c.functions.declarationAddressAt(self.w3.eth.accounts[1], 0).call(), self.address_token_one)
        self.assertEqual(c.functions.declarationAddressAt(self.w3.eth.accounts[2], 0).call(), self.address_token_one)
        self.assertEqual(c.functions.declarationAddressAt(self.w3.eth.accounts[1], 1).call(), self.address_token_two)


    def test_subject_to_declarator(self):
        c = self.w3.eth.contract(abi=self.abi, address=self.address)

        d = '0x' + os.urandom(32).hex()
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[1]})
        c.functions.addDeclaration(self.address_token_one, d).transact({'from': self.w3.eth.accounts[2]})
        c.functions.addDeclaration(self.address_token_two, d).transact({'from': self.w3.eth.accounts[1]})

        self.assertEqual(c.functions.declaratorAddressAt(self.address_token_one, 0).call(), self.w3.eth.accounts[1])
        self.assertEqual(c.functions.declaratorAddressAt(self.address_token_one, 1).call(), self.w3.eth.accounts[2])
    

if __name__ == '__main__':
    unittest.main()
