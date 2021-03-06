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
import web3
from crypto_dev_signer.eth.signer import ReferenceSigner as EIP155Signer
from crypto_dev_signer.keystore import DictKeystore
from crypto_dev_signer.eth.helper import EthTxExecutor
from chainlib.chain import ChainSpec

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-i', '--chain-spec', dest='i', type=str, default='Ethereum:1', help='Chain specification string')
argparser.add_argument('-a', '--contract-address', dest='a', type=str, help='Token endorsement contract address')
argparser.add_argument('--abi-dir', dest='abi_dir', type=str, default=data_dir, help='Directory containing bytecode and abi (default: {})'.format(data_dir))
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('-vv', action='store_true', help='Be more verbose')
args = argparser.parse_args()

if args.vv:
    logg.setLevel(logging.DEBUG)
elif args.v:
    logg.setLevel(logging.INFO)

w3 = web3.Web3(web3.Web3.HTTPProvider(args.p))

def main():
    f = open(os.path.join(args.abi_dir, 'TokenUniqueSymbolIndex.json'), 'r')
    abi = json.load(f)
    f.close()

    f = open(os.path.join(args.abi_dir, 'ERC20.json'), 'r')
    erc20_abi = json.load(f)
    f.close()


    index_contract = w3.eth.contract(address=args.a, abi=abi)

    token_addresses = []
    i = 0
    while True:
        try:
            token_addresses.append(index_contract.functions.entry(i).call())
        except ValueError:
            break
        i += 1


    for token_address in token_addresses:
        symbol = ''
        erc20_contract = w3.eth.contract(address=token_address, abi=erc20_abi)
        try:
            symbol = erc20_contract.functions.symbol().call()
        except ValueError:
            logg.error('token {} does not have symbol method'.format(token_address))
            continue
        print('{} {}'.format(symbol, token_address))


if __name__ == '__main__':
    main()
