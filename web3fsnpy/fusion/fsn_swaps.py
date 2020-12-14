
from eth_utils.toolz import (
    assoc,
    curry,
    merge,
)

from cytoolz import (
    pipe,
)

from eth_utils.curried import (
    apply_formatters_to_sequence,
    is_address,
    text_if_str,
    to_checksum_address,
    apply_formatter_if,
    apply_formatters_to_dict,
    apply_one_of_formatters,
)

from eth_utils import (
    to_bytes,
    to_int,
    is_bytes,
    is_boolean,
    is_bytes,
    is_hex,
    is_null,
    is_integer,
    is_string,
    is_dict,
    is_list_like,
    keccak,
)

from web3._utils.formatters import (
    hex_to_integer,
    integer_to_hex,
    is_array_of_dicts,
    is_array_of_strings,
    remove_key_if,
)

from web3._utils.encoding import (
    to_hex,
)

from web3.datastructures import (
    AttributeDict,
)

from .fsn_timelocks import (
    to_hex_if_datestring,
)


from .fsn_utils import *
        

from datetime import datetime, timedelta
from dateutil import tz

    
##########################################################################################################################
#
# Make asset swap
#

MAKESWAP_DEFAULTS = {
    #'gasPrice':         1000000000000000,
    #'gas':              10000,
    'chainId':          None,
    'FromStartTime':    'now',
    'FromEndTime':      'infinity',
    'ToStartTime':      'now',
    'ToEndTime':        'infinity',
}


MAKESWAP_FORMATTERS = {
    'from':             to_checksum_address,
    'nonce':            to_hex_if_integer_or_ascii,
    'gas':              to_hex_if_integer_or_ascii,
    'gasPrice':         to_hex_if_integer_or_ascii,
    'FromAssetID':      to_hex_if_integer_or_ascii,
    'FromStartTime':    apply_formatter_if(ascii, to_hex_if_datestring),
    'FromEndTime':      apply_formatter_if(ascii, to_hex_if_datestring),
    'MinFromAmount':    to_hex_if_integer_or_ascii,
    'ToAssetID':        to_hex_if_integer_or_ascii,
    'ToStartTime':      apply_formatter_if(ascii, to_hex_if_datestring),
    'ToEndTime':        apply_formatter_if(ascii, to_hex_if_datestring),
    'MinToAmount':      to_hex_if_integer_or_ascii,
    'SwapSize':         to_integer_if_hex,
    'Targes':           to_checksum_address,
    'chainId':          to_hex_if_integer_or_ascii,
}

VALID_MAKESWAP_PARAMS = [
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'FromAssetID',
    'FromStartTime',
    'FromEndTime',
    'MinFromAmount',
    'ToAssetID',
    'ToStartTime',
    'ToEndTime',
    'MinToAmount',
    'SwapSize',
    'Targes',
    'chainId',
]

REQUIRED_MAKESWAP_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'FromAssetID',
    'FromStartTime',
    'FromEndTime',
    'MinFromAmount',
    'ToAssetID',
    'ToStartTime',
    'ToEndTime',
    'MinToAmount',
    'SwapSize',
    'Targes',
    'chainId',
]


def buildMakeSwapTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in MAKESWAP_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_MAKESWAP_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_makeswap_formatter(transaction_merged)
    
    assert_check_makeswap_params(transaction_new)
    
    return transaction_new


unsigned_makeswap_formatter = apply_formatters_to_dict(MAKESWAP_FORMATTERS)


def assert_check_makeswap_params(makeswap_params):
    for param in makeswap_params:
        if param not in VALID_MAKESWAP_PARAMS:
            raise ValueError('{} is not a valid make swap parameter'.format(param))

    for param in REQUIRED_MAKESWAP_PARAMS:
        if param not in makeswap_params:
            raise ValueError('{} is required as an make swap parameter'.format(param))



##############################################################################################



