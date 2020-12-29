pragma solidity >=0.6.12;

// SPDX-License-Identifier: GPL-3.0-or-later

contract TokenUniqueSymbolIndex {

	// EIP 173
	address public owner;

	mapping ( bytes32 => uint256 ) public registry;
	address[] tokens;

	constructor() {
		owner = msg.sender;
		tokens.push(address(0));
	}

	// EIP 165
	function supportsInterface(bytes4 _interfaceCode) public pure returns ( bool ) {
		if (_interfaceCode == bytes4(0x325d15e2)) {
			return true;
		}
		if (_interfaceCode == bytes4(0x01ffc9a7)) {
			return true;
		}
		return false;
	}

	// EIP 172
	function transferOwnership() public {
		revert("owner cannot be changed");
	}

	function addressOf(bytes32 _key) public view returns ( address ) {
		uint256 idx;

		idx = registry[_key];
		return tokens[idx];
	}

	function register(bytes32 _key, address _token) public returns (bool) {
		require(msg.sender == owner);

		bytes memory token_symbol;
		bytes32 token_symbol_key;
		uint256 idx;

		(bool _ok, bytes memory _r) = _token.call(abi.encodeWithSignature('symbol()'));
		require(_ok);

		token_symbol = abi.decode(_r, (bytes));
		token_symbol_key = sha256(token_symbol);

		require(_key == token_symbol_key);
		idx = registry[token_symbol_key];
		require(idx == 0);

		registry[token_symbol_key] = tokens.length;
		tokens.push(_token);
		return true;
	}

	function registryCount() public view returns ( uint256 ) {
		return tokens.length - 1;
	}
}
