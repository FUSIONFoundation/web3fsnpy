from eth_account import (
    Account,
) 

#from eth_account.account import (
    #signTransaction,
#)

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
    is_string,
)
from eth_utils.curried import (
    is_address,
    is_bytes,
    is_integer,
    is_null,
    is_string,
    remove_0x_prefix,
    text_if_str,
)
from eth_utils.toolz import (
    assoc,
    merge,
)

from eth_keys import (
    KeyAPI,
    keys,
)

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

from web3._utils.formatters import (
    apply_formatter_if,
)

from web3._utils.blocks import (
    select_method_for_block_identifier,
)
from web3._utils.empty import (
    empty,
)
from web3._utils.encoding import (
    hex_encode_abi_type,
    to_bytes,
    to_hex,
    to_int,
    to_text,
    to_json,
)
from web3._utils.threads import (
    Timeout,
)

from web3.fusion.exceptions import (
    NotRawTransaction,
    _notConnected,
    BadSendingAddress,
    PrivateKeyNotSet,
)

from web3.fusion.fsn_transactions import (
    fill_transaction_defaults,
    SignTx,
    buildGenNotationTx,
)

from web3.fusion.fsn_assets import (
    buildGenAssetTx,
    buildSendAssetTx,
    buildIncAssetTx,
    buildDecAssetTx,
)

from web3.fusion.fsn_timelocks import (
    buildAssetToTimeLockTx,
    buildTimeLockToAssetTx,
    buildTimeLockToTimeLockTx,
)

from web3.fusion.fsn_utils import (
    get_default_modules,
    is_named_block,
    is_hexstr,
    block_number_formatter,
    to_boolean,
)

from web3 import Web3
import web3.eth

