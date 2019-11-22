#!/usr/bin/env python3
#
"""
 Demonstrate sending asset tokens from your timelock balance on the Fusion blockchain to someone else's timelock using the raw transaction method. 
 You can use this method when you wish to sign the transaction offline and broadcast it later, 
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
    'provider'    : 'WebSocket',                             # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read, or signed raw transactions
}

#

web3fsn = Fsn(linkToChain)


pub_key_sender = "0x3333333333333333333333333333333333333333"
pub_key_receiver = "0x3333333333333333333333333333333333333334"

asset_Id = '0x3ddec7217915b0c145da683402cfbb94c1b160d23a432f75a39e33e2db091437'
number_to_transfer = 0.4  # The number of tokens you wish to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
asset_name = asset_dict['Symbol']
print('The asset has the symbol ',asset_name,' and decimals ',asset_dict['Decimals'])
#
#
#  First of all send some token assets in your wallet to timelock

nToSend = int(number_to_transfer*10**float(asset_dict['Decimals']))

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction
#
# Example of valid dates for 'start' and 'end'. Can also use 'now' and 'infinity'.
#"2007-03-01T13:00:00+0100"  or  UTC = "2007-03-01T12:00:00"

transaction = {
  'from':       pub_key_sender,
  'to':         pub_key_sender,  # same wallet
  'nonce':      nonce,
  'asset':      asset_Id,
  'value':      nToSend,
  'start':      '2020-06-01T06:00:00+0400',
  'end':        'Infinity',
}

TxHash = web3fsn.assetToRawTimeLock(transaction)

#
print('Transaction hash = ',TxHash)
#
# We can optionally wait for the transaction to occur and block execution until it has done so, or times out after timeout seconds
print('Waiting for transaction to go through...')
web3fsn.waitForTransactionReceipt(TxHash, timeout=120)
#
#
res = web3fsn.getTransaction(TxHash)
#
#print(res)
#
# Show the timelocks for the pub_key_sender
#
asset_timelocks = web3fsn.getTimeLockBalance(asset_Id, pub_key_sender, 'latest')
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
    print(val/(10**asset_dict['Decimals']),' ',asset_name,'\n')
#
#
# Now we will send some timelocked tokens to someone else's wallet.
#
#
print('\nNow send the time lock tokens someone else\'s wallet...')
reply = input('Check your wallet and hit enter to continue > ')
#
transaction = {
    'from':       pub_key_sender,
    'to':         pub_key_receiver, 
    'nonce':      nonce + 1,
    'asset':      asset_Id,
    'value':      int(nToSend/2),       # Send only half
    'start':      '2020-12-01T06:00:00', # Send a later time portion
    'end':        'Infinity',
}
    
    
TxHash = web3fsn.timeLockToRawTimeLock(transaction)

#
print('Transaction hash = ',TxHash)
#
# We can optionally wait for the transaction to occur and block execution until it has done so, or times out after timeout seconds
print('Waiting for transaction to go through...')
web3fsn.waitForTransactionReceipt(TxHash, timeout=120)
#
#
res = web3fsn.getTransaction(TxHash)
#
#print(res)
#
# Show the timelocks for the pub_key_sender
#
asset_timelocks = web3fsn.getTimeLockBalance(asset_Id, pub_key_sender, 'latest')
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
    print(val/(10**asset_dict['Decimals']),' ',asset_name,'\n')
#   
