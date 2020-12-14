
import web3

import sys

from eth_account import (
    Account,
) 

from web3.middleware import (
    construct_sign_and_send_raw_middleware,
)

from eth_utils import (
    add_0x_prefix,
    apply_to_return_value,
    from_wei,    
    is_address,
    is_checksum_address,
    keccak as eth_utils_keccak,
    remove_0x_prefix,
    to_checksum_address,
    to_wei,
    to_int,
    to_hex,
    is_string,
)

from web3._utils.formatters import (
    hex_to_integer,
)

from eth_utils.curried import (
    is_address,
    is_bytes,
    is_integer,
    is_null,
    is_string,
    remove_0x_prefix,
    text_if_str,
    apply_formatter_if,
)
from eth_utils.toolz import (
    assoc,
    merge,
)

from eth_keys import (
    KeyAPI,
    keys,
)

import json

from hexbytes import (
    HexBytes,
)

from web3.datastructures import (
    AttributeDict,
)

from web3.manager import (
    RequestManager as DefaultRequestManager,
)

from web3._utils.module import (
    attach_modules,
)
from web3.net import (
    Net,
)
from web3.parity import (
    Parity,
    ParityPersonal,
    ParityShh,
)
from web3.geth import (
    Geth,
    GethAdmin,
    GethMiner,
    GethPersonal,
    GethShh,
    GethTxPool,
)

from web3._utils.blocks import (
    select_method_for_block_identifier,
)
from web3._utils.empty import (
    empty,
)
from web3._utils.request import (
    make_post_request,
)
from web3._utils.encoding import (
    hex_encode_abi_type,
    to_bytes,
    to_hex,
    to_json,
)
from web3._utils.threads import (
    Timeout,
)


from web3fsnpy.fusion.exceptions import (
    NotRawTransaction,
    _notConnected,
    BadSendingAddress,
    PrivateKeyNotSet,
)

from web3fsnpy.fusion.fsn_transactions import (
    fill_transaction_defaults,
    SignTx,
    buildGenNotationTx,
)

from web3fsnpy.fusion.fsn_assets import (
    buildGenAssetTx,
    buildSendAssetTx,
    buildIncAssetTx,
    buildDecAssetTx,
)

from web3fsnpy.fusion.fsn_timelocks import (
    buildAssetToTimeLockTx,
    buildTimeLockToAssetTx,
    buildTimeLockToTimeLockTx,
    buildSendToTimeLockTx,
)

from web3fsnpy.fusion.fsn_swaps import (
    buildMakeSwapTx,
    buildMakeMultiSwapTx,
    buildRecallSwapTx,
    buildTakeSwapTx,
)

from web3fsnpy.fusion.fsn_tickets import (
    buildBuyTicketTx,
)

from web3fsnpy.fusion.fsn_utils import (
    get_default_modules,
    is_named_block,
    is_hexstr,
    block_number_formatter,
    to_boolean,
    hex2a,
)

from web3fsnpy.fusion.fsn_timelocks import (
    numToDatetime,
    datetimeToHex
)


from web3fsnpy.fusion.fsn_api import (
    fsnapi,
)

from web3 import Web3
import web3.eth

