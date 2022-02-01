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
        self.chainId = chainId
        try:
            self.w3 = Web3(Web3.HTTPProvider(provider_uri[chainId]))

            f = open("config.json", "r")
            data = json.load(f)
            self.privateKey = data["privateKey"]
        except Exception as e:
            print(e)
        

    def get_contract_info(self, contract_name:str):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(curr_dir, f'artifacts/{contract_name.lower()}.json'), 'r') as f:
            return json.load(f)
    
    def connect_to_contract(self, contract_name:str):
        try:
            curr_dir = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(curr_dir, f'artifacts/{contract_name.lower()}.json'), 'r') as f:
                artifact = json.load(f)
            self.address = artifact[self.chainId]['address']
            self.abi = artifact['abi']
            self.contract = self.w3.eth.contract(address=self.address, abi=self.abi)
        except Exception as e:
            raise e
    

    # Async class methods
    async def get_contract(self):
        contract_address = await self.coordinator.functions.getContract(self.name.upper()).call()
        self.contract = self.w3.eth.contract(
            address=contract_address, abi=self.artifact['abi'])
        return contract_address

    def get_contract_owner(self):
        return self.loop.run_until_complete(self.__async__get_contract_owner())

    async def __async__get_contract_owner(self):
        contract_owner = await self.contract.functions.owner().call()
        return contract_owner

    # Builds transactions for write contract calls
    def buildTransaction(self, function):
        nonce = self.w3.eth.get_transaction_count("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")

        return function.buildTransaction({
            'chainId': int(self.chainId),
            'gas': 1400000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': 0,
        })

    # Bundles sending transaction
    def sendTransaction(self, transaction, privateKey):
        signed_txn = self.w3.eth.account.sign_transaction(transaction, privateKey)

        return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# base_contract = BaseContract("signer")

