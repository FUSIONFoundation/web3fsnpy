#!/usr/bin/env python3

#web3fusion
from  web3fsnpy import Fsn

linkToChain = {
    'network'     : 'testnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'HTTP',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',
}

web3fsn = Fsn(linkToChain)


#
asset_name = 'FSN'
blockNo = 'latest'
#
#
asset_Id = web3fsn.getAssetId(asset_name)   # Or you can put the asset ID as a hex number here if it is not a 'standard' asset.
#
pub_key = '0x3333333333333333333333333333333333333333'
#
bal = web3fsn.getBalance(pub_key, asset_Id, blockNo)
#
#
print('Balance for ', pub_key, ' is  ', web3fsn.fromWei(int(bal),'ether'), ' FSN')
#
#
bal_info = web3fsn.getAllBalances(pub_key)
#
#
print('Balances for ALL assets are \n')
#
for key, val in bal_info.items():
    print(key, val)
    





