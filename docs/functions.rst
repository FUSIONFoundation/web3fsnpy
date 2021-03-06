
.. |br| raw:: html

    <br>

Functions in the *Fsn* Class
============================

*Fsn* extends *web3.eth*

There are many functions that can be used via the *Fsn* class that are not described here, but are available from the *web3.eth* base class. These include functions to handle smart contracts. Please consult the web3.py documentation for their description and usage.

The functions in *Fsn* are split up into categories below.


Tickets
^^^^^^^

.. function::  ticketPrice

ticketPrice
&&&&&&&&&&&

def ticketPrice(self, block_identifier='latest'):
    """Get the most recent ticket price
    
    Args:
        block_idenfifier:
                    blockNo (int), 'latest', 'earliest', or 'pending'
                    
    Returns:
        ticket_price (int) in Wei
        
    """
    
.. literalinclude:: ../fusion_tests/fsnAllTickets.py
   :language: python
   :lines: 16-22
   :emphasize-lines: 3

   
.. function::  getStakeInfo
   

getStakeInfo
&&&&&&&&&&&&

def getStakeInfo(self, block_identifier='latest'):
    """Get the latest information about the nodes and their tickets
    
    Args:
        block_idenfifier:
                    blockNo (int), 'latest', 'earliest', or 'pending'
                    
    Returns:
        stake_info (Attribute dict) |br|
        'stakeInfo'[{'owner': pub_key1 (hex str), 'tickets':nTickets1 (int)},{'owner':pub_key2, 'tickets':nTickets2 }... ] |br|
        'summary' (Attribute dict) {'totalMiners': tot, 'totalTickets':tot_tick}
        
    """
    
.. literalinclude:: ../fusion_tests/fsnAllTickets.py
   :language: python
   :lines: 26-33
   :emphasize-lines: 3
 
Output :-
   
.. code-block:: python 

    >>>   
    0x76c2ae4281fe1ee1a79ccbdda2516d4d7eb0eb37  has  380  tickets
    0x88817ef0545ca562530f9347b20138edecfd8e30  has  374  tickets
    0x494a792d704e24309fd778641683502fd30f9913  has  290  tickets
    0x37afe6319dbd980741cd3bfe701f196694d20564  has  244  tickets
    0xced7849e100c92768bebda4575db63301f5515e2  has  222  tickets
    0x47bb222e76ff205677132fba7c6cfcddfb4128d2  has  178  tickets
    0xb2a46485d73b47af2c7a62ed1868c48a557dddc0  has  136  tickets
    0x1a77c95b429c0c5646476487d3faab422b541b18  has  109  tickets
    0xd820a610ddb18dc4f54aad3c822045fd06cd5d0b  has  104  tickets
    0x8f94b4f175298ab637f1b963a65e7fa958d2770d  has  104  tickets
    0xf01e34f541caa4a0a1fee65fa55bbf4c19869370  has  91  tickets
    0xe038cd04b17130a29fa82fc13d97df2f88b0bf61  has  83  tickets
    0xfe2b17345de9fa23a7d64406b9d3146946edb125  has  78  tickets
    0x577045c486847fa7bed968d99fa71cf43207a2e9  has  71  tickets
    0x873aea03ea1d1db7dba59b74ce7942087ee30e12  has  69  tickets
    0x83c42e8cc244c9f9f760b57d3fb7e5f10608119b  has  68  tickets
    0x32220e7c4e7448211cd2cd45216bd4cf2e737dea  has  61  tickets
    0x6aec90e7a10986c6971439784186521e57f5f4cd  has  54  tickets
    0x0cdee0d8d79380e909be5574ba05962df50039da  has  51  tickets
    0x8a7ec7b98ec2fbf67c131605868edc5288099005  has  49  tickets
    0x92fd8ad0a0567d8b07f9e0e437f5728d3dbd79fd  has  46  tickets
   

   
.. function:: getBlockReward

getBlockReward
&&&&&&&&&&&&&&

def getBlockReward(self, block_identifier='latest'):
    """Get the block reward for a block
    
    Args:
        block_idenfifier:
                    blockNo (int), 'latest', 'earliest', or 'pending'
                    
    Returns:
        block_reward (int) in Wei
        
    """
    
.. literalinclude:: ../fusion_tests/fsnAllTickets.py
   :language: python
   :lines: 37-43
   :emphasize-lines: 3
    
.. code-block:: python 

    >>>
    The block reward for the latest block was  2.500043904  FSN
   
   
        
.. function::  buyRawTicket

buyRawTicket
&&&&&&&&&&&&

def buyRawTicket(self, transaction):
    """Buy a ticket using the raw method (transaction signed and not using IPC)
    
    Args: 
        transaction (dict):    
                        'from':   pub_key, |br|
                        'nonce':  nonce
    Returns:    
        TxHash (hex str)
    
    """
        
    
Here is an example of the function usage
    
    
.. literalinclude:: ../fusion_tests/fsnBuyTicket.py
   :language: python
   :lines: 41-65
   :emphasize-lines: 12
   

.. function::  allTickets
   
allTickets
&&&&&&&&&&

def allTickets(self, block_identifier):
    """ Return information on all tickets at a certain block height
    
    Args:
        block_idenfifier:
                    blockNo (int), 'latest', 'earliest', or 'pending'
                    
    Returns:
        tickets (list of dictionaries):
                        [{'Owner':      pub_key (address str), |br|
                        'Height':       block_height(int), |br|
                        'StartTime':    datetime, |br|
                        'ExpireTime':   datetime},]
                        
        or None  (raises BlockNotFound exception)
        
    """
    
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnAllTickets.py
   :language: python
   :lines: 45-62
   :emphasize-lines: 3
   

