# standard imports
import os
import unittest
import json
import logging
import hashlib

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        )
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from giftable_erc20_token import GiftableToken
from hexathon import (
    add_0x,
    strip_0x,
    )

# local imports
from eth_address_declarator.declarator import AddressDeclarator
from eth_address_declarator import Declarator
from eth_address_declarator.unittest import TestAddressDeclaratorBase

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

testdir = os.path.dirname(__file__)

description = '0x{:<064s}'.format(b'foo'.hex())


class TestAddressDeclarator(TestAddressDeclaratorBase):

    def setUp(self):
        super(TestAddressDeclarator, self).setUp()
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)

       #c = GiftableToken(signer=self.signer, nonce_oracle=nonce_oracle, chain_id=self.chain_spec.chain_id())
        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], 'BarToken', 'BAR', 6)
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.bar_token_address = r['contract_address']


    def test_basic(self):
       
        d = add_0x(os.urandom(32).hex())

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[0], self.foo_token_address, d)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.foo_token_address, d)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[0], self.bar_token_address, d)
        self.rpc.do(o)

        o = c.declarator_count(self.address, self.foo_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declarator_count(r), 2)

        o = c.declarator_count(self.address, self.bar_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declarator_count(r), 1)


    def test_get_single_declaration(self):
        d = add_0x(os.urandom(32).hex())

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.foo_token_address, d)
        self.rpc.do(o)
        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        o = c.declaration(self.address, self.accounts[1], self.foo_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        proofs = c.parse_declaration(r)
        self.assertEqual(proofs[0], strip_0x(d))


    def test_declaration(self):

        d = add_0x(os.urandom(32).hex())
        d_two = add_0x(os.urandom(32).hex())

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.foo_token_address, d)
        self.rpc.do(o)

        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.foo_token_address, d_two)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[2], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[2], self.foo_token_address, d)
        self.rpc.do(o)

        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[2], self.bar_token_address, d)
        self.rpc.do(o)

        o = c.declaration(self.address, self.accounts[1], self.foo_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        proofs = c.parse_declaration(r)
        self.assertEqual(proofs[0], strip_0x(d))
        self.assertEqual(proofs[1], strip_0x(d_two))


    def test_declarator_to_subject(self):
        d = add_0x(os.urandom(32).hex())

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.foo_token_address, d)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[2], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[2], self.foo_token_address, d)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.bar_token_address, d)
        self.rpc.do(o)

        o = c.declaration_address_at(self.address, self.accounts[1], 0, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declaration_address_at(r), strip_0x(self.foo_token_address))

        o = c.declaration_address_at(self.address, self.accounts[2], 0, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declaration_address_at(r), strip_0x(self.foo_token_address))

        o = c.declaration_address_at(self.address, self.accounts[1], 1, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declaration_address_at(r), strip_0x(self.bar_token_address))


    def test_subject_to_declarator(self):
        d = '0x' + os.urandom(32).hex()

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.foo_token_address, d)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[2], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[2], self.foo_token_address, d)
        self.rpc.do(o)

        nonce_oracle = RPCNonceOracle(self.accounts[1], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[1], self.bar_token_address, d)
        self.rpc.do(o)

        o = c.declarator_address_at(self.address, self.foo_token_address, 0, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declaration_address_at(r), strip_0x(self.accounts[1]))

        o = c.declarator_address_at(self.address, self.foo_token_address, 1, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declaration_address_at(r), strip_0x(self.accounts[2]))


    def test_three_first(self):
        d = []
        for i in range(3):
            d.append(add_0x(os.urandom(32).hex()))

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        for proof in d:
            (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[0], self.foo_token_address, proof)
            self.rpc.do(o)

        o = c.declarator_count(self.address, self.foo_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(c.parse_declarator_count(r), 1)

        o = c.declaration(self.address, self.accounts[0], self.foo_token_address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        proofs = c.parse_declaration(r)
        self.assertEqual(len(proofs), 3)

        for i in range(3):
            self.assertEqual(proofs[i], strip_0x(d[i]))


    def test_three_first_different(self):
        d = []
        a = []
        for i in range(3):
            d.append(add_0x(os.urandom(32).hex()))
            a.append(add_0x(os.urandom(20).hex()))

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = Declarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        for i in range(3):
            (tx_hash_hex, o) = c.add_declaration(self.address, self.accounts[0], a[i], d[i])
            self.rpc.do(o)

        for i in range(3):
            o = c.declarator_count(self.address, a[i], sender_address=self.accounts[0])
            r = self.rpc.do(o)
            self.assertEqual(c.parse_declarator_count(r), 1)

            o = c.declaration(self.address, self.accounts[0], a[i], sender_address=self.accounts[0])
            r = self.rpc.do(o)
            proofs = c.parse_declaration(r)
            self.assertEqual(len(proofs), 1)
            self.assertEqual(proofs[0], strip_0x(d[i]))


if __name__ == '__main__':
    unittest.main()
