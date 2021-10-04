"""Deploys the token symbol index

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
from chainlib.eth.tx import receipt

# local imports
from eth_address_declarator.token_index.index import TokenUniqueSymbolIndexAddressDeclarator

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

arg_flags = chainlib.eth.cli.argflag_std_write
argparser = chainlib.eth.cli.ArgumentParser(arg_flags)
argparser.add_argument('--address-declarator', type=str, required=True, dest='address_declarator', help='address declarator backend address')
args = argparser.parse_args()

extra_args = {
    'address_declarator': None,
    }

config = chainlib.eth.cli.Config.from_args(args, arg_flags, extra_args=extra_args, default_fee_limit=TokenUniqueSymbolIndexAddressDeclarator.gas())

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

    c = TokenUniqueSymbolIndexAddressDeclarator(chain_spec, signer=signer, gas_oracle=gas_oracle, nonce_oracle=nonce_oracle)

    (tx_hash_hex, o) = c.constructor(signer_address, config.get('_ADDRESS_DECLARATOR'))
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
