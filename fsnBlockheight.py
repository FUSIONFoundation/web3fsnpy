#!/usr/bin/env python3

from web3fsnpy import Web3Fsn


web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider("wss://mainnetpublicgateway1.fusionnetwork.io:10001"))

print('Current block height is ',web3fsn.fsn.blockNumber)


