#!/usr/bin/env python3
#
# Demonstrate getting timelock information about an asset for a public key
#
#
from  web3fsnpy import Fsn
import os
import sys
from eth_utils import (
    to_hex,
)
from datetime import datetime, timedelta
#import pdb ; pdb.set_trace()

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',
}

web3fsn = Fsn(linkToChain)


#
pub_key = '0x3333333333333333333333333333333333333333'
asset_name = 'FSN'
blockNo = 'latest'
#
#
asset_Id = web3fsn.getAssetId(asset_name)
#
asset_timelocks = web3fsn.getTimeLockBalance(asset_Id, pub_key, blockNo)
#
print(asset_timelocks,'\n')
#
#
n_items = len(asset_timelocks.Items)
print('\nNumber of timelocked ', asset_name, ' items = ',n_items,'\n')
#

#
for i in range(n_items):
    print('Asset ',i,'\n')
    tm = asset_timelocks.Items[i].StartTime
    print('Start Time :   ',datetime.fromtimestamp(tm).strftime('%c'))
    tm = asset_timelocks.Items[i].EndTime
    if tm >= web3fsn.BN():
        endtime = 'Infinity'
    else:
        endtime = datetime.fromtimestamp(tm).strftime('%c')
    print('End Time   :   ',endtime)
    val = int(asset_timelocks.Items[i].Value)
    print(web3fsn.fromWei(val,'ether'),' ',asset_name,'\n')


