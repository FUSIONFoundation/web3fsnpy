
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

from .fsn_timelocks import (
    to_hex_if_datestring,
)


from .fsn_utils import *
        

from datetime import datetime, timedelta
from dateutil import tz

    
##########################################################################################################################
#
#  Buy Ticket
#

BUYTICKET_DEFAULTS = {
    #'gasPrice':         1000000000000000,
    #'gas':              10000,
    'chainId':          None,
}


BUYTICKET_FORMATTERS = {
    'from':             to_checksum_address,
    'nonce':            to_hex_if_integer_or_ascii,
    'gas':              to_hex_if_integer_or_ascii,
    'gasPrice':         to_hex_if_integer_or_ascii,
    'chainId':          to_hex_if_integer_or_ascii,
}

VALID_BUYTICKET_PARAMS = [
    'from',
    'nonce',
    'gas',
    'gasPrice',
    'chainId',
]

REQUIRED_BUYTICKET_PARAMS = [
    'from',
    'nonce',
    #'gas',
    #'gasPrice',
    'chainId',
]



def buildBuyTicketTx(transaction, defaultChainId):
    defaults = {}
    alreadygot = {}
    for key, default_val in BUYTICKET_DEFAULTS.items():
        if key not in transaction:
            defaults[key] = default_val
    for key, val in transaction.items():
        if key in VALID_BUYTICKET_PARAMS:
            alreadygot[key] = transaction[key]
            
    transaction_merged = merge(defaults, alreadygot)
    transaction_merged['chainId'] = defaultChainId
    transaction_new = unsigned_buyticket_formatter(transaction_merged)
    
    assert_check_buyticket_params(transaction_new)
    
    return transaction_new


unsigned_buyticket_formatter = apply_formatters_to_dict(BUYTICKET_FORMATTERS)


def assert_check_buyticket_params(buyticket_params):
    for param in buyticket_params:
        if param not in VALID_BUYTICKET_PARAMS:
            raise ValueError('{} is not a valid buy ticket parameter'.format(param))

    for param in REQUIRED_BUYTICKET_PARAMS:
        if param not in buyticket_params:
            raise ValueError('{} is required as an buy ticket parameter'.format(param))


