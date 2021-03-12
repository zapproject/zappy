import pprint
from web3 import Web3
import unittest
from unittest.mock import MagicMock
import json
import os
import sys

from tests.test_helper.helper import getArtifact, get_contract_functions
# from helper import getArtifact, get_contract_functions
# sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

pp = pprint.PrettyPrinter(indent=4)


class MockContract():
    
    def __init__(self, contract_name):
        self.name = contract_name.upper()
        self.address = f"0x{contract_name}"
        self.artifacts = getArtifact(contract_name)
        self.abi = self.artifacts['abi']
        self.list_of_functions = get_contract_functions(self.abi)

    def mock_func_and_return_value(self, function_name, rv):
        try:
            if function_name in self.list_of_functions:
                setattr(self, function_name, MagicMock(return_value=rv))
        except Exception as e:
            print(e)

