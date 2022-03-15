import os
from platform import platform
import sys
import eth_account
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import pytest

import web3
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
    zap_media.private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    zap_media.public_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
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
    zap_market.private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    zap_market.public_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
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
    zap_token.private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    zap_token.public_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
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
    auctionhouse.private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    auctionhouse.public_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
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


def test_initial_connection(auctionhouse: AuctionHouse):
    assert auctionhouse.w3.isConnected()

def test_chain_id_connection(auctionhouse: AuctionHouse):
    assert auctionhouse.chain_id == "61"

def test_auctionhouse_address(auctionhouse: AuctionHouse, auction_house_contract):
    assert auctionhouse.address == auction_house_contract.address

def test_create_auction(wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
    assert auctionhouse.w3.isConnected()
    assert zap_media.w3.isConnected()

    duration = 86400 #  number of seconds in 24 hours
    reservePrice = Web3.toWei(5, 'ether')

    zap_media.approve(auctionhouse.address, 0)
    approved_address = zap_media.get_approved(0)
    assert approved_address == auctionhouse.address

    params = [
        0, 
        zap_media.address, 
        duration, 
        reservePrice, 
        web3.constants.ADDRESS_ZERO, 
        0, 
        zap_token.address
        ]
    auctionhouse.create_auction(*params)

    # if curator is zero address, auction automatically starts.
    # if curator is the token owner, auction automatically starts.
    # if curator neither zero or token owner, the curator has to manually start the auction auctionhouse.startAuction().


    auction_info = auctionhouse.auctions(0);
    assert auction_info.token_details.token_id == 0
    assert auction_info.token_details.media_contract == zap_media.address
    assert auction_info.approved == True
    assert auction_info.duration == duration
    assert auction_info.curator_fee_percentage == 0
    assert auction_info.reserve_price == reservePrice
    assert auction_info.token_owner == wallets[0]
    assert auction_info.curator == web3.constants.ADDRESS_ZERO
    assert auction_info.auction_currency == zap_token.address


def test_create_auction_with_diff_curator(wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
    duration = 86400 #  number of seconds in 24 hours
    reservePrice = Web3.toWei(5, 'ether')

    zap_media.approve(auctionhouse.address, 0)

    params = [
        0, 
        zap_media.address, 
        duration, 
        reservePrice, 
        wallets[9], 
        0, 
        zap_token.address
        ]
    auctionhouse.create_auction(*params)

    auctionhouse.start_auction(0, True)

    auction_info = auctionhouse.auctions(0);
    assert auction_info.token_details.token_id == 0
    assert auction_info.token_details.media_contract == zap_media.address
    assert auction_info.approved == False
    assert auction_info.duration == duration
    assert auction_info.curator_fee_percentage == 0
    assert auction_info.reserve_price == reservePrice
    assert auction_info.token_owner == wallets[0]
    assert auction_info.curator == wallets[9]
    assert auction_info.auction_currency == zap_token.address

def test_start_auction(wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
    
    """
    Should start auction if the curator is not a zero address or curator is not the token owner.
    If auction was created with curator == Zero Address or the curator is the token owner, the auction is automatically started.
    We are mainly testing auction_info.approved == False, then assert auction_info.approved == True after starting the auction
    """

    duration = 86400 #  number of seconds in 24 hours
    reservePrice = Web3.toWei(5, 'ether')
    # curator = wallets[0]
    token_id = 0
    curator = wallets[9]

    zap_media.approve(auctionhouse.address, token_id)

    params = [
        token_id, 
        zap_media.address, 
        duration, 
        reservePrice, 
        curator, 
        0, 
        zap_token.address
        ]
    # create auction and assert
    auctionhouse.create_auction(*params)
    auction_info = auctionhouse.auctions(0)
    assert auction_info.approved == False
    assert auction_info.curator != web3.constants.ADDRESS_ZERO
    assert auction_info.curator == wallets[9]
    assert auction_info.auction_currency == zap_token.address

    
    # change user of auctionhouse. similar to ethersjs: .connect(signer)
    private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
    auctionhouse.connect(private_key_9)
    assert auctionhouse.public_address == wallets[9]
    assert auctionhouse.private_key == private_key_9
    

    # start_auction should reject if auctionId doesn't exist
    auctionhouse.start_auction(1234, True)
    auction_info = auctionhouse.auctions(1234)
    assert auction_info.approved == False


    # auction started by the curator - wallet[9] in this test
    auctionhouse.start_auction(0, True)
    auction_info = auctionhouse.auctions(0);
    approval_filter = auctionhouse.contract.events.AuctionApprovalUpdated.createFilter(fromBlock='0x0')
    assert approval_filter.get_new_entries()
    assert auction_info.approved == True


def test_starting_already_started_auction(wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
    duration = 86400 #  number of seconds in 24 hours
    reservePrice = Web3.toWei(5, 'ether')
    # curator = wallets[0]
    token_id = 0
    curator = wallets[9]

    zap_media.approve(auctionhouse.address, token_id)

    params = [
        token_id, 
        zap_media.address, 
        duration, 
        reservePrice, 
        curator, 
        0, 
        zap_token.address
        ]
    # create auction and assert
    auctionhouse.create_auction(*params)

    # change user of auctionhouse. similar to ethersjs: .connect(signer)
    private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
    auctionhouse.connect(private_key_9)

    tx = auctionhouse.start_auction(0, True)
    receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
    assert receipt['status'] == 1
    auction_info = auctionhouse.auctions(0);
    assert auction_info.approved == True

    # receipt status == 0 means EVM reverted
    tx = auctionhouse.start_auction(0, True)
    receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
    assert receipt['status'] == 0


def test_set_auction_reserve_price(wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
    # CREATE AUCTION

    duration = 86400 #  number of seconds in 24 hours
    reservePrice = Web3.toWei(5, 'ether')
    # curator = wallets[0]
    token_id = 0
    curator = wallets[9]

    zap_media.approve(auctionhouse.address, token_id)

    params = [
        token_id, 
        zap_media.address, 
        duration, 
        reservePrice, 
        curator, 
        0, 
        zap_token.address
        ]
    auctionhouse.create_auction(*params)

    # Should revert if not called by the curator or owner 
    
    # connect a different user
    private_key_8 = "0xdbda1821b80551c9d65939329250298aa3472ba22feea921c0cf5d620ea67b97"
    auctionhouse.connect(private_key_8)
    
    tx = auctionhouse.set_auction_reserve_price(0, 200)
    receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
    assert receipt['status'] == 0     # receipt status == 0 means EVM reverted
    
    # connect the curator
    private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
    auctionhouse.connect(private_key_9)
    tx = auctionhouse.set_auction_reserve_price(0, 200)
    receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
    assert receipt['status'] == 1

    auction_info = auctionhouse.auctions(0);
    assert auction_info.reserve_price == 200


class TestCreateBid:

    def test_reject_if_auction_id_does_not_exist(self, auctionhouse:AuctionHouse, zap_media:ZapMedia):

        bid_amount = 300
        
        # connect the curator
        private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
        auctionhouse.connect(private_key_9)
        tx = auctionhouse.create_bid(0, bid_amount, zap_media.address)
        receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
        assert receipt['status'] == 0

    def test_reject_media_contract_is_zero_address(self, wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
        # CREATE AUCTION
        duration = 86400 #  number of seconds in 24 hours
        reservePrice = Web3.toWei(5, 'ether')
        # curator = wallets[0]
        token_id = 0
        curator = wallets[9]

        zap_media.approve(auctionhouse.address, token_id)

        params = [
            token_id, 
            zap_media.address, 
            duration, 
            reservePrice, 
            curator, 
            0, 
            zap_token.address
            ]
        auctionhouse.create_auction(*params)
        
        bid_amount = 300

        # connect the curator
        private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
        auctionhouse.connect(private_key_9)
        tx = auctionhouse.create_bid(0, bid_amount, web3.constants.ADDRESS_ZERO)
        receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
        assert receipt['status'] == 0

    def test_reject_bid_less_than_reserve_price(self, wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
        # CREATE AUCTION
        duration = 86400 #  number of seconds in 24 hours
        reservePrice = Web3.toWei(5, 'ether')
        # curator = wallets[0]
        token_id = 0
        curator = wallets[9]

        zap_media.approve(auctionhouse.address, token_id)

        params = [
            token_id, 
            zap_media.address, 
            duration, 
            reservePrice, 
            curator, 
            0, 
            zap_token.address
            ]
        auctionhouse.create_auction(*params)
        bid_amount = 300
        # connect the curator
        private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
        auctionhouse.connect(private_key_9)
        auctionhouse.start_auction(0, True)
        
        tx = auctionhouse.create_bid(0, bid_amount-1, zap_media.address)
        receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
        assert receipt['status'] == 0
    
    def test_should_create_bid(self, wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
        private_key_1 = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

        # make sure wallets[1] has zap to bid with
        zap_token.transfer(wallets[1], Web3.toWei(7, 'ether'))
        zap_token.connect(private_key_1)
        zap_token.approve(auctionhouse.address, Web3.toWei(10,'ether'))

        # CREATE AUCTION
        duration = 86400 #  number of seconds in 24 hours
        reservePrice = Web3.toWei(5, 'ether')
        # curator = wallets[0]
        token_id = 0
        curator = wallets[9]

        zap_media.approve(auctionhouse.address, token_id)

        params = [
            token_id, 
            zap_media.address, 
            duration, 
            reservePrice, 
            curator, 
            0, 
            zap_token.address
            ]
        auctionhouse.create_auction(*params)
        # connect the curator
        private_key_9 = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
        auctionhouse.connect(private_key_9)
        auctionhouse.start_auction(0, True)
        auction_info = auctionhouse.auctions(0);
        print(auction_info)
        print(auction_info.auction_currency)
        print(zap_token.address)
        assert auction_info.approved == True
        
        bid_amount = Web3.toWei(6, 'ether')
        auctionhouse.connect(private_key_1)
        assert auctionhouse.private_key == private_key_1

        assert zap_token.balanceOf(auctionhouse.address) == 0 # before creating bid
        auctionhouse.create_bid(0, bid_amount, zap_media.address)
        assert zap_token.balanceOf(wallets[1]) == Web3.toWei(1, 'ether')
        assert zap_token.balanceOf(auctionhouse.address) == bid_amount # after creating bid


class TestCancelAuction:
    def test_cancel_auction(self, wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
        # CREATE AUCTION
        duration = 86400 #  number of seconds in 24 hours
        reservePrice = Web3.toWei(5, 'ether')
        # curator = wallets[0]
        token_id = 0
        curator = wallets[9]

        zap_media.approve(auctionhouse.address, token_id)

        params = [
            token_id, 
            zap_media.address, 
            duration, 
            reservePrice, 
            curator, 
            0, 
            zap_token.address
            ]
        auctionhouse.create_auction(*params)
        auctionhouse.cancel_auction(0)

        auction_info = auctionhouse.auctions(0);

        assert auction_info.amount == 0
        assert auction_info.duration == 0
        assert auction_info.first_bid_Time == 0
        assert auction_info.reserve_price == 0
        assert auction_info.curator_fee_percentage == 0
        assert auction_info.token_owner == web3.constants.ADDRESS_ZERO
        assert auction_info.bidder == web3.constants.ADDRESS_ZERO
        assert auction_info.curator == web3.constants.ADDRESS_ZERO
        assert auction_info.auction_currency == web3.constants.ADDRESS_ZERO

        assert zap_media.owner_of(0) == wallets[0]


class TestEndAuction:
    def test_revert_if_auction_not_completed(self, wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
        private_key_1 = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

        # make sure wallets[1] has zap to bid with
        zap_token.transfer(wallets[1], Web3.toWei(7, 'ether'))
        zap_token.connect(private_key_1)
        zap_token.approve(auctionhouse.address, Web3.toWei(10,'ether'))

        # CREATE AUCTION
        duration = 86400 #  number of seconds in 24 hours
        reservePrice = Web3.toWei(5, 'ether')
        # curator = wallets[0]
        token_id = 0
        curator = wallets[9]

        zap_media.approve(auctionhouse.address, token_id)

        params = [
            token_id, 
            zap_media.address, 
            duration, 
            reservePrice, 
            curator, 
            0, 
            zap_token.address
            ]
        auctionhouse.create_auction(*params)
        
        bid_amount = Web3.toWei(6, 'ether')
        auctionhouse.connect(private_key_1)
        auctionhouse.create_bid(0, bid_amount, zap_media.address)
        tx = auctionhouse.end_auction(0, zap_media.address)
        receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
        assert receipt['status'] == 0

    # def test_end_auction(self, wallets, zap_token:ZapTokenBSC, auctionhouse:AuctionHouse, zap_media:ZapMedia, mint_token0):
    #     private_key_1 = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

    #     # make sure wallets[1] has zap to bid with
    #     zap_token.transfer(wallets[1], Web3.toWei(7, 'ether'))
    #     zap_token.connect(private_key_1)
    #     zap_token.approve(auctionhouse.address, Web3.toWei(10,'ether'))

    #     # CREATE AUCTION
    #     duration = 60 * 15 #  number of seconds in 24 hours
    #     reservePrice = Web3.toWei(5, 'ether')
    #     # curator = wallets[0]
    #     token_id = 0
    #     curator = wallets[9]

    #     zap_media.approve(auctionhouse.address, token_id)

    #     params = [
    #         token_id, 
    #         zap_media.address, 
    #         duration, 
    #         reservePrice, 
    #         curator, 
    #         0, 
    #         zap_token.address
    #         ]
    #     auctionhouse.create_auction(*params)
        
    #     bid_amount = Web3.toWei(6, 'ether')
    #     auctionhouse.connect(private_key_1)
    #     auctionhouse.create_bid(0, bid_amount, zap_media.address)
        
    #     tx = auctionhouse.connect(private_key_1).end_auction(0, zap_media.address)
    #     receipt = auctionhouse.w3.eth.get_transaction_receipt(tx)
    #     assert receipt['status'] == 0



