#!/usr/bin/env python3
#
# Demonstrate getting asset information
#
#
from web3fsnpy import Web3Fsn
import os
import sys
from eth_utils import (
    to_hex,
)
from getpass import getpass
from eth_keys import keys

#import pdb ; pdb.set_trace()

testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"
httptestnet = "http://testnetpublicgateway1.fusionnetwork.io:10000"
#
web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider(testnet))
#web3fsn = Web3Fsn(Web3Fsn.HTTPProvider(httptestnet))
#
asset_name = 'FSN'
blockNo = 'latest'
#
#
asset_Id = web3fsn.fsn.getAssetId(asset_name)
#
asset_dict = web3fsn.fsn.getAsset(asset_Id,blockNo)
#
print(asset_dict,'\n')
#
#
for key, Id in asset_dict.items():
    print(key, ' :    ', Id)

