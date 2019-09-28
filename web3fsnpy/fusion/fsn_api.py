#!/usr/bin/env python3
#
"""
    Class to interact with Fusion's api
"""
#
#
import os
import sys
import urllib.request
import json
import datetime

#import pdb ; pdb.set_trace()

class apiWallet:

    public_key = None
    url_api = None
    api = None


    def __init__(self,pub_key):
    
        self.public_key = pub_key
        
        url_api = 'https://api.fusionnetwork.io/balances/' + pub_key
        
        try:
            response = urllib.request.urlopen(url_api)
        except:
            return('-1')
        
        apifsn = response.read()
        apifsn = apifsn.decode("utf-8")
        self.api = json.loads(apifsn)
        
        
    def fsnapi_swaps(self):
        
        #print('ORIG ',self.api[0])
        api_dict = dict(self.api[0])
        #print('DICT ',api_dict)
        balanceInfo = api_dict['balanceInfo']
       
        
        return balanceInfo
    
    
    
    
    
    
    
