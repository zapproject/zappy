from web3 import Web3
from unittest.mock import MagicMock
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

class MockContract():

    def __init__(self, contract_name:str, node_url: str = "http://127.0.0.1:8545"):
        self.node_url = node_url
        # self.network_id = network_id
        self.web3 = Web3(Web3.HTTPProvider(node_url))
        self.contract = self.connectToContract(contract_name)

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
            self.web3.eth.chain_id)]['address']
        contract = self.web3.eth.contract(
            address=contract_address, abi=contract_abi)
        return contract

    def list_of_functions(self):
        return dir(self.contract.functions)

    def mock_func_and_return_value(self, function_name, rv):
        try:
            func = self.contract.get_function_by_name(function_name)
            if func:
                # with patcurn_vh(f'{path}.{function_name}') as mock:
                #     mock.retalue = rv
                setattr(self.contract.functions, function_name, MagicMock(return_value=rv))                

        except Exception as e:
            print(e)
    


# registry = MockContract('registry')
# registry.mock_func_rv('initiateProvider', 'woof')
# print(registry.contract.functions.initiateProvider())