Output:-


    
.. code-block:: python 

    >>>    
    Owner:  0xced7849e100c92768bebda4575db63301f5515e2  Block Height:  932667  Start Time:  Mon Nov 18 12:51:14 2019  Expiry Time:  Wed Dec 18 12:51:14 2019
    Owner:  0x8f94b4f175298ab637f1b963a65e7fa958d2770d  Block Height:  937746  Start Time:  Tue Nov 19 07:16:32 2019  Expiry Time:  Thu Dec 19 07:16:32 2019
    Owner:  0x8f94b4f175298ab637f1b963a65e7fa958d2770d  Block Height:  935119  Start Time:  Mon Nov 18 21:43:25 2019  Expiry Time:  Wed Dec 18 21:43:25 2019
    Owner:  0xced7849e100c92768bebda4575db63301f5515e2  Block Height:  936422  Start Time:  Tue Nov 19 02:28:36 2019  Expiry Time:  Thu Dec 19 02:28:36 2019
    Owner:  0x494a792d704e24309fd778641683502fd30f9913  Block Height:  934627  Start Time:  Mon Nov 18 19:53:32 2019  Expiry Time:  Wed Dec 18 19:53:32 2019
    Owner:  0x6680871ca9c0d0936fe8f875833709381b53e588  Block Height:  938503  Start Time:  Tue Nov 19 10:01:13 2019  Expiry Time:  Thu Dec 19 10:01:13 2019
    Owner:  0xfe2b17345de9fa23a7d64406b9d3146946edb125  Block Height:  937625  Start Time:  Tue Nov 19 06:40:53 2019  Expiry Time:  Thu Dec 19 06:40:53 2019
    Owner:  0x3ee9acfaa487a816ed279945166d04c806b82b3e  Block Height:  937642  Start Time:  Tue Nov 19 06:53:54 2019  Expiry Time:  Thu Dec 19 06:53:54 2019
    Owner:  0x37afe6319dbd980741cd3bfe701f196694d20564  Block Height:  938341  Start Time:  Tue Nov 19 09:25:57 2019  Expiry Time:  Thu Dec 19 09:25:57 2019
    Owner:  0x76c2ae4281fe1ee1a79ccbdda2516d4d7eb0eb37  Block Height:  937771  Start Time:  Tue Nov 19 07:21:58 2019  Expiry Time:  Thu Dec 19 07:21:58 2019
    Owner:  0x19f2ca673faaaab7cd28b1c21d466097c3bf8e32  Block Height:  936858  Start Time:  Tue Nov 19 04:03:20 2019  Expiry Time:  Thu Dec 19 04:03:20 2019
    Owner:  0xfe354642776310a10049b0d90ad2ccad3b12c5ab  Block Height:  937054  Start Time:  Tue Nov 19 04:46:00 2019  Expiry Time:  Thu Dec 19 04:46:00 2019
    Owner:  0xfe2b17345de9fa23a7d64406b9d3146946edb125  Block Height:  935018  Start Time:  Mon Nov 18 21:22:53 2019  Expiry Time:  Wed Dec 18 21:22:53 2019


    Total number of tickets =  4588


    or using totalNumberOfTickets =  4588


    
.. function::  totalNumberOfTickets
    
totalNumberOfTickets
&&&&&&&&&&&&&&&&&&&&

