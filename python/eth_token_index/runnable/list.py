"""Adds a new token to the token symbol index

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import json
import argparse
import logging
import hashlib

# third-party imports
from crypto_dev_signer.eth.signer import ReferenceSigner as EIP155Signer
from crypto_dev_signer.keystore.dict import DictKeystore
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.erc20 import ERC20

# local imports
from eth_token_index import TokenUniqueSymbolIndex

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()
default_format = 'terminal'

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-i', '--chain-spec', dest='i', type=str, default='Ethereum:1', help='Chain specification string')
argparser.add_argument('-a', '--contract-address', dest='a', type=str, required=True, help='Token endorsement contract address')
argparser.add_argument('-f', '--format', dest='f', type=str, default=default_format, help='Output format [human, brief]')
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('-vv', action='store_true', help='Be more verbose')
argparser.add_argument('token_symbol', type=str, nargs='?', help='Token symbol to return address for')
args = argparser.parse_args()

if args.vv:
    logg.setLevel(logging.DEBUG)
elif args.v:
    logg.setLevel(logging.INFO)

rpc = EthHTTPConnection(args.p)
contract_address = args.a

token_symbol = args.token_symbol
fmt = args.f


def out_element(e, fmt=default_format, w=sys.stdout):
    if fmt == 'brief':
        w.write(e[1] + '\n')
    else:
        w.write('{} {}\n'.format(e[0], e[1]))


def element(ifc, contract_address, token_symbol, fmt=fmt, w=sys.stdout):
    o = ifc.address_of(contract_address, token_symbol)
    r = rpc.do(o)
    a = ifc.parse_address_of(r)
    out_element((token_symbol, a), fmt, w)


def ls(ifc, contract_address, token_ifc, fmt=fmt, w=sys.stdout):
    o = ifc.entry_count(contract_address)
    r = rpc.do(o)
    count = ifc.parse_entry_count(r)
    logg.debug('count {}'.format(count))

    for i in range(count):
        o = ifc.entry(contract_address, i)
        r = rpc.do(o)
        token_address = ifc.parse_entry(r)

        o = token_ifc.symbol(token_address)
        r = rpc.do(o)
        token_symbol = token_ifc.parse_symbol(r)

        element(ifc, contract_address, token_symbol, fmt, w)


def main():
    token_ifc = ERC20()
    ifc = TokenUniqueSymbolIndex()
    if token_symbol != None:
        element(ifc, contract_address, token_ifc, token_symbol, fmt, sys.stdout)
    else:
        ls(ifc, contract_address, token_ifc, fmt, sys.stdout)


if __name__ == '__main__':
    main()
