#!/usr/bin/env python3
#
"""
 Demonstrate sending asset tokens on the Fusion blockchain using the raw transaction method. You can use this method
 when you wish to sign the transaction offline and broadcast it later, or if you do not have an unlocked wallet (i.e. you are not using the IPC mode).
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
    'provider'    : 'HTTP',                             # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read operations
}

#

web3fsn = Fsn(linkToChain)

#pdb.set_trace()

pub_key_sender = "0x7fbFa5679411a97bb2f73Dd5ad01Ca0822FaD9a6"
USAN_receiver = "4128"


asset_Id = '0x5fd3f254ae34bf9bf9dc46f72e4fbbc75844dbe6823f970fa3f7aaedb2925ff6'
number_to_transfer = 0.1  # The number of tokens you wish to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
print('The asset has the symbol ',asset_dict['Symbol'],' and decimals ',asset_dict['Decimals'])

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  'from':       pub_key_sender,
  'toUSAN':     USAN_receiver,
  'nonce':      nonce,
  'asset':      asset_Id,
  'value':      int(number_to_transfer*10**float(asset_dict['Decimals'])),    # This is the integer number of the smallest unit that can be sent, defined by the decimals of the asset.
}

TxHash = web3fsn.sendRawAsset(transaction)

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
#print(res,'\n')
#
#  Get the new balance of each account
bal = web3fsn.getBalance(pub_key_sender, asset_Id, 'latest')
#
print('Balance for sender   ', pub_key_sender, ' is  ', float(bal)/(10**float(asset_dict['Decimals'])), ' ',asset_dict['Symbol'])
#
# Need Fusion to fix a bug in getAddressByNotation before you can getBalance using a USAN. When they do, the following can be uncommented
# The issue has been reported and a bug report filed
#
##bal = web3fsn.getBalance(USAN_receiver, asset_Id, 'latest')
#
##print('Balance for receiver ', USAN_receiver, ' is  ', float(bal)/(10**float(asset_dict['Decimals'])), ' ',asset_dict['Symbol'])

