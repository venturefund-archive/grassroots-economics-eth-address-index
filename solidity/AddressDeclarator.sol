pragma solidity >0.6.11;

// SPDX-License-Identifier: GPL-3.0-or-later

contract AddressDeclarator {

	mapping( address => address[] ) declarationIndex;
	mapping( bytes32 => uint256 ) declarationContentIndex; // the _latest_ content pointer for the declarator to subject mapping
	mapping( address => address[] ) declarator;
	mapping( address => address[] ) declaratorReverse;
	mapping( bytes32 => bool ) declarationExistIndex;
	bytes32[][] public contents;

	event DeclarationAdded(address _declarator, address _subject, bytes32 _proof);

	constructor(bytes32 _initialDescription) public {
		bytes32[] memory foundation;

		contents.push(foundation);
		contents[contents.length-1].push(blockhash(block.number));

		addDeclaration(msg.sender, _initialDescription);
	}
	
	function toReference(address _declarator, address _subject) private pure returns ( bytes32 ) {
		bytes32 k;
		bytes memory signMaterial = new bytes(40);
		bytes memory addrBytes = abi.encodePacked(_declarator);
		for (uint256 i = 0; i < 20; i++) {
			signMaterial[i] = addrBytes[i];
		}
		addrBytes = abi.encodePacked(_subject);
		for (uint256 i = 0; i < 20; i++) {
			signMaterial[i+20] = addrBytes[i];
		}
		k = sha256(signMaterial);
		return k;
	}

	function toReference(address _declarator, address _subject, bytes32 _proof) private pure returns ( bytes32[2] memory ) {
		bytes32 k;
		bytes32[2] memory ks;
		bytes memory signMaterial = new bytes(64);

		k = toReference(_declarator, _subject);
		for (uint256 i = 0; i < 32; i++) {
			signMaterial[i] = k[i];
		}
		for (uint256 i = 0; i < 32; i++) {
			signMaterial[i+32] = _proof[i];
		}

		ks[0] = k;
		ks[1] = sha256(signMaterial);

		return ks;
	}

	// Implements Declarator
	function declaratorCount(address _subject) public view returns ( uint256 ) {
		return declarator[_subject].length;
	}

	// Implements Declarator
	function declaratorAddressAt(address _subject, uint256 _idx) public view returns ( address ) {
		return declarator[_subject][_idx];
	}

	// Implements Declarator
	function addDeclaration(address _subject, bytes32 _proof) public returns ( bool ) {
		bytes32[2] memory ks;
		bytes32[] memory declarationContents;
		uint256 idx;
		ks = toReference(tx.origin, _subject, _proof);
		idx = declarationContentIndex[ks[0]];
		if (idx == 0) { // This also works for the constructor :)
			declarator[_subject].push(tx.origin);
			contents.push(declarationContents);
			declarationIndex[tx.origin].push(_subject);
		}

		idx = contents.length-1;
		declarationContentIndex[ks[0]] = idx;
		contents[idx].push(_proof);

		declarationExistIndex[ks[1]] = true;

		return true;
	}

	// Implements Declarator
	function declaration(address _declarator, address _subject) public view returns ( bytes32[] memory ) {
		bytes32 k;
		uint256 idx;
		k = toReference(_declarator, _subject);
		idx = declarationContentIndex[k];
		return contents[idx];
	}

	// Implements Declarator
	function haveDeclaration(address _declarator, address _subject, bytes32 _proof) public view returns (bool) {
		bytes32[2] memory ks;
		
		ks = toReference(_declarator, _subject, _proof);

		return declarationExistIndex[ks[1]];
	}

	// Implements Declarator
	function declarationCount(address _declarator) public view returns ( uint256 ) {
		return declarationIndex[_declarator].length;
	}

	// Implements Declarator
	function declarationAddressAt(address _declarator, uint256 _idx) public view returns ( address ) {
		return declarationIndex[_declarator][_idx];
	}

	// Implements EIP165
	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x27beb910) { // Implements Declarator
			return true;
		}
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		return false;
	}
}
