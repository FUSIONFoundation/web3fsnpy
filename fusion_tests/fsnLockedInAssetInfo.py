#!/usr/bin/env python3
#
"""
 Demonstrate the asset information api and how to get information about assets that can be locked in to the Fusion
 blockchain
 
"""
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

token = web3fsn.assetNameToAssetInfo('BTC')

#print('BTC = {}'.format(token))
if token != None:
    for key, Id in token.items():
        print(key, ' :    ', Id)

print('\n\n')
    
# Now find Info about an assetId 
assetId = '0x8094eac0cf78d898c8ad3a17ed0af3809560464ebb3e48088edce97a158ea433'

token = web3fsn.assetIdToAssetInfo(assetId)
if token != None:
    for key, Id in token.items():     # Should return the BAT token
        print(key, ' :    ', Id)

