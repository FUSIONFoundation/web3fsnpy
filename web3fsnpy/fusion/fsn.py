from eth_account import (
    Account,
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
from hexbytes import (
    HexBytes,
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
from web3.fusion.fsn_transactions import (
    fill_transaction_defaults,
)
from web3.fusion.exceptions import (
    NotRawTransaction,
)
from web3.fusion import (
    fsn_assets,
)
from web3.fusion.fsn_utils import (
    is_named_block,
    is_hexstr,
    block_number_formatter,
    to_boolean,
)

from web3 import Web3
import web3.eth

class Fsn(web3.eth.Eth):
    

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


    def __init__(self, linkToChain):

        for key, val in linkToChain.items():
            if key == 'network':
                if val not in ['testnet','mainnet']:
                    raise TypeError('Error in linkToChain dictionary: Found ',val, 'but network must be one of testnet, or mainnet')
            elif key == 'provider':
                if val not in ['WebSocket', 'HTTP', 'IPC']:
                    raise TypeError('Error in linkToChain dictionary: Found ',val, 'but provider must be one of WebSocket, HTTP, or IPC')
            elif key == 'gateway':
                pass
            else:
                raise TypeError('Error in linkToChain dictionary: Illegal key ',key )
        
        if linkToChain['provider'] == 'WebSocket':
            self.web3 = Web3(Web3.WebsocketProvider(linkToChain['gateway']))
        elif linkToChain['provider'] == 'HTTP':
            self.web3 = Web3(Web3.HTTPProvider(linkToChain['gateway']))
        else:
            self.web3 = Web3(Web3.IPCProvider(linkToChain['gateway']))
        
        if linkToChain['network'] == 'testnet':
            self.__defaultChainId = 46688
        elif linkToChain['network'] == 'mainnet':
            self.__defaultChainId = 32659
        
        
        
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
            
            "BN":                                    18446744073709551615,
        }
            
        self.tokens = {
            "FSNToken":         "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "FSN":         "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        }

        

        
        


    @property
    def chainId(self):
    #    return self.web3fsnpy.manager.request_blocking("eth_chainId", [])
        return self.__defaultChainId
        
    def BN(self):
        return self.consts['BN']

    def fill_tx_defaults(self, transaction):
        return fill_transaction_defaults(self, transaction,self.__defaultChainId)


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

    def createRawAsset(self, raw_transaction):
        if isinstance(raw_transaction,dict):
            raise NotRawTransaction(
                'This looks like a dict and not like a signed raw transaction'
            )
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_genRawAsset",
            [raw_transaction],
        )
        return TxHash
        
    def createAsset(self, transaction):
        if not isinstance(transaction,dict):
            raise TypeError(
                'This does not look like a dict of a transaction'
            )
                
        Tx =  fsn_assets.fsn_asset_create(transaction)
            
        print('Is the endpoint alive? : ',self.web3fsnpy.manager.provider.isConnected())
        #TxHash = self.web3fsnpy.manager._make_request("fsntx_genAsset", [Tx])
        #TxHash = self.web3fsnpy.manager.request_blocking("fsntx_genAsset", [Tx])
        #print('Return from request = ', TxHash)
        json_rpc = self.web3.manager.provider.encode_rpc_request("fsntx_genAsset",Tx)
            
        print(json_rpc)
        #return TxHash


    def sendRawAsset(self, raw_transaction):
        if isinstance(raw_transaction,dict):
            raise NotRawTransaction(
                'This looks like a dict and not like a signed raw transaction'
            )
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_sendRawAsset", 
            [raw_transaction])
        return TxHash


    def sendAsset(self, account, transaction):
        if not isinstance(transaction,dict):
            raise TypeError(
                'This transaction is not a dict'
            )
        TxHash =  self.web3.manager.request_blocking(
            "fsntx_sendAsset",
            [transaction],
        )
        return TxHash
        
    def getAssetId(self,asset_name):
        if not is_string(asset_name):
            raise TypeError(
            'asset_name must be the name of an asset as a string'   
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
            

            

