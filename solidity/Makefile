SOLC = /usr/bin/solc

all: address_declarator token_index accounts_index

address_declarator:
	$(SOLC) AddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > AddressDeclarator.json
	$(SOLC) AddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > AddressDeclarator.bin
	truncate -s -1 AddressDeclarator.bin

token_index:
	$(SOLC) TokenUniqueSymbolIndexAddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndexAddressDeclarator.json
	$(SOLC) TokenUniqueSymbolIndexAddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndexAddressDeclarator.bin
	truncate -s -1 TokenUniqueSymbolIndexAddressDeclarator.bin


accounts_index:
	$(SOLC) AccountsIndexAddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > AccountsIndexAddressDeclarator.json
	$(SOLC) AccountsIndexAddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > AccountsIndexAddressDeclarator.bin
	truncate -s -1 AccountsIndexAddressDeclarator.bin

#test: all
	#python test.py
	#python test_tokenindex.py

install: all
	cp -v AddressDeclarator.{json,bin} ../python/eth_address_declarator/data/
	cp -v TokenUniqueSymbolIndexAddressDeclarator.{json,bin} ../python/eth_address_declarator/data/
	cp -v AccountsIndexAddressDeclarator.{json,bin} ../python/eth_address_declarator/data/
	
.PHONY: test install
