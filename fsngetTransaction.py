#!/usr/bin/env python3

from web3fsnpy import Web3Fsn

testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"

web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider(mainnet))


TxID = 0x25557995e5ed36cc41c156e7f8fa7be10c6d45e25e37cd2e1f8d2d443480b2f2

Tx = web3fsn.fsn.getTransaction(TxID)

#print(Tx)   # Print the whole dictionary

#print('from        : ',Tx.from)
print('to          : ',Tx.to)
print('blocknumber : ',Tx.blockNumber)




