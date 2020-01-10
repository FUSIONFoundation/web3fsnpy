import operator

from binascii import (
    unhexlify
)

import json

from cytoolz import (
    pipe,
)

import rlp

from eth_account import (
    Account,
)

from eth_account._utils.signing import (
    sign_transaction_hash,
    sign_message_hash,
    to_eth_v,
)

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

from web3.parity import (
    Parity,
    ParityPersonal,
    ParityShh,
)
from web3.net import (
    Net,
)
from web3.testing import (
    Testing,
)
from web3.version import (
    Version,
)
from web3.geth import (
    Geth,
    GethAdmin,
    GethMiner,
    GethPersonal,
    GethShh,
    GethTxPool,
)

from web3._utils.validation import (
    assert_one_val,
)

from eth_rlp import (
    HashableRLP,
)

from rlp.sedes import (
    big_endian_int, binary, boolean, text,
)

from eth_keys import (
    KeyAPI,
    keys,
)


from eth_utils.curried import (
    apply_formatters_to_sequence,
    is_address,
    is_bytes,
    is_integer,
    is_null,
    is_string,
    remove_0x_prefix,
    text_if_str,
    to_checksum_address,
    apply_formatter_if,
    apply_formatters_to_dict,
    apply_one_of_formatters,
)

from eth_account._utils.transactions import (
    ChainAwareUnsignedTransaction,
    strip_signature,
    chain_id_to_v,
)

from hexbytes import (
    HexBytes,
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

def get_default_modules():
    return {
        "net": (Net,),
        "version": (Version,),
        "parity": (Parity, {
            "personal": (ParityPersonal,),
            "shh": (ParityShh,),
        }),
        "geth": (Geth, {
            "admin": (GethAdmin,),
            "miner": (GethMiner,),
            "personal": (GethPersonal,),
            "shh": (GethShh,),
            "txpool": (GethTxPool,),
        }),
        "testing": (Testing,),
    }


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
def to_hex_if_integer_or_ascii(val):
    if isinstance(val, int):
        result = hex(val)
    elif is_hex(val):
        result = val
    elif isinstance(val, str):
        result = hex(int(val))
    else:
        raise TypeError("Cannot convert %r to hex" % val)
    return result


def is_named_block(value):
    return value in {"latest", "earliest", "pending"}


def is_hexstr(value):
    return is_string(value) and is_hex(value)


def to_boolean(value=None, intval=None, hexstr=None, text=None):
    """
    Converts value to it's boolean representation.

    Values are converted this way:

     * value:
       * bytes: big-endian integer
       * big_endian_integer: 1=>True, 0=>False
     * hexstr: interpret hex as integer
     * text: interpret as string of digits, like '1' => True
    """
    assert_one_val(value, intval=intval, hexstr=hexstr, text=text)

    if intval is not None:
        if intval == 0:
            return(False)
        elif intval == 1:
            return(True)
        else:
            raise TypeError("Cannot convert int to boolean")
    elif hexstr is not None:
        if hexstr == '0x0':
            return(False)
        elif hexstr == '0x01':
            return(True)
        else:
            raise TypeError("Cannot convert hex number to boolean")
    elif text is not None:
        if text == '0':
            return(False)
        elif text == '1':
            return(True)
        else:
            raise TypeError("Cannot convert text string to boolean")
    elif isinstance(value, bytes):
        if value == b'0':
            return(False)
        elif value == b'1':
            return(True)
        else:
            raise TypeError("Cannot convert byte to boolean")
    elif isinstance(value, str):
        raise TypeError("Pass in strings with keyword hexstr or text")
    else:
        return bool(value)
    
    
def to_0hex(v):
    s = f"0x{v:02x}"
    return s



def hex2a(datastr):
    
    datastr = remove_0x_prefix(datastr)
    
    str = unhexlify(datastr)
    
    str = str.decode('utf8')
    
    str_dict = dict(json.loads(str))
    
    return str_dict

