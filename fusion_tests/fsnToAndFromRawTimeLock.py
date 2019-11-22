#!/usr/bin/env python3
#
"""
 Demonstrate sending asset tokens on the Fusion blockchain to timelock using the raw transaction method and back again, 
 without changing the time lock. You can use this method when you wish to sign the transaction offline and broadcast it later, 
 or if you do not have an unlocked wallet (i.e. you are not using the IPC mode).
"""
#
#
import os
import sys
from datetime import datetime
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
pub_key_receiver = "0x3333333333333333333333333333333333333334"

asset_Id = '0x3ddec7217915b0c145da683402cfbb94c1b160d23a432f75a39e33e2db091437'
number_to_transfer = 5  # The number of tokens you wish to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
asset_name = asset_dict['Symbol']
print('The asset has the symbol ',asset_name,' and decimals ',asset_dict['Decimals'])


nToSend = int(number_to_transfer*10**float(asset_dict['Decimals']))

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction
#
# We do not include start or end times here :-
#
transaction = {
  'from':       pub_key_sender,
  'to':         pub_key_sender,   # send the assets to the same wallet, but as a timelock
  'nonce':      nonce,
  'asset':      asset_Id,
  'value':      nToSend,
}

TxHash = web3fsn.assetToRawTimeLock(transaction)

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
#print(res)
#
#
# Now send them back to assets again
#
    print('\nNow send the time lock tokens back to assets...')
    reply = input('Check your wallet and hit enter to continue > ')
#
    transaction['nonce'] = nonce + 1
    
# Use the same transaction data
#
TxHash = web3fsn.timeLockToRawAsset(transaction)

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
#print(res)
#
