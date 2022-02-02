import os
from platform import platform
import sys
import eth_account
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import pytest

from web3 import (
    EthereumTesterProvider,
    Web3,
)
from eth_tester import EthereumTester

from unittest.mock import patch


import tests.nft.test_utilities as utils
from src.nft.ZapMedia import ZapMedia
from src.nft.ZapMarket import ZapMarket
from src.nft.ZapToken import ZapTokenBSC
from src.nft.AuctionHouse import AuctionHouse

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
def wallets(w3, eth_tester):
    for pk in utils.hh_private_keys:
        eth_tester.add_account(pk)

    all_wallets = eth_tester.get_accounts()
    wallets = all_wallets[10:]

    for i, wallet in enumerate(wallets):
        w3.eth.send_transaction({
            'to': wallet,
            'from': all_wallets[i],
            'value': 100000000000000000000
        })
    return wallets


@pytest.fixture
def zap_token_contract(eth_tester,w3, wallets):
    deploy_address = wallets[0]
    artifacts = utils.get_ABI_Bytecode('zaptokenbsc')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']

    # Create our contract class.
    ZapTokenBSC = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ZapTokenBSC.constructor().transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    
    return ZapTokenBSC(tx_receipt.contractAddress)

@pytest.fixture
def zap_vault_contract(eth_tester,w3, zap_token_contract, wallets):
    deploy_address = wallets[0]
    artifacts = utils.get_ABI_Bytecode('zapvault')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']

    # Create our contract class.
    ZapVaultContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ZapVaultContract.constructor(zap_token_contract.address).transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    zapVault = ZapVaultContract(tx_receipt.contractAddress)
    zapVault.functions.initializeVault(tx_receipt.contractAddress).transact({
        'from': deploy_address
    })
    
    return zapVault

@pytest.fixture
def zap_market_contract(eth_tester,w3, zap_vault_contract, wallets):
    deploy_address = wallets[0]
    artifacts = utils.get_ABI_Bytecode('zapmarket')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']

    # Create our contract class.
    ZapMarketContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ZapMarketContract.constructor(zap_vault_contract.address).transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.

    zapMarket = ZapMarketContract(tx_receipt.contractAddress)
    zapMarket.functions.initializeMarket(tx_receipt.contractAddress).transact({
        'from': deploy_address
    })
    
    platformFee = {
        "fee" : {"value":5000000000000000000}        
    }

    tx_hash_setFee = zapMarket.functions.setFee(platformFee).transact({
        'from': deploy_address,
    })

    w3.eth.wait_for_transaction_receipt(tx_hash_setFee, 180)
    return zapMarket


@pytest.fixture
def auction_house_contract(eth_tester,w3, zap_token_contract, zap_market_contract, wallets):
    deploy_address = wallets[0]
    artifacts = utils.get_ABI_Bytecode('auctionhouse')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']

    # Create our contract class.
    AuctionHouseContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = AuctionHouseContract.constructor(zap_token_contract.address, zap_market_contract.address).transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    ah = AuctionHouseContract(tx_receipt.contractAddress)

    ah.functions.initialize(zap_token_contract.address, zap_market_contract.address).transact({
        'from': deploy_address
    })
    
    return ah

@pytest.fixture
def zap_media_contract(eth_tester, w3, wallets):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = wallets[0]
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

    zapMedia = ZapMediaContract(tx_receipt.contractAddress)
    
    return zapMedia

@pytest.fixture
def media_factory_contract(eth_tester, w3, zap_market_contract, zap_media_contract, wallets):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = wallets[0]
    artifacts = utils.get_ABI_Bytecode('mediafactory')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']   

    # Create our contract class.
    MediaFactoryContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # issue a transaction to deploy the contract.

    tx_hash = MediaFactoryContract.constructor().transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.

    mediaFactory = MediaFactoryContract(tx_receipt.contractAddress)

    mediaFactory.functions.initialize(zap_market_contract.address, zap_media_contract.address).transact({
        'from': deploy_address
    })
    return mediaFactory


