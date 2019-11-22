#!/usr/bin/env python3
#
"""
 Demonstrate creating a swap on the Quantum Swap market and then recalling that swap. 
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
pub_key_receiver = "0x3333333333333333333333333333333333333334"  # For a private swap

assetId_TST1 = '0x3ddec7217915b0c145da683402cfbb94c1b160d23a432f75a39e33e2db091437'
assetId_TST2 = '0x34ab2db7e4e5a69e5ec1441d580b9e9599e806cbecf821b87bf4a5952e27ee21'

number_to_swap = 5      # The minimum number of tokens you wish to swap
number_to_receive = 1   # The minimum number of tokens you wish to receive

# Find out some information about these assets
asset_dict = web3fsn.getAsset(assetId_TST1,'latest')
asset_TST1_name = asset_dict['Symbol']
asset_TST1_decimals = asset_dict['Decimals']

asset_dict = web3fsn.getAsset(assetId_TST2,'latest')
asset_TST2_name = asset_dict['Symbol']
asset_TST2_decimals = asset_dict['Decimals']
#
#

nToSend = int(number_to_swap*10**float(asset_TST1_decimals))
nToReceive = int(number_to_receive*10**float(asset_TST2_decimals))

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction
#
# Example of valid dates for 'start' and 'end'. Can also use 'now' and 'infinity', 
# or a hex string with the number of seconds since "1970-01-01T00:00:00+0000".
# "2007-03-01T13:00:00+0100"  or  UTC = "2007-03-01T12:00:00"

transaction = {
    'from':                 pub_key_sender,
    'nonce':                nonce,
    'ToAssetID':            assetId_TST1,
    'ToStartTime':          'now',
    'ToEndTime':            '2020-06-01T06:00:00+0400',
    'MinToAmount':          nToSend,
    'FromAssetID':          assetId_TST2,
    #'FromStartTime':       Defaults to 'now'
    #'FromEndTime':         Defaults to 'infinity'
    'MinFromAmount':        nToReceive,
    'SwapSize':             3,
    'Targes':               [],  # Leave as an empty list [] for a public swap.
}

TxHash = web3fsn.makeRawSwap(transaction)

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
# Show the timelocks for the pub_key_sender
#
asset_timelocks = web3fsn.getTimeLockBalance(assetId_TST1, pub_key_sender, 'latest')
#
n_items = len(asset_timelocks.Items)
print('\nNumber of timelocked ', asset_TST1_name, ' = ',n_items,'\n')
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
    print(val/(10**asset_dict['Decimals']),' ',asset_TST1_name,'\n')
#
#
#
# Now we will recall the swap.
#
#
print('\nNow recall the swap...')
reply = input('Check your wallet Quantum Swaps and hit enter to continue > ')
#
swap_dict = web3fsn.getAllSwaps()   # THIS ONLY WORKS FOR THE MAINNET SWAPS

for ii in range(len(swap_dict)):
    if swap_dict[ii]['fromAddress'] == pub_key_sender :     # This should be the most recent swap created by the pub_key_sender
        swap = swap_dict[ii]['swapID']

#
transaction = {
    'from':                 pub_key_sender,
    'nonce':                nonce + 1,
    'SwapID':               swap,
}

TxHash = web3fsn.recallRawSwap(transaction)
# We can optionally wait for the transaction to occur and block execution until it has done so, or times out after timeout seconds
print('Waiting for transaction to go through...')
web3fsn.waitForTransactionReceipt(TxHash, timeout=20)
#
#
res = web3fsn.getTransaction(TxHash)
#
print(res)
#