class Fsn(web3.eth.Eth):
    
   
    RequestManager = DefaultRequestManager

    # Encoding and Decoding
    toBytes = staticmethod(to_bytes)
    #toInt = staticmethod(to_int)
    toHex = staticmethod(to_hex)
    #toText = staticmethod(to_text)
    toJSON = staticmethod(to_json)

    # Currency Utility
    toWei = staticmethod(to_wei)
    fromWei = staticmethod(from_wei)

    # Address Utility
    isAddress = staticmethod(is_address)
    isChecksumAddress = staticmethod(is_checksum_address)
    toChecksumAddress = staticmethod(to_checksum_address)
    
    
    provider = None
    
    acct = None            # This is the Fusion account.
    
    api = None             # This is Fusion's api


    def __init__(self, linkToChain):
        
        
        gotprivatekey = False

        for key, val in linkToChain.items():
            if key == 'network':
                if val not in ['testnet','mainnet']:
                    raise TypeError('Error in linkToChain dictionary: Found ',val, 'but network must be one of testnet, or mainnet')
            elif key == 'provider':
                if val not in ['WebSocket', 'HTTP', 'IPC']:
                    raise TypeError('Error in linkToChain dictionary: Found ',val, 'but provider must be one of WebSocket, HTTP, or IPC')
            elif key == 'gateway':
                pass          # Can be 'default'
            elif key == 'private_key':
                if is_string(val) and len(val) > 0:
                    private_key = val
                    if private_key[0:1] == '0x':
                        private_key = remove_0x_prefix(private_key)
                    gotprivatekey = True
                    self.acct = Account.from_key(private_key)
            else:
                raise TypeError('Error in linkToChain dictionary: Illegal key ',key )
            
        
        
            
        if linkToChain['network'] == 'testnet':
            self.__defaultChainId = 46688
        elif linkToChain['network'] == 'mainnet':
            self.__defaultChainId = 32659
        else:
            raise ValueError(
                'Error: You must specify a network (\'testnet\' or \'mainnet\')'
            )
            
            
        if linkToChain['gateway'] == 'default':
            if linkToChain['network'] == 'testnet':
                if linkToChain['provider'] == 'WebSocket':
                    linkToChain['gateway'] = 'wss://testnetpublicgateway1.fusionnetwork.io:10001'
                elif linkToChain['provider'] == 'HTTP':
                    linkToChain['gateway'] = 'https://testnetpublicgateway1.fusionnetwork.io:10000/'
                elif linkToChain['provider'] == 'IPC':
                    raise TypeError('Error: Cannot specify a default gateway for IPC')
            elif linkToChain['network'] == 'mainnet':
                if linkToChain['provider'] == 'WebSocket':
                    linkToChain['gateway'] = 'wss://mainnetpublicgateway1.fusionnetwork.io:10001'
                elif linkToChain['provider'] == 'HTTP':
                    linkToChain['gateway'] = 'https://mainnetpublicgateway1.fusionnetwork.io:10000/'
                elif linkToChain['provider'] == 'IPC':
                    linkToChain['gateway'] = '/home/root/fusion-node/data/efsn.ipc'
        

        print('Connecting to : ',linkToChain['network'],linkToChain['gateway'], ' with the ',linkToChain['provider'], ' method')
        
        if linkToChain['provider'] == 'WebSocket':
            self.manager = self.RequestManager(Web3.WebsocketProvider(linkToChain['gateway']))
            self.web3 = Web3(Web3.WebsocketProvider(linkToChain['gateway']))
        elif linkToChain['provider'] == 'HTTP':
            self.manager = self.RequestManager(Web3.HTTPProvider(linkToChain['gateway']))
            self.web3 = Web3(Web3.HTTPProvider(linkToChain['gateway']))
        elif linkToChain['provider'] == 'IPC':
            self.manager = self.RequestManager(Web3.IPCProvider(linkToChain['gateway']))
            self.web3 = Web3(Web3.IPCProvider(linkToChain['gateway']))
        else:
            raise ValueError(
                'Error: You must specify a provider'
            )
        
        self.gateway = linkToChain['gateway']
            
        modules = get_default_modules()
        attach_modules(self, modules)
        
        self.defaultAccount = None      
        
        if gotprivatekey:
            #print('Adding account to list')
            self.addAccount()

  
  
        # Connect to the fusion api 
        
        self.api = fsnapi(self.defaultAccount, linkToChain['network'])
            
        
        
        self.consts = {
            "TimeForever":       0xffffffffffffffff, 
            "TimeForeverStr":   "0xffffffffffffffff",

            "OwnerUSANAssetID": "0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe",
    
            "TicketLogAddress": "0xfffffffffffffffffffffffffffffffffffffffe",
            "TicketLogAddress_Topic_To_Function": {
                "0": "ticketSelected",
                "1": "ticketReturn",
                "2": "ticketExpired"
            },

            "TicketLogAddress_Topic_ticketSelected": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "TicketLogAddress_Topic_ticketReturn":   "0x0000000000000000000000000000000000000000000000000000000000000001",
            "TicketLogAddress_Topic_ticketExpired":  "0x0000000000000000000000000000000000000000000000000000000000000002",

            "FSNCallAddress":                        "0xffffffffffffffffffffffffffffffffffffffff",
            
            "EMPTY_HASH":                            "0x0000000000000000000000000000000000000000000000000000000000000000",
            
            "BN":                                    int('0xffffffffffffffff',16)  # 18446744073709551615, used in time locks to signify infinity
        }
            
        self.tokens = {
            "FSNToken":         "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "FSN":         "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        }
        
        self.burn = '0xffffffffffffffffffffffffffffffffffffffff'

        self.__defaultSendTransactionGasPrice       = 0.000000021          # Default gasPrice in FSN for sendTransaction
        self.__defaultGenAssetGasPrice              = 0.00009              # Default gasPrice in FSN for genAsset
        self.__defaultSendAssetGasPrice             = 0.00005              # Default gasPrice in FSN for sendAsset
        self.__defaultSendTimeLockGasPrice          = 0.00005              # Default gasPrice in FSN for sendAsset
        self.__defaultIncDecAssetGasPrice           = 0.00003              # Default gasPrice in FSN for incAsset, or decAsset
        self.__defaultGenNotationGasPrice           = 0.00005              # Default gasPrice in FSN for genNotation
        self.__defaultAssetToTimeLockGasPrice       = 0.00003              # Default gasPrice in FSN for assetToTimeLock
        self.__defaultTimeLockToAssetGasPrice       = 0.00003              # Default gasPrice in FSN for TimeLockToAsset
        self.__defaultTimeLockToTimeLockGasPrice    = 0.00005              # Default gasPrice in FSN for TimeLockToTimeLock
        self.__defaultMakeSwapGasPrice              = 0.00006              # Default gasPrice in FSN for makeSwap
        self.__defaultRecallSwapGasPrice            = 0.00005              # Default gasPrice in FSN for recallSwap
        self.__defaultTakeSwapGasPrice              = 0.00003              # Default gasPrice in FSN for takeSwap
        self.__defaultBuyTicketGasPrice             = 0.00003              # Default gasPrice in FSN for buyTicket
        
        


    @property
    def chainId(self):
    #    return self.web3.manager.request_blocking("eth_chainId", [])
        return self.__defaultChainId
        
    def BN(self):
        return self.consts['BN']

    #def fill_tx_defaults(self, transaction):
        #return fill_transaction_defaults(transaction,self.__defaultChainId)
    
    def isConnected(self):
        try:
            self.blockNumber
            return True
        except(_notConnected):
            return False
     
    def addAccount(self):
        #self.web3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.acct))
        self.defaultAccount = self.acct.address

    def getBalance(self, account, assetId, block_identifier=None):
        if is_integer(account):
            account = self.getAddressByNotation(account)
        if not is_address(account):
            raise TypeError(
                'The account {} does not have a valid address format. Should be a 20 character hex address'.format(account)
            )
        if not is_hexstr(assetId):
            raise TypeError(
                'assetId must be a hex string'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
        
        return int(self.web3.manager.request_blocking(
            "fsn_getBalance",
            [assetId, account, block_identifier],
        ))
    
    
    def signAndTransmit(self, Tx_dict):
        
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        
        if 'r' in Tx_dict and 's' in Tx_dict:
            if hex_to_integer(Tx_dict['r']) == 0 and hex_to_integer(Tx_dict['s']) == 0:
                #print('before SignTx = : ',Tx_dict)
                Tx_signed = SignTx(Tx_dict, self.acct) 
                #print('\n\nTx_signed = : ',Tx_signed)
            
                TxHash =  self.web3.manager.request_blocking(
                    "fsntx_sendRawTransaction",
                    [Tx_signed],
                )
        else:
            Tx_signed = self.acct.sign_transaction(Tx_dict)
            TxHash =  self.web3.manager.request_blocking(
                "eth_sendRawTransaction",
                [Tx_signed.rawTransaction],
            )
            
        if is_bytes(TxHash):
            return to_hex(TxHash)
        else:
            return TxHash


    def allInfoByAddress(self, account, block_identifier=None):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        account_dict =  self.web3.manager.request_blocking(
            "fsn_allInfoByAddress",
            [account, block_identifier],
        )
        return account_dict
                


    def allTickets(self, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
            
        result = self.web3.manager.request_blocking(
            "fsn_allTickets",
            [block_identifier],
        )
        return result


    def ticketsByAddress(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "fsn_allTicketsByAddress",
            [account, block_identifier],
        )

    def totalNumberOfTickets(self, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "fsn_totalNumberOfTickets",
            [block_identifier],
        )

    def totalNumberOfTicketsByAddress(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "fsn_totalNumberOfTicketsByAddress",
            [account, block_identifier],
        )

    def ticketPrice(self, block_identifier='latest'):
        
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
        
        return int(self.web3.manager.request_blocking(
            "fsn_ticketPrice",
            [block_identifier],
        ))


    def getStakeInfo(self, block_identifier='latest'):
        
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
        
        return self.web3.manager.request_blocking(
            "fsn_getStakeInfo",
            [block_identifier],
        )


    def getBlockReward(self, block_identifier='latest'):
        
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
        
        return int(self.web3.manager.request_blocking(
            "fsn_getBlockReward",
            [block_identifier],
        ))

  
    
    def buyRawTicket(self, transaction, prepareOnly=False):
        
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the buyRawTicket method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultBuyTicketGasPrice, 'ether'))    #  Fusion gas price for GenAsset
        
        Tx =  buildBuyTicketTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildBuyTicketTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
        
     
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def buyTicket(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the buyTicket method'
            )
        
        
        Tx =  buildBuyTicketTx(transaction, self.__defaultChainId)
      
        #print('\n',Tx,'\n')

        TxHash = self.web3.manager.request_blocking(
            "fsntx_buyTicket", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_buyTicket",Tx)
        #print(json_rpc)
        return TxHash

   
   
   
    def sendTransaction(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict of a transaction'
            )
        
        return self.web3.manager.request_blocking(
            "eth_sendTransaction",
            [transaction],
        )
    
   

    def sendRawTransaction(self,transaction, prepareOnly=False):
        
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the sendRawTransaction method'
            )
        
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultSendTransactionGasPrice, 'ether'))    #  Fusion gas price for Transaction
            

        transaction = fill_transaction_defaults(web3,transaction, self.__defaultChainId)
        
        
     
        if prepareOnly == True:
            return transaction
        else:
            Tx_signed = self.acct.sign_transaction(transaction)
            #print(Tx_signed)
            TxHash =  self.web3.manager.request_blocking(
                "eth_sendRawTransaction",
                [Tx_signed.rawTransaction],
            )
            return TxHash
       
    
    def getTransactionAndReceipt(self, TxHash):
        if not is_string(TxHash):
            raise TypeError(
            'In getTransactionAndReceipt, the variable TxHash must be a hex string'   
            )
        
        Tx_dict = self.web3.manager.request_blocking(
            "fsn_getTransactionAndReceipt", 
            [TxHash]
        )
        return dict(Tx_dict)
    


    def createRawAsset(self, transaction, prepareOnly=False):
        
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the createRawAsset method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultGenAssetGasPrice, 'ether'))    #  Fusion gas price for GenAsset
        
        Tx =  buildGenAssetTx(transaction, self.__defaultChainId)
        Txnew =  self.web3.manager.request_blocking(
            "fsntx_buildGenAssetTx",
            [Tx],
        )
        Tx_dict = dict(Txnew)
        
        #print('Tx = ',Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
     
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)
     
 
 
    def createAsset(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the createAsset method'
            )
        
        
        Txnew =  buildGenAssetTx(transaction, self.__defaultChainId)
        
        Tx_dict = dict(Txnew)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
      

        TxHash = self.web3.manager.request_blocking(
            "fsntx_genAsset", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_genAsset",Tx)
        #print(json_rpc)
        return TxHash



    def incRawAsset(self, transaction, prepareOnly=False):
        
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the incRawAsset method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultIncDecAssetGasPrice, 'ether'))    #  Fusion gas price for incAsset
        
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildIncAssetTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
        
        
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)
 
    
    
    def incAsset(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the incAsset method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultIncDecAssetGasPrice, 'ether'))    #  Fusion gas price for incAsset
        
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
      
        print('\n',Tx,'\n')

        TxHash = self.web3.manager.request_blocking(
            "fsntx_incAsset", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_incAsset",Tx)
        #print(json_rpc)
        return TxHash
  

  
    def decAsset(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the decAsset method'
            )
        
        
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
      
        print('\n',Tx,'\n')

        TxHash = self.web3.manager.request_blocking(
            "fsntx_decAsset", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_decAsset",Tx)
        #print(json_rpc)
        return TxHash
 
 
    def decRawAsset(self, transaction, prepareOnly=False):
        
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the decRawAsset method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultIncDecAssetGasPrice, 'ether'))    #  Fusion gas price for decAsset
        
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildDecAssetTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
        
     
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)

 

    def sendAsset(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the sendAsset method'
            )
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        
        Tx =  buildSendAssetTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_sendAsset",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_sendAsset",
            [Tx],
        )
        return TxHash



    def sendRawAsset(self, transaction, prepareOnly=False):
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the sendAsset method'
            )
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultSendAssetGasPrice, 'ether'))    #  Fusion gas price for SendAsset
        
        Tx = buildSendAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildSendAssetTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)


    def sendTimeLock(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the assetToTimeLock method'
            )
        
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        
        Tx =  buildSendTimeLockTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_sendTimeLock",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_sendTimeLock",
            [Tx],
        )
        return TxHash




    def sendRawTimeLock(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the assetToRawTimeLock method'
            )
        
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultSendTimeLockGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        
        Tx = buildSendToTimeLockTx(transaction, self.__defaultChainId)

        Txnew =  self.web3.manager.request_blocking(
            "fsntx_buildSendTimeLockTx",
            [Tx],
        )
        
        Tx_dict = dict(Txnew)
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)




    def assetToTimeLock(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the assetToTimeLock method'
            )
        
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        
        Tx =  buildAssetToTimeLockTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_assetToTimeLock",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_assetToTimeLock",
            [Tx],
        )
        return TxHash




    def assetToRawTimeLock(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the assetToRawTimeLock method'
            )
        
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultAssetToTimeLockGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        
        Tx = buildAssetToTimeLockTx(transaction, self.__defaultChainId)

        Txnew =  self.web3.manager.request_blocking(
            "fsntx_buildAssetToTimeLockTx",
            [Tx],
        )
        
        Tx_dict = dict(Txnew)
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def timeLockToAsset(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the timeLockToAsset method'
            )
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        
        Tx =  buildTimeLockToAssetTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_timeLockToAsset",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_timeLockToAsset",
            [Tx],
        )
        return TxHash




    def timeLockToRawAsset(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the timeLockToRawAsset method'
            )
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultTimeLockToAssetGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        
        Tx = buildTimeLockToAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildTimeLockToAssetTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def timeLockToTimeLock(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the timeLockToTimeLock method'
            )
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        
        Tx =  buildTimeLockToTimeLockTx(transaction, self.__defaultChainId)
        
        #print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_timeLockToTimeLock",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_timeLockToTimeLock",
            [Tx],
        )
        return TxHash



    def timeLockToRawTimeLock(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the timeLockToRawTimeLock method'
            )
        if 'toUSAN' in transaction:
            if is_integer(transaction['toUSAN']):
               transaction['to'] = self.getAddressByNotation(transaction['toUSAN'])
               del transaction['toUSAN']
            else:
                raise TypeError(
                'The USAN you are sending to is not an integer'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultTimeLockToTimeLockGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        
        Tx = buildTimeLockToTimeLockTx(transaction, self.__defaultChainId)
        Txnew =  self.web3.manager.request_blocking(
            "fsntx_buildTimeLockToTimeLockTx",
            [Tx],
        )
        
        Tx_dict = dict(Txnew)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def makeSwap(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the makeSwap method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultMakeSwapGasPrice, 'ether'))    #  Fusion gas price for makeSwap
        
        Tx =  buildMakeSwapTx(transaction, self.__defaultChainId)
        
        #print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_makeSwap",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_makeSwap",
            [Tx],
        )
        return TxHash




    def makeRawSwap(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the makeRawSwap method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultMakeSwapGasPrice, 'ether'))    #  Fusion gas price for makeSwap
        
        Tx = buildMakeSwapTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildMakeSwapTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def makeRawMultiSwap(self, transaction, prepareOnly=False):
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the makeRawMultiSwap method'
            )
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
        
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultMakeSwapGasPrice, 'ether'))    #  Fusion gas price for makeSwap
        
        Tx = buildMakeMultiSwapTx(transaction, self.__defaultChainId)
        
        #print('\n',Tx,'\n')
        
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_makeMultiSwap",Tx['params'])
        #print('\n',json_rpc,'\n')
        
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildMakeMultiSwapTx",
            Tx['params'],
        )
        
        Tx_dict = dict(Tx)
        
        #print('After fsntx_buildMakeMultiSwapTx Tx_dict = ',Tx_dict)
