
from .fsn_utils import *
        
VALID_ASSETCREATE_PARAMS = [
    'from',
    'gas',
    'gasPrice',
    'nonce',
    'chainId',
    'name',
    'symbol',
    'decimals',
    'total',
    'canChange',
]

ASSETCREATE_DEFAULTS = {
    'nonce':     None,
    'chainId':   None,
    'gas':       300000,
    'gasPrice':  2000000000,
}


ASSETCREATE_FORMATTERS = {
    'nonce': to_integer_if_hex,
    'gas': to_integer_if_hex,
    'gasPrice': to_integer_if_hex,
    'from': to_checksum_address,
    #'r': to_hexbytes(32, variable_length=True),
    #'s': to_hexbytes(32, variable_length=True),
    #'hash': to_hexbytes(32),
    #'v': apply_formatter_if(is_not_null, to_integer_if_hex),
    'name': to_ascii_if_bytes,
    'symbol': to_ascii_if_bytes,
    'decimals': to_integer_if_hex,
    'total': apply_formatter_if(is_not_null, to_integer_if_hex),
    'canChange': apply_formatter_if(is_integer, to_boolean),
}

assetcreate_formatter = apply_formatters_to_dict(ASSETCREATE_FORMATTERS)



def fsn_asset_create(transaction_dict):
    """
            Create a Fusion asset suitable for broadcast.
    """
            
    assert_valid_asset_create_params(transaction_dict)
        
    filled_transaction = pipe(
        transaction_dict,
        dict,
        partial(merge, ASSETCREATE_DEFAULTS),
        chain_id_to_v,
        apply_formatters_to_dict(ASSETCREATE_FORMATTERS),
    )

    return filled_transaction


def sign_asset_create(transaction_dict, private_key):
    """
    Sign an assetCreate using a local private key. Produces signature details
    and the hex-encoded transaction suitable for broadcast.
    """
        
        
    if not isinstance(transaction_dict, dict):
        raise TypeError("transaction_dict must be dict-like, got %r" % transaction_dict)

    account = Account.from_key(private_key)

    # allow from field, *only* if it matches the private key
    if 'from' in transaction_dict:
        if transaction_dict['from'] == account.address:
            sanitized_transaction = dissoc(transaction_dict, 'from')
        else:
            raise TypeError("from field must match key's %s, but it was %s" % (
                account.address,
                transaction_dict['from'],
            ))
    else:
        sanitized_transaction = transaction_dict

    # sign transaction
    (
        v,
        r,
        s,
        rlp_encoded,
    ) = sign_assetCreate_dict(private_key, sanitized_transaction)

    transaction_hash = keccak(rlp_encoded)

    return AttributeDict({
        'rawTransaction': HexBytes(rlp_encoded),
        'hash': HexBytes(transaction_hash),
        'r': r,
        's': s,
        'v': v,
    })




def sign_assetCreate_dict(private_key, transaction_dict):
    # generate RLP-serializable transaction, with defaults filled
    unsigned_assetcreate = serializable_unsigned_asset_create_from_dict(transaction_dict)

    assetcreate_hash = unsigned_assetcreate.hash()

    # detect chain
    if isinstance(unsigned_assetcreate, UnsignedAssetCreate):
        chain_id = None
    else:
        chain_id = unsigned_assetcreate.v

    # sign with private key
    account = keys.PrivateKey(bytes.fromhex(private_key))
    (v, r, s) = sign_transaction_hash(account, assetcreate_hash, chain_id)

    # serialize transaction with rlp
    encoded_assetcreate = encode_assetcreate(unsigned_assetcreate, vrs=(v, r, s))

    return (v, r, s, encoded_assetcreate)


def serializable_unsigned_asset_create_from_dict(assetcreate_dict):
    assert_valid_asset_create_params(assetcreate_dict)
    filled_transaction = pipe(
        assetcreate_dict,
        dict,
        partial(merge, ASSETCREATE_DEFAULTS),
        chain_id_to_v,
        apply_formatters_to_dict(ASSETCREATE_FORMATTERS),
    )
    if 'v' in filled_transaction:
        serializer = Transaction
    else:
        serializer = UnsignedAssetCreate
    return serializer.from_dict(filled_transaction)



def assert_valid_asset_create_params(assetcreate_params):
    for param in assetcreate_params:
        if param not in VALID_ASSETCREATE_PARAMS:
            raise ValueError('{} is not a valid asset create parameter'.format(param))



SIGNED_ASSETCREATE_FORMATTER = {
    'raw': HexBytes,
    'tx': assetcreate_formatter,
}

signed_assetcreate_formatter = apply_formatters_to_dict(SIGNED_ASSETCREATE_FORMATTER)


UNSIGNED_ASSETCREATE_FIELDS = (
    ('nonce', big_endian_int),
    ('gasPrice', big_endian_int),
    ('gas', big_endian_int),
    ('name', text),
    ('symbol', text),
    ('decimals', big_endian_int),
    ('total', big_endian_int),
    ('canChange', boolean),
)


def UnsignedAssetCreate(HashableRLP):
    fields = UNSIGNED_ASSETCREATE_FIELDS




def AssetCreate(HashableRLP):
    fields = UNSIGNED_ASSETCREATE_FIELDS + (
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
    )

def encode_assetcreate(unsigned_assetcreate, vrs):
    (v, r, s) = vrs
    chain_naive_assetcreate = dissoc(unsigned_assetcreate.as_dict(), 'v', 'r', 's')
    signed_assetcreate = AssetCreate(v=v, r=r, s=s, **chain_naive_assetcreate)
    return rlp.encode(signed_assetcreate)






