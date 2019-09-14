import datetime
import time



class NotRawTransaction(Exception):
    """
    Checks to see if we have a dict object rather than a raw transaction
    """
    pass
