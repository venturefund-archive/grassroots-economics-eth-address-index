"""Deploys address declaration contract

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import json
import argparse
import logging

# third-party imports
from crypto_dev_signer.eth.signer import ReferenceSigner as EIP155Signer
from crypto_dev_signer.keystore.dict import DictKeystore
from crypto_dev_signer.eth.helper import EthTxExecutor
from chainlib.chain import ChainSpec
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.gas import RPCGasOracle
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt

# local imports
from eth_address_declarator import AddressDeclarator

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-w', action='store_true', help='Wait for the last transaction to be confirmed')
argparser.add_argument('-ww', action='store_true', help='Wait for every transaction to be confirmed')
argparser.add_argument('-i', '--chain-spec', dest='i', type=str, default='evm:ethereum:1', help='Chain specification string')
argparser.add_argument('-y', '--key-file', dest='y', type=str, help='Ethereum keystore file to use for signing')
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('-vv', action='store_true', help='Be more verbose')
argparser.add_argument('--env-prefix', default=os.environ.get('CONFINI_ENV_PREFIX'), dest='env_prefix', type=str, help='environment prefix for variables to overwrite configuration')
argparser.add_argument('owner_description_digest', type=str, help='SHA256 of description metadata of contract deployer')
args = argparser.parse_args()

if args.vv:
    logg.setLevel(logging.DEBUG)
elif args.v:
    logg.setLevel(logging.INFO)

block_last = args.w
block_all = args.ww

passphrase_env = 'ETH_PASSPHRASE'
if args.env_prefix != None:
    passphrase_env = args.env_prefix + '_' + passphrase_env
passphrase = os.environ.get(passphrase_env)
if passphrase == None:
    logg.warning('no passphrase given')
    passphrase=''

signer_address = None
keystore = DictKeystore()
if args.y != None:
    logg.debug('loading keystore file {}'.format(args.y))
    signer_address = keystore.import_keystore_file(args.y, password=passphrase)
    logg.debug('now have key for signer address {}'.format(signer_address))
signer = EIP155Signer(keystore)

chain_spec = ChainSpec.from_chain_str(args.i)

rpc = EthHTTPConnection(args.p)
nonce_oracle = RPCNonceOracle(signer_address, rpc)
gas_oracle = RPCGasOracle(rpc, code_callback=AddressDeclarator.gas)

initial_description = args.owner_description_digest

def main():
    c = AddressDeclarator(chain_spec, signer=signer, gas_oracle=gas_oracle, nonce_oracle=nonce_oracle)
    (tx_hash_hex, o) = c.constructor(signer_address, initial_description)
    rpc.do(o)
    if block_last:
        r = rpc.wait(tx_hash_hex)
        if r['status'] == 0:
            sys.stderr.write('EVM revert while deploying contract. Wish I had more to tell you')
            sys.exit(1)
        # TODO: pass through translator for keys (evm tester uses underscore instead of camelcase)
        address = r['contractAddress']

        print(address)
    else:
        print(tx_hash_hex)

    sys.exit(0)


if __name__ == '__main__':
    main()
