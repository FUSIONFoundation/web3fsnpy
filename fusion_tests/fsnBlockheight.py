#!/usr/bin/env python3

#web3fusion
from  web3fsnpy import Fsn

linkToChain = {
    'network'     : 'testnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',
}

web3fsn = Fsn(linkToChain)


print('Current block height is ',web3fsn.blockNumber)


