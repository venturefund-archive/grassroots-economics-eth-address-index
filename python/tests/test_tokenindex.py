# standard imports
import os
import unittest
import json
import logging
import hashlib

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from giftable_erc20_token import GiftableToken
from chainlib.eth.tx import unpack
from hexathon import strip_0x

# local imports
from eth_token_index import TokenUniqueSymbolIndex

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('eth.vm').setLevel(logging.WARNING)

testdir = os.path.dirname(__file__)


class Test(EthTesterCase):

    def setUp(self):
        super(Test, self).setUp()
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        #c = TokenUniqueSymbolIndex(signer=self.signer, nonce_oracle=nonce_oracle, chain_id=self.chain_spec.chain_id())
        c = TokenUniqueSymbolIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0])
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.address = r['contract_address']

        #c = GiftableToken(signer=self.signer, nonce_oracle=nonce_oracle, chain_id=self.chain_spec.chain_id())
        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], 'FooToken', 'FOO', 6)
        self.rpc.do(o)

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.token_address = r['contract_address']


    def test_register(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        #c = TokenUniqueSymbolIndex(signer=self.signer, nonce_oracle=nonce_oracle, chain_id=self.chain_spec.chain_id())
        c = TokenUniqueSymbolIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        
        (tx_hash_hex, o) = c.register(self.address, self.accounts[0], self.token_address)
        self.rpc.do(o)
        e = unpack(bytes.fromhex(strip_0x(o['params'][0])), self.chain_spec)
        logg.debug('e {}'.format(e))

        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        o = c.address_of(self.address, 'FOO', sender_address=self.accounts[0])
        r = self.rpc.do(o)
        address = c.parse_address_of(r)
        self.assertEqual(address, self.token_address)
        
        o = c.entry(self.address, 0, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        address = c.parse_entry(r)
        self.assertEqual(address, self.token_address)
        
        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 1)
        

if __name__ == '__main__':
    unittest.main()