def totalNumberOfTickets(self, block_identifier=None):
    """ Get the total number of tickets at a block height
    
    Args:   
        block_identifier (int),  'latest', 'earliest', or 'pending'
    
    Returns:
        totalNoTickets (int)
        

        
.. function::  ticketsByAddress
   
ticketsByAddress
&&&&&&&&&&&&&&&&

def ticketsByAddress(self, account, block_identifier=None):
    """ Retrieve all tickets for a given address
    
    Args:
        account (public key address str),
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        tickets (list of dictionaries):
                        [{'Height':       block_height(int), |br|
                        'StartTime':    datetime, |br|
                        'ExpireTime':   datetime},]
                        
        or None  (raises BlockNotFound exception)
        
    """
    
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnTicketsByAddress.py
   :language: python
   :lines: 21-33
   :emphasize-lines: 2
   
Output:-

.. code-block:: python 

    >>>
    Block Height:  930018  Start Time:  Mon Nov 18 03:14:49 2019  Expiry Time:  Wed Dec 18 03:14:49 2019
    Block Height:  931191  Start Time:  Mon Nov 18 07:30:07 2019  Expiry Time:  Wed Dec 18 07:30:07 2019
    Block Height:  927881  Start Time:  Sun Nov 17 19:29:47 2019  Expiry Time:  Tue Dec 17 19:29:47 2019
    Block Height:  937145  Start Time:  Tue Nov 19 05:05:52 2019  Expiry Time:  Thu Dec 19 05:05:52 2019
    Block Height:  936443  Start Time:  Tue Nov 19 02:33:09 2019  Expiry Time:  Thu Dec 19 02:33:09 2019
    Block Height:  925714  Start Time:  Sun Nov 17 11:38:26 2019  Expiry Time:  Tue Dec 17 11:38:26 2019


    
.. function::  totalNumberOfTicketsByAddress

    
totalNumberOfTicketsByAddress
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

def totalNumberOfTicketsByAddress(self, account, block_identifier=None):
    """Output the number of tickets for an address
    
    Args:
        account (hex str)   Public key, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        totalTickets (int) 
        
    """

.. function::  isAutoBuyTicket
        
isAutoBuyTicket
&&&&&&&&&&&&&&&

def isAutoBuyTicket(self):
    """Check to see if tickets are automatically bought for this account (if sufficient balance exists)
    
    Args:
        None
        
    Returns:
        isAuto (bool)
        
    """

.. function::  startAutoBuyTicket
    
startAutoBuyTicket
&&&&&&&&&&&&&&&&&&

def startAutoBuyTicket(self):
    """Start to auto buy tickets for your account
    
    Args:
        None
        
    Returns:
        None
        
    """

.. function::   stopAutoBuyTicket   

stopAutoBuyTicket
&&&&&&&&&&&&&&&&&&

def stopAutoBuyTicket(self):
    """Stop to auto buy tickets for your account
    
    Args:
        None
        
    Returns:
        None
        
    """


    
Transactions
^^^^^^^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.


.. function::  getAllBalances

getAllBalances
&&&&&&&&&&&&&&

def getAllBalances(self, account, block_identifier=None):
    """ Get the balances of all non-timelocked assets for an account
    
    Args:
        account (hex str)   Public key, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        bal_info (dict)  key, value pairs for each asset of asset ID and balance
        
    """

.. code-block:: python 

    >>> bal_info = web3fsn.getAllBalances(pub_key)
    >>> for key, val in bal_info.items():
    >>>     print(key, val)
    
    0x0e437e96f105776f7f3f96e01ec9def69a6e66ac37d6560b23181350050238f1 95
    0x15805e688c7516b8cf005fcb3496cf1e904c4d2579955500f5a18a7957a9d59b 1990
    0x34ab2db7e4e5a69e5ec1441d580b9e9599e806cbecf821b87bf4a5952e27ee21 1930
    0x3ddec7217915b0c145da683402cfbb94c1b160d23a432f75a39e33e2db091437 1880
    0x54cbfda5d4cb46ef1f63d6642f561dcd38dec9fa27a68a0408e9b2b17cc5cfc7 1880
    0x5fd3f254ae34bf9bf9dc46f72e4fbbc75844dbe6823f970fa3f7aaedb2925ff6 17
    0x6fe2a4955f1424b72627a81a105d483720630e70fc4743182d874c9acc6d5647 99
    0xcc966efc1aed2a70d602e9718d528f88cfe304cb91d89338d7f1fe1db3266590 90
    0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff 62866649839999999971

    

.. function::  getTransaction

getTransaction
&&&&&&&&&&&&&&

def getTransaction(self, TxHash):
    """
    
    Args:
        TxHash (hex str) Transaction hash
        
    """
    
Example of usage :-

.. literalinclude:: ../fusion_tests/fsnSendRawFSN.py
   :language: python
   :lines: 67-78
   :emphasize-lines: 2

Output :-
   
.. code-block:: python 

    >>>
    Block number:  891233
    From        :  0x7fbFa5679411a97bb2f73Dd5ad01Ca0822FaD9a6
    To          :  0xaa8c70e134a5A88aBD0E390F2B479bc31C70Fee1
    Value       :  0.02  FSN
    Gas price   :  21  gwei
    
    
.. function::  getTransactionAndReceipt

getTransactionAndReceipt
&&&&&&&&&&&&&&&&&&&&&&&&

def getTransactionAndReceipt(self, TxHash):
    """
    
    Args:
        TxHash (hex str) Transaction hash
        
    Returns:
        txData (dict) The transaction data and a receipt
    
    
    """
    
Example output:

.. code-block:: python 

    >>>print(web3fsn.getTransactionAndReceipt('0x8700056ef2896b47760e661902b21d8f294a80bff87c7e4108d7bbd5bce4ce6d'))
    
    "txData": {
    "fsnTxInput": {
      "FuncType": "SendAssetFunc",
      "FuncParam": {
        "AssetID": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "To": "0x37a200388caa75edcc53a2bd329f7e9563c6acb6",
        "Value": 1e+18
      }
    },
    "tx": {
      "blockHash": "0xd8d4b5f054cb398b1f0b5bb5d4add5e80d10a432f2c15226f620609577536b6b",
      "blockNumber": "0xad1a5",
      "from": "0x0122bf3930c1201a21133937ad5c83eb4ded1b08",
      "gas": "0x15f90",
      "gasPrice": "0x3b9aca00",
      "hash": "0x8700056ef2896b47760e661902b21d8f294a80bff87c7e4108d7bbd5bce4ce6d",
      "input": "0xf84402b841f83fa0ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9437a200388caa75edcc53a2bd329f7e9563c6acb6880de0b6b3a7640000",
      "nonce": "0xa7cc",
      "to": "0xffffffffffffffffffffffffffffffffffffffff",
      "transactionIndex": "0x2",
      "value": "0x0",
      "v": "0x16ce3",
      "r": "0x8244e44f720023b240faafab08bb401b1b3167087f2882fa6b8f4fc87b59bdfc",
      "s": "0x277635df431668f4a8b8c8b0702077634dd404db9a1139539d3c276651d3d1ce"
    },
    "receipt": {
      "blockHash": "0xd8d4b5f054cb398b1f0b5bb5d4add5e80d10a432f2c15226f620609577536b6b",
      "blockNumber": "0xad1a5",
      "contractAddress": null,
      "cumulativeGasUsed": "0x10f60",
      "from": "0x0122bf3930c1201a21133937ad5c83eb4ded1b08",
      "fsnLogData": {
        "AssetID": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "To": "0x37a200388caa75edcc53a2bd329f7e9563c6acb6",
        "Value": 1e+18
      },
      "fsnLogTopic": "SendAssetFunc",
      "gasUsed": "0x63e0",
      "logs": [
        {
          "address": "0xffffffffffffffffffffffffffffffffffffffff",
          "topics": [
            "0x0000000000000000000000000000000000000000000000000000000000000002"
          ],
          "data": "0x7b2241737365744944223a22307866666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666222c22546f223a22307833376132303033383863616137356564636335336132626433323966376539353633633661636236222c2256616c7565223a313030303030303030303030303030303030307d",
          "blockNumber": "0xad1a5",
          "transactionHash": "0x8700056ef2896b47760e661902b21d8f294a80bff87c7e4108d7bbd5bce4ce6d",
          "transactionIndex": "0x2",
          "blockHash": "0xd8d4b5f054cb398b1f0b5bb5d4add5e80d10a432f2c15226f620609577536b6b",
          "logIndex": "0x2",
          "removed": false
        }
      ],
      "logsBloom": "0x04000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000000000000002000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000008000000000000000000000",
      "status": "0x1",
      "to": "0xffffffffffffffffffffffffffffffffffffffff",
      "transactionHash": "0x8700056ef2896b47760e661902b21d8f294a80bff87c7e4108d7bbd5bce4ce6d",
      "transactionIndex": "0x2"
    },
    "receiptFound": true
  }

    
    
    
.. function:: getTransactionByBlockNumberAndIndex

getTransactionByBlockNumberAndIndex
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

def getTransactionByBlockNumberAndIndex(self, index, block_identifier=None):
    """Get transactions from a block with a particular index
    
        Args:
            index:  (int)  Index starting at 0, |br|
            block_identifier (int),  'latest', 'earliest', or 'pending',
            
        Returns:
            blockinfo (dict)  See documentation from web3.py, since this function simply redirects to that
    
    """

block_identifier (int),  'latest', 'earliest', or 'pending'
   
.. function::  sendTransaction

sendTransaction
&&&&&&&&&&&&&&&

def sendTransaction(self,transaction):
    """Send FSN tokens to another wallet. You can use this method if you have an unlocked wallet (IPC method)
    
        Args:
            transaction :
        
            'from'  : pub_key_sender (hex str), |br|
            'to'    : pub_key_receiver (hex str), |br|
            'nonce' : nonce (int), |br|
            'value' : value (int)  number of FSN * (10**18),
            
    Returns:
        TxHash transaction hash (hex str)
        
    """



.. function::  sendRawTransaction

.. _sendRawTransaction:

sendRawTransaction
&&&&&&&&&&&&&&&&&&

def sendRawTransaction(self,transaction, prepareOnly=False):
    """Send FSN tokens to another wallet. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction :
        
            'from'  : pub_key_sender (hex str), |br|
            'to'    : pub_key_receiver (hex str), |br|
            'nonce' : nonce (int), |br|
            'value' : value (int)  number of FSN * (10**18),
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point
            
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, then return a Tx_dict (dict)
        
    """

    Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnSendRawFSN.py
   :language: python
   :lines: 42-66
   :emphasize-lines: 17
   
   
.. function::  getTransactionCount
   
getTransactionCount
&&&&&&&&&&&&&&&&&&&

def getTransactionCount(self, pub_key):
    """Get the next unused transaction ID for this public key
    
    Args:
        pub_key (hex str)
        
    Returns:
        nonce (int) The next unused transaction ID for this public key
        
    """
    
See :ref:`sendRawTransaction` for an example of usage


.. function::  waitForTransactionReceipt

waitForTransactionReceipt
&&&&&&&&&&&&&&&&&&&&&&&&&

def waitForTransactionReceipt(self, TxHash, timeout):
    """Check to see that a transaction occured on the blockchain
    
    Args:
        TxHash (hex str) the transaction hash
        
        timeout (int) Optional timeout in seconds to block program execution and wait for waitForTransactionReceipt
        
    """
    
See :ref:`sendRawTransaction` for an example of usage    


.. function::  signAndTransmit

signAndTransmit
&&&&&&&&&&&&&&&

def signAndTransmit(self, Tx_dict):
    """Sign and transmit a raw transaction on the blockchain
    
    Args:
        Tx_dict: (dict) transaction
        
    """
    
See :doc:`offline_transactions` for an example of usage

   
Assets
^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.




.. function::  getAsset
    
getAsset
&&&&&&&&

def getAsset(self, assetId, block_identifier=None):
    """ Retrieve asset from the blockchain with its asset block_identifier
    The asset need not be 'enabled' and 'whiteListEnabled' in the fsnapi
    
    Args:
        assetId (hex str)   Hex string asset idenfifier, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        assetInfo (dict)
        
    """
    
        
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnGetAsset.py
   :language: python
   :lines: 16-30
   :emphasize-lines: 9
   
Outputs :-


.. code-block:: python 

    >>>assetInfo
    {ID  :     0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
    Owner  :     0x0000000000000000000000000000000000000000,
    Name  :     Fusion,
    Symbol  :     FSN,
    Decimals  :     18,
    Total  :     81920000000000000000000000,
    CanChange  :     False,
    Description  :     https://fusion.org
    }


.. function::  createAsset
    

createAsset
&&&&&&&&&&&

def createAsset(self, transaction):
    """Create asset token on the blockchain. You can use this method if you have an unlocked wallet
       and are using the IPC mode
       
    Args:
        transaction (dict):
            'from':     pub_key (hex str), |br|
            'name':     asset_description (str), |br|
            'nonce':    nonce (int), |br|
            'symbol':   asset_name (str), |br|
            'decimals': decimal_places (int), |br|
            'total':    total_supply (int), |br|
            'canChange': change (bool)
        
        
    Returns:
        TxHash transaction hash (hex str)
        
    """

.. function::  createRawAsset
    
createRawAsset
&&&&&&&&&&&&&&

def createRawAsset(self, transaction, prepareOnly=False):
    """Create asset token on the blockchain. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction (dict):
            'from':     pub_key (hex str), |br|
            'name':     asset_description (str), |br|
            'nonce':    nonce (int), |br|
            'symbol':   asset_name (str), |br|
            'decimals': decimal_places (int), |br|
            'total':    total_supply (int), |br|
            'canChange': change (bool)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
        
        
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """
    
 Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnCreateRawAsset.py
   :language: python
   :lines: 37-56
   :emphasize-lines: 16
   
   
.. function::  incAsset
   
incAsset
&&&&&&&&

def incAsset(self, transaction):
    """Increment the supply of an asset. You can use this method if you have an unlocked wallet
       and are using the IPC mode
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    number_to_inc (int), |br|
            'transacData':    message (str)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """

.. function:: incRawAsset 
    
incRawAsset
&&&&&&&&&&&

def incRawAsset(self, transaction, prepareOnly=False):
    """Increment the supply of an asset. You can use this method if you have a locked wallet, with a private key, or password
    
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    number_to_inc (int), |br|
            'transacData':    message (str)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """

Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnInc_and_DecRawAsset.py
   :language: python
   :lines: 38-63
   :emphasize-lines: 22

   
.. function::  decAsset

decAsset
&&&&&&&&

def decAsset(self, transaction, prepareOnly=False):
    """Decrement the supply of an asset. You can use this method if you have an unlocked wallet (IPC method)
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    number_to_dec (int), |br|
            'transacData':    message (str)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """
      
.. function::  decRawAsset   
   
decRawAsset
&&&&&&&&&&&

def decRawAsset(self, transaction, prepareOnly=False):
    """Decrement the supply of an asset. You can use this method if you have a locked wallet, with a private key, or password
    
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    number_to_dec (int), |br|
            'transacData':    message (str)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """
    
.. function::  sendAsset
    
sendAsset
&&&&&&&&&

def sendAsset(self, transaction):
    """Send an asset to another wallet.  You can use this method if you have an unlocked wallet (IPC method).
    
    Args:
        transaction :
        
        'from':       pub_key_sender (hex str), |br|
        'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
        'nonce':      nonce (int), |br|
        'asset':      asset_Id (hex str), |br|
        'value':      val (int) Number of the asset to send * decimals
        
    Returns:
        TxHash transaction hash (hex str)
        
    """

.. function:: sendRawAsset 
    
sendRawAsset
&&&&&&&&&&&&

def sendRawAsset(self, transaction, prepareOnly=False):
    """Send an asset to another wallet. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction :
        
        'from':       pub_key_sender (hex str), |br|
        'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
        'nonce':      nonce (int), |br|
        'asset':      asset_Id (hex str), |br|
        'value':      val (int) Number of the asset to send * decimals
        
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str).  If prepareOnly=True, the return a Tx_dict (dict)
        
    """

    Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnSendRawAsset.py
   :language: python
   :lines: 39-63
   :emphasize-lines: 21
   
    
    
    

Timelocks
^^^^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.


.. function::  getAllTimeLockBalances

getAllTimeLockBalances
&&&&&&&&&&&&&&&&&&&&&&

def getAllTimeLockBalances(self, account, block_identifier=None):
    """Demonstrate getting timelock information for all assets for a public key
    
    Args:
        account (hex str)   Public key, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        asset_timelocks (list of dicts)
        
    """
    
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnGetAllTimelockInfo.py
   :language: python
   :lines: 25-31
   :emphasize-lines: 6
   

.. code-block:: python 

    >>>print(asset_timelocks)
    AttributeDict({'0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff': 
    AttributeDict({'Items': 
    [AttributeDict({'StartTime': 1576582707, 'EndTime': 1583280000, 'Value': '5000000000000000000000'}), 
    AttributeDict({'StartTime': 1576610988, 'EndTime': 1583280000, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576638890, 'EndTime': 1581465600, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576654208, 'EndTime': 1581465600, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576658926, 'EndTime': 1581465600, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576676450, 'EndTime': 1581465600, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576679139, 'EndTime': 1581120000, 'Value': '5000000000000000000000'}), 
    AttributeDict({'StartTime': 1576689626, 'EndTime': 1580083200, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576694666, 'EndTime': 1578787200, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576698618, 'EndTime': 1578787200, 'Value': '5000000000000000000000'}),
    AttributeDict({'StartTime': 1576680247, 'EndTime': 1580083200, 'Value': '2600000000000000000000'}),
    AttributeDict({'StartTime': 1576691387, 'EndTime': 1578787200, 'Value': '2600000000000000000000'}),
    AttributeDict({'StartTime': 1576680247, 'EndTime': 1580774400, 'Value': '2400000000000000000000'}),
    AttributeDict({'StartTime': 1576691387, 'EndTime': 1580083200, 'Value': '2400000000000000000000'}),
    AttributeDict({'StartTime': 1590421416, 'EndTime': 18446744073709551615, 'Value': '20000'}),
    AttributeDict({'StartTime': 1593031827, 'EndTime': 18446744073709551615, 'Value': '10000'})]})})


.. function::  getTimeLockBalance
    
getTimeLockBalance
&&&&&&&&&&&&&&&&&&

def getTimeLockBalance(self, assetId, account, block_identifier=None):
    """Demonstrate getting timelock information about an asset for a public key
    
    Args:
        assetId (hex str)   Hex string asset idenfifier, |br|
        account (hex str)   Public key, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending' |br|
        
    Returns:
        asset_timelocks (list of dicts)
        
    """
    
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnGetTimelockInfo.py
   :language: python
   :lines: 24-32
   :emphasize-lines: 9
   
   

.. code-block:: python 

    >>>n_items = len(asset_timelocks.Items)
    >>>print('\nNumber of timelocked ', asset_name, ' items = ',n_items,'\n')
    Number of timelocked  FSN  items =  3
    >>>for i in range(n_items):
    print('Asset ',i,'\n')
    tm = asset_timelocks.Items[i].StartTime
    print('Start Time :   ',datetime.fromtimestamp(tm).strftime('%c'))
    tm = asset_timelocks.Items[i].EndTime
    if tm >= web3fsn.BN():
        endtime = 'Infinity'
    else:
        endtime = datetime.fromtimestamp(tm).strftime('%c')
    print('End Time   :   ',endtime)
    val = int(asset_timelocks.Items[i].Value)
    print(web3fsn.fromWei(val,'ether'),' ',asset_name,'\n')
    
    Asset  0 

    Start Time :    Sun Dec 15 13:30:03 2019
    End Time   :    Wed Mar  4 00:00:00 2020
    5000   FSN 

    Asset  1 

    Start Time :    Tue Dec 17 11:38:27 2019
    End Time   :    Wed Mar  4 00:00:00 2020
    5000   FSN 

    Asset  2 

    Start Time :    Tue Dec 17 19:29:48 2019
    End Time   :    Wed Feb 12 00:00:00 2020
    5000   FSN


.. function::  sendToTimeLock
    
    
sendToTimeLock
&&&&&&&&&&&&&&&

def sendToTimeLock(self, transaction):
    """To send asset tokens on the Fusion blockchain to timelock with an unlocked wallet (IPC method)
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """
    

.. function::  sendToRawTimeLock

.. _sendToRawTimeLock: 

sendToRawTimeLock
&&&&&&&&&&&&&&&&&&

def sendToRawTimeLock(self, transaction, prepareOnly=False):
    """To send asset tokens on the Fusion blockchain to timelock using the raw transaction method, 
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """

Here is an example of the function usage without start and end dates (see :ref:`timeLockToRawTimeLock` function below for 
an example using 'start' and 'end'

.. literalinclude:: ../fusion_tests/fsnSendToRawTimeLock.py
   :language: python
   :lines: 40-106


.. function::  assetToTimeLock
    
    
assetToTimeLock
&&&&&&&&&&&&&&&

def assetToTimeLock(self, transaction):
    """To send asset tokens on the Fusion blockchain to timelock with an unlocked wallet (IPC method)
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """
    
    




.. function::  assetToRawTimeLock

.. _assetToRawTimeLock: 

assetToRawTimeLock
&&&&&&&&&&&&&&&&&&

def assetToRawTimeLock(self, transaction, prepareOnly=False):
    """To send asset tokens on the Fusion blockchain to timelock using the raw transaction method, 
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """

Here is an example of the function usage without start and end dates (see :ref:`timeLockToRawTimeLock` function below for 
an example using 'start' and 'end'

.. literalinclude:: ../fusion_tests/fsnToAndFromRawTimeLock.py
   :language: python
   :lines: 40-101
   :emphasize-lines: 27,51


.. function::  timeLockToAsset
   
   
timeLockToAsset
&&&&&&&&&&&&&&&

def timeLockToAsset(self, transaction):
    """To send timelocked asset tokens on the Fusion blockchain to assets with an unlocked wallet (IPC method)
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int)
    Returns:
        TxHash transaction hash (hex str)
        
    """      
    
    
.. function::   timeLockToRawAsset  
   

timeLockToRawAsset
&&&&&&&&&&&&&&&&&&

def timeLockToRawAsset(self, transaction, prepareOnly=False):
    """To send timelocked asset tokens on the Fusion blockchain to assets using the raw transaction method, 
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point. If prepareOnly=True, the return a Tx_dict (dict)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """

    See the example code for :ref:`assetToRawTimeLock` for usage

    
.. function::  timeLockToTimeLock   

timeLockToTimeLock
&&&&&&&&&&&&&&&&&&

def timeLockToTimeLock(self, transaction):
    """To create a new timelock for an existing timelocked asset with an unlocked wallet (IPC method)
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
        
    Returns:
        TxHash transaction hash (hex str)
        
    """
    



.. function::  timeLockToRawTimeLock

.. _timeLockToRawTimeLock:

timeLockToRawTimeLock
&&&&&&&&&&&&&&&&&&&&&

def timeLockToRawTimeLock(self, transaction, prepareOnly=False):
    """To create a new timelock for an existing timelocked asset using the raw transaction method
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':         pub_key_receiver (hex str) **OR**  'toUSAN': usan (int), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """
    
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnTimeLockToRawTimeLock.py
   :language: python
   :lines: 40-157
   :emphasize-lines: 85
   
