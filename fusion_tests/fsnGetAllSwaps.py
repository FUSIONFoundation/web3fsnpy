#!/usr/bin/env python3
#
"""
 Demonstrate getting swaps from the Quantum Swap market
"""
#
#
import os
import sys
import json
#import pdb ; pdb.set_trace()


#web3fusion
from  web3fsnpy import Fsn


linkToChain = {
    'network'     : 'testnet',                          # One of 'testnet', or 'mainnet'
    'provider'    : 'HTTP',                             # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
#    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read, or signed raw transactions
}

#

web3fsn = Fsn(linkToChain)

pageNo = 0   # Only get the most recent 100 records on the first page

swap_dict = web3fsn.getAllSwaps(pageNo)


print('No. swaps = ',len(swap_dict),'\n')


for ii in range(len(swap_dict)):
    for key, value in swap_dict[ii].items():
        if key == 'timeStamp' or key == 'FromStartTime' or key == 'ToEndTime' or key == 'Time' :
            value = web3fsn.numToDatetime(value)
        elif key == 'fromAsset' or key == 'toAsset':
            if value == web3fsn.tokens['FSN']:
                value = 'FSN'
        print(key, value)




