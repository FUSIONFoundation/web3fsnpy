#!/usr/bin/env python3
#
"""
 Demonstrate sending asset tokens on the Fusion blockchain to timelock using the raw transaction method. You can use this method
 when you wish to sign the transaction offline and broadcast it later, or if you do not have an unlocked wallet (i.e. you are not using the IPC mode).
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


pub_key_sender = "0x1111111111111111111111111111111111111111"
pub_key_receiver = "0x2222222222222222222222222222222222222222"

#asset_Id = '0x5fd3f254ae34bf9bf9dc46f72e4fbbc75844dbe6823f970fa3f7aaedb2925ff6'
asset_Id = web3fsn.getAssetId('FSN')
#asset_Id = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
number_to_transfer = 2  # The number of tokens you wish to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
asset_name = asset_dict['Symbol']
print('The asset has the symbol ',asset_name,' and decimals ',asset_dict['Decimals'])


nToSend = int(number_to_transfer*10**float(asset_dict['Decimals']))

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction
#
# Example of valid dates for 'start' and 'end'. Can also use 'now' and 'infinity'.
#"2007-03-01T13:00:00+0100"  or  UTC = "2007-03-01T12:00:00"

transaction = {
  'from':       pub_key_sender,
  'to':         pub_key_receiver,
  'nonce':      nonce,
  'asset':      asset_Id,
  'value':      nToSend,
  #'start':      'now',
  #'end':        '2020-06-01T06:00:59',
  'start':      '2020-12-20T06:01:01',
  'end':        'infinity',
}

TxHash = web3fsn.sendRawTimeLock(transaction)

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
# Show the timelocks for the pub_key_receiver
#
asset_timelocks = web3fsn.getTimeLockBalance(asset_Id, pub_key_receiver, 'latest')
#
n_items = len(asset_timelocks.Items)
print('\nNumber of timelocked ', asset_name, ' = ',n_items,'\n')
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