Output from this code :-


.. code-block:: python 

    >>>
    Number of timelocked  TST1  items =  2 

    Asset  0 

    Start Time :    Wed Nov 20 15:15:26 2019
    End Time   :    Infinity
    3.5   TST1 

    Asset  1 

    Start Time :    Wed Nov 20 15:15:26 2019
    End Time   :    Tue Dec  1 05:59:59 2020
    2.7   TST1 


    Now send the time lock tokens someone else's wallet...
    Check your wallet and hit enter to continue > 
    Transaction hash =  0x6e13854a339778494580d61c7094f4eec579744f9a86042ffcca7cad3c60b53d
    Waiting for transaction to go through...

    Number of timelocked  TST1  items =  2 

    Asset  0 

    Start Time :    Wed Nov 20 15:15:26 2019
    End Time   :    Infinity
    3.3   TST1 

    Asset  1 

    Start Time :    Wed Nov 20 15:15:26 2019
    End Time   :    Tue Dec  1 05:59:59 2020
    2.9   TST1

    
    
    
Swaps
^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.


    
.. function::  getSwap

getSwap
&&&&&&&

def getSwap(self, swapId, block_identifier='latest'):
    """Get the information about one swap
    
    Args:
        swapId (hex str), |br| 
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        swap_dict (dict) information about the swap.
        
        "ID": (hex str), |br|
        "Owner": (hex str) public_key, |br|
        "FromAssetID": (hex str) asset ID, |br|
        "FromStartTime": (int) seconds since epoch, |br|
        "FromEndTime": (int) seconds since epoch, |br|
        "MinFromAmount": (float) tokens*decimals, |br|
        "ToAssetID": (hex str) asset ID, |br|
        "ToStartTime": (int) seconds since epoch, |br|
        "ToEndTime": (int) seconds since epoch, |br|
        "MinToAmount": (float) tokens*decimals, |br|
        "SwapSize": (int), |br|
        "Targes": (list of hex str) list of private addresses, or [] for none, |br|
        "Time": (int) seconds since epoch. Time swap initiated, |br|
        "Description": (str), |br|
        "Notation": (int) USAN
        
    """
    
