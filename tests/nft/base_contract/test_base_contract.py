import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))
from src.zappy.zapmedia import ZapMedia


# create Zap Media
zap_media = ZapMedia('31337')

def test_zap_media():
    assert zap_media.address == "0x3Ca8f9C04c7e3E1624Ac2008F92f6F366A869444"



# from unittest.mock import MagicMock, patch

# from src.BaseContract.base_contract import BaseContract


# MockContract = MagicMock(address="0x000000000000000000", name="MOCKCONTRACT")
# @patch('src.BaseContract.base_contract.Web3', autospec=True)
# def test_instance(mock_Web3):
#     # mock w3.eth.contract to return a mocked contract
#     w3 = MagicMock()
    
#     # set return value of Web3(HTTPProvider) to mocked w3 above
#     mock_Web3.HTTPProvider.return_value = w3
#     w3.eth.contract.return_value = MockContract
    
#     instance = BaseContract("ARBITER", mock_Web3)
#     assert instance

#     # w3.eth.contract = MagicMock(address="WOOFWOOF")
    
#     # print(dir(w3))
#     # # contract = 
#     # # print(w3.eth.contract())

#     # contract = w3.eth.contract()
#     # print(contract.address)
#     # print(contract)
    

# # test_instance()

    
    
    
#     instance = BaseContract('ARBITER', mock_Web3)
#     assert instance
