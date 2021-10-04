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

logg = logging.getLogger(__name__)

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, '..', 'data')


def to_identifier(s):
    h = hashlib.new('sha256')
    h.update(s.encode('utf-8'))
    return h.digest().hex()


class TokenUniqueSymbolIndex(TxFactory):

    def register(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('register')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def address_of(self, contract_address, token_symbol, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('addressOf')
        enc.typ(ABIContractType.BYTES32)
        token_symbol_digest = to_identifier(token_symbol)
        enc.bytes32(token_symbol_digest)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    def entry(self, contract_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('entry')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(idx)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    def entry_count(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('entryCount')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    @classmethod
    def parse_address_of(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)


    @classmethod
    def parse_entry(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)


    @classmethod
    def parse_entry_count(self, v):
        return abi_decode_single(ABIContractType.UINT256, v)