.. literalinclude:: ../fusion_tests/fsnTakeRawSwap.py
   :language: python
   :lines: 74-82
   :emphasize-lines: 7    
        
    

.. function::  makeSwap
    
makeSwap
&&&&&&&&

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.

def makeSwap(self, transaction):
    """Create a swap on the Quantum Swap Market. You can use this method if you have an unlocked wallet (IPC method)
    
    Args:
        transaction (dict)
        
        'from':                 pub_key_sender (hex str), |br|
        'nonce':                nonce  (int), |br|
        'ToAssetID':            assetId (hex str), |br|
        'ToStartTime':          to_st_time (str) can be 'now', |br|
        'ToEndTime':            to_en_time (str) can be 'infinity', or e.g. '2020-06-01T06:00:00+0400', |br|
        'MinToAmount':          nToSend (str) Minimum No. of tokens*decimals to swap, |br|
        'FromAssetID':          assetId (hex str), |br|
        'FromStartTime':        from_st_time (str) Defaults to 'now' |br|
        'FromEndTime':          from_en_time (str) Defaults to 'infinity' |br|
        'MinFromAmount':        nToReceive (int), Minimum No. tokens to receive * decimals|br|
        'SwapSize':             swap_size (int) swap size, |br|
        'Targes':               target wallets (list),  # Leave as an empty list [] for a public swap.

    
    Returns:
        TxHash transaction hash (hex str)
        
    """

