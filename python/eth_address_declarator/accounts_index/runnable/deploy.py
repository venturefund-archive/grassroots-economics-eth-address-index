"""Deploys accounts index, registering arbitrary number of writers

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import json
import argparse
import logging

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt

# local imports
from eth_address_declarator.accounts_index import AccountsIndexAddressDeclarator

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

arg_flags = chainlib.eth.cli.argflag_std_write
argparser = chainlib.eth.cli.ArgumentParser(arg_flags)
argparser.add_argument('--address-declarator', type=str, required=True, dest='address_declarator', help='address declarator backend address')
argparser.add_argument('--token-address', type=str, required=True, dest='token_address', help='token address context for accounts registry')
args = argparser.parse_args()

extra_args = {
    'address_declarator': None,
    'token_address': None,
    }
config = chainlib.eth.cli.Config.from_args(args, arg_flags, extra_args=extra_args, default_fee_limit=AccountsIndexAddressDeclarator.gas())

wallet = chainlib.eth.cli.Wallet()
wallet.from_config(config)

rpc = chainlib.eth.cli.Rpc(wallet=wallet)
conn = rpc.connect_by_config(config)

chain_spec = ChainSpec.from_chain_str(config.get('CHAIN_SPEC'))


def main():
    signer = rpc.get_signer()
    signer_address = rpc.get_sender_address()

    gas_oracle = rpc.get_gas_oracle()
    nonce_oracle = rpc.get_nonce_oracle()

    address_declarator = config.get('_ADDRESS_DECLARATOR')
    if not config.true('_UNSAFE') and not is_checksum_address(address_declarator):
        raise ValueError('address declarator {} is not a valid checksum address'.format(address_declarator))

    token_address = config.get('_TOKEN_ADDRESS')
    if not config.true('_UNSAFE') and not is_checksum_address(token_address):
        raise ValueError('token {} is not a valid checksum address'.format(token_address))

    c = AccountsIndexAddressDeclarator(chain_spec, signer=signer, gas_oracle=gas_oracle, nonce_oracle=nonce_oracle)

    (tx_hash_hex, o) = c.constructor(signer_address, token_address, address_declarator)

    if config.get('_RPC_SEND'):
        conn.do(o)
        if config.get('_WAIT'):
            r = conn.wait(tx_hash_hex)
            if r['status'] == 0:
                sys.stderr.write('EVM revert while deploying contract. Wish I had more to tell you')
                sys.exit(1)
            # TODO: pass through translator for keys (evm tester uses underscore instead of camelcase)
            address = r['contractAddress']

            print(address)
        else:
            print(tx_hash_hex)
    else:
        print(o)


if __name__ == '__main__':
    main()
