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
    wallets = [w3.eth.account.from_key(pk) for pk in utils.hh_private_keys]

    for i, wallet in enumerate(wallets):
        w3.eth.send_transaction({
            'to': wallet.address,
            'from': eth_tester.get_accounts()[i],
            'value': 100000000000000000000
        })
    return wallets


def test_accounts(w3, eth_tester, wallets):
    wallet = wallets[0]
    assert w3.eth.get_balance(wallet.address) == 100000000000000000000
    assert (wallet.key).hex() == "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    # assert account1.privateKey


@pytest.fixture
def zap_token_contract(eth_tester,w3):
    deploy_address = eth_tester.get_accounts()[0]
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
def zap_vault_contract(eth_tester,w3, zap_token_contract):
    deploy_address = eth_tester.get_accounts()[0]
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
def zap_market_contract(eth_tester,w3, zap_vault_contract):
    deploy_address = eth_tester.get_accounts()[0]
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
def auction_house_contract(eth_tester,w3, zap_token_contract, zap_market_contract):
    deploy_address = eth_tester.get_accounts()[0]
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
def zap_media_contract(eth_tester, w3):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = eth_tester.get_accounts()[0]
    # assert wallet.address == deploy_address
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
def media_factory_contract(eth_tester, w3, zap_market_contract, zap_media_contract):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = eth_tester.get_accounts()[0]
    # assert wallet.address == deploy_address
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
def zap_media_proxy_contract(eth_tester, w3, zap_market_contract, media_factory_contract):
    """
    Deploy contract using web3py EthereumTesterProvider.
    Don't need to separately run a local node.
    """

    deploy_address = eth_tester.get_accounts()[0]

    tx_hash_setMediaFactory = zap_market_contract.functions.setMediaFactory(media_factory_contract.address).transact({
    'from': deploy_address
    })
    w3.eth.wait_for_transaction_receipt(tx_hash_setMediaFactory, 180)

    args = ['TEST COLLECTION', 'TC', zap_market_contract.address, True, 'https://testing.com']

    tx_deploy_media = media_factory_contract.functions.deployMedia(*args).transact({'from': deploy_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_deploy_media, 180)
    # pp.pprint(tx_receipt)

    logs = media_factory_contract.events.MediaDeployed.getLogs()
    # assert len(logs) == 1

    event = logs[0]
    zap_media_proxy_address = event.args.mediaContract
    

    artifacts = utils.get_ABI_Bytecode('zapmedia')
    abi = artifacts['abi']
    bytecode = artifacts['bytecode']   

    # Create our contract class.
    zapMedia = w3.eth.contract(address=zap_media_proxy_address, abi=abi)

    tx_claim = zapMedia.functions.claimTransferOwnership().transact({'from': deploy_address})
    w3.eth.wait_for_transaction_receipt(tx_claim, 180)

    return zapMedia


@pytest.fixture
@patch('src.nft.base_contract.json', autospec=True)
def zap_media(mock_json, w3, zap_media_proxy_contract):
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

def test_initial_connection(zap_media):
    assert zap_media.w3.isConnected()

def test_chainId_connection(zap_media):
    assert zap_media.chainId == "61"

def test_zap_media_address(zap_media, zap_media_proxy_contract):
    assert zap_media.address == zap_media_proxy_contract.address

def test_name(zap_media):
    assert zap_media.name() == "TEST COLLECTION"

def test_symbol(zap_media):
    assert zap_media.symbol() == "TC"

def test_total_supply(zap_media):
    assert zap_media.totalSupply() == 0

def test_media_mint(w3, wallets, zap_media):
    # assert w3.eth.accounts[1] == utils.wallets[0].address
    before_mint = zap_media.totalSupply()
    assert before_mint == 0

    tokenURI = "Test CarZ"
    metadataURI = "Test CarMZ"

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

    after_mint = zap_media.totalSupply()
    assert after_mint == before_mint + 1

def test_media_mint2(w3, wallets, zap_media):
    # assert w3.eth.accounts[1] == utils.wallets[0].address
    before_mint = zap_media.totalSupply()
    assert before_mint == 0

    tokenURI = "Test CarZ"
    metadataURI = "Test CarMZ"

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

    after_mint = zap_media.totalSupply()
    assert after_mint == before_mint + 1

def test_media_set_bid(w3, wallets, zap_media, zap_market, zap_token_contract, zap_token):
    tokenURI = "https://test1"
    metadataURI = "http://test1"

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

    # nonce @ 0 ! 0
    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None
    print("Mint: ", receipt)

    zap_media.privateKey = wallets[1].key.hex()
    bidder = wallets[1].address

    bid = zap_media.makeBid(
        100,
        zap_token_contract.address,
        bidder,
        wallets[0].address,
        10
    )
    
    token_id = zap_media.totalSupply() - 1

    current_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    print(current_bid)
    assert current_bid[0] == 0
    assert current_bid[1] == '0x0000000000000000000000000000000000000000'
    assert current_bid[2] == '0x0000000000000000000000000000000000000000'
    assert current_bid[3] == '0x0000000000000000000000000000000000000000'
    assert current_bid[4][0] == 0

    # nonce @ 1 ! 1
    tx = zap_token.approve(zap_market.address, 100000000000000000000)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None
    print("Approve: ", receipt)

    # nonce @ 2 ! 0
    tx = zap_media.setBid(token_id, bid)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None
    print("Set BID: ",receipt)

    new_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    print(new_bid)
    assert new_bid[0] == bid["amount"]
