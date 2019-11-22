#!/usr/bin/env python3
#
"""
 Demonstrate sending asset tokens on the Fusion blockchain. You can use this method
 when you have an unlocked wallet (i.e. you are using the IPC mode and are running a node).
"""
#
#
import os
import sys
#import pdb ; pdb.set_trace()



#web3fusion
from  web3fsnpy import Fsn

#   Remember to set your environment variables to run this test
#    e.g. export FSN_PRIVATE_KEY=123456789123456789ABCDEF 



linkToChain = {
    'network'     : 'testnet',                          # One of 'testnet', or 'mainnet'
    'provider'    : 'IPC',                             # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read operations
}

#

web3fsn = Fsn(linkToChain)

#pdb.set_trace()

pub_key_sender = "0x3333333333333333333333333333333333333333"
pub_key_receiver = "0x3333333333333333333333333333333333333334"

asset_Id = '0x5fd3f254ae34bf9bf9dc46f72e4fbbc75844dbe6823f970fa3f7aaedb2925ff6'
number_to_transfer = 5  # The number of tokens you wish to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
print('The asset has the symbol ',asset_dict['Symbol'],' and decimals ',asset_dict['Decimals'])

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  'from':       pub_key_sender,
  'to':         pub_key_receiver,
  'nonce':      nonce,
  'asset':      asset_Id,
  'value':      int(number_to_transfer*10**float(asset_dict['Decimals'])),    # This is the integer number of the smallest unit that can be sent, defined by the decimals of the asset.
}

TxHash = web3fsn.sendAsset(transaction)


#
print('Transaction hash = ',TxHash)
#
# We can optionally wait for the transaction to occur and block execution until it has done so, or times out after timeout seconds
print('Waiting for transaction to go through...')
web3fsn.waitForTransactionReceipt(TxHash, timeout=20)
#
#
res = web3fsn.getTransaction(TxHash)
#
print(res)
#

