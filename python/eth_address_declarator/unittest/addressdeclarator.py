# standard imports
import unittest
import logging
import os

# external imports
from hexathon import add_0x
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from giftable_erc20_token import GiftableToken

# local imports
from eth_address_declarator.declarator import AddressDeclarator

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestAddressDeclaratorBase(EthTesterCase):

    def setUp(self):
        super(TestAddressDeclaratorBase, self).setUp()
        self.description = add_0x(os.urandom(32).hex())
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = AddressDeclarator(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], self.description)
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.address = r['contract_address']
        logg.debug('address declarator deployed with address {}'.format(self.address))

        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], 'FooToken', 'FOO', 6)
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.foo_token_address = r['contract_address']
        logg.debug('foo token deployed with address {}'.format(self.foo_token_address))
