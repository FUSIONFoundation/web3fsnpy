#!/usr/bin/env python3

#web3fusion
from  web3fsnpy import Fsn
from datetime import datetime

linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',   # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'wss://mainnetpublicgateway1.fusionnetwork.io:10001',
    #'gateway'     : 'wss://testnetpublicgateway1.fusionnetwork.io:10001',
}

web3fsn = Fsn(linkToChain)

# Get the ticket price 

ticket_price = web3fsn.ticketPrice()
ticket_price = web3fsn.fromWei(ticket_price,'ether')

print('\nThe ticket price = ',ticket_price,' FSN')

input('Hit a key to continue ')


# Get the staking information

stake_info = web3fsn.getStakeInfo()
#print(stake_info)

for node in range(stake_info.summary.totalMiners):
    print(stake_info.stakeInfo[node].owner, ' has ', stake_info.stakeInfo[node].tickets, ' tickets')

input('Hit a key to continue ')


# Get the block reward

block_reward = web3fsn.getBlockReward()

print('\nThe block reward for the latest block was ',web3fsn.fromWei(block_reward,'ether'),' FSN\n')

input('Hit a key to continue ')

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




