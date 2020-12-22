pragma solidity >=0.6.12;

// SPDX-License-Identifier: GPL-3.0-or-later

contract TokenEndorsement {

	uint256 count;
	mapping ( bytes32 => bytes32 ) public endorsement;
	mapping ( address => uint256 ) public tokenIndex;
	mapping ( address => uint256[] ) public endorser;
	mapping ( address => uint256 ) public endorserTokenCount;
	mapping ( string => address ) public tokenSymbolIndex;
	address[] public tokens;

	event EndorsementAdded(address indexed _token, address indexed _adder, uint256 indexed _index, bytes32 _data);

	constructor() {
		count = 1;
		tokens.push(address(0x0));
	}

	function register(address _token) private returns (bool) {
		if (tokenIndex[_token] > 0) {
			return false;
		}
		(bool _ok, bytes memory _r) = _token.call(abi.encodeWithSignature('symbol()'));
		require(_ok);

		string memory token_symbol = abi.decode(_r, (string));
		require(tokenSymbolIndex[token_symbol] == address(0));

		tokens.push(_token);
		tokenIndex[_token] = count;
		tokenSymbolIndex[token_symbol] = _token;
		count++;
		return true;
	}

	function add(address _token, bytes32 _data) public returns (bool) {
		register(_token);
		bytes32 k;
		bytes memory signMaterial = new bytes(40);
		bytes memory addrBytes = abi.encodePacked(_token);
		for (uint256 i = 0; i < 20; i++) {
			signMaterial[i] = addrBytes[i];
		}
		addrBytes = abi.encodePacked(msg.sender);
		for (uint256 i = 0; i < 20; i++) {
			signMaterial[i+20] = addrBytes[i];
		}
		k = sha256(signMaterial);
		require(endorsement[k] == bytes32(0x00));
		endorsement[k] = _data;
		endorser[msg.sender].push(tokenIndex[_token]);
		endorserTokenCount[msg.sender]++;
		emit EndorsementAdded(_token, msg.sender, count, _data);
		return true;
	}
}
