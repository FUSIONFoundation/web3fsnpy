
from eth_utils.toolz import (
    assoc,
    curry,
    merge,
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
        

from datetime import datetime, timedelta
from dateutil import tz



def dateStringToDatetime(datestring):
#
# Example of valid dates 
#"2007-03-01T13:00:00+0100"  or  UTC = "2007-03-01T12:00:00" or UTC = "2019-09-18T19:29:05.000Z"
    
    if len(datestring) == 19 or datestring[23] == 'Z':
        datestring = datestring + '+0000'          # Assume the user meant UTC
        
    
    try:
        dt = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError as ve:
            print('ValueError: ', ve, ' in string ',datestring)
            
    return dt


def datetimeToHex(dt):
    tzero = datetime.strptime('1970-01-01T00:00:00+0000', '%Y-%m-%dT%H:%M:%S%z')
    tdelta = (dt - tzero).total_seconds()
    tdelta = int(tdelta)
    #print('tdelta = ',tdelta)
    
    return hex(tdelta)


def numToDatetime(tdelta):
    tzero = datetime.strptime('1970-01-01T00:00:00+0000', '%Y-%m-%dT%H:%M:%S%z')
    if is_integer(tdelta):
        pass
    elif is_hex(tdelta):
        tdelta = hex_to_integer(tdelta)
    
    else:
        raise TypeError(
            'Unrecognised raw date ', tdelta
        )
    
    return tzero + timedelta(seconds = tdelta)





@curry
def to_hex_if_datestring(datestring):
#
    tzlocal = tz.tzoffset('UTC', 0)
    if datestring == 'now' or datestring == 'Now':
        return datetimeToHex(datetime.now(tzlocal))  # Make sure that stored times are in UTC, with timezone included
    elif datestring == 'infinity' or datestring == 'Infinity':
        return '0xffffffffffffffff'
    elif datestring[0:2] != '0x':
        dt = dateStringToDatetime(datestring)
        #print('dt = ',dt)
        return datetimeToHex(dt)
    else:
        return datestring
    
    
##########################################################################################################################
#
# Asset to TimeLock


ASSETTOTL_DEFAULTS = {
    #'gasPrice': 2000000000,
    #'gas':     90000,
    'chainId':  None,
}


ASSETTOTL_FORMATTERS = {
    'to':    to_checksum_address,
    'toUSAN': apply_formatter_if(is_string, int),
    'from': to_checksum_address,
    'nonce': to_hex_if_integer_or_ascii,
    'gas': to_hex_if_integer_or_ascii,
    'gasPrice': to_hex_if_integer_or_ascii,
    'asset': to_hex_if_integer_or_ascii,
    'value': to_hex_if_integer_or_ascii,
    'start': apply_formatter_if(ascii, to_hex_if_datestring),
    'end':  apply_formatter_if(ascii, to_hex_if_datestring),
    'chainId': to_hex_if_integer_or_ascii,
}

VALID_ASSETTOTL_PARAMS = [
    'to',
    'toUSAN',
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'asset',
    'value',
    'start',
    'end',
    'chainId',
]

REQUIRED_ASSETTOTL_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'asset',
    'value',
    'chainId',
]


def buildAssetToTimeLockTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in ASSETTOTL_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_ASSETTOTL_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_assettotl_formatter(transaction_merged)
    
    assert_check_assettotl_params(transaction_new)
    
    return transaction_new


unsigned_assettotl_formatter = apply_formatters_to_dict(ASSETTOTL_FORMATTERS)


def assert_check_assettotl_params(assettotl_params):
    for param in assettotl_params:
        if param not in VALID_ASSETTOTL_PARAMS:
            raise ValueError('{} is not a valid asset to time lock parameter'.format(param))

    for param in REQUIRED_ASSETTOTL_PARAMS:
        if param not in assettotl_params:
            raise ValueError('{} is required as an asset to time lock parameter'.format(param))
    if 'to' not in assettotl_params and 'toUSAN' not in assettotl_params:
            raise ValueError('Either \'to\' or \'toUSAN\' is required as an asset to time lock parameter')


##############################################################################################################
#
# TimeLock to Asset
#
TLTOASSET_DEFAULTS = ASSETTOTL_DEFAULTS
TLTOASSET_FORMATTERS = ASSETTOTL_FORMATTERS
VALID_TLTOASSET_PARAMS = VALID_ASSETTOTL_PARAMS
REQUIRED_TLTOASSET_PARAMS = REQUIRED_ASSETTOTL_PARAMS

def buildTimeLockToAssetTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in TLTOASSET_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_TLTOASSET_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_tltoasset_formatter(transaction_merged)
    
    assert_check_tltoasset_params(transaction_new)
    
    return transaction_new

