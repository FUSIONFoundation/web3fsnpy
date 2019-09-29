#!/usr/bin/env python3
#
"""
    Class to interact with Fusion's api. THESE METHODS ARE DEPRECATED
"""
#
#
import os
import sys
import urllib.request
import json
import datetime

#import pdb ; pdb.set_trace()

class fsnapi:

    public_key = None
    url_api = None
    api = None


    def __init__(self,pub_key):
    
        self.public_key = pub_key        
        self.url_api = 'https://api.fusionnetwork.io/'
        
        
        
    def fsnapi_swaps(self):
        
        swapurl = self.url_api + 'swaps2/all?page=0&size=1000&sort=desc' 
        
        
        try:
            response = urllib.request.urlopen(swapurl)
        except:
            return('-1')
        
        
        apifsn = response.read()
        apifsn = apifsn.decode("utf-8")
        swap_dict = json.loads(apifsn)
        
        #print(swap_dict)
        
       
        
        return swap_dict
    
    
    
    
    
    
    
