#!/usr/bin/env python3
#
"""
 Demonstrate increasing and decreasing the number of tokens of an asset on the Fusion blockchain using the raw transaction method. You can use this method
 when you wish to sign the transaction offline and broadcast it later, or if you do not have an unlocked wallet (i.e. you are not using the IPC mode).
"""
#
#
import os
import sys
#import pdb ; pdb.set_trace()



#web3fusion
from  web3fsnpy import Fsn

#   Remember to set your environment variable to run this test
#    e.g. export FSN_PRIVATE_KEY=123456789123456789ABCDEF 



linkToChain = {
    'network'     : 'testnet',                          # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',                        # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read, or signed raw transactions
}

#

web3fsn = Fsn(linkToChain)


pub_key_sender = "0x3333333333333333333333333333333333333333"
pub_key_receiver = "0x3333333333333333333333333333333333333333"

asset_Id = '0x5fd3f254ae34bf9bf9dc46f72e4fbbc75844dbe6823f970fa3f7aaedb2925ff6'
number_to_increase = 5  # The number of tokens you wish to increment by and to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
print('The asset has the symbol ',asset_dict['Symbol'],' and decimals ',asset_dict['Decimals'], ' and CanChange is set to ',asset_dict['CanChange'])

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  'from':        pub_key_sender,
  'to':          pub_key_receiver,
  'nonce':       nonce,
  'asset':       asset_Id,
  'value':       int(number_to_increase*10**float(asset_dict['Decimals'])),    # This is the integer number of the smallest unit that can be increased, defined by the decimals of the asset.
  'transacData': 'Huge airdrop',   # Optional message
}

TxHash = web3fsn.incRawAsset(transaction)

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
bal = web3fsn.getBalance(pub_key_receiver, asset_Id, 'latest')
#
print('Balance for receiver ', pub_key_receiver, ' is  ', float(bal)/(10**float(asset_dict['Decimals'])), ' ',asset_dict['Symbol'])
#
#
# Now we will do a token burn
#
number_to_decrease = 50
#
print('\nPerforming a token burn of ',number_to_decrease, ' ',asset_dict['Symbol'])
#
nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  'from':        pub_key_sender,
  'to':          pub_key_sender,  # set to same as 'from'
  'nonce':       nonce,
  'asset':       asset_Id,
  'value':       int(number_to_decrease*10**float(asset_dict['Decimals'])),    # This is the integer number of the smallest unit that can be decreased, defined by the decimals of the asset.
  'transacData': 'Token burn',   # Optional message
}

TxHash = web3fsn.decRawAsset(transaction)

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
#  Get the new balance of the account
bal = web3fsn.getBalance(pub_key_sender, asset_Id, 'latest')
#
print('Balance for token burn account  ', pub_key_sender, ' is  ', float(bal)/(10**float(asset_dict['Decimals'])), ' ',asset_dict['Symbol'])
#




