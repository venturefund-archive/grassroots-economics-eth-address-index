SOLC = /usr/bin/solc

all:
	$(SOLC) AddressDeclarator.sol --abi --evm-version byzantium | awk 'NR>3' > AddressDeclarator.json
	$(SOLC) AddressDeclarator.sol --bin --evm-version byzantium | awk 'NR>3' > AddressDeclarator.bin
	truncate -s -1 AddressDeclarator.bin
	$(SOLC) TokenUniqueSymbolIndex.sol --abi --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndex.json
	$(SOLC) TokenUniqueSymbolIndex.sol --bin --evm-version byzantium | awk 'NR>3' > TokenUniqueSymbolIndex.bin
	truncate -s -1 TokenUniqueSymbolIndex.bin

test: all
	#python test.py
	python test_tokenindex.py

install: all
	cp -v AddressDeclarator.{json,bin} ../python/eth_address_declarator/data/
	cp -v TokenUniqueSymbolIndex.{json,bin} ../python/eth_token_index/data/
	
.PHONY: test install
