import math

from eth_utils.toolz import (
    assoc,
    curry,
    merge,
)

from web3.datastructures import (
    AttributeDict,
)

from eth_utils import (
    to_hex,
    to_bytes,
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


from ..eth_account._utils.transactions import (
    ChainAwareUnsignedTransaction,
    strip_signature,
    Transaction,
    vrs_from,
)


import rlp

from eth_utils.toolz import (
    complement,
    compose,
    curried,
    curry,
    partial,
    assoc,
    dissoc,
    merge,
)

from eth_rlp import (
    HashableRLP,
)

from rlp.sedes import (
    big_endian_int, binary, boolean, text,
)

from hexbytes import (
    HexBytes,
)


from web3._utils.threads import (
    Timeout,
)
from web3.exceptions import (
    TransactionNotFound,
)

import operator

from eth_utils import (
    add_0x_prefix,
    to_checksum_address,
    is_address,
    big_endian_to_int,
    decode_hex,
    encode_hex,
    int_to_big_endian,
    is_boolean,
    is_bytes,
    is_hex,
    is_integer,
    is_list_like,
    remove_0x_prefix,
    to_hex,
    to_wei,
    from_wei,
)


from eth_utils.curried import (
    apply_formatter_at_index,
    apply_formatter_if,
    apply_formatter_to_array,
    apply_formatters_to_dict,
    apply_one_of_formatters,
)

from web3._utils.formatters import(
    hex_to_integer,
    integer_to_hex,
    is_array_of_dicts,
    is_array_of_strings,
    remove_key_if,
)

from web3._utils.encoding import (
    #bytes_to_ascii,
    trim_hex,
)

import codecs


from .fsn_utils import *
  


VALID_TRANSACTION_PARAMS = [
    'from',
    'to',
    'gas',
    'gasPrice',
    'value',
    'data',
    'nonce',
    'chainId',
]


def bytes_to_ascii(value):
    return codecs.decode(value, 'ascii')


to_ascii_if_bytes = apply_formatter_if(is_bytes, bytes_to_ascii)
to_integer_if_hex = apply_formatter_if(is_string, hex_to_integer)
block_number_formatter = apply_formatter_if(is_integer, integer_to_hex)

is_false = partial(operator.is_, False)

is_not_false = complement(is_false)
is_not_null = complement(is_null)



@curry
def to_hexbytes(self, num_bytes, val, variable_length=False):
    if isinstance(val, (str, int, bytes)):
        result = HexBytes(val)
    else:
        raise TypeError("Cannot convert %r to HexBytes" % val)

    extra_bytes = len(result) - num_bytes
    if extra_bytes == 0 or (variable_length and extra_bytes < 0):
        return result
    elif all(byte == 0 for byte in result[:extra_bytes]):
        return HexBytes(result[extra_bytes:])
    else:
        raise ValueError(
            "The value %r is %d bytes, but should be %d" % (
                result, len(result), num_bytes
            )
        )


@curry
def fill_nonce(web3, transaction):
    if 'from' in transaction and 'nonce' not in transaction:
        return assoc(
            transaction,
            'nonce',
            web3.fsn.getTransactionCount(
                transaction['from'],
                block_identifier='pending'))
    else:
        return transaction



TRANSACTION_DEFAULTS = {
#    'value': 0,
#    'data': b'',
    #'gas': lambda web3, tx: web3.fsn.estimateGas(tx),
    #'gasPrice': lambda web3, tx: web3.fsn.generateGasPrice(tx) or web3.fsn.gasPrice,
    'chainId':   None,
    'gas':       300000,
}

    

def estimateGas(transaction):
    return to_wei(21,'gwei')    # value from MyFusionWallet JS code
            


@curry
def fill_transaction_defaults(web3,transaction, chain=None):
    """
    if web3 is None, fill as much as possible while offline
    """
    defaults = {}
    for key, default_getter in TRANSACTION_DEFAULTS.items():
        if key not in transaction:
            if callable(default_getter):
                if web3 is not None:
                    default_val = default_getter(web3, transaction)
                else:
                    raise ValueError("You must specify %s in the transaction" % key)
            else:
                default_val = default_getter
            defaults[key] = default_val
            if key=='chainId':
                defaults['chainId'] = chain
        if 'gasPrice' not in defaults:
            defaults['gasPrice'] = estimateGas(transaction)
        if 'gas' not in defaults:
            defaults['gas'] = TRANSACTION_DEFAULTS['gas']
        if 'to' in transaction:
            if is_address(transaction['to']):
               transaction['to'] = to_checksum_address(transaction['to'])
            else:
               raise TypeError(
                  'Error: Bad \'to\' field in sendRawTransaction'
               )
        if is_address(transaction['from']):
            transaction['from'] = to_checksum_address(transaction['from'])
        else:
            raise TypeError(
                'Error: Bad \'from\' field in sendRawTransaction'
            )
    
    return merge(defaults, transaction)




def wait_for_transaction_receipt(web3, txn_hash, timeout=30, poll_latency=0.1):
    with Timeout(timeout) as _timeout:
        while True:
            try:
                txn_receipt = web3.fsn.getTransactionReceipt(txn_hash)
            except TransactionNotFound:
                txn_receipt = None
            if txn_receipt is not None and txn_receipt['blockHash'] is not None:
                break
            _timeout.sleep(poll_latency)
    return txn_receipt



def SignTx(Tx_tosign, account):
    
    
    defaultChainId = Tx_tosign['chainId']
    
    oldinput = Tx_tosign['input']
    rawTx = dict(Tx_tosign)
    
    Tx_tosign['data'] = oldinput
    
    del Tx_tosign['input']
    del Tx_tosign['v']
    del Tx_tosign['r']
    del Tx_tosign['s']
    del Tx_tosign['hash']
    
    
    Tx_signed = account.sign_transaction(Tx_tosign)

    
    rawTx['r'] = hex(Tx_signed['r'])
    rawTx['s'] = hex(Tx_signed['s'])
    rawTx['v'] = hex(Tx_signed['v'])
    rawTx['input'] = oldinput
    rawTx['data']  = oldinput
    rawTx['chainId'] = defaultChainId
    
    return rawTx


######################################################################################################
#
#   GenNotation
#

GENNOTATION_DEFAULTS = {
    #'gasPrice': 100000000000000000,
    #'gas':     1000,
    'chainId':  None,
}

GENNOTATION_FORMATTERS = {
    'from': to_checksum_address,
    'nonce': to_hex_if_integer_or_ascii,
    'chainId': to_hex_if_integer_or_ascii,
    'gas': to_hex_if_integer_or_ascii,
    'gasPrice': to_hex_if_integer_or_ascii,
}

VALID_GENNOTATIONTX_PARAMS = [
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'chainId',
]

REQUIRED_GENNOTATIONTX_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'chainId',
]

def buildGenNotationTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in GENNOTATION_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_GENNOTATIONTX_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_gennotation_formatter(transaction_merged)
    
    assert_check_gen_notation_params(transaction_new)
    
    return transaction_new


unsigned_gennotation_formatter = apply_formatters_to_dict(GENNOTATION_FORMATTERS)

def assert_check_gen_notation_params(gennotation_params):
    for param in gennotation_params:
        if param not in VALID_GENNOTATIONTX_PARAMS:
            raise ValueError('{} is not a valid gen notation parameter'.format(param))

    for param in REQUIRED_GENNOTATIONTX_PARAMS:
        if param not in gennotation_params:
            raise ValueError('{} is required as a gen notation parameter'.format(param))

