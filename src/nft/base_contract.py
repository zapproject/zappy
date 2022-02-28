import os
import sys
from tokenize import Number

# import web3
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))
# import asyncio
import json

# from typing import Any
from web3 import Web3
from src.nft.providers import provider_uri

import json
# from src.BaseContract.utils import Utils
# from src.Artifacts.src.index import Artifacts
#from portedFiles.types import base_contract_type


class BaseContract:

    """
    Base Class to create Contract Classes with.
    Base class contains method(s) to get contract address and abi based on chainID
   
    """

    def __init__(self, chainId: str = '31337'):
        """
        Contract classes are instantiated through the given chainId and a config.json which contains the private_key of the user.
        That in turn generated the public_address.


        """

        self.chainId = chainId
        try:
            self.w3 = Web3(Web3.HTTPProvider(provider_uri[chainId]))    
            with open("config.json", "r") as f:
                data = json.load(f)
            self.private_key = data["privateKey"]

            wallet = self.w3.eth.account.from_key(self.private_key)
            self.public_address = wallet.address        
        except Exception as e:
            print(e)            


    def get_contract_info(self, contract_name:str):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        print("curr_dir", curr_dir)
        with open(os.path.join(curr_dir, f'artifacts/{contract_name.lower()}.json'), 'r') as f:
            return json.load(f)
    
    def connect_to_contract(self, contract_name:str):
        try:
            # curr_dir = os.path.dirname(os.path.realpath(__file__))
            # with open(os.path.join(curr_dir, f'artifacts/{contract_name.lower()}.json'), 'r') as f:
            #     artifact = json.load(f)
            artifact = self.get_contract_info(contract_name)
            self.address = artifact[self.chainId]['address']
            self.abi = artifact['abi']
            self.contract = self.w3.eth.contract(address=self.address, abi=self.abi)
        except Exception as e:
            raise e


    def connect(self, private_key: str):
        """
        Method to help a user connect to an instance of a contract class.
        """
        self.private_key = private_key
        wallet = self.w3.eth.account.from_key(self.private_key)
        self.public_address = wallet.address
        return self
    

    # # Async class methods
    # async def get_contract(self):
    #     contract_address = await self.coordinator.functions.getContract(self.name.upper()).call()
    #     self.contract = self.w3.eth.contract(
    #         address=contract_address, abi=self.artifact['abi'])
    #     return contract_address

    # def get_contract_owner(self):
    #     return self.loop.run_until_complete(self.__async__get_contract_owner())

    # async def __async__get_contract_owner(self):
    #     contract_owner = await self.contract.functions.owner().call()
    #     return contract_owner

    # Builds transactions for write contract calls
    def send_transaction(self, function, **kwargs):
        default_tx_params = {
            'chainId': int(self.chainId),
            'gas': 1400000, # how much gas you're paying. this is the gas cap. most we're willing to spend
            'gasPrice': self.w3.eth.gas_price, # how much gas we're actually going to pay. typically 40 gwei.
            'nonce': self.w3.eth.get_transaction_count(self.public_address),
        }

        tx_params = {**default_tx_params, **kwargs}
        tx = function.buildTransaction(tx_params)
        signed_txn = self.w3.eth.account.sign_transaction(tx, self.private_key)
        return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)


b = BaseContract()
b.get_contract_info("zapmedia")