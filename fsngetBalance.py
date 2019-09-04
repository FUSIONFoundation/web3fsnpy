#!/usr/bin/env python3

from web3fsnpy import Web3Fsn

testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"

web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider("wss://mainnetpublicgateway1.fusionnetwork.io:10001"))

pub_key = "0x432baf0AB7261819fCf587De7e6D68f902E43195"

print('Balance for ', pub_key, ' is  ', web3fsn.fromWei(web3fsn.fsn.getBalance(pub_key),'ether'), ' FSN')



