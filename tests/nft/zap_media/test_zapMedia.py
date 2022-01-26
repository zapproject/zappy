import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import pytest

from web3 import (
    EthereumTesterProvider,
    Web3,
)
from unittest.mock import patch

import tests.nft.test_utilities as utils
from src.nft.ZapMedia import ZapMedia

import pprint
pp = pprint.PrettyPrinter(indent=4)



@pytest.fixture
def tester_provider():
    return EthereumTesterProvider()


@pytest.fixture
def eth_tester(tester_provider):
    return tester_provider.ethereum_tester


@pytest.fixture
def w3(tester_provider):
    # chainId is 61
    return Web3(tester_provider)


@pytest.fixture
def zap_media_contract(eth_tester, w3):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = eth_tester.get_accounts()[0]
    wallet = utils.wallets[0]
    artifacts = utils.get_ABI_Bytecode('zapmedia')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']
    

    # Create our contract class.
    ZapMediaContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # issue a transaction to deploy the contract.
    tx_hash = ZapMediaContract.constructor().transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    return ZapMediaContract(tx_receipt.contractAddress)

@pytest.fixture
@patch('src.nft.base_contract.json', autospec=True)
def zap_media(mock_json, w3, zap_media_contract):
    zap_media_address = zap_media_contract.address
    artifact = utils.get_artifact('zapmedia')
    artifact[str(w3.eth.chain_id)] = {'address': zap_media_address}
    mock_json.load.return_value = artifact

    abi = artifact['abi']
    abi = artifact['abi']

    # return ZapMedia(str(w3.eth.chain_id))
    zap_media = ZapMedia(str(w3.eth.chain_id))
    zap_media.contract = w3.eth.contract(address=zap_media_address, abi=abi)
    return zap_media
    
    


def test_initial_connection(w3):
    assert w3.isConnected()

# def test_chainId_connection(zap_media_contract):
#     assert zap_media_contract.address == "5"

def test_zap_media_address(zap_media,zap_media_contract):
    print(dir(zap_media))
    assert zap_media.address
    assert zap_media.address == zap_media_contract.address

def test_total_supply(zap_media):
    assert zap_media.totalSupply().call() == 0

# 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b
# 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b
# def test_can_update_greeting(w3, foo_contract):
#     # send transaction that updates the greeting
#     tx_hash = foo_contract.functions.setBar(
#         "testing contracts is easy",
#     ).transact({
#         'from': w3.eth.accounts[1],
#     })
#     w3.eth.wait_for_transaction_receipt(tx_hash, 180)

#     # verify that the contract is now using the updated greeting
#     hw = foo_contract.caller.bar()
#     assert hw == "testing contracts is easy"


# def test_updating_greeting_emits_event(w3, foo_contract):
#     # send transaction that updates the greeting
#     tx_hash = foo_contract.functions.setBar(
#         "testing contracts is easy",
#     ).transact({
#         'from': w3.eth.accounts[1],
#     })
#     receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)

#     # get all of the `barred` logs for the contract
#     logs = foo_contract.events.barred.getLogs()
#     assert len(logs) == 1

#     # verify that the log's data matches the expected value
#     event = logs[0]
#     assert event.blockHash == receipt.blockHash
#     assert event.args._bar == "testing contracts is easy"