class Fsn(web3.eth.Eth):
    
   
    RequestManager = DefaultRequestManager

    # Encoding and Decoding
    toBytes = staticmethod(to_bytes)
    toInt = staticmethod(to_int)
    toHex = staticmethod(to_hex)
    toText = staticmethod(to_text)
    toJSON = staticmethod(to_json)

    # Currency Utility
    toWei = staticmethod(to_wei)
    fromWei = staticmethod(from_wei)

    # Address Utility
    isAddress = staticmethod(is_address)
    isChecksumAddress = staticmethod(is_checksum_address)
    toChecksumAddress = staticmethod(to_checksum_address)
    
    acct = None            # This is the Fusion account.


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
                    raise TypeError('Error: Cannot specify a default gateway for IPC')
        

        print('Connecting to : ',linkToChain['network'],linkToChain['gateway'], ' with the ',linkToChain['provider'], ' method')
        
        if linkToChain['provider'] == 'WebSocket':
            self.manager = self.RequestManager(Web3.WebsocketProvider(linkToChain['gateway']))
            self.web3 = Web3(Web3.WebsocketProvider(linkToChain['gateway']))
        elif linkToChain['provider'] == 'HTTP':
            self.manager = self.RequestManager(Web3.HTTPProvider(linkToChain['gateway']))
            self.web3 = Web3(Web3.HTTPProvider(linkToChain['gateway']))
        else:
            self.manager = self.RequestManager(Web3.IPCProvider(linkToChain['gateway']))
            self.web3 = Web3(Web3.IPCProvider(linkToChain['gateway']))
            
        modules = get_default_modules()
        attach_modules(self, modules)
        
        defaultAccount = None      
        
        if gotprivatekey:
            #print('Adding account to list')
            self.addAccount()
            
        
        
        self.consts = {
            "TimeForever":       0xffffffffffffffff, # javascript will convert this to 0x10000000000
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
            
            "BN":                                    18446744073709551615,   # = '0xffffffffffffffff' Used in time locks to signify infinity
        }
            
        self.tokens = {
            "FSNToken":         "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "FSN":         "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        }

        self.__defaultGenAssetGasPrice              = 0.0000001            # Default gasPrice in FSN for genAsset
        self.__defaultSendAssetGasPrice             = 0.000000002          # Default gasPrice in FSN for sendAsset
        self.__defaultIncDecAssetGasPrice           = 0.000000003          # Default gasPrice in FSN for incAsset, or decAsset
        self.__defaultGenNotationGasPrice           = 0.1                  # Default gasPrice in FSN for genNotation
        self.__defaultAssetToTimeLockGasPrice       = 0.000000002          # Default gasPrice in FSN for assetToTimeLock
        self.__defaultTimeLockToAssetGasPrice       = 0.000000002          # Default gasPrice in FSN for TimeLockToAsset
        self.__defaultTimeLockToTimeLockGasPrice    = 0.000000002          # Default gasPrice in FSN for TimeLockToTimeLock
        
        


    @property
    def chainId(self):
    #    return self.web3.manager.request_blocking("eth_chainId", [])
        return self.__defaultChainId
        
    def BN(self):
        return self.consts['BN']

    def fill_tx_defaults(self, transaction):
        return fill_transaction_defaults(transaction,self.__defaultChainId)
    
    def isConnected(self):
        try:
            self.blockNumber
            return True
        except(_notConnected):
            return False
     
    def addAccount(self):
        self.web3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.acct))
        self.defaultAccount = self.acct.address

    def getBalance(self, account, assetId, block_identifier=None):
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
        
        return self.web3.manager.request_blocking(
            "fsn_getBalance",
            [assetId, account, block_identifier],
        )
    
    
    def signAndTransmit(self, Tx_dict):
        
        if self.acct == None:
            raise PrivateKeyNotSet (
                'No private key was set for this unsigned transaction'
            )
        
        Tx_signed = SignTx(Tx_dict, self.acct)    
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_sendRawTransaction",
            [Tx_signed],
        )
        return TxHash


    def buyTicket(self, account):
        block_identifier = self.defaultBlock
        TxHash = self.web3.manager.request_blocking(
            "fsntx_buyTicket",
            [account],
        )
        return TxHash
                


    def allTickets(self, block_identifier):
        method = "fsn_allTickets"
        result = self.web3.manager.request_blocking(
            method,
            [block_identifier],
        )
        if result is None:
            raise BlockNotFound(f"Block with id: {block_identifier} not found.")
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
        
        Tx =  buildGenNotationTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildGenNotationTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultGenNotationGasPrice, 'ether'))    #  Fusion gas price for GenNotation
        Tx_dict['chainId'] = self.__defaultChainId
        
     
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



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
      
        print('\n',Tx,'\n')

        TxHash = self.web3.manager.request_blocking(
            "fsntx_genNotation", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_genAsset",Tx)
        #print(json_rpc)
        return TxHash



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
            
        Tx =  buildGenAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildGenAssetTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultGenAssetGasPrice, 'ether'))    #  Fusion gas price for GenAsset
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
        
        
        Tx =  buildGenAssetTx(transaction, self.__defaultChainId)
      
        print('\n',Tx,'\n')

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
            
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildIncAssetTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultIncDecAssetGasPrice, 'ether'))    #  Fusion gas price for incAsset
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
        
        
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
      
        print('\n',Tx,'\n')

        TxHash = self.web3.manager.request_blocking(
            "fsntx_incAsset", 
            [Tx]
        )
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_genAsset",Tx)
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
            
        Tx =  buildIncAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildDecAssetTx",
            [Tx],
        )
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultIncDecAssetGasPrice, 'ether'))    #  Fusion gas price for decAsset
        Tx_dict['chainId'] = self.__defaultChainId
        
     
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)
 
  
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
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_genAsset",Tx)
        #print(json_rpc)
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
        
        
        Tx = buildSendAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildSendAssetTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultSendAssetGasPrice, 'ether'))    #  Fusion gas price for SendAsset
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
        
        
        Tx =  buildSendAssetTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_sendAsset",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_sendAsset",
            [Tx],
        )
        return TxHash


    def assetToRawTimeLockTx(self, transaction, prepareOnly=False):

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
        
        Tx = buildAssetToTimeLockTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildAssetToTimeLockTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultAssetToTimeLockGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)


    def assetToTimeLockTx(self, transaction):
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
        
        
        Tx =  buildAssetToTimeLockTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_sendAsset",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_assetToTimeLock",
            [Tx],
        )
        return TxHash


    def timeLockToRawAssetTx(self, transaction, prepareOnly=False):

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
        
        Tx = buildTimeLockToAssetTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildTimeLockToAssetTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultTimeLockToAssetGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def timeLockToAssetTx(self, transaction):
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
        
        
        Tx =  buildAssetToTimeLockTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_sendAsset",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_timeLockToAsset",
            [Tx],
        )
        return TxHash


    def timeLockToRawTimeLockTx(self, transaction, prepareOnly=False):

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
        
        Tx = buildTimeLockToTimeLockTx(transaction, self.__defaultChainId)
        Tx =  self.web3.manager.request_blocking(
            "fsntx_buildTimeLockToTimeLockTx",
            [Tx],
        )
        
        Tx_dict = dict(Tx)
        
        Tx_dict['gasPrice'] = hex(to_wei(self.__defaultTimeLockToTimeLockGasPrice, 'ether'))    #  Fusion gas price for assetToTimeLock
        Tx_dict['chainId'] = self.__defaultChainId
             
        if prepareOnly == True:
            return Tx_dict
        else:
            return self.signAndTransmit(Tx_dict)



    def timeLockToTimeLockTx(self, transaction):
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
        
        
        Tx =  buildTimeLockToTimeLockTx(transaction, self.__defaultChainId)
        
        print('\n',Tx,'\n')
        
        #json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_sendAsset",Tx)
        #print(json_rpc)
        
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_timeLockToTimeLock",
            [Tx],
        )
        return TxHash


       
    def getAssetId(self,asset_name):
        if not is_string(asset_name):
            raise TypeError(
            'In getAssetId, the variable asset_name must be the name of an asset as a string'   
            )
        for key, tokenId in self.tokens.items():
            if key == asset_name:
                return tokenId
        else:
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



    def getAddressByNotation(self, notation, block_identifier=None):
        
        if not is_integer(notation):
            raise TypeError(
                'The supplied notation must be an integer'
            )
        if block_identifier is None:
            block_identifier = self.defaultBlock
        else:
            block_identifier = block_number_formatter(block_identifier)
            
        pub_key = self.web3.manager.request_blocking(
            "fsn_getAddressByNotation",
            [notation, block_identifier],
        )
        return notation
    

        
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
        
        
    def fsnGetAllTimeLockBalances(self, account, block_identifier=None):
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
            
        

    def estimateGas(self, transaction, block_identifier=None):
            
        return web3fsn.toWei(21,'gwei')    # value from MyFusionWallet JS code
            

            

