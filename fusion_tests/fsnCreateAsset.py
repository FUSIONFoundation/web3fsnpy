#!/usr/bin/env python3
#
"""
 Demonstrate creating asset tokens on the Fusion blockchain. You can use this method
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
    'provider'    : 'IPC',                              # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read operations
}

#

web3fsn = Fsn(linkToChain)

#pdb.set_trace()

pub_key_sender = "0x3333333333333333333333333333333333333333"



nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  "from":       pub_key_sender,
  "name":       "TestCoin",
  "nonce":       nonce,
  "symbol":     "TST4",
  "decimals":   1,
  "total":      2000,
  "canChange":  True,
}

TxHash = web3fsn.createAsset(transaction)

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

