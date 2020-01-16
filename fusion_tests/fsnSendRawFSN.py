#!/usr/bin/env python3
#
# Demonstrate sending FSN tokens from one account to another
#
#
import os
import sys
from getpass import getpass


#web3fusion
from  web3fsnpy import Fsn


#
# Don't leave a private key hardcoded, so you could use an environmental variable to store it
#
try:  
   private_key_sender = os.environ["FSN_PRIVATE_KEY"]
except KeyError: 
   print('Set environment variable FSN_PRIVATE_KEY to be private key of sending wallet (without 0x prefix)')
   sys.exit(1)



linkToChain = {
    'network'     : 'testnet',                          # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',                        # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key' : private_key_sender,                 # Do not include (comment out) for just read transactions
}

web3fsn = Fsn(linkToChain)

#


pub_key_sender = "0x3333333333333333333333333333333333333333"
pub_key_receiver = "0x3333333333333333333333333333333333333334"




value = web3fsn.toWei(0.02,'ether')    # How much FSN are we sending?

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the sending wallet

# Construct the transaction

transaction = {
            "from"  : pub_key_sender,
            "to"    : pub_key_receiver,
            "nonce" : nonce,
            "value" : value,
}

# Send the raw transaction. 
TxHash = web3fsn.sendRawTransaction(transaction)
#
#
print('TxHash = ',web3fsn.toHex(TxHash))
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
print('\nResults from the transaction :\n')
print('Block number: ',res["blockNumber"])
print('From        : ',res["from"])
print('To          : ',res["to"])
print('Value       : ',web3fsn.fromWei(res["value"],'ether'),' FSN')
print('Gas price   : ',web3fsn.fromWei(res["gasPrice"],'gwei'),' gwei')

