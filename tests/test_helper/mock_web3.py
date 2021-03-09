from web3 import Web3
from unittest.mock import MagicMock
import json
import pprint
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

pp = pprint.PrettyPrinter(indent=4)


class MockWeb3():

    def __init__(self, node_url: str = "http://127.0.0.1:8545"):
        self.node_url = node_url
        # self.network_id = network_id
        self.web3 = Web3(Web3.HTTPProvider(node_url))

    def getArtifact(self, contract_name: str):
        base_path = os.path.dirname(os.path.abspath("./__file__"))
        artifacts_directory = "src/Artifacts/contracts"
        artifact_path = os.path.join(base_path, artifacts_directory, f"{contract_name.capitalize()}.json")
        with open(artifact_path) as f:
            artifact = json.load(f)
            return artifact

    def isConnected(self):
        return self.web3.isConnected()

    # def pprint_dir(self):
    #     pp.pprint(dir(self.web3))

    # def connectToContract(self, contract_name):
    def mockContract(self, contract_name):
        artifacts = self.getArtifact(contract_name)
        contract_abi = artifacts['abi']
        contract_address = artifacts['networks'][str(
            self.web3.eth.chain_id)]['address']
        contract = self.web3.eth.contract(
            address=contract_address, abi=contract_abi)
        mock_contract = MagicMock(name=contract_name, spec=contract)
        return mock_contract

        # return self.web3.eth.contract(address=contract_address, abi=contract_abi)
        # return self.web3.eth.contract(address=contract_abi)


w3 = MockWeb3()

registry = w3.connectToContract('registry')
