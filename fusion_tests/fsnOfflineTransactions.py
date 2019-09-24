#!/usr/bin/env python3
#
"""
 Demonstrate the creation of some transactions without needing a private key and then signing and 
 sending them later as a batch with signAndTransmit using a private key, 
 perhaps from a more secure computer or in a hardened environment.
 
"""
#
#
import os
import sys
import json
#import pdb ; pdb.set_trace()



#web3fusion
from  web3.fusion import Fsn


linkToChain = {
    'network'     : 'testnet',                          # One of 'testnet', or 'mainnet'
    'provider'    : 'HTTP',                             # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    #'private_key'                 No private key provided this time
}

#

web3fsn = Fsn(linkToChain)

#pdb.set_trace()

pub_key_sender = "0x7fbFa5679411a97bb2f73Dd5ad01Ca0822FaD9a6"
pub_key_receiver = "0xaa8c70e134a5A88aBD0E390F2B479bc31C70Fee1"

asset_Id = '0x5fd3f254ae34bf9bf9dc46f72e4fbbc75844dbe6823f970fa3f7aaedb2925ff6'
number_to_transfer = 5  # The number of tokens you wish to send

# Find out some information about this asset
asset_dict = web3fsn.getAsset(asset_Id,'latest')
#print(asset_dict)
print('The asset has the symbol ',asset_dict['Symbol'],' and decimals ',asset_dict['Decimals'])

nonce = web3fsn.getTransactionCount(pub_key_sender)  # Get the nonce for the wallet

# Construct the transaction

transaction = {
  'from':       pub_key_sender,
  'to':         pub_key_receiver,
  'nonce':      nonce,
  'asset':      asset_Id,
  'value':      int(number_to_transfer*10**float(asset_dict['Decimals'])),    # This is the integer number of the smallest unit that can be sent, defined by the decimals of the asset.
}

# Open a file to store json data
fp = open('fusion_transaction_dict.json','w')

Tx_dict = web3fsn.sendRawAsset(transaction, prepareOnly=True)     # Set the prepareOnly flag to stop them being signed now.
#
# Store the data
json_tx = json.dumps(Tx_dict)
fp.write(json_tx+'\n')
#
# Add another transaction
transaction['nonce'] = nonce + 1
Tx_dict = web3fsn.sendRawAsset(transaction, prepareOnly=True)
json_tx = json.dumps(Tx_dict)
fp.write(json_tx+'\n')
#
fp.close()
del web3fsn    # Clean up and delete the Fsn object
#
#
# At a later time, or from a more secure computer, you can sign and transmit the data
#
print('\nWe have finished generating the transactions now. At a later time we can actually sign and transmit them...\n')
#
#   Remember to set your environment variables to run this test
#    e.g. export FSN_PRIVATE_KEY=123456789123456789ABCDEF 



linkToChain = {
    'network'     : 'testnet',                          # One of 'testnet', or 'mainnet'
    'provider'    : 'HTTP',                             # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',                          # Either set to 'default', or specify your uri endpoint
    'private_key'     : os.environ["FSN_PRIVATE_KEY"],  # This time we need a private key
}
#
web3fsn = Fsn(linkToChain)
#
# Get the transaction data we stored previously
fp = open('fusion_transaction_dict.json','r')
#
ii = 1
#
for line in fp:
    Tx_dict = json.loads(line)
    print('Signing and transmitting ',ii)
    TxHash = web3fsn.signAndTransmit(Tx_dict)
    print('Transaction hash = ',TxHash)
    web3fsn.waitForTransactionReceipt(TxHash, timeout=20)
    ii = ii+1
#
print('\nFinished')
#
os.remove('fusion_transaction_dict.json')
fp.close()
#

