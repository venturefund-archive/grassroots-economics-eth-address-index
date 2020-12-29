pragma solidity >=0.6.12;

// SPDX-License-Identifier: GPL-3.0-or-later

contract AddressDeclarator {

	mapping( bytes32 => uint256[] ) 
	//mapping( address => uint256[] ) declaratorItemsIndex;
	//mapping( address => uint256 ) public declaratorCount;
	//mapping( address => mapping ( address => declaratorItem ) ) declarationByDeclaratorIndex;
	bytes32[][] contents;

//	constructor(bytes32[] memory _descriptions) {
//		for (uint i; i < _descriptions.length; i++) {
//			addDeclaration(msg.sender, _descriptions[i]);
//		}
//	}
//
//	function addDeclaration(address _subject, bytes32 _proof) public returns ( bool ) {
//		declaratorItem storage item;
//
//		item = declarationByDeclaratorIndex[msg.sender][_subject];
//		if (item.signer == address(0)) {
//			item.signer = msg.sender;
//			declaratorItemsIndex[_subject].push(declaratorItems.length);
//			declaratorItems.push(item);
//			declaratorCount[_subject]++;
//		}
//		item.content.push(_proof);
//
//		return true;
//	}
//
//	function declarator(address _target, uint256 _idx) public view returns ( address ) {
//		uint256 idx;
//		declaratorItem storage item;
//		
//		idx = declaratorItemsIndex[_target][_idx];
//		item = declaratorItems[idx];
//
//		return item.signer;
//	}
//
//	function declaration(address _declarator, address _target) public view returns ( bytes32[] memory ) {
//		declaratorItem storage item;
//		
//		item = declarationByDeclaratorIndex[_declarator][_target];
//
//		return item.content;
//	}
}
