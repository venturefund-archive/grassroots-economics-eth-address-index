"""Adds a new Address declaration

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import os
import json
import argparse
import logging

# third-party imports
import web3


logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-r', '--contract-address', dest='r', type=str, help='Token endorsement contract address')
argparser.add_argument('-o', '--endorser-address', dest='o', type=str, help='Address to use to sign endorsement transaction')
argparser.add_argument('--abi-dir', dest='abi_dir', type=str, default=data_dir, help='Directory containing bytecode and abi (default: {})'.format(data_dir))
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('address', type=str, help='Ethereum address to add declaration to')
argparser.add_argument('declaration', type=str, help='SHA256 sum of endorsement data to add')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)

def main():
    w3 = web3.Web3(web3.Web3.HTTPProvider(args.p))

    f = open(os.path.join(args.abi_dir, 'AddressDeclarator.json'), 'r')
    abi = json.load(f)
    f.close()

    w3.eth.defaultAccount = w3.eth.accounts[0]
    if args.o != None:
        w3.eth.defaultAccount = args.o
    logg.debug('endorser address {}'.format(w3.eth.defaultAccount))

    c = w3.eth.contract(abi=abi, address=args.r)

    tx_hash = c.functions.addDeclaration(args.address, args.declaration).transact()
    print(tx_hash.hex())


if __name__ == '__main__':
    main()
