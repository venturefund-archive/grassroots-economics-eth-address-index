SOLC = /usr/bin/solc

all: address_declarator token_index accounts_index

address_declarator:
	$(SOLC) AddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > AddressDeclarator.json
	$(SOLC) AddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > AddressDeclarator.bin
	truncate -s -1 AddressDeclarator.bin

token_index:
	$(SOLC) TokenUniqueSymbolIndex.sol --abi --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndex.json
	$(SOLC) TokenUniqueSymbolIndex.sol --bin --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndex.bin
	truncate -s -1 TokenUniqueSymbolIndex.bin


accounts_index:
	$(SOLC) AccountsIndexAddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > AccountsIndexAddressDeclarator.json
	$(SOLC) AccountsIndexAddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > AccountsIndexAddressDeclarator.bin
	truncate -s -1 AccountsIndexAddressDeclarator.bin

#test: all
	#python test.py
	#python test_tokenindex.py

install: all
	cp -v AddressDeclarator.{json,bin} ../python/eth_address_declarator/data/
	cp -v TokenUniqueSymbolIndex.{json,bin} ../python/eth_token_index/data/
	cp -v AccountsIndexAddressDeclarator.{json,bin} ../python/eth_address_declarator/data/
	
.PHONY: test install
