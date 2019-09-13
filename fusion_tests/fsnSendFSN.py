#!/usr/bin/env python3
#
# Demonstrate sending FSN tokens from one account to another
#
#
import os
import sys
from getpass import getpass


#web3fusion
from  web3.fusion import Fsn

linkToChain = {
    'network'     : 'testnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'http://testnetpublicgateway1.fusionnetwork.io:10000',
}

web3fsn = Fsn(linkToChain)

#
#
# Don't leave a private key hardcoded, so you could use an environmental variable to store it
#
try:  
   private_key_sender = os.environ["FSN_PRIVATE_KEY"]
except KeyError: 
   print('Set environment variable FSN_PRIVATE_KEY to be private key of sending wallet (without 0x prefix)')
   sys.exit(1)


pub_key_sender = "0x7fbFa5679411a97bb2f73Dd5ad01Ca0822FaD9a6"
pub_key_receiver = "0xaa8c70e134a5A88aBD0E390F2B479bc31C70Fee1"



# Unlock account
#
#unlockDuration = 2
#
#password = getpass('Password: ')
#
#res = web3fsn.geth.personal.unlockAccount(pub_key_sender, password, unlockDuration)

#print(res)

value = web3fsn.toWei(0.02,'ether')    # How much FSN are we sending?

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the sending wallet

# Construct the transaction

transaction = {
            "from"  : pub_key_sender,
            "to"    : pub_key_receiver,
            "nonce" : nonce,
            "value" : value,
}

# Fill in the defaults, including gas and gasLimit

tx = web3fsn.fill_tx_defaults(transaction)

#print(tx)

# Sign the transaction if you want to send a raw transaction. No need for an unsigned transaction

signed_tx = web3fsn.account.sign_transaction(tx,private_key_sender)

# Send the raw transaction (i.e. signed)
TxHash = web3fsn.sendRawTransaction(signed_tx.rawTransaction)
#
# Or send an unsigned transaction (open wallet with unlockAccount above first)
#TxHash = web3fsn.fsn.sendTransaction(tx)
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