@pytest.fixture
def zap_media_proxy_contract(eth_tester, w3, zap_market_contract, media_factory_contract, wallets):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = wallets[0]

    tx_hash_setMediaFactory = zap_market_contract.functions.setMediaFactory(media_factory_contract.address).transact({
    'from': deploy_address
    })
    w3.eth.wait_for_transaction_receipt(tx_hash_setMediaFactory, 180)

    args = ['TEST COLLECTION', 'TC', zap_market_contract.address, True, 'https://testing.com']

    tx_deploy_media = media_factory_contract.functions.deployMedia(*args).transact({'from': wallets[0]})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_deploy_media, 180)
    # pp.pprint(tx_receipt)

    logs = media_factory_contract.events.MediaDeployed.getLogs()

    event = logs[0]
    zap_media_proxy_address = event.args.mediaContract
    

    artifacts = utils.get_ABI_Bytecode('zapmedia')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']   

    # Create our contract class.
    zapMedia = w3.eth.contract(address=zap_media_proxy_address, abi=abi)
    tx_claim = zapMedia.functions.claimTransferOwnership().transact({'from': wallets[0]})
    w3.eth.wait_for_transaction_receipt(tx_claim, 180)
    return zapMedia


@pytest.fixture
@patch('src.nft.base_contract.json', autospec=True)
def zap_media(mock_json, w3, zap_media_proxy_contract) -> ZapMedia:
    zap_media_address = zap_media_proxy_contract.address
    artifact = utils.get_artifact('zapmedia')
    artifact[str(w3.eth.chain_id)] = {'address': zap_media_address}
    mock_json.load.return_value = artifact

    abi = artifact['abi']

    zap_media = ZapMedia(str(w3.eth.chain_id))
    zap_media.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    zap_media.publicAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    zap_media.w3 = w3
    zap_media.contract = w3.eth.contract(address=zap_media_address, abi=abi)
    
    return zap_media
    

@pytest.fixture
@patch('src.nft.base_contract.json', autospec=True)
def zap_market(mock_json, w3, zap_market_contract):
    zap_market_address = zap_market_contract.address
    artifact = utils.get_artifact('zapmarket')
    artifact[str(w3.eth.chain_id)] = {'address': zap_market_address}
    mock_json.load.return_value = artifact

    abi = artifact['abi']

    zap_market = ZapMarket(str(w3.eth.chain_id))
    zap_market.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    zap_market.publicAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    zap_market.w3 = w3
    zap_market.contract = w3.eth.contract(address=zap_market_address, abi=abi)
    return zap_market

@pytest.fixture
@patch('src.nft.base_contract.json', autospec=True)
def zap_token(mock_json, w3, zap_token_contract):
    zap_token_address = zap_token_contract.address
    artifact = utils.get_artifact('zaptokenbsc')
    artifact[str(w3.eth.chain_id)] = {'address': zap_token_address}
    mock_json.load.return_value = artifact

    abi = artifact['abi']

    zap_token = ZapTokenBSC(str(w3.eth.chain_id))
    zap_token.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    zap_token.publicAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    zap_token.w3 = w3
    zap_token.contract = w3.eth.contract(address=zap_token_address, abi=abi)
    return zap_token

@pytest.fixture
@patch('src.nft.base_contract.json', autospec=True)
def auctionhouse(mock_json, w3, auction_house_contract):
    auction_house_address = auction_house_contract.address
    artifact = utils.get_artifact('auctionhouse')
    artifact[str(w3.eth.chain_id)] = {'address': auction_house_address}
    mock_json.load.return_value = artifact

    abi = artifact['abi']

    auctionhouse = AuctionHouse(str(w3.eth.chain_id))
    auctionhouse.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    auctionhouse.publicAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    auctionhouse.w3 = w3
    auctionhouse.contract = w3.eth.contract(address=auction_house_address, abi=abi)
    return auctionhouse


@pytest.fixture
def mint_token0(w3, zap_media):
    tokenURI = "https://tokenURI.com"
    metadataURI = "https://metadataURI.com"

    mediaData = {
        "tokenURI": tokenURI,
        "metadataURI": metadataURI,
        "contentHash": Web3.toBytes(text=tokenURI),
        "metadataHash": Web3.toBytes(text=metadataURI)
    }
    bidShares = {
        "creator" : {"value":90000000000000000000},
        "owner" : {"value":5000000000000000000},
        "collaborators": [],
        "collabShares": []
    }

    tx_hash = zap_media.mint(mediaData, bidShares)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)


def test_initial_connection(auctionhouse):
    assert auctionhouse.w3.isConnected()

def test_chainId_connection(auctionhouse):
    assert auctionhouse.chainId == "61"

def test_auctionhouse_address(auctionhouse, auction_house_contract):
    assert auctionhouse.address == auction_house_contract.address

