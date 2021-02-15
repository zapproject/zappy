import pytest
import os
import json

import utils

#
## @notice: Function 'load_abi()' would be better tested within integration tests
#


class TestLoadAddress:

    @pytest.fixture
    def mocked_abi(self):
        self.abi_dict = {
            "contractName": "Arbiter", 
            "abi": [], 
            "random_key": "random_value",
            "networks": {
                "1": {
                    "random_key": "random_value",
                    "address": "0x131e22ae3e90f0eeb1fb739eaa62ea0290c3fbe1"
                    },
                "42": {
                    "address": "0x828ec5789af6cdd8af2059f48beeff2740c45362",
                    "random_key": "random_value"
                }
                }
            }
        return self.abi_dict

    
    def test_mock_abi(self, mocked_abi):
        assert type(mocked_abi) == dict
        

    def test_abi_address_return_type(self, mocked_abi):
        return_val = utils.load_address('Arbiter', '1', mocked_abi)
        assert type(return_val) == str
    
    def test_abi_address_return_type_fail(self, mocked_abi):
        return_val = utils.load_address('Arbiter', '1', mocked_abi)
        with pytest.raises(AssertionError):
            assert type(return_val) == dict


    def test_mainnet_address(self, mocked_abi):
        return_addr = utils.load_address('Arbiter', '1', mocked_abi)
        assert return_addr == '0x131e22ae3e90f0eeb1fb739eaa62ea0290c3fbe1'

    def test_kovan_address(self, mocked_abi):
        return_addr = utils.load_address('Arbiter', '42', mocked_abi)
        assert return_addr == '0x828ec5789af6cdd8af2059f48beeff2740c45362'

    def test_kovan_address_fail(self, mocked_abi):
        wrong_addr = utils.load_address('Arbiter', '1', mocked_abi)
        with pytest.raises(AssertionError):
            assert wrong_addr == '0x828ec5789af6cdd8af2059f48beeff2740c45362'