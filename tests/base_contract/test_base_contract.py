import os
import sys
from unittest import mock
import unittest
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from unittest.mock import MagicMock, patch


from src.BaseContract.base_contract import BaseContract


MockContract = MagicMock(abi = ['abi'], address="0x000000000000000000", name="MOCKCONTRACT")

@patch('src.BaseContract.base_contract.Web3', autospec=True)
def test_instance(mock_Web3):

    # mock instantaited web3
    mock_Web3.return_value = MagicMock()
    w3 = mock_Web3()

    # set return value of a contract
    w3.eth.contract.return_value = MockContract

    instance = BaseContract(artifact_name="ZAPCOORDINATOR")

    # test if instantiated
    assert instance
    
    # test name
    assert "ZAPCOORDINATOR" == instance.name
