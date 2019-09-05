#!/usr/bin/env python3

from web3fsnpy import Web3Fsn

testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"


web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider(mainnet))

print('Current block height is ',web3fsn.fsn.blockNumber)


