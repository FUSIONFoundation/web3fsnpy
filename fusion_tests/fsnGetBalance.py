#!/usr/bin/env python3

#web3fusion
from  web3fsnpy import Fsn

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
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
pub_key = '0x7fbFa5679411a97bb2f73Dd5ad01Ca0822FaD9a6'
#
bal = web3fsn.getBalance(pub_key, asset_Id, blockNo)
#
#print(ret_dict)
#
print('Balance for ', pub_key, ' is  ', web3fsn.fromWei(int(bal),'ether'), ' FSN')



