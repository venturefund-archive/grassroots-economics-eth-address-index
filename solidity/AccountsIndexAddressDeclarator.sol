pragma solidity >0.6.11;

// SPDX-License-Identifier: GPL-3.0-or-later


contract AdccountsIndexAddressDeclarator {

	address public tokenAddress;
	bytes32 tokenAddressHash;
	address public addressDeclaratorAddress;
	mapping(address => uint256) entryIndex;
	uint256 count;

	address public owner;
	address newOwner;

	event AddressAdded(address indexed addedAccount, uint256 indexed accountIndex); // AccountsIndex
	event OwnershipTransferred(address indexed previousOwner, address indexed newOwner); // EIP173

	constructor(address _tokenAddress, address _addressDeclaratorAddress) public {
		bytes memory _tokenAddressPadded;
		owner = msg.sender;
		addressDeclaratorAddress = _addressDeclaratorAddress;
		tokenAddress = _tokenAddress;
		_tokenAddressPadded = abi.encode(tokenAddress);
		tokenAddressHash = sha256(_tokenAddressPadded);
		count = 1;
	}

	function add(address _account) external returns (bool) {
		bool ok;
		bytes memory r;
		uint256 oldEntryIndex;

		(ok, r) = addressDeclaratorAddress.call(abi.encodeWithSignature("addDeclaration(address,bytes32)", _account, tokenAddressHash));
		require(ok);
		require(r[31] == 0x01);

		oldEntryIndex = count;
		entryIndex[_account] = oldEntryIndex;
		count++;

		emit AddressAdded(_account, oldEntryIndex);
		return true;
	}

	function have(address _account) external view returns (bool) {
		return entryIndex[_account] > 0;
	}
}