.. function:: makeRawSwap 

makeRawSwap
&&&&&&&&&&&

def makeRawSwap(self, transaction, prepareOnly=False):
    """Create a swap on the Quantum Swap Market. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction (dict) |br|
        
        'from':                 pub_key_sender (hex str), |br|
        'nonce':                nonce  (int), |br|
        'ToAssetID':            assetId (hex str), |br|
        'ToStartTime':          to_st_time (datetime) can be 'now', |br|
        'ToEndTime':            to_en_time (datetime) can be 'infinity', or e.g. '2020-06-01T06:00:00+0400', |br|
        'MinToAmount':          nToSend (int) Minimum No. of tokens*decimals to swap, |br|
        'FromAssetID':          assetId (hex str), |br|
        'FromStartTime':        from_st_time (datetime) Defaults to 'now' |br|
        'FromEndTime':          from_en_time (datetime) Defaults to 'infinity' |br|
        'MinFromAmount':        nToReceive (int), Minimum No. tokens to receive * decimals|br|
        'SwapSize':             swap_size (int) swap size, |br|
        'Targes':               target wallets (list),  # Leave as an empty list [] for a public swap.
        
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
    
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """
    
.. literalinclude:: ../fusion_tests/fsnMakeAndRecallRawSwap.py
   :language: python
   :lines: 39-94
   :emphasize-lines: 45

   
   
.. function:: makeRawMultiSwap 

makeRawMultiSwap
&&&&&&&&&&&&&&&&

def makeRawMultiSwap(self, transaction, prepareOnly=False):
    """Create a multi swap on the Quantum Swap Market. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction (dict) : |br|
        
        'from':                 pub_key_sender (hex str), |br|
        'nonce':                nonce  (int), |br|
        'ToAssetID':            assetId (list of hex str), |br|
        'ToStartTime':          to_st_time (datetime), optional, can be 'now', |br|
        'ToEndTime':            to_en_time (datetime) can be 'infinity', or e.g. '2020-06-01T06:00:00+0400', |br|
        'MinToAmount':          nToSend (list of int) Minimum No. of tokens*decimals to swap, |br|
        'FromAssetID':          assetId (list of hex str), |br|
        'FromStartTime':        from_st_time (list of datetime) Defaults to 'now' |br|
        'FromEndTime':          from_en_time (list of datetime) Defaults to 'infinity' |br|
        'MinFromAmount':        nToReceive (list of int), Minimum No. tokens to receive * decimals|br|
        'SwapSize':             swap_size (int) swap size, |br|
        'Targes':               target wallets (list),  # Leave as an empty list [] for a public swap.
        
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
    
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """
    
   

.. function::  recallSwap
   
recallSwap
&&&&&&&&&&

def recallSwap(self, transaction):
    """ Recall a swap from the Quantum Swap Market. You can use this method if you have an unlocked wallet (IPC method)
    
    Args:
        transaction (dict) |br|
        
        'from':                 pub_key_sender, |br|
        'nonce':                nonce (int), |br|
        'SwapID':               swapId (hex str)
        
    Returns:
        TxHash transaction hash (hex str)
        
    """
    
.. function::  recallRawSwap
    
recallRawSwap
&&&&&&&&&&&&&

def recallRawSwap(self, transaction, prepareOnly=False):
    """ Recall a swap from the Quantum Swap Market. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction (dict)
        
        'from':                 pub_key_sender, |br|
        'nonce':                nonce (int), |br|
        'SwapID':               swapId (hex str)
        
        prepareOnly flag (bool) set to True to defer transaction signing to a later point
    
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """

Example code :-
    
.. literalinclude:: ../fusion_tests/fsnMakeAndRecallRawSwap.py
   :language: python
   :lines: 132-139
   :emphasize-lines: 8

   
.. function::  takeSwap
    
takeSwap
&&&&&&&&

def takeSwap(self, transaction):
    """Take a swap on the Quantum Swap Market.  You can use this method if you have an unlocked wallet (IPC method)
     
    Args:
        transaction (dict) 
        
        'from':             pub_key  (hex str), |br|
        'nonce':            nonce  (int), |br|
        'SwapID':           swapHash  (hex str), |br|
        'Size':             number_to_receive (int)

    Returns:
        TxHash transaction hash (hex str)
        
    """

    
.. function:: takeRawSwap 
   
takeRawSwap
&&&&&&&&&&&

def takeRawSwap(self, transaction, prepareOnly=False):
    """Take a swap on the Quantum Swap Market. You can use this method if you have a locked wallet, with a private key, or password
     
    Args:
        transaction (dict) 
        
        'from':             pub_key  (hex str), |br|
        'nonce':            nonce  (int), |br|
        'SwapID':           swapHash  (hex str), |br|
        'Size':             number_to_receive (int)

        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
    
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, then return a Tx_dict (dict)
        
    """

Example code :-
    
.. literalinclude:: ../fusion_tests/fsnTakeRawSwap.py
   :language: python
   :lines: 37-67
   :emphasize-lines: 28
   


