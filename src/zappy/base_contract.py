import os
# import sys
# sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))
import json

from web3 import Web3

from .providers import provider_uri


class BaseContract:

    """
    Base Class to create Contract Classes with.
    Base class contains method(s) to get contract address and abi based on chainID
   
    """

    def __init__(self, chain_id: str = '31337', custom_contract_address: str = ""):
        """
        Contract classes are instantiated through the given chainId and a config.json which contains the private_key of the user.
        That in turn generated the public_address.


        """

        self.chain_id = chain_id
        self.address = custom_contract_address
        try:
            self.w3 = Web3(Web3.HTTPProvider(provider_uri[chain_id]))    
            with open("config.json", "r") as f:
                data = json.load(f)
            self.private_key = data["privateKey"]

            wallet = self.w3.eth.account.from_key(self.private_key)
            self.public_address = wallet.address        
        except Exception as e:
            print(e)            


    def get_contract_info(self, contract_name:str):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        artifact_path = os.path.join(curr_dir, f'artifacts/{contract_name.lower()}.json')
        with open(artifact_path, 'r') as f:
            return json.load(f)
    
    def connect_to_contract(self, contract_name:str):
        try:
            artifact = self.get_contract_info(contract_name)

            if self.address == "":
                self.address = artifact[self.chain_id]['address']
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
    

    # Builds transactions for write contract calls
    def send_transaction(self, function, **kwargs):
        default_tx_params = {
            'chainId': int(self.chain_id),
            'gas': 1400000, # how much gas you're paying. this is the gas cap. most we're willing to spend
            'gasPrice': self.w3.eth.gas_price, # how much gas we're actually going to pay. typically 40 gwei.
            'nonce': self.w3.eth.get_transaction_count(self.public_address),
        }

        tx_params = {**default_tx_params, **kwargs}
        tx = function.buildTransaction(tx_params)
        signed_txn = self.w3.eth.account.sign_transaction(tx, self.private_key)
        return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)


# b = BaseContract()
# art = b.get_contract_info()
# print(art)
