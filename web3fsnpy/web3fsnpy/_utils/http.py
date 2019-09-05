def construct_user_agent(class_name):
    from web3fsnpy import __version__ as web3fsnpy_version

    user_agent = 'Web3Fsn.py/{version}/{class_name}'.format(
        version=web3fsnpy_version,
        class_name=class_name,
    )
    return user_agent