Notation (USAN)
^^^^^^^^^^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.

.. function:: getNotation 

getNotation
&&&&&&&&&&&

def getNotation(self, account, block_identifier=None):
    """Get the USAN for a public key address
    
    Args:
        account (hex str)   Public key, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        usan (int)
        
    """
    
See :ref:`genRawNotation` for an example of usage

.. function::  getLatestNotation

getLatestNotation
&&&&&&&&&&&&&&&&&

def getLatestNotation(self, account, block_identifier=None):
    """Get the last notation on the blockchain
    
    Args:
        account (hex str)   Public key, |br|
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns:
        usan (int)
        
    """

.. function::  getAddressByNotation

getAddressByNotation
&&&&&&&&&&&&&&&&&&&&

def getAddressByNotation(self, notation, block_identifier=None):
    """Get the public key corresponding to a USAN
    
    Args:
        notation (int)  USAN
        block_identifier (int),  'latest', 'earliest', or 'pending'
        
    Returns: 
        pub_key (hex str)
        
    """
    
See :ref:`genRawNotation` for an example of usage
 


.. function:: genRawNotation 

.. _genRawNotation:

genRawNotation
&&&&&&&&&&&&&&

def genRawNotation(self,transaction, prepareOnly=False):
    """Generate a new USAN for an account
    
    Args:
        transaction (dict) :
        
        'from':       pub_key_sender (hex str), |br|
        'nonce':      nonce (int)
        
         prepareOnly flag (bool) set to True to defer transaction signing to a later point.
        
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, then return a Tx_dict (dict)
        
    """

Example code :-
    
.. literalinclude:: ../fusion_tests/fsnGenNotation.py
   :language: python
   :lines: 37-74
   :emphasize-lines: 11

   
Fusion API
^^^^^^^^^^

There is a centralized service generating data about Fusion's blockchain. The output is served via an express server in JSON format. This can provide quick access to important data without having to scan the whole blockchain youself to compile it. It is possible that the format of the output will change with time (or may even cease), but below you can find some functions currently to access various parts of the data in a format useful for application development.


.. function:: fsnprice

fsnprice
&&&&&&&&

def fsnprice(self):
    """Information about the current price, market capitation and circulating supply of the Fusion token
    
        Returns:
            fsnInfo (dict)
            
    """

.. function::  getAllSwaps

getAllSwaps
&&&&&&&&&&&

def getAllSwaps(self, pageNo):
    """Get information on all current swaps from fsnapi
    
    Args:
        PageNo (int)  The data is served with 100 records per page, starting at page 0. Simply increment until the list is exhausted and the length of the output is less than 100.
        
    Returns:
        swap_dict (dict) with fields :-
        
        'swapID'   (hex str) Can be used for taking swaps etc. |br|
        'timeStamp' (str) date and time swap appears on chain |br|
        'fromAddress' (hex str)  public pub_key |br|
        'fromAsset' (hex str)  assetId |br|
        'toAsset'   (hex str)  assetId |br|
        'recCreated' (str)  date and time |br|
        'height'  (int)  block height swap recCreated |br|
        'hash'   (hex str)  transaction hash for swap creation |br|
        'size'  (int) Total swap size |br|
        'Description' (str) |br|
        'FromStartTime' (str) start of swap timelock |br|
        'ToEndTime'  (str) end of swap timelock |br|
        'MinFromAmount'(int) minimum amount for the swap - from |br|
        'MinToAmount' (int) minumum amount for the swap - to |br|
        'SwapSize' (int) |br|
        'Targes' (list) Target wallets for private swaps |br|
        'Time' (str) date and time swap created |br|
        'ToAssetID' (hex str) to assetId |br|
        
    """
    
    Example code
    
.. literalinclude:: ../fusion_tests/fsnGetAllSwaps.py
   :language: python
   :lines: 28-45
   :emphasize-lines: 4
   
Output from this code :-

.. code-block:: python 

    >>>
    No. swaps =  30 

    swapID 0x5a6cb08db87f0519471dcc9fb34a0a3e2163d6e1567db0c140f13e9dbeea51eb
    timeStamp 2019-11-20 19:29:32+00:00
    fromAddress 0x048c6f41542e55dd22a9a37b04b8122fa1ce1006
    fromAsset FSN
    toAsset FSN
    recCreated 2019-11-20T19:29:53.000Z
    height 947735
    hash 0x8d3ba97b26a633d0e401ebb48546be109901100644144853bbcbaafe4b6020b9
    size 10
    Description 
    FromStartTime 1970-01-01 00:00:00+00:00
    ToEndTime 2019-12-30 00:00:00+00:00
    MinFromAmount 29100000000000000000
    MinToAmount 2500000000000000000000
    SwapSize 10
    Targes []
    Time 2019-11-20 19:29:19+00:00
    ToAssetID 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    
    swapID 0x9bd0e524e4eef8c9585b43a6c7f6c293428212f8f1900c68dc33780dbe584958
    timeStamp 2019-11-19 20:40:10+00:00
    fromAddress 0x24714cc6408cf123979e37e03ed9dbcc84666620
    fromAsset FSN
    toAsset FSN
    recCreated 2019-11-19T20:40:26.000Z
    height 941439
    hash 0x7428e50f375dcac87f661583f5e8c97dcb9c4e4adc90dc865fc748d4839aaf08
    size 1
    Description 
    FromStartTime 1970-01-01 00:00:00+00:00
    ToEndTime 2019-11-30 00:00:00+00:00
    MinFromAmount 25000000000000000000
    MinToAmount 5000000000000000000000
    SwapSize 1
    Targes []
    Time 2019-11-19 20:39:57+00:00
    ToAssetID 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    
    swapID 0x2a79788a33f87b5a78de7805f6f8c361be47d16f9808b9fbc7f7fd7bf33644e6
    timeStamp 2019-11-19 20:35:37+00:00
    fromAddress 0x24714cc6408cf123979e37e03ed9dbcc84666620
    fromAsset FSN
    toAsset FSN
    recCreated 2019-11-19T20:35:58.000Z
    height 941418
    hash 0x28740d793691c805c3611d813bcd48196853fed27aebb7fb230e5d0695ec4ce1
    size 1
    Description 
    FromStartTime 1970-01-01 00:00:00+00:00
    ToEndTime 2019-12-31 00:00:00+00:00
    MinFromAmount 50000000000000000000
    MinToAmount 5000000000000000000000
    SwapSize 1
    Targes []
    Time 2019-11-19 20:35:11+00:00
    ToAssetID 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    
    etc.


.. function::  assetNameToAssetInfo

.. _assetNameToAssetInfo:

assetNameToAssetInfo
&&&&&&&&&&&&&&&&&&&&

