# Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
# SPDX-License-Identifier:	GPL-3.0-or-later
# File-version: 1
# Description: Python interface to abi and bin files for faucet contracts

# standard imports
import logging
import json
import os
import hashlib

# external imports
from hexathon import (
        strip_0x,
        add_0x,
        )
from chainlib.eth.tx import (
        TxFormat,
        TxFactory,
        )
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        abi_decode_single,
        )
from chainlib.eth.constant import ZERO_ADDRESS

# local imports
from eth_address_declarator import Declarator

logg = logging.getLogger(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, 'data')


def to_declarator_key(declarator_address_hex, declaration_address_hex):
    h = hashlib.new('sha256')
    h.update(bytes.fromhex(strip_0x(declaration_address_hex)))
    h.update(bytes.fromhex(strip_0x(declarator_address_hex)))
    return h.digest()


class AddressDeclarator(Declarator):

    __abi = None
    __bytecode = None

    @staticmethod
    def abi():
        if AddressDeclarator.__abi == None:
            f = open(os.path.join(datadir, 'AddressDeclarator.json'), 'r')
            AddressDeclarator.__abi = json.load(f)
            f.close()
        return AddressDeclarator.__abi


    @staticmethod
    def bytecode():
        if AddressDeclarator.__bytecode == None:
            f = open(os.path.join(datadir, 'AddressDeclarator.bin'))
            AddressDeclarator.__bytecode = f.read()
            f.close()
        return AddressDeclarator.__bytecode


    @staticmethod
    def gas(code=None):
        return 2000000


    def constructor(self, sender_address, initial_description):
        code = AddressDeclarator.bytecode()
        enc = ABIContractEncoder()
        initial_description_hex = add_0x(initial_description)
        enc.bytes32(initial_description_hex)
        code += enc.get()
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.build(tx)
