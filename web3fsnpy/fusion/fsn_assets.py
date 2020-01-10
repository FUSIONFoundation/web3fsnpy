
from eth_utils.toolz import (
    assoc,
    curry,
    merge,
)

from ..eth_account._utils.signing import (
    sign_transaction_hash,
    sign_message_hash,
    to_eth_v,
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


from web3._utils.formatters import (
    apply_formatter_at_index,
    apply_formatter_to_array,
    hex_to_integer,
    integer_to_hex,
    is_array_of_dicts,
    is_array_of_strings,
    remove_key_if,
)

from web3.datastructures import (
    AttributeDict,
)


from .fsn_utils import *
        



GENASSET_DEFAULTS = {
    #'gasPrice': 100000000000,
    #'gas':     90000,
    'value':   '0x0',
    'chainId':  None,
}


ASSETCREATE_FORMATTERS = {
    'nonce': to_hex_if_integer_or_ascii,
    'chainId': to_hex_if_integer_or_ascii,
    'gas': to_integer_if_hex,
    #'gasPrice': to_integer_if_hex,
    'gasPrice': to_hex_if_integer_or_ascii,
    'from': to_checksum_address,
    'name': to_ascii_if_bytes,
    'symbol': to_ascii_if_bytes,
    'decimals': to_integer_if_hex,
    'total': to_hex_if_integer_or_ascii,
    'canChange': apply_formatter_if(is_integer, to_boolean),
}

VALID_GENASSETTX_PARAMS = [
    'nonce',
    'gas',
    'gasPrice',
    'value',
    'chainId',
    'name',
    'symbol',
    'decimals',
    'total',
    'description',
    'canChange',
]

REQUIRED_GENASSETTX_PARAMS = [
    'nonce',
    #'gas',
    #'gasPrice',
    'value',
    'chainId',
    'name',
    'symbol',
    'decimals',
    'total',
    'canChange',
]


def buildGenAssetTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in GENASSET_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_GENASSETTX_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_assetcreate_formatter(transaction_merged)
    
    assert_check_gen_asset_params(transaction_new)
    
    return transaction_new


unsigned_assetcreate_formatter = apply_formatters_to_dict(ASSETCREATE_FORMATTERS)

def assert_check_gen_asset_params(assetcreate_params):
    for param in assetcreate_params:
        if param not in VALID_GENASSETTX_PARAMS:
            raise ValueError('{} is not a valid asset create parameter'.format(param))

    for param in REQUIRED_GENASSETTX_PARAMS:
        if param not in assetcreate_params:
            raise ValueError('{} is required as an asset create parameter'.format(param))
        



################################################################################################
#  SEND ASSET


SENDASSET_DEFAULTS = {
    #'gasPrice': 2000000000,
    #'gas':     90000,
    'chainId':  None,
}

SENDASSET_FORMATTERS = {
    'from': to_checksum_address,
    'to': to_checksum_address,
    'toUSAN': apply_formatter_if(is_string, int),
    'nonce': to_hex_if_integer_or_ascii,
    'chainId': to_hex_if_integer_or_ascii,
    'gas': to_hex_if_integer_or_ascii,
    #'gasPrice': to_integer_if_hex,
    'gasPrice': to_hex_if_integer_or_ascii,
    'value': to_hex_if_integer_or_ascii,
    'asset': to_hex_if_integer_or_ascii,
}

VALID_SENDASSETTX_PARAMS = [
    'nonce',
    'from',
    'to',
    'toUSAN',
    'gas',
    'gasPrice',
    'value',
    'chainId',
    'asset',
]

REQUIRED_SENDASSETTX_PARAMS = [
    'nonce',
    'from',
    #'gas',
    #'gasPrice',
    'value',
    'chainId',
    'asset',
]


def buildSendAssetTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in SENDASSET_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_SENDASSETTX_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_sendasset_formatter(transaction_merged)
    
    assert_check_send_asset_params(transaction_new)
    
    return transaction_new


unsigned_sendasset_formatter = apply_formatters_to_dict(SENDASSET_FORMATTERS)



def assert_check_send_asset_params(sendasset_params):
    for param in sendasset_params:
        if param not in VALID_SENDASSETTX_PARAMS:
            raise ValueError('{} is not a valid send asset parameter'.format(param))

    for param in REQUIRED_SENDASSETTX_PARAMS:
        if param not in sendasset_params:
            raise ValueError('{} is required as a send asset parameter'.format(param))
    if 'to' not in sendasset_params and 'toUSAN' not in sendasset_params:
            raise ValueError('Either \'to\' or \'toUSAN\' is required as a send asset parameter'.format(param))


#############################################################################################
#
#   Increment and Decrement assets 
#

INCDECASSET_DEFAULTS = {
    #'gasPrice': 3000000000,
    #'gas':     90000,
    'chainId':  None,
}

INCDECASSET_FORMATTERS = {
    'from': to_checksum_address,
    'to': to_checksum_address,
    'nonce': to_hex_if_integer_or_ascii,
    'chainId': to_hex_if_integer_or_ascii,
    'gas': to_hex_if_integer_or_ascii,
    #'gasPrice': to_integer_if_hex,
    'gasPrice': to_hex_if_integer_or_ascii,
    'value': to_hex_if_integer_or_ascii,
    'asset': to_hex_if_integer_or_ascii,
    'transacData': to_ascii_if_bytes,
}

VALID_INCDECASSETTX_PARAMS = [
    'nonce',
    'from',
    'to',
    'gas',
    'gasPrice',
    'value',
    'chainId',
    'asset',
    'transacData',
]

REQUIRED_INCDECASSETTX_PARAMS = [
    'nonce',
    'from',
    'to',
    #'gas',
    #'gasPrice',
    'value',
    'chainId',
    'asset',
]



def buildIncAssetTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in INCDECASSET_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_INCDECASSETTX_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_incasset_formatter(transaction_merged)
    
    assert_check_incdec_asset_params(transaction_new)
    
    return transaction_new


unsigned_incasset_formatter = apply_formatters_to_dict(INCDECASSET_FORMATTERS)


def buildDecAssetTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in INCDECASSET_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_INCDECASSETTX_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_decasset_formatter(transaction_merged)
    
    assert_check_incdec_asset_params(transaction_new)
    
    return transaction_new


unsigned_decasset_formatter = apply_formatters_to_dict(INCDECASSET_FORMATTERS)



def assert_check_incdec_asset_params(incdecasset_params):
    for param in incdecasset_params:
        if param not in VALID_INCDECASSETTX_PARAMS:
            raise ValueError('{} is not a valid inc or dec asset parameter'.format(param))

    for param in REQUIRED_INCDECASSETTX_PARAMS:
        if param not in incdecasset_params:
            raise ValueError('{} is required as an inc or dec asset parameter'.format(param))







