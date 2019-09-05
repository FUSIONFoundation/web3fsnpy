#!/usr/bin/env python3

from web3fsnpy import Web3Fsn
from datetime import datetime


testnet = "wss://testnetpublicgateway1.fusionnetwork.io:10001"
mainnet = "wss://mainnetpublicgateway1.fusionnetwork.io:10001"

web3fsn = Web3Fsn(Web3Fsn.WebsocketProvider(mainnet))

pub_key = "0x432baf0AB7261819fCf587De7e6D68f902E43195"

Tckts = web3fsn.fsn.ticketsByAddress(pub_key)

#print(Tckts)

print('Total number of tickets: ',len(Tckts))
print('\nor using totalNumberOfTicketsByAddress: ',web3fsn.fsn.totalNumberOfTicketsByAddress(pub_key),'\n')
      
for a in Tckts:
    tck = Tckts[a]
    st = datetime.fromtimestamp(tck.StartTime).strftime('%c')
    ex = datetime.fromtimestamp(tck.ExpireTime).strftime('%c')
    print('Block Height: ',tck.Height,' Start Time: ',st,' Expiry Time: ',ex)