def buildMakeMultiSwapTx(transaction, defaultChainId):
    tx = transaction['params']
    if len(tx) > 0:
        #print(tx)
        for ii in range(len(tx)):
            if 'ToAssetID' not in tx[ii]:
                raise ValueError('In buildMakeMultiSwapTx, could not find ToAssetID in tx')
            elif not isinstance(tx[ii]['ToAssetID'], list):
                raise ValueError('In buildMakeMultiSwapTx, ToAssetID is not a list')
            else:
                nToAsset = len(tx[ii]['ToAssetID'])
                if 'ToStartTime' not in tx[ii]:
                    tx[ii]['ToStartTime'] = []
                    for jj in range(nToAsset):
                        tx[ii]['ToStartTime'].append(to_hex_if_datestring('now'))
                else:
                    if not isinstance(tx[ii]['ToStartTime'], list):
                        raise ValueError('In buildMakeMultiSwapTx, ToStartTime is not a list')
                    elif len(tx[ii]['ToStartTime']) != nToAsset:
                        raise ValueError('In buildMakeMultiSwapTx, ToStartTime list is not the same length as ToAssetID')
                    else:
                        for jj in range(nToAsset):
                            tx[ii]['ToStartTime'][jj] = to_hex_if_datestring(tx[ii]['ToStartTime'][jj])
                if 'ToEndTime' not in tx[ii]:
                    tx[ii]['ToEndTime'] = []
                    for jj in range(nToAsset):
                        tx[ii]['ToEndTime'].append(to_hex_if_datestring('infinity'))
                else:
                    if not isinstance(tx[ii]['ToEndTime'], list):
                        raise ValueError('In buildMakeMultiSwapTx, ToEndTime is not a list')
                    elif len(tx[ii]['ToEndTime']) != nToAsset:
                        raise ValueError('In buildMakeMultiSwapTx, ToEndTime list is not the same length as ToAssetID')
                    else:
                        for jj in range(nToAsset):
                            tx[ii]['ToEndTime'][jj] = to_hex_if_datestring(tx[ii]['ToEndTime'][jj])
            
                if 'MinToAmount' not in tx[ii]:
                    raise ValueError('In buildMakeMultiSwapTx, could not find MinToAmount in tx')
                else:
                    if not isinstance(tx[ii]['MinToAmount'], list):
                        raise ValueError('In buildMakeMultiSwapTx, MinToAmount is not a list')
                    elif len(tx[ii]['MinToAmount']) != nToAsset:
                        raise ValueError('In buildMakeMultiSwapTx, MinToAmount list is not the same length as ToAssetID')
                    else:
                        for jj in range(nToAsset):
                            tx[ii]['MinToAmount'][jj] = to_hex_if_integer_or_ascii(tx[ii]['MinToAmount'][jj])
            
            if 'FromAssetID' not in tx[ii]:
                raise ValueError('In buildMakeMultiSwapTx, could not find FromAssetID in tx')
            elif not isinstance(tx[ii]['FromAssetID'], list):
                raise ValueError('In buildMakeMultiSwapTx, FromAssetID is not a list')
            else:
                nFromAsset = len(tx[ii]['FromAssetID'])
                if 'FromStartTime' not in tx[ii]:
                    tx[ii]['FromStartTime'] = []
                    for jj in range(nFromAsset):
                        tx[ii]['FromStartTime'].append(to_hex_if_datestring('now'))
                else:
                    if not isinstance(tx[ii]['FromStartTime'], list):
                        raise ValueError('In buildMakeMultiSwapTx, FromStartTime is not a list')
                    elif len(tx[ii]['FromStartTime']) != nFromAsset:
                        raise ValueError('In buildMakeMultiSwapTx, FromStartTime list is not the same length as FromAssetID')
                    else:
                        for jj in range(nFromAsset):
                            tx[ii]['FromStartTime'][jj] = to_hex_if_datestring(tx[ii]['FromStartTime'][jj])
                    
                if 'FromEndTime' not in tx[ii]:
                    tx[ii]['FromEndTime'] = []
                    for jj in range(nFromAsset):
                        tx[ii]['FromEndTime'].append(to_hex_if_datestring('infinity'))
                else:
                    if not isinstance(tx[ii]['FromEndTime'], list):
                        raise ValueError('In buildMakeMultiSwapTx, FromEndTime is not a list')
                    elif len(tx[ii]['FromEndTime']) != nFromAsset:
                        raise ValueError('In buildMakeMultiSwapTx, FromEndTime list is not the same length as FromAssetID')
                    else:
                        for jj in range(nFromAsset):
                            tx[ii]['FromEndTime'][jj] = to_hex_if_datestring(tx[ii]['FromEndTime'][jj])
            
                if 'MinFromAmount' not in tx[ii]:
                    raise ValueError('In buildMakeMultiSwapTx, could not find MinFromAmount in tx')
                else:
                    if not isinstance(tx[ii]['MinFromAmount'], list):
                        raise ValueError('In buildMakeMultiSwapTx, MinFromAmount is not a list')
                    elif len(tx[ii]['MinFromAmount']) != nFromAsset:
                        raise ValueError('In buildMakeMultiSwapTx, MinFromAmount list is not the same length as FromAssetID')
                    else:
                        for jj in range(nFromAsset):
                            tx[ii]['MinFromAmount'][jj] = to_hex_if_integer_or_ascii(tx[ii]['MinFromAmount'][jj])
                    
            if 'SwapSize' not in tx[ii]:
                raise ValueError('In buildMakeMultiSwapTx, could not find SwapSize in tx')
            else:
                tx[ii]['SwapSize'] = to_int(tx[ii]['SwapSize'])
        #    
            if 'Targes' not in tx[ii]:
                raise ValueError('In buildMakeMultiSwapTx, could not find Targes in tx')
            elif not isinstance(tx[ii]['Targes'], list):
                raise ValueError('In buildMakeMultiSwapTx, Targes is not a list')
            else:
                for jj in range(len(tx[ii]['Targes'])):
                    if not is_address(tx[ii]['Targes'][jj]):
                        raise ValueError('In buildMakeMultiSwapTx, found an invalid address in Targes ',tx[ii]['Targes'][jj])
                    
    transaction['params'] = tx
            
    if 'nonce' not in transaction:
        raise ValueError('In buildMakeMultiSwapTx, could not find nonce in transaction')
    else:
        transaction['nonce'] = to_hex_if_integer_or_ascii(transaction['nonce'])
        
    if 'gas' in transaction:
        transaction['gas'] = to_hex_if_integer_or_ascii(transaction['gas'])
        
    if 'gasPrice' in transaction:
        transaction['gasPrice'] = to_hex_if_integer_or_ascii(transaction['gasPrice'])
    
    
    transaction['chainId'] = to_hex_if_integer_or_ascii(defaultChainId)
    
    return transaction



