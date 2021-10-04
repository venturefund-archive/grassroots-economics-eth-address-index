# Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
# SPDX-License-Identifier:	GPL-3.0-or-later
# File-version: 1
# Description: Python interface to abi and bin files for token index with address declarator backend

# standard imports
import logging
import json
import os
import hashlib

# external imports
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.eth.tx import (
        TxFactory,
        TxFormat,
        )
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.constant import ZERO_ADDRESS
from hexathon import (
        add_0x,
        )

# local imports
from .interface import (
        TokenUniqueSymbolIndex,
        to_identifier,
        )

logg = logging.getLogger(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, '..', 'data')



class TokenUniqueSymbolIndexAddressDeclarator(TokenUniqueSymbolIndex):

    __abi = None
    __bytecode = None


    @staticmethod
    def abi():
        if TokenUniqueSymbolIndexAddressDeclarator.__abi == None:
            f = open(os.path.join(datadir, 'TokenUniqueSymbolIndexAddressDeclarator.json'), 'r')
            TokenUniqueSymbolIndexAddressDeclarator.__abi = json.load(f)
            f.close()
        return TokenUniqueSymbolIndexAddressDeclarator.__abi


    @staticmethod
    def bytecode():
        if TokenUniqueSymbolIndexAddressDeclarator.__bytecode == None:
            f = open(os.path.join(datadir, 'TokenUniqueSymbolIndexAddressDeclarator.bin'))
            TokenUniqueSymbolIndexAddressDeclarator.__bytecode = f.read()
            f.close()
        return TokenUniqueSymbolIndexAddressDeclarator.__bytecode


    @staticmethod
    def gas(code=None):
        return 2000000


    def constructor(self, sender_address, address_declarator_address):
        code = TokenUniqueSymbolIndexAddressDeclarator.bytecode()
        tx = self.template(sender_address, None, use_nonce=True)
        enc = ABIContractEncoder()
        enc.address(address_declarator_address)
        code += enc.get()
        tx = self.set_code(tx, code)
        return self.build(tx)
