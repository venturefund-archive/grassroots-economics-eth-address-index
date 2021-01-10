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

# third-party imports
import web3
from crypto_dev_signer.keystore import DictKeystore

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

logging.getLogger('web3').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--provider', dest='p', default='http://localhost:8545', type=str, help='Web3 provider url (http only)')
argparser.add_argument('-r', '--contract-address', dest='r', type=str, help='Address declaration contract address')
argparser.add_argument('-i', '--chain-spec', dest='i', type=str, default='Ethereum:1', help='Chain specification string')
argparser.add_argument('-a', '-declarator-address', dest='a', type=str, help='Signing address for the declaration')
argparser.add_argument('-y', '--key-file', dest='y', type=str, help='Ethereum keystore file to use for signing')
argparser.add_argument('--resolve', action='store_true', help='Attempt to resolve the hashes to actual content')
argparser.add_argument('--resolve-http', dest='resolve_http', type=str, help='Base url to look up content hashes')
argparser.add_argument('--abi-dir', dest='abi_dir', type=str, default=data_dir, help='Directory containing bytecode and abi (default: {})'.format(data_dir))
argparser.add_argument('-v', action='store_true', help='Be verbose')
argparser.add_argument('-vv', action='store_true', help='Be more verbose')
argparser.add_argument('address', type=str, help='Ethereum declaration address to look up')
args = argparser.parse_args()

if args.vv:
    logg.setLevel(logging.DEBUG)
elif args.v:
    logg.setLevel(logging.INFO)

w3 = web3.Web3(web3.Web3.HTTPProvider(args.p))

def try_sha256(s):
    r = urllib.request.urlopen(os.path.join(args.resolve_http, s.hex()))
    return r.read().decode('utf-8')

def try_utf8(s):
    return s.decode('utf-8')

signer_address = None
keystore = DictKeystore()
if args.y != None:
    logg.debug('loading keystore file {}'.format(args.y))
    signer_address = keystore.import_keystore_file(args.y)
    logg.debug('now have key for signer address {}'.format(signer_address))


def main():

    f = open(os.path.join(args.abi_dir, 'AddressDeclarator.json'), 'r')
    abi = json.load(f)
    f.close()

    declarator_address = signer_address
    if declarator_address == None:
        declarator_address = args.a
    if declarator_address == None:
        sys.stderr.write('missing declarator address, specify -y or -a\n')
        sys.exit(1)

    logg.debug('declarator address {}'.format(declarator_address))

    c = w3.eth.contract(abi=abi, address=args.r)

    declarations = c.functions.declaration(declarator_address, args.address).call()

    for d in declarations:
        if not args.resolve:
            print(d.hex())
            continue
        if args.resolve_http:
            try:
                r = try_sha256(d)
                print(r)
                continue
            except urllib.error.HTTPError:
                pass
        try:
            print(try_utf8(d))
        except UnicodeDecodeError:
            pass


if __name__ == '__main__':
    main()