#
        Tx_dict['nonce'] = Tx['nonce']
        Tx_dict['chainId'] = self.__defaultChainId
        
       
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)




    def recallSwap(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the recallSwap method'
            )
        
        
        Tx =  buildMakeSwapTx(transaction, self.__defaultChainId)
        
        #print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_recallSwap",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_recallSwap",
            [Tx],
        )
        return TxHash



    def recallRawSwap(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the recallRawSwap method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultRecallSwapGasPrice, 'ether'))    #  Fusion gas price for recallSwap
        
        Tx = buildRecallSwapTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildRecallSwapTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)


    def recallRawMultiSwap(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the recallRawSwap method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultRecallSwapGasPrice, 'ether'))    #  Fusion gas price for recallSwap
        
        Tx = buildRecallSwapTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildRecallMultiSwapTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def takeSwap(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the takeSwap method'
            )
        
        
        Tx =  buildTakeSwapTx(transaction, self.__defaultChainId)
        
        #print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_takeSwap",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_takeSwap",
            [Tx],
        )
        return TxHash



    def takeRawSwap(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the takeRawSwap method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultTakeSwapGasPrice, 'ether'))    #  Fusion gas price for takeSwap
        
        Tx = buildTakeSwapTx(transaction, self.__defaultChainId)
        Tx['Size'] = hex_to_integer(Tx['Size'])  # Deals with a parsing bug in fsntx_buildTakeSwapTx
        
        
        #print('\n\n',transaction,'\n',Tx)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildTakeSwapTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)
        

        
    def takeRawMultiSwap(self, transaction, prepareOnly=False):

        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the takeRawSwap method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultTakeSwapGasPrice, 'ether'))    #  Fusion gas price for takeSwap
        
        Tx = buildTakeSwapTx(transaction, self.__defaultChainId)
        Tx['Size'] = hex_to_integer(Tx['Size'])  # Deals with a parsing bug in fsntx_buildTakeSwapTx
        
        
        #print('\n\n',transaction,'\n',Tx)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildTakeMultiSwapTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def isAutoBuyTicket(self):
        
        isAuto =  self.web3.manager.request_blocking(
            "fsntx_isAutoBuyTicket",
            ['latest'],
        )
        return isAuto



    def startAutoBuyTicket(self):
        
        self.web3.manager.request_blocking(
            "miner_startAutoBuyTicket",
            [None],
        )
        return



    def stopAutoBuyTicket(self):
        
        self.web3.manager.request_blocking(
            "miner_stopAutoBuyTicket",
            [None],
        )
        return

       
    def getAssetId(self,asset_name):
        if not is_string(asset_name):
            raise TypeError(
            'In getAssetId, the variable asset_name must be the name of an asset as a string'   
            )
        for key, tokenId in self.tokens.items():
            if key == asset_name:
                return tokenId
        else:
            token = self.assetNameToAssetInfo(asset_name)
            if token == None:
                return None
            if not token['disabled'] and token['whiteListEnabled']:
                return token['assetID']
            return None
        
        
   
        
    def getAssetDecimals(self,asset_name):
        if not is_string(asset_name):
            raise TypeError(
            'In getAssetId, the variable asset_name must be the name of an asset as a string'   
            )
        
        token = self.assetNameToAssetInfo(asset_name)
        if token == None:
            return None
        if not token['disabled'] and token['whiteListEnabled']:
            return token['decimals']
        return None
            
            
        
    def getAsset(self, assetId, block_identifier=None):
        if not is_hexstr(assetId):
            raise TypeError(
                'assetId must be a hex string'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        asset_dict =  self.web3.manager.request_blocking(
            "fsn_getAsset",
            [assetId, block_identifier],
        )
        return asset_dict



    def getNotation(self, account, block_identifier=None):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
        )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        notation = self.web3.manager.request_blocking(
            "fsn_getNotation",
            [account, block_identifier],
        )
        return notation
    
    
    def getLatestNotation(self, account, block_identifier='latest'):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
        )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        notation = self.web3.manager.request_blocking(
            "fsn_getLatestNotation",
            [account, block_identifier],
        )
        return notation



    def getAddressByNotation(self, notation, block_identifier=None):
        
        if not is_integer(notation):
            raise TypeError(
                'The supplied notation must be an integer'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        json_rpc = self.web3.manager.provider.encode_rpc_request("fsn_getAddressByNotation",[notation, block_identifier])
        #print(json_rpc)
            
        pub_key = self.web3.manager.request_blocking(
            "fsn_getAddressByNotation",
            [notation, block_identifier],
        )
        return pub_key


    def genNotation(self, transaction):
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        if transaction['from'] != self.acct.address:
            raise BadSendingAddress (
                'The public key you are sending from does not match the account for the private key'
            )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the genNotation method'
            )
        
        
        Tx =  buildGenNotationTx(transaction, self.__defaultChainId)
      
        #print('\n',Tx,'\n')

        TxHash = self.web3.manager.request_blocking(
            "fsntx_genNotation", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_genNotation",Tx)
        #print(json_rpc)
        return TxHash

 
   
    def genRawNotation(self,transaction, prepareOnly=False):
        
        if prepareOnly == False:
            if self.acct == None:
                raise PrivateKeyNotSet (
                    'No private key was set for this unsigned transaction'
                )
            if transaction['from'] != self.acct.address:
                raise BadSendingAddress (
                    'The public key you are sending from does not match the account for the private key'
                )
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict that is required for the genRawNotation method'
            )
        
        if 'gasPrice' in transaction:
            if transaction['gasPrice'] == 'default':
                transaction['gasPrice'] = hex(to_wei(self.__defaultGenNotationGasPrice, 'ether'))    #  Fusion gas price for GenNotation
        
        Tx =  buildGenNotationTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildGenNotationTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        Tx_dict['chainId'] = self.__defaultChainId
        
     
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)


        
    def getTimeLockBalance(self, assetId, account, block_identifier=None):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
        )
        if not is_hexstr(assetId):
            raise TypeError(
                'assetId must be a hex string'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        timelock_dict =  self.web3.manager.request_blocking(
            "fsn_getTimeLockBalance",
            [assetId, account, block_identifier],
        )
        return timelock_dict
    
    
    def getAllBalances(self, account, block_identifier=None):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
        )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        timelock_dict =  self.web3.manager.request_blocking(
            "fsn_getAllBalances",
            [account, block_identifier],
        )
        return timelock_dict   
    
        
    def getAllTimeLockBalances(self, account, block_identifier=None):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
        )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        timelock_dict =  self.web3.manager.request_blocking(
            "fsn_getAllTimeLockBalances",
            [account, block_identifier],
        )
        return timelock_dict       
    
    
    def getTimeLockValueByInterval(self, account, assetId, startTime, endTime, block_identifier=None):
        if is_integer(account):
            account = to_hex(account)
        if not is_address(account):
            raise TypeError(
                'The account does not have a valid address format'
        )
        if not is_hexstr(assetId):
            raise TypeError(
                'assetId must be a hex string'
            )
        if not is_hex(startTime):
            if is_integer(startTime):
                startTime = to_hex(startTime)
            else:
                raise TypeError(
                'The startTime does not have a valid format'
            )
        if not is_hex(endTime):
            if is_integer(endTime):
                endTime = to_hex(endTime)
            else:
                raise TypeError(
                'The endTime does not have a valid format'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        timelock_dict =  self.web3.manager.request_blocking(
            "fsn_getTimeLockValueByInterval",
            [account, block_identifier],
        )
        return timelock_dict   
            
    
    def getAllSwaps(self, pageNo):
        
        swap_rawdict = self.api.fsnapi_swaps(pageNo)
        
        #print('swaps = ',swap_rawdict)
        
        swap_dict = [{k:[] for k in ['swapID', 'timeStamp', 'fromAddress', 'fromAsset', 'toAsset', 'recCreated',
                                    'height', 'timeStamp', 'hash', 'size', 'Description', 
                                    'FromStartTime', 'ToEndTime', 'MinFromAmount', 'MinToAmount', 
                                    'SwapSize', 'Targes', 'Time', 'ToAssetID'
                                    ]
        } for ii in range(len(swap_rawdict)-1)]
        
        for ii in range(len(swap_rawdict)-1):
        
            data_string = swap_rawdict[ii]['data']
            #print(data_string)
            data_dict = json.loads(data_string)
            
            swap_dict[ii]['swapID'] = swap_rawdict[ii]['swapID']
            swap_dict[ii]['timeStamp'] = swap_rawdict[ii]['timeStamp']
            swap_dict[ii]['fromAddress'] = swap_rawdict[ii]['fromAddress']
            swap_dict[ii]['fromAsset'] = swap_rawdict[ii]['fromAsset']
            swap_dict[ii]['toAsset'] = swap_rawdict[ii]['toAsset']
            swap_dict[ii]['recCreated'] = swap_rawdict[ii]['recCreated']
            swap_dict[ii]['height'] = swap_rawdict[ii]['height']
            swap_dict[ii]['hash'] = swap_rawdict[ii]['hash']
            swap_dict[ii]['size'] = swap_rawdict[ii]['size']
            swap_dict[ii]['Description'] = data_dict['Description']
            swap_dict[ii]['FromStartTime'] = data_dict['FromStartTime']
            swap_dict[ii]['ToEndTime'] = data_dict['ToEndTime']
            swap_dict[ii]['MinFromAmount'] = data_dict['MinFromAmount']
            swap_dict[ii]['MinToAmount'] = data_dict['MinToAmount']
            swap_dict[ii]['SwapSize'] = data_dict['SwapSize']
            swap_dict[ii]['Targes'] = data_dict['Targes']
            swap_dict[ii]['Time'] = data_dict['Time']
            swap_dict[ii]['ToAssetID'] = data_dict['ToAssetID']
        
        
        
        return swap_dict


    
    def getSwap(self, txHash, block_identifier='latest'):
        if not is_hexstr(txHash):
            raise TypeError(
                'txHash must be a hex string'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        swap_dict =  self.web3.manager.request_blocking(
            "fsn_getSwap",
            [txHash, block_identifier],
        )
        return swap_dict       
    
    
    
    def getMultiSwap(self, txHash, block_identifier='latest'):
        if not is_hexstr(txHash):
            raise TypeError(
                'txHash must be a hex string'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)

        swap_dict =  self.web3.manager.request_blocking(
            "fsn_getMultiSwap",
            [txHash, block_identifier],
        )
        return dict(swap_dict)
    
    
 
    def assetNameToAssetInfo(self, asset_name):
        return self.api.assetNameToAssetInfo(asset_name)
    
    
    
    def fsnapiVerifiedAssetInfo(self):
        asset_dict = self.api.fsnapiVerifiedAssetInfo()
        
        verified_assets = []
        ii = 0
        
        for asset in asset_dict:
            if isinstance(asset, dict):
                if not asset['disabled'] and asset['whiteListEnabled']:
                    ii = ii+1
                    verified_assets.append(asset['shortName'])
                    
        return verified_assets
    
    
    def assetIdToAssetInfo(self, asset_Id):
        return self.api.assetIdToAssetInfo(asset_Id)
    
    
    def fsnapi_swaps_pubkey(self, pubKey, pageNo):
        swap_dict = self.api.fsnapi_swaps_pubkey(pubKey, pageNo)
        pubkey_swaps = []
        ii = 0
        for swap in swap_dict:
            if isinstance(swap, dict):
                ii = ii+1
                swap['data'] = json.loads(swap['data'])
                pubkey_swaps.append(swap)   
        if ii == 0:
            pubkey_swaps = None
        return pubkey_swaps
    
    
    def fsnapi_swaps_target(self, pubKey, pageNo):
        swap_dict = self.api.fsnapi_swaps_target(pubKey, pageNo)
        target_swaps = []
        ii = 0
        for swap in swap_dict:
            if isinstance(swap, dict):
                swap['data'] = json.loads(swap['data'])
                target_swaps.append(swap)
        if ii == 0:
            target_swaps = None
        return target_swaps
    
    
    def fsnapiAssetAllInfo(self, pageNo):
        return self.api.fsnapiAssetAllInfo(pageNo)



    def pubKeyInfo(self, pubKey):
        add_info = self.api.pubKeyInfo(pubKey)['address'][0]
        balanceInfo = json.loads(add_info['balanceInfo'])
            
        info_dict = {
            'recCreated':           add_info['recCreated'],
            'recEdited':            add_info['recEdited'],
            'ticketsWon':           add_info['ticketsWon'],
            'rewardEarn':           add_info['rewardEarn'],
            'fsnBalance':           add_info['fsnBalance'],
            'numberOfTransactions': add_info['numberOfTransactions'],
            'usan':                 add_info['san'],
            'assetsHeld':           add_info['assetsHeld'],
            'balanceInfo':          balanceInfo,     # holds 'balances' and 'timeLockBalances'
        }
        return info_dict
    
    
    def fsnprice(self):
        return self.api.fsnprice()
    
    
    def numToDatetime(self,tdelta):
        if tdelta >= self.consts['BN']:
            return 'infinity'
        else:
            return numToDatetime(tdelta)
 
    def datetimeToHex(self, dt):
        return datetimeToHex(dt)
    
    def datetimeToInt(self, dt):
        dt_hex = datetimeToHex(dt)
        return hex_to_integer(dt_hex)
    
    def hex2a(self, datastr):
        return hex2a(datastr)
 
 
    def getBlock(self, block_identifier=None):
        
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        
        return int(self.web3.manager.request_blocking(
            "eth_getBlockByNumber",
            [block_identifier, True],
        ))
    
    
    def getTransactionByBlockNumberAndIndex(self, indx, block_identifier=None):
        
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        
        return self.web3.manager.request_blocking(
            "eth_getTransactionByBlockNumberAndIndex",
            [block_identifier, indx],
        )
 
    def transactionNoTicketsDesc(self, pageNo):
        return self.api.transactionNoTicketsDesc(pageNo)
    
    
    def transactionsDesc(self, pageNo):
        return self.api.transactionsDesc(pageNo)
    
    def takeSwapsDesc(self, pageNo):
        return self.api.takeSwapsDesc(pageNo)
 
    
    #def estimateGas(self, transaction, block_identifier=None):
        #if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            #transaction = assoc(transaction, 'from', self.defaultAccount)

        #if block_identifier is None:
            #params = [transaction]
        #else:
            #params = [transaction, block_identifier]
            
        

        #return self.web3.manager.request_blocking(
            #"eth_estimateGas",
            #params,
        #)



            

