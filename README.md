# web3fsnpy

The Python3 implementation of FUSION’s Web3 functions


# Quick start

Install some dependencies (you will need > python3.6) :-

#> sudo apt install python3 python3-pip

#> sudo pip3 install web3fsnpy  (or pip3 install web3fsnpy --user if you want to install a username only copy)

You can find some example python programs at https://github.com/FUSIONFoundation/web3fsnpy/tree/master/fusion_tests 

designed to demonstrate the API's functionality. These will be added to as new functions are developed.

You will probably need to set the environmental variable FSN_PRIVATE_KEY to be able to use any write transaction methods. 

Get your private key from your Fusion wallet (click on 'View details') and then :-

#> export FSN_PRIVATE_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXX

To update (frequent updates available) just type :-

#> sudo pip3 install --update web3fsnpy  (or pip3 install --update web3fsnpy --user)



# Developer setup

For a developer setup, you will likely need to install Ethereum's web3.py according to the instructions at https://github.com/ethereum/web3.py

Then install web3fsnpy :-

#> git clone https://github.com/FUSIONFoundation/web3fsnpy.git

The dependencies are listed in the file requirements.txt


Now you need to update the PYTHONPATH environmental variable to your .bashrc file assuming that you are in the folder web3fsnpy :-

#> echo "export PYTHONPATH=$PYTHONPATH:$PWD">>~/.bashrc

Now restart your shell to activate the PYTHONPATH. You can now try some of the scripts in the folder fusion_tests to make sure that it is working.

It is best practice to operate within a virtualenv when modifying code, so as to isolate dependency issues.


# Bugs and enhancements

Please report bugs or suggest enhancements by creating a git pull request to https://github.com/FUSIONFoundation/web3fsnpy



# INTRODUCTION


By creating a pythonic version of the JavaScript web3.js API for it's blockchain, Fusion Foundation has made it possible
to easily unlock all the functionality that makes Fusion unique. With only single function calls, a user can now create assets, send tokens, or generate time locks to unlock the time value of assets and other cryptocurrencies locked in to Fusion's blockchain.

Because python is easy to learn and is platform independent, every user now has access to Fusion's features and can combine them with every other python module, including math and scientific modules, specialist financial modules, to assist them in developing feature rich applications. 


# Fusion's developer community

You can easily interact with other Fusion developers through its Telegram channel https://t.me/FsnDevCommunity.

Here you can discuss new project ideas, or seek technical assistance from other developers and the Fusion technical team.

If you have some code that you would like to add to the repository, please create a pull request to https://github.com/FUSIONFoundation/web3fsnpy 

and let's create a powerful resource for all developers.

Don't be a stranger!



