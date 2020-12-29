all:
	solc AddressDeclarator.sol --abi | awk 'NR>3' > AddressDeclarator.json
	solc AddressDeclarator.sol --bin | awk 'NR>3' > AddressDeclarator.bin
	truncate -s -1 AddressDeclarator.bin

test: all
	python test.py
	
.PHONY: test
