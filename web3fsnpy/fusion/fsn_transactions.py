import math

from eth_utils.toolz import (
    assoc,
    curry,
    merge,
)

from eth_utils import (
    to_hex,
)


from web3._utils.threads import (
    Timeout,
)
from web3.exceptions import (
    TransactionNotFound,
)

from eth_utils import (
    add_0x_prefix,
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
)


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




TRANSACTION_DEFAULTS = {
#    'value': 0,
#    'data': b'',
#    'gas': lambda web3, tx: web3.fsn.estimateGas(tx),
#    'gasPrice': lambda web3, tx: web3.fsn.generateGasPrice(tx) or web3.fsn.gasPrice,
#    'nonce':     None,
    'chainId':   None,
    'gas':       300000,
    'gasPrice':  2000000000,
}





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


@curry
def fill_transaction_defaults(web3, transaction, chain=None):
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




