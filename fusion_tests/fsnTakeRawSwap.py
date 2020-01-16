#!/usr/bin/env python3
#
"""
 Demonstrate taking asset tokens on the Quantum Swap market of the Fusion blockchain using the raw transaction method. 
 You can use this method when you wish to sign the transaction offline and broadcast it later, 
 or if you do not have an unlocked wallet (i.e. you are not using the IPC mode).
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


pub_key = '0x7fbFa5679411a97bb2f73Dd5ad01Ca0822FaD9a6'  # For a private swap

swapInfo = web3fsn.getAllSwaps()

#print(swapInfo)

for swp in swapInfo:
    print('SwapID : {} From asset : {} To asset : {} Size : {} MinFromAmount : {} MinToAmount : {} SwapSize : {}\n'
          .format(swp['swapID'],swp['fromAsset'],swp['toAsset'],swp['size'],
          swp['MinFromAmount'],swp['MinToAmount'],swp['SwapSize']))

swapID = input('Enter a swapID from the above list  ')


number_to_receive = input('Enter the number you wish to receive ')   # The number of tokens you wish to receive


nonce = web3fsn.getTransactionCount(pub_key)  # Get the nonce for the wallet

# Construct the transaction
#

transaction = {
    'from':             pub_key,
    'nonce':            nonce,
    'SwapID':           swapID,
    'Size':             number_to_receive,
}

TxHash = web3fsn.takeRawSwap(transaction)

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
# Get some information about the swap
#
swap_dict = web3fsn.getSwap(TxHash)
#
print(swap_dict)

