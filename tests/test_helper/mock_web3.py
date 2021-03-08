import pprint
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import json
pp = pprint.PrettyPrinter(indent=4)

from web3 import Web3

class MockWeb3():

    def __init__(self, node_url: str = "http://127.0.0.1:8545"):
        self.node_url = node_url
        self.web3 = Web3(Web3.HTTPProvider(node_url))

    def getAbi(contract_name:str):
        base_path = os.path.dirname(os.path.abspath("./__file__"))
        artifacts_directory = "src/Artifacts"
        artifact_path = os.path.join(base_path, artifacts_directory, f"{contract_name.capitalize()}.json")
        with open("tests/test_helper/Arbiter.json") as f:
            artifact = json.load(f)
            return artifact['abi']

    def isConnected(self):
        return self.web3.isConnected()

    def pprint_dir(self):
        pp.pprint(dir(self.web3))

    def connectToContract(self, contract_name):
         contract_abi = getAbi(contract_name)
        #  return self.web3.eth.contract(addres:)




w3 = MockWeb3()
# print(w3.pprint_dir())
