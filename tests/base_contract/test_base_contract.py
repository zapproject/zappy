import os
import sys
from unittest import mock
import unittest
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from unittest.mock import MagicMock, patch


from src.BaseContract.base_contract import BaseContract
from tests.test_helper.mc import MockContract



def test_instance():


    mock_w3 = MagicMock()
    mock_w3.eth.contract.side_effect = [MockContract('zapcoordinator'), MockContract('registry')]

    instance = BaseContract(artifact_name="REGISTRY", web3=mock_w3)
    contract = instance.contract

    # test if instantiated
    assert instance
    
    # test name
    assert "REGISTRY" == contract.name
    assert "registry" != contract.name
    assert "ARBITER" != contract.name
