#!/usr/bin/env python3
#
"""
 Demonstrate generating a USAN notation on Fusion. 
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
    'provider'    : 'WebSocket',                        # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # Do not include (comment out) for just read operations
}

#

web3fsn = Fsn(linkToChain)

#pdb.set_trace()

pub_key_sender = "0xaa8c70e134a5A88aBD0E390F2B479bc31C70Fee1"


nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  'from':       pub_key_sender,
  'nonce':      nonce,
}

TxHash = web3fsn.genRawNotation(transaction)


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
# Request the value back
#
notation = web3fsn.getNotation(pub_key_sender)
#
print('The generated notation is ',notation)
#
# Check that this notation refers to our public key 
#
pubk = web3fsn.getAddressByNotation(notation)
#
print('The public address is ',pubk)
#


