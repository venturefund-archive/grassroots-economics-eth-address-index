all:
	solc AddressDeclarator.sol --abi | awk 'NR>3' > AddressDeclarator.json
	solc AddressDeclarator.sol --bin | awk 'NR>3' > AddressDeclarator.bin
	truncate -s -1 AddressDeclarator.bin
	solc TokenUniqueSymbolIndex.sol --abi | awk 'NR>3' > TokenUniqueSymbolIndex.json
	solc TokenUniqueSymbolIndex.sol --bin | awk 'NR>3' > TokenUniqueSymbolIndex.bin
	truncate -s -1 TokenUniqueSymbolIndex.bin


old:
	solc TokenEndorser.sol --abi | awk 'NR>3' > TokenEndorser.json
	solc TokenEndorser.sol --bin | awk 'NR>3' > TokenEndorser.bin
	truncate -s -1 TokenEndorser.bin

test: all
	#python test.py
	python test_tokenindex.py
	
.PHONY: test
