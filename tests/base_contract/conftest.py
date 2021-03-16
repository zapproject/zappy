from unittest.mock import MagicMock, patch
import pytest
import re
import src.base_contract.base_contract as base_contract

"""Default setup"""

MOCK_ABI = {
    'TEST_ARTIFACT': {'abi': [], 'networks':
        {'1': {'address': '0xmainnet'},
         '42': {'address': '0xkovan'},
         '31337': {'address': '0xdevnet'}}},
    'ZAPCOORDINATOR': {'abi': [], 'networks':
        {'1': {'address': '0xcoormainnet'},
         '42': {'address': '0xcoorkovan'},
         '31337': {'address': '0xcoordevnet'}}}
}


@pytest.fixture
def anyio_backend():
    """
    Ensures anyio uses the default, pytest-asyncio plugin
    for running async tests.
    """
    return 'asyncio'


@pytest.fixture
@patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True)
@patch('src.base_contract.Web3', autospec=True)
def instance(mock_Web3):
    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = MagicMock()
        return base_contract.BaseContract(artifact_name='TEST_ARTIFACT', web3=w3)
