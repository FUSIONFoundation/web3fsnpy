#!/usr/bin/env python3
#
# Demonstrate getting timelock balances information
#
#web3fusion
from  web3fsnpy import Fsn

import os
import sys
from eth_utils import (
    to_hex,
)
from datetime import datetime, timedelta

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'HTTP',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',
}

web3fsn = Fsn(linkToChain)



#
pub_key = '0x3333333333333333333333333333333333333333'
blockNo = 'latest'
#
#
asset_timelocks = web3fsn.getAllTimeLockBalances(pub_key, block_identifier=None)
#
print(asset_timelocks,'\n')
#
