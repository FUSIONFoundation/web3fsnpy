#!/usr/bin/env python3
#
# Demonstrate getting asset information
#
#
#web3fusion
from  web3fsnpy import Fsn

linkToChain = {
    'network'     : 'testnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',
}

web3fsn = Fsn(linkToChain)
#
#
asset_name = 'FSN'
#
#
assetInfo = web3fsn.assetNameToAssetInfo(asset_name)
#
print(assetInfo)
#

