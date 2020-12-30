# Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
# SPDX-License-Identifier:	GPL-3.0-or-later
# File-version: 1
# Description: Python interface to abi and bin files for faucet contracts

# standard imports
import logging
import json
import os
import hashlib

logg = logging.getLogger(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')


class TokenUniqueSymbolIndex:

    __abi = None
    __bytecode = None
    __address = None
    __erc20_abi = None

    def __init__(self, w3, address, signer_address=None):
        abi = TokenUniqueSymbolIndex.abi()
        TokenUniqueSymbolIndex.bytecode()
        self.__address = address
        self.contract = w3.eth.contract(abi=abi, address=address)
        self.w3 = w3
        if signer_address != None:
            self.signer_address = signer_address
        else:
            if type(self.w3.eth.defaultAccount).__name__ == 'Empty':
                self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
            self.signer_address = self.w3.eth.defaultAccount
        
        f = open(os.path.join(datadir, 'ERC20.json'), 'r')
        TokenUniqueSymbolIndex.__erc20_abi = json.load(f)
        f.close()


    @staticmethod
    def abi():
        if TokenUniqueSymbolIndex.__abi == None:
            f = open(os.path.join(datadir, 'TokenUniqueSymbolIndex.json'), 'r')
            TokenUniqueSymbolIndex.__abi = json.load(f)
            f.close()
        return TokenUniqueSymbolIndex.__abi


    @staticmethod
    def bytecode():
        if TokenUniqueSymbolIndex.__bytecode == None:
            f = open(os.path.join(datadir, 'TokenUniqueSymbolIndex.bin'))
            TokenUniqueSymbolIndex.__bytecode = f.read()
            f.close()
        return TokenUniqueSymbolIndex.__bytecode


    def add(self, address):
        c = self.w3.eth.contract(abi=TokenUniqueSymbolIndex.__erc20_abi, address=address)
        s = c.functions.symbol().call()
        h = to_ref(s)
        return self.contract.functions.register(h, address).transact({'from':self.signer_address})


    def count(self):
        return self.contract.functions.registryCount().call()


    def get_index(self, idx):
        return self.contract.functions.entry(idx).call()


    def get_token_by_symbol(self, symbol):
        ref = to_ref(symbol)
        return self.contract.functions.addressOf(symbol).call()


def to_ref(s):
    h = hashlib.new('sha256')
    h.update(s.encode('utf-8'))
    return h.digest().hex()
