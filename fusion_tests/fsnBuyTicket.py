#!/usr/bin/env python3
#
"""
 Demonstrate buying a ticket. 
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


pub_key = '0x3333333333333333333333333333333333333333' 


print('Is autoBuyTicket set? : ',web3fsn.isAutoBuyTicket())


nonce = web3fsn.getTransactionCount(pub_key)  # Get the nonce for the wallet

# Construct the transaction
#

transaction = {
    'from':             pub_key,
    'nonce':            nonce,
}

TxHash = web3fsn.buyRawTicket(transaction)

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

