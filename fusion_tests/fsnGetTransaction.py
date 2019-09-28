#!/usr/bin/env python3

#web3fusion
from  web3fsnpy import Fsn

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://mainnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
}

web3fsn = Fsn(linkToChain)


TxID = 0x25557995e5ed36cc41c156e7f8fa7be10c6d45e25e37cd2e1f8d2d443480b2f2

Tx = web3fsn.getTransaction(TxID)

print(Tx)   # Print the whole dictionary

#print('from        : ',Tx.from)
#print('to          : ',Tx.to)
#print('blocknumber : ',Tx.blockNumber)

TxCount = web3fsn.getBlockTransactionCount(Tx.blockNumber)

print('There were ',TxCount,' transactions in block number ',Tx.blockNumber)






