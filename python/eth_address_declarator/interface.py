# standard imports
import logging
import json
import os

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
from chainlib.jsonrpc import JSONRPCRequest
from chainlib.eth.constant import ZERO_ADDRESS

logg = logging.getLogger(__name__)


class Declarator(TxFactory):

    def add_declaration(self, contract_address, sender_address, subject_address, proof, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('addDeclaration')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.BYTES32)
        enc.address(subject_address)
        enc.bytes32(proof)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def declarator_count(self, contract_address, subject_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('declaratorCount')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(subject_address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    def declaration(self, contract_address, declarator_address, subject_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('declaration')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.ADDRESS)
        enc.address(declarator_address)
        enc.address(subject_address)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    def declaration_address_at(self, contract_address, declarator_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('declarationAddressAt')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.UINT256)
        enc.address(declarator_address)
        enc.uint256(idx)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    def declarator_address_at(self, contract_address, subject_address, idx, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('declaratorAddressAt')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.UINT256)
        enc.address(subject_address)
        enc.uint256(idx)
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o = j.finalize(o)
        return o


    @classmethod
    def parse_declarator_count(self, v):
        return abi_decode_single(ABIContractType.UINT256, v)

    
    @classmethod
    def parse_declaration(self, v):
        cursor = 0
        r = []
        try:
            v = strip_0x(v)
        except ValueError:
            return r
        position = int.from_bytes(bytes.fromhex(v[cursor:cursor+64]), 'big')
        cursor += (position * 2)
        length = int.from_bytes(bytes.fromhex(v[cursor:cursor+64]), 'big')
        cursor += 64
        for i in range(length):
            r.append(v[cursor:cursor+64])
            cursor += 64
        return r 


    @classmethod
    def parse_declaration_address_at(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)


    @classmethod
    def parse_declarator_address_at(self, v):
        return abi_decode_single(ABIContractType.ADDRESS, v)
