#!/usr/bin/env python3

#web3fusion
from  web3.fusion import Fsn

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://mainnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
}

web3fsn = Fsn(linkToChain)


#
asset_name = 'FSN'
blockNo = 'latest'
#
#
asset_Id = web3fsn.getAssetId(asset_name)
#
pub_key = '0x432baf0AB7261819fCf587De7e6D68f902E43195'
#
bal = web3fsn.getBalance(pub_key, asset_Id, blockNo)
#
#print(ret_dict)
#
print('Balance for ', pub_key, ' is  ', web3fsn.fromWei(int(bal),'ether'), ' FSN')



