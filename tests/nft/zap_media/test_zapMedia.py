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
def wallets(w3, eth_tester):
    wallets = [w3.eth.account.from_key(pk) for pk in utils.hh_private_keys]

    for i, wallet in enumerate(wallets):
        w3.eth.send_transaction({
            'to': wallet.address,
            'from': eth_tester.get_accounts()[i],
            'value': 12
        })
    return wallets


def test_accounts(w3, eth_tester, wallets):
    wallet = wallets[0]
    assert w3.eth.get_balance(wallet.address) == 12
    assert (wallet.key).hex() == "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    # assert account1.privateKey




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
    zap_media.w3 = w3
    zap_media.contract = w3.eth.contract(address=zap_media_address, abi=abi)
    return zap_media
    
    


def test_initial_connection(zap_media):
    assert zap_media.w3.isConnected()

# def test_chainId_connection(zap_media_contract):
#     assert zap_media_contract.address == "5"

def test_zap_media_address(zap_media,zap_media_contract):
    assert zap_media.address
    assert zap_media.address == zap_media_contract.address

def test_total_supply(zap_media):
    assert zap_media.totalSupply().call() == 0



def test_media_mint(w3, zap_media):

    # assert w3.eth.accounts[1] == utils.wallets[0].address
    before_mint = zap_media.totalSupply().call()
    assert before_mint == 0

    tokenURI = "Test CarZ"
    metadataURI = "Test CarMZ"

    mediaData = {
        "tokenURI": tokenURI,
        "metadataURI": metadataURI,
        "contentHash": Web3.toBytes(text=tokenURI),
        "metadataHash": Web3.toBytes(text=metadataURI)
    };

    zapTokenBscAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    ownerWalletAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    recipientAddress = "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"

    bidShares = {
        "creator" : {"value":90000000000000000000},
        "owner" : {"value":5000000000000000000},
        "collaborators": [],
        "collabShares": []
    }
    account_1 = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    # account_2 = "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"

    # tx = zap_media.mint(mediaData, bid).
    zap_media.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    nonce = zap_media.w3.eth.getTransactionCount(utils.wallets[0].address)

    tx = {
        'chainId':61,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': zap_media.w3.toWei('50', 'gwei'),
    }

    tx_hash = zap_media.mint(mediaData, bidShares).transact({
        'from': w3.eth.accounts[1],
    })
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    after_mint = zap_media.totalSupply().call()
    assert after_mint == before_mint + 1

# 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b
# 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b