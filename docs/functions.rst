
.. |br| raw:: html

    <br>

Functions in the *Fsn* Class
============================

*Fsn* extends *web3.eth*

There are many functions that can be used via the *Fsn* class that are not described here, but are available from the *web3.eth* base class. These include functions to handle smart contracts. Please consult the web3.py documentation for their description and usage.

The functions in *Fsn* are split up into categories below.


Tickets
^^^^^^^


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
    
    
.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnBuyTicket.py
   :language: python
   :lines: 41-65
   :emphasize-lines: 12
   
   
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnAllTickets.py
   :language: python
   :lines: 16-36
   :emphasize-lines: 5
   

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


    
totalNumberOfTickets
&&&&&&&&&&&&&&&&&&&&

def totalNumberOfTickets(self, block_identifier=None):
    """ Get the total number of tickets at a block height
    
    Args:   
        block_identifier (int),  'latest', 'earliest', or 'pending'
    
    Returns:
        totalNoTickets (int)
        
   
   
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnTicketsByAddress.py
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

        
isAutoBuyTicket
&&&&&&&&&&&&&&&

def isAutoBuyTicket(self):
    """Check to see if tickets are automatically bought for this account (if sufficient balance exists)
    
    Args:
        None
        
    Returns:
        isAuto (bool)
        
    """
    
    
startAutoBuyTicket
&&&&&&&&&&&&&&&&&&

def startAutoBuyTicket(self):
    """Start to auto buy tickets for your account
    
    Args:
        None
        
    Returns:
        None
        
    """
    
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


getTransaction
&&&&&&&&&&&&&&

def getTransaction(self, TxHash):
    """
    
    Args:
        TxHash (hex str) Transaction hash
        
    """
    
Example of usage :-

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnSendRawFSN.py
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnSendRawFSN.py
   :language: python
   :lines: 42-66
   :emphasize-lines: 17
   

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


waitForTransactionReceipt
&&&&&&&&&&&&&&&&&&&&&&&&&

def waitForTransactionReceipt(self, TxHash, timeout):
    """Check to see that a transaction occured on the blockchain
    
    Args:
        TxHash (hex str) the transaction hash
        
        timeout (int) Optional timeout in seconds to block program execution and wait for waitForTransactionReceipt
        
    """
    
See :ref:`sendRawTransaction` for an example of usage    


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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnGetAsset.py
   :language: python
   :lines: 16-30
   :emphasize-lines: 8
   
   

getAssetDecimals
&&&&&&&&&&&&&&&&

def getAssetId(self, asset_name):
    """ Retrieve the decimals for a given verified asset name
    The asset *must be* 'enabled' and 'whiteListEnabled' in the fsnapi
    
    Args:
        asset_name (str)   Short string asset idenfifier
        
    Returns:
        decimals (int)  
        
        or None if not found or not enabled/whiteListEnabled

    """

.. _assetNameToAssetInfo:
    
assetNameToAssetInfo
&&&&&&&&&&&&&&&&&&&&

def assetNameToAssetInfo(self, asset_name):
    """ Retrieve inforamtion about a given verified asset name
    The asset *must be* 'enabled' and 'whiteListEnabled' in the fsnapi
    
    Args:
        asset_name (str)   Short string asset idenfifier
        
    Returns:
        assetInfo (dict)
        
    """
    
 Here is an example of the function usage

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnAssetNameToAssetInfo.py
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnGetAsset.py
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnCreateRawAsset.py
   :language: python
   :lines: 37-56
   :emphasize-lines: 16
   

   
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnInc_and_DecRawAsset.py
   :language: python
   :lines: 38-63
   :emphasize-lines: 22

   

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

    
sendAsset
&&&&&&&&&

def sendAsset(self, transaction):
    """Send an asset to another wallet.  You can use this method if you have an unlocked wallet (IPC method).
    
    Args:
        transaction :
        
        'from':       pub_key_sender (hex str), |br|
        'to':         pub_key_receiver (hex str), |br|
        'nonce':      nonce (int), |br|
        'asset':      asset_Id (hex str), |br|
        'value':      val (int) Number of the asset to send * decimals
        
    Returns:
        TxHash transaction hash (hex str)
        
    """

    
sendRawAsset
&&&&&&&&&&&&

def sendRawAsset(self, transaction, prepareOnly=False):
    """Send an asset to another wallet. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction :
        
        'from':       pub_key_sender (hex str), |br|
        'to':         pub_key_receiver (hex str), |br|
        'nonce':      nonce (int), |br|
        'asset':      asset_Id (hex str), |br|
        'value':      val (int) Number of the asset to send * decimals
        
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
            
    Returns:
        TxHash transaction hash (hex str).  If prepareOnly=True, the return a Tx_dict (dict)
        
    """

    Here is an example of the function usage

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnSendRawAsset.py
   :language: python
   :lines: 39-63
   :emphasize-lines: 21
   
    
    
    

Timelocks
^^^^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.

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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnGetAllTimelockInfo.py
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnGetTimelockInfo.py
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


    
    
assetToTimeLock
&&&&&&&&&&&&&&&

def assetToTimeLock(self, transaction):
    """To send asset tokens on the Fusion blockchain to timelock with an unlocked wallet (IPC method)
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """
    
    

.. _assetToRawTimeLock: 

assetToRawTimeLock
&&&&&&&&&&&&&&&&&&

def assetToRawTimeLock(self, transaction, prepareOnly=False):
    """To send asset tokens on the Fusion blockchain to timelock using the raw transaction method, 
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnToAndFromRawTimeLock.py
   :language: python
   :lines: 40-101
   :emphasize-lines: 27,51

   
