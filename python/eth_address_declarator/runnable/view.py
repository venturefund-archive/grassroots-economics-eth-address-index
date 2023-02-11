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
from chainlib.eth.cli.arg import (
        Arg,
        ArgFlag,
        process_args,
        )
from chainlib.eth.cli.config import (
        Config,
        process_config,
        )
from chainlib.eth.cli.log import process_log
from chainlib.eth.settings import process_settings
from chainlib.settings import ChainSettings


# local imports
from eth_address_declarator import Declarator
from eth_address_declarator.declarator import AddressDeclarator

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


def process_config_local(config, arg, args, flags):
    a = strip_0x(config.get('_POSARG'))
    ac = to_checksum_address(a)
    if config.true('_UNSAFE'):
        a = ac
    else:
        if a != ac:
            raise ValueError('declarator is not a valid checksum address')
    config.add(a, '_DECLARATOR')
    return config


arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_WRITE | arg_flags.WALLET | arg_flags.EXEC

argparser = chainlib.eth.cli.ArgumentParser()
argparser = process_args(argparser, arg, flags)
argparser.add_argument('declarator', type=str, help='Ethereum declaration address to look up')
args = argparser.parse_args()

logg = process_log(args, logg)

config = Config()
config = process_config(config, arg, args, flags, positional_name='declarator')
config = process_config_local(config, arg, args, flags)
logg.debug('config loaded:\n{}'.format(config))

settings = ChainSettings()
settings = process_settings(settings, config)
logg.debug('settings loaded:\n{}'.format(settings))


def out_element(e, w=sys.stdout):
    w.write(e[1] + '\n')


def ls(ifc, conn, contract_address, declarator_address, subject_address, w=sys.stdout):
    o = ifc.declaration(contract_address, declarator_address, subject_address)
    r =  conn.do(o)
    declarations = ifc.parse_declaration(r)

    for i, d in enumerate(declarations):
        out_element((i, d), w)


def main():

    c = Declarator(
            settings.get('CHAIN_SPEC')
            )

    ls(
            c,
            settings.get('CONN'),
            settings.get('EXEC'),
            config.get('_DECLARATOR'),
            settings.get('RECIPIENT'),
            )

    declarations = []


if __name__ == '__main__':
    main()
