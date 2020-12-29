all:
	solc AddressDeclarator.sol --abi | awk 'NR>3' > AddressDeclarator.json
	solc AddressDeclarator.sol --bin | awk 'NR>3' > AddressDeclarator.bin
	truncate -s -1 AddressDeclarator.bin

old:
	solc TokenEndorser.sol --abi | awk 'NR>3' > TokenEndorser.json
	solc TokenEndorser.sol --bin | awk 'NR>3' > TokenEndorser.bin
	truncate -s -1 TokenEndorser.bin

test: all
	python test.py
	
.PHONY: test