def assetNameToAssetInfo(self, asset_name):
    """ Retrieve information about a given verified asset name
    The asset *must be* 'enabled' and 'whiteListEnabled' in the fsnapi
    
    Args:
        asset_name (str)   Short string asset idenfifier
        
    Returns:
        assetInfo (dict)
        
    """
    
 Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnAssetNameToAssetInfo.py
   :language: python
   :lines: 7-24
   :emphasize-lines: 15
   
.. code-block:: python 

    >>>assetInfo
    {'assetID': '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
    'recCreated': '2019-07-09T06:40:19.000Z',
    'recEdited': '2019-07-09T06:40:19.000Z',
    'assetAuthority': '0xcf62374bc2b4e195ca7f2aecbe0076d9d4f89d1e',
    'name': 'Fusion',
    'shortName': 'FSN',
    'image': 'EFSN_LIGHT.svg',
    'erc20': 1, 
    'ethereum': 1, 
    'address': '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 
    'disabled': 0, 
    'whiteListEnabled': 1, 
    'bitcoin': 0, 
    'decimals': 18, 
    'lockInDisabled': 1, 
    'reservedID': 1, 
    'totalFusionSupply': '0', 
    'msgSignedWithAssetAuthority': 'Signed:Fusion:0xfffffffffffffffffffffffffffffffffffffff
    fffffffffffffffffffffffff:0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff:FSN', 
    'msgSignature':'0xf92792db22d1bb53c5c2bd8ccbdbfc1745c15fba35c1c0fb65d066f6dd03db937f5257
    ec5244d04ce5584eb59029d11d453b9cf92057ecc194ce2d4f12bd97'
    }


.. function::  assetIdToAssetInfo
    
assetIdToAssetInfo
&&&&&&&&&&&&&&&&&&&&

def assetIdToAssetInfo(self, assetId):
    """ Retrieve inforamtion about a given verified asset name
    The asset must be 'enabled' and 'whiteListEnabled' in the fsnapi
    
    Args:
        assetId (hex str)   Hex string asset idenfifier
        
    Returns:
        assetInfo (dict)   See :ref:`assetNameToAssetInfo` for typical output
        
    """

.. function::  getAssetId

getAssetId
&&&&&&&&&&

def getAssetId(self, asset_name):
    """ Retrieve the hexadecimal assetId for a given verified asset name
    The asset *must be* 'enabled' and 'whiteListEnabled' in the fsnapi
    
    Args:
        asset_name (str)   Short string asset idenfifier
        
    Returns:
        assetId (hex str)  
        
        or None if not found or not enabled/whiteListEnabled

    """
        
Here is an example of the function usage

.. literalinclude:: ../fusion_tests/fsnGetAsset.py
   :language: python
   :lines: 16-30
   :emphasize-lines: 8
   

.. function::  getAssetDecimals
   

getAssetDecimals
&&&&&&&&&&&&&&&&

def getAssetId(self, asset_name):
    """ Retrieve the decimals for a given verified asset name
    The asset must be **enabled** and **whiteListEnabled** 
    
    Args:
        asset_name (str)   Short string asset idenfifier
        
    Returns:
        decimals (int)  
        
        or None if not found or not enabled/whiteListEnabled

    """
    
    
.. function:: fsnapiVerifiedAssetInfo

fsnapiVerifiedAssetInfo
&&&&&&&&&&&&&&&&&&&&&&&

def fsnapiVerifiedAssetInfo(self):
    """Get a list of the shortnames of all assets that are **whitelisted** and **verified**
    
    Args:
        None
        
    Returns:
        verifiedAssets (list)   e.g. ['BTC','ETH','FSN',...]
        
    """
    
.. function:: fsnapi_swaps_pubkey

fsnapi_swaps_pubkey
&&&&&&&&&&&&&&&&&&&

def fsnapi_swaps_pubkey(self, account, pageNo):
    """Output a list of all swaps have been generated by a public pub_key
    
    Args:
        account (hex string)  public key, |br|
        PageNo (int)  The data is served with 100 records per page, starting at page 0. Simply increment until the list is exhausted and the length of the output is less than 100.
        
    Returns:
        swap_dict (dict) 
        
    """
    
    
.. function:: fsnapi_swaps_target

fsnapi_swaps_target
&&&&&&&&&&&&&&&&&&&

def fsnapi_swaps_target(self, account, pageNo):
    """Output a list of all swaps have been targetted at a public pub_key
    
    Args:
        account (hex string)  public key, |br|
        PageNo (int)  The data is served with 100 records per page, starting at page 0. Simply increment until the list is exhausted and the length of the output is less than 100.
        
    Returns:
        swap_dict (dict) 
        
    """
    
.. function:: transactionNoTicketsDesc

transactionNoTicketsDesc
&&&&&&&&&&&&&&&&&&&&&&&&

def transactionNoTicketsDesc(self, pageNo):
    """Output transactions from the blockchain with the most recent first and ignoring ticket purchase transactions
    
    Args:
        PageNo (int)  The data is served with 100 records per page, starting at page 0. Simply increment until the list is exhausted and the length of the output is less than 100.
        
    Returns:
        Txs (dict)
        
    """
    
.. function:: takeSwapsDesc

takeSwapsDesc
&&&&&&&&&&&&&

def takeSwapsDesc(self, pageNo):
    """Output a list of all takeSwap transactions, wiht the most recent first
    
    Args:
        PageNo (int)  The data is served with 100 records per page, starting at page 0. Simply increment until the list is exhausted and the length of the output is less than 100.
        
    Returns:
        swaps (dict)
        
    """
    
   
   
Miscellaneous
^^^^^^^^^^^^^


    
.. function:: numToDatetime

numToDatetime
&&&&&&&&&&&&&
    
def numToDatetime(self, tdelta):
    """Converts the simple integer number of seconds since 1970/01/01:0000 UTC to a timezone enabled python DateTime object
    
    Args:
        tdelta (int), |br|
        
    Returns:
        dateTime (DateTime object)
        
    """
    
.. function:: datetimeToHex

datetimeToHex
&&&&&&&&&&&&&

def datetimeToHex(self, dateTime):
    """Converts a python timezone enabled DateTime object to a hex string representing the number of seconds since 1970/01/01:0000 UTC
    
    Args:
        dateTime (DateTime object)
        
    Returns:
        dtHex (hex string)
        
    """
    
.. function:: datetimeToInt

datetimeToInt
&&&&&&&&&&&&&

def datetimeToInt(self, dateTime):
    """Converts a python timezone enabled DateTime object to an int representing the number of seconds since 1970/01/01:0000 UTC
    
    Args:
        dateTime (DateTime object)
        
    Returns:
        dt (int)
        
    """
    
.. function:: hex2a

hex2a
&&&&&

def hex2a(self, datastr):
    """Decodes the 'data' string in a Fusion blockchain transaction to reveal the 'to' hexadecimal address of the recipient
    
    Args:
        datastr  (string)
        
    Returns:
        pub_key  (20 char hex string)
        
    """
    
    

   
   





           

   

   
   
   