timeLockToAsset
&&&&&&&&&&&&&&&

def timeLockToAsset(self, transaction):
    """To send timelocked asset tokens on the Fusion blockchain to assets with an unlocked wallet (IPC method)
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int)
    Returns:
        TxHash transaction hash (hex str)
        
    """      
    
   
   

timeLockToRawAsset
&&&&&&&&&&&&&&&&&&

def timeLockToRawAsset(self, transaction, prepareOnly=False):
    """To send timelocked asset tokens on the Fusion blockchain to assets using the raw transaction method, 
    without changing the time lock.
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int)
            
        prepareOnly flag (bool) set to True to defer transaction signing to a later point. If prepareOnly=True, the return a Tx_dict (dict)
            
    Returns:
        TxHash transaction hash (hex str)
        
    """

    See the example code for :ref:`assetToRawTimeLock` for usage

    
    

timeLockToTimeLock
&&&&&&&&&&&&&&&&&&

def timeLockToTimeLock(self, transaction):
    """To create a new timelock for an existing timelocked asset with an unlocked wallet (IPC method)
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
            'nonce':    nonce (int), |br|
            'asset':    asset_Id (hex str), |br|
            'value':    nToSend (int), |br|
            'start':    startdate (date str - Optional), |br|
            'end':      enddate (date str - Optional)
        
    Returns:
        TxHash transaction hash (hex str)
        
    """
    

.. _timeLockToRawTimeLock:
    
timeLockToRawTimeLock
&&&&&&&&&&&&&&&&&&&&&

def timeLockToRawTimeLock(self, transaction, prepareOnly=False):
    """To create a new timelock for an existing timelocked asset using the raw transaction method
    
    Args:
        transaction (dict):
            'from':     pub_key_sender (hex str), |br|
            'to':       pub_key_receiver (hex str), |br|
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

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnTimeLockToRawTimeLock.py
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

getAllSwaps
&&&&&&&&&&&

def getAllSwaps(self):
    """Get information on all current swaps from fsnapi
    
    Args:
        None
        
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
    
.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnGetAllSwaps.py
   :language: python
   :lines: 28-45
   :emphasize-lines: 3
   
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
    

makeRawSwap
&&&&&&&&&&&

def makeRawSwap(self, transaction, prepareOnly=False):
    """Create a swap on the Quantum Swap Market. You can use this method if you have a locked wallet, with a private key, or password
    
    Args:
        transaction (dict) |br|
        
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
        
        prepareOnly flag (bool) set to True to defer transaction signing to a later point.
    
    Returns:
        TxHash transaction hash (hex str). If prepareOnly=True, the return a Tx_dict (dict)
        
    """
    
.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnMakeAndRecallRawSwap.py
   :language: python
   :lines: 39-94
   :emphasize-lines: 45
   
   
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
    
.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnMakeAndRecallRawSwap.py
   :language: python
   :lines: 132-139
   :emphasize-lines: 8

    
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
    
.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnTakeRawSwap.py
   :language: python
   :lines: 40-60
   :emphasize-lines: 20
   


Notation (USAN)
^^^^^^^^^^^^^^^

For all write transactions, you may optionally specify the 'gas' and/or the 'gasLimit'. You may set 'gas': 'default' to use the hardcoded value in the class definition.

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
    
.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnGenNotation.py
   :language: python
   :lines: 37-74
   :emphasize-lines: 11

   
   





           

   

   
   
   
