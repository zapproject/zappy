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
            self.contract.name = contract_name.upper()

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

# registry_artifacts = registry.artifacts
# registry_abi = registry.abi


# web3 = registry.w3
# accounts = web3.eth.accounts

# # print(accounts)
# testProvider = {
#     'publicKey': 123,
#     'title': 'testProvider',
#     'endpointParams': ['p1.md', 'p2.json'],
#     'markdownFile': 'https://raw.githubusercontent.com/mxstbr/markdown-test-file/master/TEST.md',
#     'jsonFile': ' https://gateway.ipfs.io/ipfs/QmaWPP9HFvWZceV8en2kisWdwZtrTo8ZfamEzkTuFg3PFr',
#     'endpoint': 'testEndpoint',
#     'curve': [3, 0, 2, 1, 100],
#     'emptyBroker': '0x0000000000000000000000000000000000000000'
# }

# key = testProvider['publicKey']
# title = Web3.toBytes(text=testProvider['title'])


# ep = testProvider['endpoint']
# term = testProvider['curve']
# broker = testProvider['emptyBroker']
# account = Web3.toChecksumAddress(accounts[-1])


# tx_hash = registry.contract.functions.initiateProvider(
#     key, title).transact({'from': account})
# # ==> HexBytes('0x3619c6ef87d5ea65cbeb5dabfc8bea2afc74cfd4c0faee5ff80a5eb0c37dd2cf')

# receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# # ==> AttributeDict({'transactionHash': HexBytes('0x3619c6ef87d5ea65cbeb5dabfc8bea2afc74cfd4c0faee5ff80a5eb0c37dd2cf'),
#     # 'transactionIndex': 0,
#     # 'blockHash': HexBytes('0x26bae4af46947683dd53a45dde08f78753d8a349f59d53908dfcacf59343e89f'),
#     # 'blockNumber': 97,
#     # 'from': '0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199',
#     # 'to': '0xa513E6E4b8f2a923D98304ec87F64353C4D5C853',
#     # 'cumulativeGasUsed': 106669,
#     # 'gasUsed': 106669,
#     # 'contractAddress': None,
#     # 'logs': [AttributeDict({'removed': False,
#     #                         'logIndex': 0,
#     #                         'transactionIndex': 0,
#     #                         'transactionHash': HexBytes('0x3619c6ef87d5ea65cbeb5dabfc8bea2afc74cfd4c0faee5ff80a5eb0c37dd2cf'),
#     #                         'blockHash': HexBytes('0x26bae4af46947683dd53a45dde08f78753d8a349f59d53908dfcacf59343e89f'),
#     #                         'blockNumber': 97,
#     #                         'address': '0xa513E6E4b8f2a923D98304ec87F64353C4D5C853',
#     #                         'data': '0x',
#     #                         'topics': [HexBytes('0x96c4fc31a3e383225857c821101daf68248108597da8ddde0ac2b431eb9a16be'),
#     #                                 HexBytes(
#     #                             '0x0000000000000000000000008626f6940e2eb28930efb4cef49b2d1f2c9c1199'),
#     #                             HexBytes('0x7465737450726f76696465720000000000000000000000000000000000000000')]})],
#     # 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000008000000010000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000010000000010000000000000000100010400000000000000000000000000000000000000000000000000000000000800000000000008000000000002000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
#     # 'status': 1})

# tx_getProviderTitle = registry.contract.functions.getProviderTitle(
#     account).transact({'from': account})
# # => HexBytes('0xd942af74ece32cdba134a51de0be1f040a21e549a69f6a3d64e54b93a3213374')

# tx_getTitle = registry.contract.functions.getTitle(account).call()
# #  => b'testProvider\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


# # registry.contract.functions.initiateProviderCurve(Web3.toBytes(text=ep), term, broker).transact(
# #     {'from': Web3.toChecksumAddress('0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266')})

# tx_getProviderEP = registry.contract.functions.getProviderEndpoints(
#     account).call()
