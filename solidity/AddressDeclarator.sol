pragma solidity >=0.6.12;

// SPDX-License-Identifier: GPL-3.0-or-later

contract AddressDeclarator {

	// EIP 173
	address public owner;

	mapping( address => address[] ) declarationIndex;
	mapping( bytes32 => uint256 ) declarationContentIndex;
	mapping( address => address[] ) declarator;
	mapping( address => address[] ) declaratorReverse;
	bytes32[][] public contents;

	constructor(bytes32 _initialDescription) {
		bytes32[] memory foundation;

		owner = msg.sender;
		contents.push(foundation);
		contents[contents.length-1].push(blockhash(block.number));

		addDeclaration(msg.sender, _initialDescription);
	}

	// EIP 172
	function transferOwnership() public {
		revert("owner cannot be changed");
	}

	// EIP-165
	function supportsInterface(bytes4 interfaceID) public view returns ( bool ) {
		return false;
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

	function declaratorCount(address _subject) public view returns ( uint256 ) {
		return declarator[_subject].length;
	}

	function declaratorAddressAt(address _subject, uint256 _idx) public view returns ( address ) {
		return declarator[_subject][_idx];
	}

	function addDeclaration(address _subject, bytes32 _proof) public returns ( bool ) {
		bytes32 k;
		bytes32[] memory declarationContents;
		uint256 idx;
		k = toReference(msg.sender, _subject);
		idx = declarationContentIndex[k];
		if (idx == 0) { // This also works for the constructor :)
			declarator[_subject].push(msg.sender);
			contents.push(declarationContents); //= contents[idx],
			declarationIndex[msg.sender].push(_subject);
		}
		idx = contents.length-1;
		declarationContentIndex[k] = idx;
		contents[idx].push(_proof);

		return true;
	}

	function declaration(address _declarator, address _subject) public view returns ( bytes32[] memory ) {
		bytes32 k;
		uint256 idx;
		k = toReference(_declarator, _subject);
		idx = declarationContentIndex[k];
		return contents[idx];
	}

	function declarationCount(address _declarator) public view returns ( uint256 ) {
		return declarationIndex[_declarator].length;
	}

	function declarationAddressAt(address _declarator, uint256 _idx) public view returns ( address ) {
		return declarationIndex[_declarator][_idx];
	}
}
