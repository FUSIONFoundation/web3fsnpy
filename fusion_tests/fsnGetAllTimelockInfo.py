#!/usr/bin/env python3
#
# Demonstrate getting asset information
#
#web3fusion
from  web3.fusion import Fsn

import os
import sys
from eth_utils import (
    to_hex,
)
from datetime import datetime, timedelta

linkToChain = {
    'network'     : 'testnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://mainnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'http://testnetpublicgateway1.fusionnetwork.io:10000',
}

web3fsn = Fsn(linkToChain)

#
pub_key = '0x432baf0AB7261819fCf587De7e6D68f902E43195'
blockNo = 'latest'
#
#
asset_timelocks = web3fsn.fsnGetAllTimeLockBalances(pub_key, block_identifier=None)
#
print(asset_timelocks,'\n')
#