unsigned_tltoasset_formatter = apply_formatters_to_dict(TLTOASSET_FORMATTERS)


def assert_check_tltoasset_params(tltoasset_params):
    for param in tltoasset_params:
        if param not in VALID_TLTOASSET_PARAMS:
            raise ValueError('{} is not a valid asset to time lock parameter'.format(param))

    for param in REQUIRED_TLTOASSET_PARAMS:
        if param not in tltoasset_params:
            raise ValueError('{} is required as a time lock to asset parameter'.format(param))
    if 'to' not in tltoasset_params and 'toUSAN' not in tltoasset_params:
            raise ValueError('Either \'to\' or \'toUSAN\' is required a time lock to asset parameter')

######################################################################################################
#
#  Timelock to TimeLock
#
#
TLTOTL_DEFAULTS = {
    #'gasPrice': 2000000000,
    #'gas':     90000,
    'chainId':  None,
}


TLTOTL_FORMATTERS = {
    'to':    to_checksum_address,
    'toUSAN': apply_formatter_if(is_string, int),
    'from': to_checksum_address,
    'nonce': to_hex_if_integer_or_ascii,
    'gas': to_hex_if_integer_or_ascii,
    'gasPrice': to_hex_if_integer_or_ascii,
    'asset': to_hex_if_integer_or_ascii,
    'value': to_hex_if_integer_or_ascii,
    'start': apply_formatter_if(ascii, to_hex_if_datestring),
    'end':  apply_formatter_if(ascii, to_hex_if_datestring),
    'chainId': to_hex_if_integer_or_ascii,
}

VALID_TLTOTL_PARAMS = [
    'to',
    'toUSAN',
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'asset',
    'value',
    'start',
    'end',
    'chainId',
]

REQUIRED_TLTOTL_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'asset',
    'value',
    'chainId',
]


def buildTimeLockToTimeLockTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in TLTOTL_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_TLTOTL_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_tltotl_formatter(transaction_merged)
    
    assert_check_tltotl_params(transaction_new)
    
    return transaction_new


unsigned_tltotl_formatter = apply_formatters_to_dict(TLTOTL_FORMATTERS)


def assert_check_tltotl_params(tltotl_params):
    for param in tltotl_params:
        if param not in VALID_TLTOTL_PARAMS:
            raise ValueError('{} is not a valid time lock to time lock parameter'.format(param))

    for param in REQUIRED_TLTOTL_PARAMS:
        if param not in tltotl_params:
            raise ValueError('{} is required as an time lock to time lock parameter'.format(param))
    if 'to' not in tltotl_params and 'toUSAN' not in tltotl_params:
            raise ValueError('Either \'to\' or \'toUSAN\' is required as an time lock to time lock parameter')
#
#
################################################################################################################
#
# SendToTimeLock
#
#

SENDTOTL_DEFAULTS = {
    #'gasPrice': 2000000000,
    #'gas':     90000,
    'chainId':  None,
}


SENDTOTL_FORMATTERS = {
    'to':    to_checksum_address,
    'toUSAN': apply_formatter_if(is_string, int),
    'from': to_checksum_address,
    'nonce': to_hex_if_integer_or_ascii,
    'gas': to_hex_if_integer_or_ascii,
    'gasPrice': to_hex_if_integer_or_ascii,
    'asset': to_hex_if_integer_or_ascii,
    'value': to_hex_if_integer_or_ascii,
    'start': apply_formatter_if(ascii, to_hex_if_datestring),
    'end':  apply_formatter_if(ascii, to_hex_if_datestring),
    'chainId': to_hex_if_integer_or_ascii,
}

VALID_SENDTOTL_PARAMS = [
    'to',
    'toUSAN',
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'asset',
    'value',
    'start',
    'end',
    'chainId',
]

REQUIRED_SENDTOTL_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'asset',
    'value',
    'chainId',
]


def buildSendToTimeLockTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in SENDTOTL_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_SENDTOTL_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_sendtotl_formatter(transaction_merged)
    
    assert_check_sendtotl_params(transaction_new)
    
    return transaction_new


unsigned_sendtotl_formatter = apply_formatters_to_dict(SENDTOTL_FORMATTERS)


def assert_check_sendtotl_params(sendtotl_params):
    for param in sendtotl_params:
        if param not in VALID_SENDTOTL_PARAMS:
            raise ValueError('{} is not a valid send to time lock parameter'.format(param))

    for param in REQUIRED_SENDTOTL_PARAMS:
        if param not in sendtotl_params:
            raise ValueError('{} is required as an send to time lock parameter'.format(param))
    if 'to' not in sendtotl_params and 'toUSAN' not in sendtotl_params:
            raise ValueError('Either \'to\' or \'toUSAN\' is required as a send to time lock parameter')



