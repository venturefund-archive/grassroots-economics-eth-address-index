"""View address declaration, and attempt to resolve contents

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import urllib
import os
import json
import argparse
import logging
import sys

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.error import JSONRPCException
from chainlib.eth.address import to_checksum_address
from hexathon import (
        add_0x,
        strip_0x,
        )

# local imports
from eth_address_declarator import Declarator
from eth_address_declarator.declarator import AddressDeclarator

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

#argparser.add_argument('--resolve', action='store_true', help='Attempt to resolve the hashes to actual content')
#argparser.add_argument('--resolve-http', dest='resolve_http', type=str, help='Base url to look up content hashes')
arg_flags = chainlib.eth.cli.argflag_std_read | chainlib.eth.cli.Flag.EXEC
argparser = chainlib.eth.cli.ArgumentParser(arg_flags)
argparser.add_argument('--declarator-address', required=True, type=str, help='Declarator of address')
argparser.add_positional('address', type=str, help='Ethereum declaration address to look up')
args = argparser.parse_args()

extra_args = {
    'declarator_address': None,
    'address': None,
        }
config = chainlib.eth.cli.Config.from_args(args, arg_flags, extra_args=extra_args, default_fee_limit=AddressDeclarator.gas())

wallet = chainlib.eth.cli.Wallet()
wallet.from_config(config)

rpc = chainlib.eth.cli.Rpc()
conn = rpc.connect_by_config(config)

chain_spec = ChainSpec.from_chain_str(config.get('CHAIN_SPEC'))


def out_element(e, w=sys.stdout):
    w.write(e[1] + '\n')


def ls(ifc, conn, contract_address, declarator_address, subject_address, w=sys.stdout):
    o = ifc.declaration(contract_address, declarator_address, subject_address)
    r =  conn.do(o)
    declarations = ifc.parse_declaration(r)

    for i, d in enumerate(declarations):
        out_element((i, d), w)


def main():

    c = Declarator(chain_spec)

    contract_address = to_checksum_address(config.get('_EXEC_ADDRESS'))
    if not config.true('_UNSAFE') and contract_address != add_0x(config.get('_EXEC_ADDRESS')):
        raise ValueError('invalid checksum address for contract')


    declarator_address = to_checksum_address(config.get('_DECLARATOR_ADDRESS'))
    if not config.true('_UNSAFE') and declarator_address != add_0x(config.get('_DECLARATOR_ADDRESS')):
        raise ValueError('invalid checksum address for declarator')

    subject_address = to_checksum_address(config.get('_ADDRESS'))
    if not config.true('_UNSAFE') and subject_address != add_0x(config.get('_ADDRESS')):
        raise ValueError('invalid checksum address for subject')

    ls(c, conn, contract_address, declarator_address, subject_address)

    declarations = []

#    for d in declarations:
#        if not args.resolve:
#            print(d.hex())
#            continue
#        if args.resolve_http:
#            try:
#                r = try_sha256(d)
#                print(r)
#                continue
#            except urllib.error.HTTPError:
#                pass
#        try:
#            print(try_utf8(d))
#        except UnicodeDecodeError:
#            pass


if __name__ == '__main__':
    main()
