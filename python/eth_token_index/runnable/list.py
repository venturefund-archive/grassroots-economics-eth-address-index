"""Adds a new token to the token symbol index

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
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

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-i', '--chain-spec', dest='i', type=str, default='Ethereum:1', help='Chain specification string')
argparser.add_argument('-a', '--contract-address', dest='a', type=str, required=True, help='Token endorsement contract address')
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('-vv', action='store_true', help='Be more verbose')
args = argparser.parse_args()

if args.vv:
    logg.setLevel(logging.DEBUG)
elif args.v:
    logg.setLevel(logging.INFO)

rpc = EthHTTPConnection(args.p)
contract_address = args.a


def main():
    ct = ERC20()
    c = TokenUniqueSymbolIndex()
    o = c.entry_count(contract_address)
    r = rpc.do(o)
    count = TokenUniqueSymbolIndex.parse_entry_count(r)

    for i in range(count):
        o = c.entry(contract_address, i)
        r = rpc.do(o)
        token_address = TokenUniqueSymbolIndex.parse_entry(r)

        o = ct.symbol(token_address)
        r = rpc.do(o)
        token_symbol = ERC20.parse_symbol(r)

        print('{} {}'.format(token_symbol, token_address))


if __name__ == '__main__':
    main()
