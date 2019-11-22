#!/usr/bin/env python3


from datetime import datetime

#web3fusion
from  web3fsnpy import Fsn

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://mainnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
}

web3fsn = Fsn(linkToChain)



pub_key = "0x3333333333333333333333333333333333333333"

Tckts = web3fsn.ticketsByAddress(pub_key)

#print(Tckts)

print('Total number of tickets: ',len(Tckts))
print('\nor using totalNumberOfTicketsByAddress: ',web3fsn.totalNumberOfTicketsByAddress(pub_key),'\n')
      
for a in Tckts:
    tck = Tckts[a]
    st = datetime.fromtimestamp(tck.StartTime).strftime('%c')
    ex = datetime.fromtimestamp(tck.ExpireTime).strftime('%c')
    print('Block Height: ',tck.Height,' Start Time: ',st,' Expiry Time: ',ex)




