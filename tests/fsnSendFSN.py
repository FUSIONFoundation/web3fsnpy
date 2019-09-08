#!/usr/bin/env python3
#
# Demonstrate sending FSN tokens from one account to another
#
#
from web3fsnpy import Web3Fsn
import os
import sys
from eth_utils import (
    to_hex,
)


testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"

web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider(testnet))
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


value = web3fsn.toWei(0.02,'ether')    # How much FSN are we sending?

nonce = web3fsn.fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the sending wallet

# Construct the transaction

transaction = {
            "from"  : pub_key_sender,
            "to"    : pub_key_receiver,
            "nonce" : nonce,
            "value" : value,
}

# Fill in the defaults, including gas and gasLimit

tx = web3fsn.fsn.fill_tx_defaults(transaction)

# Sign the transaction

signed_tx = web3fsn.fsn.account.sign_transaction(tx,private_key_sender)

# Send the raw transaction (i.e. signed)

TxHash = web3fsn.fsn.sendRawTransaction(signed_tx.rawTransaction)
#
print('TxHash = ',to_hex(TxHash))
#
# We can optionally wait for the transaction to occur and block execution until it has done so, or times out after timeout seconds
print('Waiting for transaction to go through...')
web3fsn.fsn.waitForTransactionReceipt(TxHash, timeout=20)
#
#
res = web3fsn.fsn.getTransaction(TxHash)
#
#print(res)
#
print('\nResults from the transaction :\n')
print('Block number: ',res["blockNumber"])
print('From        : ',res["from"])
print('To          : ',res["to"])
print('Value       : ',web3fsn.fromWei(res["value"],'ether'),' FSN')
print('Gas price   : ',web3fsn.fromWei(res["gasPrice"],'gwei'),' gwei')

