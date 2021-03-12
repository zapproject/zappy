import pprint
from unittest.mock import MagicMock
import json
import os
import sys

from web3 import (
    EthereumTesterProvider,
    Web3,
)

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

pp = pprint.PrettyPrinter(indent=4)
class MockContract():

    def __init__(self, contract_name: str, use_hardhat: bool = False, node_url: str = "http://127.0.0.1:8545"):
        self.node_url = node_url
        self.hardhat = use_hardhat
        self.provider = Web3.HTTPProvider(
            self.node_url) if use_hardhat else EthereumTesterProvider()
        self.w3 = Web3(self.provider)
        self.artifacts = self.getArtifact(contract_name)
        self.abi = self.artifacts['abi']
        self.list_of_functions = self.get_contract_functions(self.abi)
        self.contract = self.connectToContract(contract_name) if use_hardhat else MagicMock()

        if not self.hardhat:
            self.contract.address = f"0x{contract_name}"

    def grab_function_name(self, dct):
        name = dct.get('name')
        if name:
            return name

    def get_contract_functions(self, abi):
        return list(map(self.grab_function_name, abi))

    def getArtifact(self, contract_name: str):
        base_path = os.path.dirname(os.path.abspath("./__file__"))
        artifacts_directory = "src/Artifacts/contracts"
        artifact_path = os.path.join(
            base_path, artifacts_directory, f"{contract_name.capitalize()}.json")
        with open(artifact_path) as f:
            artifact = json.load(f)
            return artifact

    def connectToContract(self, contract_name):
        artifacts = self.getArtifact(contract_name)
        contract_abi = artifacts['abi']
        contract_address = artifacts['networks'][str(
            self.w3.eth.chain_id)]['address']
        contract = self.w3.eth.contract(
            address=contract_address, abi=contract_abi)
        return contract

    def list_of_functions(self):
        return dir(self.contract.functions)

    def mock_func_and_return_value(self, function_name, rv):
        try:
            func = self.contract.get_function_by_name(function_name)
            if func:
                setattr(self.contract.functions, function_name, MagicMock(return_value=rv))
        except Exception as e:
            print(e)
    
# example of use:
  
# registry = MockContract('registry') # hardhat not used
# registry.mock_func_and_return_value('initiateProvider', 'woof')
# registry.contract.functions.initiateProvider()

# rh = MockContract('registry', use_hardhat=True) # hardhat used