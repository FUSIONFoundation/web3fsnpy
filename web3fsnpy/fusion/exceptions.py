import datetime
import time

class _notConnected(Exception):
    pass

class NotRawTransaction(Exception):
    """
    Checks to see if we have a dict object rather than a raw transaction
    """
    pass
class BadSendingAddress(Exception):
    """
    Checks that the sending public address matches the account of the private key for unsigned transactions
    """
    pass
class PrivateKeyNotSet(Exception):
    """
    Checks that a private key was supplied for an unsigned transaction
    """
    pass
