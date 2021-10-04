# standard imports
import os

# external imports
from chainlib.eth.tx import (
        TxFormat,
        )
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        )
from eth_accounts_index.interface import AccountsIndex

moddir = os.path.dirname(__file__)
datadir = os.path.join(moddir, '..', 'data')


class AccountsIndexAddressDeclarator(AccountsIndex):

    __abi = None
    __bytecode = None

    @staticmethod
    def abi():
        if AccountsIndexAddressDeclarator.__abi == None:
            f = open(os.path.join(datadir, 'AccountsIndexAddressDeclarator.json'), 'r')
            AccountsIndexAddressDeclarator.__abi = json.load(f)
            f.close()
        return AccountsIndexAddressDeclarator.__abi


    @staticmethod
    def bytecode():
        if AccountsIndexAddressDeclarator.__bytecode == None:
            f = open(os.path.join(datadir, 'AccountsIndexAddressDeclarator.bin'))
            AccountsIndexAddressDeclarator.__bytecode = f.read()
            f.close()
        return AccountsIndexAddressDeclarator.__bytecode


    @staticmethod
    def gas(code=None):
        return 700000


    def constructor(self, sender_address, context_address, address_declarator_address):
        code = AccountsIndexAddressDeclarator.bytecode()
        tx = self.template(sender_address, None, use_nonce=True)
        enc = ABIContractEncoder()
        enc.address(context_address)
        enc.address(address_declarator_address)
        code += enc.get()
        tx = self.set_code(tx, code)
        return self.build(tx)
