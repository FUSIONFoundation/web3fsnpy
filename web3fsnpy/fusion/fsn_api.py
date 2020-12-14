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


    def __init__(self, pub_key, network=None):
        self.public_key = pub_key 
        
        if network == 'mainnet':
            self.url_api = 'https://api.fusionnetwork.io/'
        elif network == 'testnet':
            self.url_api = 'https://testnetapi.fusionnetwork.io/'
        else:
            raise TypeError('Error in fsnapi: network not set')
        
        self.assetInfoUrl = self.url_api + 'assets/verified?page=0&size=100&sort=desc' 
        
        
        self.pubkeyInfoUrl = self.url_api + 'search/'
        
        self.priceUrl = self.url_api + 'fsnprice'
        

    def fsnprice(self):
        try:
            response = urllib.request.urlopen(self.priceUrl)
        except:
            return('-1')
            
            
        apifsnPrice = response.read()
        apifsnPrice = apifsnPrice.decode("utf-8")
        priceInfo = json.loads(apifsnPrice)
        
        #print(pkInfo)
        
        
        return priceInfo
        
        
        
    def fsnapi_swaps(self, pageNo):
        
        swapurl = self.url_api + 'swaps2/all?page={}&size=10000&sort=desc'.format(pageNo) 
        
        
        try:
            response = urllib.request.urlopen(swapurl)
        except:
            return('-1')
        
        
        apifsn = response.read()
        apifsn = apifsn.decode("utf-8")
        swap_dict = json.loads(apifsn)
        
        #print(swap_dict)
        
        return swap_dict
    
    
    def fsnapi_swaps_pubkey(self, pubKey, pageNo):
        
        swapurl = self.url_api + 'swaps2/all?page={}&size=100&sort=desc&address='.format(pageNo) + pubKey 
        
        
        try:
            response = urllib.request.urlopen(swapurl)
        except:
            print('Exception in fsnapi_swaps_pubkey')
            return('-1')
        
        
        apifsn = response.read()
        apifsn = apifsn.decode("utf-8")
        swap_dict = json.loads(apifsn)
        
        #print(swap_dict)
        
        return swap_dict

    
    def fsnapi_swaps_target(self, pubKey, pageNo):
        
        swapurl = self.url_api + 'swaps2/all?page={}&size=100&sort=desc&target='.format(pageNo) + pubKey 
        #print(swapurl)
        
        try:
            response = urllib.request.urlopen(swapurl)
        except:
            return('-1')
        
        
        apifsn = response.read()
        apifsn = apifsn.decode("utf-8")
        swap_dict = json.loads(apifsn)
        
        #print(swap_dict)
        
        return swap_dict
    
    
    
    def fsnapiVerifiedAssetInfo(self):
        
        try:
            response = urllib.request.urlopen(self.assetInfoUrl)
        except:
            return('-1')
        
        
        apifsnAssets = response.read()
        apifsnAssets = apifsnAssets.decode("utf-8")
        assetInfo = json.loads(apifsnAssets)
        
        #print(assetInfo)
        
        
        return assetInfo
    
    
    def fsnapiAssetAllInfo(self, pageNo=0):
        
        assetAllInfoUrl = self.url_api + 'assets/all?page={}size=100&sort=desc'.format(pageNo)
        
        try:
            response = urllib.request.urlopen(assetAllInfoUrl)
        except:
            return('-1')
        
        
        apifsnAssets = response.read()
        apifsnAssets = apifsnAssets.decode("utf-8")
        assetInfo = json.loads(apifsnAssets)
        
        #print(assetInfo)
        
        
        return assetInfo
        
        
        
    def assetNameToAssetInfo(self, asset_name):
        
        assetInfo = self.fsnapiAssetInfo()
        
        for asset in assetInfo:
            if asset['shortName'] == asset_name:
                return asset
        return None
        
        
    
    def assetIdToAssetInfo(self, asset_Id):
        
        assetInfo = self.fsnapiAssetAllInfo()
        
        #print(assetInfo)
        
        for assetblock in assetInfo:
            asset = json.loads(assetblock['data'])
            
            if asset['AssetID'] == asset_Id:
                #print(asset)
                return asset
        return None


    
    def pubKeyInfo(self, pubKey):
        
        try:
            response = urllib.request.urlopen(self.pubkeyInfoUrl + pubKey)
        except:
            return('-1')
            
            
        apifsnPk = response.read()
        apifsnPk = apifsnPk.decode("utf-8")
        pkInfo = json.loads(apifsnPk)
        
        #print(pkInfo)
        
        
        return pkInfo
        
        
    def transactionNoTicketsDesc(self, pageNo):
        
        # e.g. https://testnetapi.fusionnetwork.io/transactions/all?page=18&returnTickets=notickets
    
        txPage = self.url_api + 'transactions/all?sort=desc&page={}&returnTickets=notickets'.format(pageNo)
        
        try:
            response = urllib.request.urlopen(txPage)
        except:
            return('-1')
    
        txInfo = response.read()
        txInfo = txInfo.decode("utf-8")
        txInfo = json.loads(txInfo)
        
        return txInfo
    
    
    def transactionsDesc(self, pageNo):
        
        txPage = self.url_api + 'transactions/all?sort=desc&page={}&size=100&field=height'.format(pageNo)
        print(txPage)
        
        try:
            response = urllib.request.urlopen(txPage)
        except:
            return('-1')
    
        txInfo = response.read()
        txInfo = txInfo.decode("utf-8")
        txInfo = json.loads(txInfo)
        
        return txInfo
    
    
    def takeSwapsDesc(self, pageNo):
        
        txInfo = self.transactionNoTicketsDesc(pageNo)
        #print('\n', txInfo)
        
        txTakeSwaps = []
        
        for tx in txInfo:
            if tx['fusionCommand'] == 'TakeMultiSwapFunc':
                txTakeSwaps.append(tx)
        
        return txTakeSwaps
