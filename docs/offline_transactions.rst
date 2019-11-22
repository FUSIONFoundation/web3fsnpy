.. _OfflineTransactions:

Offline Transactions
====================

We can separate out the preparation of a transaction (sending FSN, or assets, creating Notations, timelocks, making swaps etc.) from the actual signing and sending of the transaction onto the blockchain. In this way it is possible for a different group of people to be responsible for the organising the transactions to those who have control of the wallets themselves, perhaps using more secure computers.

Here we show an example of how this is accomplished. The initial part is done using the optional *prepareOnly* flag in the function calls. The transaction dictionaries are written as JSON strings to a text file. This same text file could be sent to someone else and used to sign and send the transactions at a later time.

.. literalinclude:: ../../web3fsnpy/fusion_tests/fsnOfflineTransactions.py
   :language: python
   :lines: 42-127
