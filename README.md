# web3fsnpy

The Python3 implementation of FUSION’s Web3 functions

All installation instructions, description of functions and examples of usage are described on the [web3fsnpy readthedocs page](https://web3fsnpy.readthedocs.io/en/latest/index.html)

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

#> sudo pip3 install --upgrade web3fsnpy  (or pip3 install --upgarde web3fsnpy --user)



# Developer setup

For a developer setup, you will likely need to install Ethereum's web3.py according to the instructions at https://github.com/ethereum/web3.py

Then install web3fsnpy :-

#> git clone https://github.com/FUSIONFoundation/web3fsnpy.git

The dependencies are listed in the file requirements.txt


Now you need to update the PYTHONPATH environmental variable to your .bashrc file assuming that you are in the folder web3fsnpy :-

#> echo "export PYTHONPATH=$PWD:$PWD/web3fsnpy:$PYTHONPATH">>~/.bashrc

Now restart your shell to activate the PYTHONPATH. You can now try some of the scripts in the folder fusion_tests to make sure that it is working.

It is best practice to operate within a virtualenv when modifying code, so as to isolate dependency issues.


# Bugs and enhancements

Please report bugs or suggest enhancements by creating a git pull request to https://github.com/FUSIONFoundation/web3fsnpy



 






