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


class TokenEndorser:

    __abi = None
    __bytecode = None
    __address = None

    def __init__(self, w3, address, signer_address=None):
        abi = TokenEndorser.abi()
        TokenEndorser.bytecode()
        self.__address = address
        self.contract = w3.eth.contract(abi=abi, address=address)
        self.w3 = w3
        if signer_address != None:
            self.signer_address = signer_address
        else:
            if type(self.w3.eth.defaultAccount).__name__ == 'Empty':
                self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
            self.signer_address = self.w3.eth.defaultAccount


    @staticmethod
    def abi():
        if TokenEndorser.__abi == None:
            f = open(os.path.join(datadir, 'AccountDeclarator.json'), 'r')
            AccountDeclarator.__abi = json.load(f)
            f.close()
        return TokenEndorser.__abi


    @staticmethod
    def bytecode():
        if TokenEndorser.__bytecode == None:
            f = open(os.path.join(datadir, 'AccountDeclarator.bin'))
            AccountDeclarator.__bytecode = f.read()
            f.close()
        return TokenEndorser.__bytecode


#    def token_from_symbol(self, symbol):
#        return self.contract.functions.tokenSymbolIndex(symbol).call()
#    def 

#
#    def endorsed_tokens(self, endorser_address):
#        tokens = []
#        for i in range(self.contract.functions.endorserTokenCount(endorser_address).call()):
#            tidx = self.contract.functions.endorser(endorser_address, i).call()
#            t = self.contract.functions.tokens(tidx).call()
#            tokens.append(t)
#        return tokens
#
#    def declared(self, declarator_address):
#        addresses = []
#        for i 
#
#
#    def add(self, token_address, data):
#        self.contract.functions.add(token_address, data).transact({'from': self.signer_address})
#

def to_endorsement_key(declarator_address_hex, declaration_address_hex):
    h = hashlib.new('sha256')
    h.update(bytes.fromhex(token_address_hex[2:]))
    h.update(bytes.fromhex(endorser_address_hex[2:]))
    return h.digest()


