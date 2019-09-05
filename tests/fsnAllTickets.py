#!/usr/bin/env python3

from web3fsnpy import Web3Fsn
from datetime import datetime

testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"


web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider(mainnet))


# Print out details of all tickets at current block height


allTckts = web3fsn.fsn.allTickets('latest')

#print(allTckts)



for a in allTckts:
    tck = allTckts[a]
    st = datetime.fromtimestamp(tck.StartTime).strftime('%c')
    ex = datetime.fromtimestamp(tck.ExpireTime).strftime('%c')
    print('Owner: ',tck.Owner,' Block Height: ',tck.Height,' Start Time: ',st,' Expiry Time: ',ex)


print('\n\nTotal number of tickets = ',len(allTckts))

print('\n\nor using totalNumberOfTickets = ',web3fsn.fsn.totalNumberOfTickets())