##############################################################################################
#
#  Recall Swap
#

RECALLSWAP_DEFAULTS = {
    #'gasPrice':         1000000000000000,
    #'gas':              10000,
    'chainId':          None,
}


RECALLSWAP_FORMATTERS = {
    'from':             to_checksum_address,
    'nonce':            to_hex_if_integer_or_ascii,
    'gas':              to_hex_if_integer_or_ascii,
    'gasPrice':         to_hex_if_integer_or_ascii,
    'SwapID':           to_hex_if_integer_or_ascii,
    'chainId':          to_hex_if_integer_or_ascii,
}

VALID_RECALLSWAP_PARAMS = [
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'SwapID',
    'chainId',
]

REQUIRED_RECALLSWAP_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'SwapID',
    'chainId',
]


def buildRecallSwapTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in RECALLSWAP_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_RECALLSWAP_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_recallswap_formatter(transaction_merged)
    
    assert_check_recallswap_params(transaction_new)
    
    return transaction_new


unsigned_recallswap_formatter = apply_formatters_to_dict(RECALLSWAP_FORMATTERS)


def assert_check_recallswap_params(recallswap_params):
    for param in recallswap_params:
        if param not in VALID_RECALLSWAP_PARAMS:
            raise ValueError('{} is not a valid recall swap parameter'.format(param))

    for param in REQUIRED_RECALLSWAP_PARAMS:
        if param not in recallswap_params:
            raise ValueError('{} is required as an recall swap parameter'.format(param))


#########################################################################################################
#
#  Take Swap
#

TAKESWAP_DEFAULTS = {
    #'gasPrice':         1000000000000000,
    #'gas':              10000,
    'chainId':          None,
}


TAKESWAP_FORMATTERS = {
    'from':             to_checksum_address,
    'nonce':            to_hex_if_integer_or_ascii,
    'gas':              to_hex_if_integer_or_ascii,
    'gasPrice':         to_hex_if_integer_or_ascii,
    'SwapID':           to_hex_if_integer_or_ascii,
    'Size':             to_hex_if_integer_or_ascii,
    'chainId':          to_hex_if_integer_or_ascii,
}

VALID_TAKESWAP_PARAMS = [
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'SwapID',
    'Size',
    'chainId',
]

REQUIRED_TAKESWAP_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'SwapID',
    'Size',
    'chainId',
]



def buildTakeSwapTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in TAKESWAP_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_TAKESWAP_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_takeswap_formatter(transaction_merged)
    
    assert_check_takeswap_params(transaction_new)
    
    return transaction_new


unsigned_takeswap_formatter = apply_formatters_to_dict(TAKESWAP_FORMATTERS)


def assert_check_takeswap_params(takeswap_params):
    for param in takeswap_params:
        if param not in VALID_TAKESWAP_PARAMS:
            raise ValueError('{} is not a valid take swap parameter'.format(param))

    for param in REQUIRED_TAKESWAP_PARAMS:
        if param not in takeswap_params:
            raise ValueError('{} is required as an take swap parameter'.format(param))





