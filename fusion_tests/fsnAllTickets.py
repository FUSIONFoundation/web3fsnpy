#!/usr/bin/env python3

#web3fusion
from  web3.fusion import Fsn
from datetime import datetime

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://mainnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
}

web3fsn = Fsn(linkToChain)


# Print out details of all tickets at current block height


allTckts = web3fsn.allTickets('latest')

#print(allTckts)



for a in allTckts:
    tck = allTckts[a]
    st = datetime.fromtimestamp(tck.StartTime).strftime('%c')
    ex = datetime.fromtimestamp(tck.ExpireTime).strftime('%c')
    print('Owner: ',tck.Owner,' Block Height: ',tck.Height,' Start Time: ',st,' Expiry Time: ',ex)


print('\n\nTotal number of tickets = ',len(allTckts))

print('\n\nor using totalNumberOfTickets = ',web3fsn.totalNumberOfTickets())

