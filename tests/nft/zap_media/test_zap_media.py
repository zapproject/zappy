import os
from platform import platform
import sys
import time
import pytest
import web3

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

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


def test_accounts(w3, eth_tester, wallets):
    # print(wallets)

    account10 = eth_tester.get_accounts()[10]
    account10_2 = wallets[0]


    # account0 = wallets[0]
    assert w3.eth.get_balance(wallets[0]) == 100000000000000000000
    # print(dir(wallets[0]))
    # assert (wallet.key).hex() == "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    # # assert account1.private_key


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
    # assert len(logs) == 1

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
def mint_token0(w3, zap_media):
    token_URI = "https://tokenURI.com"
    metadataURI = "https://metadataURI.com"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)


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
    assert zap_media.total_supply() == 0

def test_contract_URI(zap_media):
    assert zap_media.contract_URI() == b"https://testing.com"

def test_token_by_index(zap_media, mint_token0):
    assert zap_media.token_by_index(0) == 0

def test_supports_interface(zap_media):
    assert zap_media.supports_interface("0x5b5e139f")

def test_media_mint(w3, wallets, zap_media: ZapMedia, zap_market: ZapMarket):
    # assert w3.eth.accounts[1] == utils.wallets[0].address
    before_mint = zap_media.total_supply()
    assert before_mint == 0

    before_balance = zap_media.balance_of(zap_media.public_address)
    assert before_balance == 0
    # creator = zap_media.owner_of(0);
    # print(creator);
    # assert False


    token_URI = "Test CarZ"
    metadataURI = "Test CarMZ"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )
    # also testing kwargs in this example
    tx_params = {'gas': 5400000}

    tx_hash = zap_media.mint(mediaData, bidShares, **tx_params)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    after_mint = zap_media.total_supply()
    assert after_mint == before_mint + 1

    after_balance = zap_media.balance_of(zap_media.public_address)
    assert after_balance == before_balance + 1

    metadataURI = zap_media.get_token_metadata_URIs(before_mint)
    assert metadataURI == mediaData["metadataURI"]

    metadataHash = zap_media.get_token_metadata_hashes(before_mint)
    assert metadataHash == mediaData["metadataHash"].ljust(32, b'\x00')

    contentURI = zap_media.token_URI(before_mint)
    assert contentURI == mediaData["tokenURI"]

    contentHash = zap_media.get_token_content_hashes(before_mint)
    assert contentHash == mediaData["contentHash"].ljust(32, b'\x00')

    owner_of = zap_media.owner_of(before_mint)
    assert owner_of == zap_media.public_address

    token = zap_media.token_of_owner_by_index(zap_media.public_address, 0)
    assert token == before_mint

    current_bid_shares = zap_market.bidSharesForToken(zap_media.address, before_mint)
    assert current_bid_shares[0][0] == bidShares["creator"]["value"]
    assert current_bid_shares[1][0] == bidShares["owner"]["value"]
    assert current_bid_shares[2] == bidShares["collaborators"]
    assert current_bid_shares[3] == bidShares["collabShares"]


def test_media_mint2(w3, wallets, zap_media, zap_market):
    # assert w3.eth.accounts[1] == utils.wallets[0].address
    before_mint = zap_media.total_supply()
    assert before_mint == 0

    before_balance = zap_media.balance_of(zap_media.public_address)
    assert before_balance == 0

    token_URI = "Test CarZ"
    metadataURI = "Test CarMZ"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    after_mint = zap_media.total_supply()
    assert after_mint == before_mint + 1

    after_balance = zap_media.balance_of(zap_media.public_address)
    assert after_balance == before_balance + 1

    metadataURI = zap_media.get_token_metadata_URIs(before_mint)
    assert metadataURI == mediaData["metadataURI"]

    metadataHash = zap_media.get_token_metadata_hashes(before_mint)
    assert metadataHash == mediaData["metadataHash"].ljust(32, b'\x00')

    contentURI = zap_media.token_URI(before_mint)
    assert contentURI == mediaData["tokenURI"]

    contentHash = zap_media.get_token_content_hashes(before_mint)
    assert contentHash == mediaData["contentHash"].ljust(32, b'\x00')

    owner_of = zap_media.owner_of(before_mint)
    assert owner_of == zap_media.public_address

    token = zap_media.token_of_owner_by_index(zap_media.public_address, 0)
    assert token == before_mint

    current_bid_shares = zap_market.bidSharesForToken(zap_media.address, before_mint)
    assert current_bid_shares[0][0] == bidShares["creator"]["value"]
    assert current_bid_shares[1][0] == bidShares["owner"]["value"]
    assert current_bid_shares[2] == bidShares["collaborators"]
    assert current_bid_shares[3] == bidShares["collabShares"]


def test_media_set_bid(w3, wallets, zap_media, zap_market, zap_token):
    token_URI = "https://test"
    metadataURI = "http://test"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    zap_media.private_key = utils.hh_private_keys[1]
    zap_media.public_address = wallets[1]
   
    bidder = wallets[1]

    bid = zap_media.make_bid(
        100,
        zap_token.address,
        bidder,
        wallets[1],
        10
    )
    
    token_id = zap_media.total_supply() - 1

    current_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    assert current_bid[0] == 0
    assert current_bid[1] == '0x0000000000000000000000000000000000000000'
    assert current_bid[2] == '0x0000000000000000000000000000000000000000'
    assert current_bid[3] == '0x0000000000000000000000000000000000000000'
    assert current_bid[4][0] == 0

    tx = zap_token.transfer(wallets[1], 100)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)

    zap_token.private_key = utils.hh_private_keys[1]
    zap_token.public_address = wallets[1]
    tx = zap_token.approve(zap_market.address, 100)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.set_bid(token_id, bid)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    new_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    print(new_bid)
    assert new_bid[0] == bid["amount"]
    assert new_bid[1] == bid["currency"]
    assert new_bid[2] == bid["bidder"]
    assert new_bid[3] == bid["recipient"]
    assert new_bid[4][0] == bid["sellOnShare"]["value"]


def test_media_mint_w_sig(w3, wallets, zap_media):
    token_URI = "https://test"
    metadataURI = "http://test"

    media_data = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bid_shares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )
    deadline = int(time.time() + 60 * 60 * 24)

    sig = zap_media.get_mint_signature(media_data, bid_shares, deadline) 

    tx = zap_media.mint_with_sig(zap_media.public_address, media_data, bid_shares, sig)
    w3.eth.wait_for_transaction_receipt(tx, 360)


def test_media_remove_bid(w3, wallets, zap_media, zap_market, zap_token):
    token_URI = "https://test"
    metadataURI = "http://test"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    zap_media.private_key = utils.hh_private_keys[1]
    # zap_media.public_address
    bidder = wallets[1]

    # zap_media.private_key = wallets[1].key.hex()
    zap_media.public_address = wallets[1]
    # bidder = zap_media.public_address
    bid = zap_media.make_bid(
        100,
        zap_token.address,
        bidder,
        wallets[1],
        10
    )
    
    token_id = zap_media.total_supply() - 1

    tx = zap_token.transfer(wallets[1], 100)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)

    zap_token.private_key = utils.hh_private_keys[1]
    zap_token.public_address = wallets[1]

    tx = zap_token.approve(zap_market.address, 100)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.set_bid(token_id, bid)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.remove_bid(token_id)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    current_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    assert current_bid[0] == 0
    assert current_bid[1] == '0x0000000000000000000000000000000000000000'
    assert current_bid[2] == '0x0000000000000000000000000000000000000000'
    assert current_bid[3] == '0x0000000000000000000000000000000000000000'
    assert current_bid[4][0] == 0


def test_media_set_ask(w3, wallets, zap_media, zap_market, zap_token):
    token_URI = "https://test2"
    metadataURI = "http://test2"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    token_id = zap_media.total_supply() - 1

    ask = zap_media.make_ask(
        100,
        zap_token.address
    )

    tx_hash = zap_media.set_ask(token_id, ask)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.currentAskForToken(zap_media.address, token_id)

    assert current_ask[0] == ask["amount"]

    assert current_ask[1] == ask["currency"]

    # overwrite current ask
    new_ask = zap_media.make_ask(200, zap_token.address)

    tx_hash = zap_media.set_ask(token_id, new_ask)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.currentAskForToken(zap_media.address, token_id)

    assert current_ask[0] == new_ask["amount"]

    assert current_ask[1] == new_ask["currency"]


def test_media_remove_ask(w3, wallets, zap_media, zap_market, zap_token):
    token_URI = "https://test2"
    metadataURI = "http://test2"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    token_id = zap_media.total_supply() - 1

    ask = zap_media.make_ask(
        100,
        zap_token.address
    )

    tx_hash = zap_media.set_ask(token_id, ask)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    tx_hash = zap_media.remove_ask(token_id)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.currentAskForToken(zap_media.address, token_id)
    assert current_ask[0] == 0
    assert current_ask[1] == "0x0000000000000000000000000000000000000000"
    
    # overwrite current ask
    new_ask = zap_media.make_ask(200, zap_token.address)

    tx_hash = zap_media.set_ask(token_id, new_ask)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.currentAskForToken(zap_media.address, token_id)

    assert current_ask[0] == new_ask["amount"]

    assert current_ask[1] == new_ask["currency"]


def test_media_accept_bid(w3, wallets, zap_media, zap_market, zap_token):
    token_URI = "https://test2"
    metadataURI = "http://test2"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )
    
    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    token_id = zap_media.total_supply() - 1

    zap_media.private_key = utils.hh_private_keys[1]
    zap_media.public_address = wallets[1]
    bidder = wallets[1]

    bid = zap_media.make_bid(
        100,
        zap_token.address,
        bidder,
        wallets[1],
        10
    )
    
    token_id = zap_media.total_supply() - 1

    tx = zap_token.transfer(wallets[1], 100)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)

    creator_before_bal = zap_token.balanceOf(wallets[0])
    bidder_before_bal = zap_token.balanceOf(wallets[1])
    creator_before_token_bal = zap_media.balance_of(wallets[0])
    bidder_before_token_bal = zap_media.balance_of(wallets[1])

    zap_token.private_key = utils.hh_private_keys[1]
    zap_token.public_address = wallets[1]
    tx = zap_token.approve(zap_market.address, 100)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.set_bid(token_id, bid)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    # restore private and public keys
    zap_token.private_key = utils.hh_private_keys[0]
    zap_token.public_address = wallets[0]
    zap_media.private_key = utils.hh_private_keys[0]
    zap_media.public_address = wallets[0]

    tx = zap_media.accept_bid(token_id, bid)
    receipt = w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    # check balance of creator
    creator_after_bal = zap_token.balanceOf(wallets[0])
    assert creator_after_bal == creator_before_bal + int(
        bid["amount"] * (bidShares["creator"]["value"] / 100000000000000000000)) + int(
            bid["amount"] * (bidShares["owner"]["value"] / 100000000000000000000)
        )

    creator_after_token_bal = zap_media.balance_of(wallets[0])
    assert creator_after_token_bal == creator_before_token_bal - 1

    # check if the new owner is the bidder
    new_owner = zap_media.owner_of(token_id)
    assert new_owner == wallets[1]

    bidder_after_token_bal = zap_media.balance_of(wallets[1])
    assert bidder_after_token_bal == bidder_before_token_bal + 1


def test_media_update_metadata_uri(w3, wallets, zap_media, zap_market):
    token_URI = "Test CarZ"
    metadataURI = "Test CarMZ"

    mediaData = zap_media.make_media_data(
        token_URI, 
        metadataURI,
        Web3.toBytes(text=token_URI),
        Web3.toBytes(text=metadataURI)
    )
    bidShares = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx_hash = zap_media.mint(mediaData, bidShares)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    token_id = zap_media.total_supply() - 1

    new_metadata_uri = "new Test metadata uri"
    tx_hash = zap_media.update_token_metadata_URI(token_id, new_metadata_uri)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    metadata = zap_media.get_token_metadata_URIs(token_id)
    assert metadata == new_metadata_uri


def test_update_token_URI(zap_media: ZapMedia, mint_token0):
    token_URI = "https://tokenURI.com"
    newURI = "https://www.newURI.com"

    original_tokenURI_of_0 = zap_media.token_URI(0)
    assert original_tokenURI_of_0 == token_URI

    zap_media.update_token_URI(0, newURI)
    new_tokenURI_of_0 = zap_media.token_URI(0)
    assert new_tokenURI_of_0 == newURI

def test_approve(zap_media:ZapMedia, wallets, mint_token0):
    # Return the address approved for token id 0 before approval
    preApprovedAddr = zap_media.get_approved(0)
    
    # Expect the address to equal a zero address
    assert preApprovedAddr == web3.constants.ADDRESS_ZERO
    
    # The owner (signers[0]) approves signerOne for token id 0
    zap_media.approve(wallets[1], 0)

    # Returns the address approved for token id  0 after approval
    postApprovedStatus = zap_media.get_approved(0)
    assert postApprovedStatus == wallets[1]


def test_media_burn(w3, wallets, zap_media, mint_token0):
    before_bal = zap_media.balance_of(zap_media.public_address)
    token_id = zap_media.total_supply() - 1

    tx = zap_media.burn(token_id)
    w3.eth.wait_for_transaction_receipt(tx, 180)

    after_bal = zap_media.balance_of(zap_media.public_address)
    assert after_bal == before_bal - 1
    assert after_bal == 0

    assert zap_media.total_supply() == 0

    total_supply = zap_media.owner_of(token_id)
    assert total_supply is None


def test_media_revoke_approval(w3, wallets, zap_media, mint_token0):
    token_id = zap_media.total_supply() - 1

    tx = zap_media.approve(wallets[1], token_id)
    w3.eth.wait_for_transaction_receipt(tx, 180)

    postApprovedStatus = zap_media.get_approved(token_id)
    assert postApprovedStatus == wallets[1]

    tx = zap_media.revoke_approval(token_id)
    w3.eth.wait_for_transaction_receipt(tx, 180)

    assert zap_media.get_approved(token_id) == "0x0000000000000000000000000000000000000000"

def test_media_permit(w3, wallets, zap_media, mint_token0):
    token_id = zap_media.total_supply() - 1
    deadline = int(time.time() + 60 * 60 * 24)

    sig = zap_media.get_permit_signature(wallets[1], token_id, deadline)
    
    # make sure wallets[1] is not already approved
    assert zap_media.get_approved(token_id) == "0x0000000000000000000000000000000000000000"

    tx = zap_media.permit(wallets[1], token_id, sig)
    w3.eth.wait_for_transaction_receipt(tx, 180)

def test_approved_for_all(wallets, zap_media: ZapMedia, mint_token0):
    
    is_approved = zap_media.is_approved_for_all(wallets[0], wallets[1]);
    assert is_approved == False

    # approve wallet 1 for all
    zap_media.set_approval_for_all(wallets[1], True);

    is_approved = zap_media.is_approved_for_all(wallets[0], wallets[1]);
    assert is_approved == True


def test_safe_transfer_from(wallets, zap_media: ZapMedia, mint_token0):
    owner = wallets[0]
    recipient = wallets[1]
    
    # check owner of token 0 is currently not the recipient
    assert zap_media.owner_of(0) != recipient
    
    # transfer the token to wallets[1]/recipient    
    zap_media.safe_transfer_from(owner, recipient, 0)
    
    # check owner of token 0 is now wallets[1]/recipient
    assert zap_media.owner_of(0) == recipient


def test_transfer_from(wallets, zap_media: ZapMedia, mint_token0):
    owner = wallets[0]
    recipient = wallets[1]
    
    # check token 0 owner is wallets[0]/owner
    assert zap_media.owner_of(0) == owner

    # transfer the token to wallets[1]/recipient    
    zap_media.transfer_from(owner, recipient, 0)
    
    # after transferring the token, check token 0 owner is now wallets[1]/recipient
    assert zap_media.owner_of(0) == recipient



    #   describe("#transferFrom", () => {
    #     it("Should transfer token to another address", async () => {
    #       const recipient = await signerOne.getAddress();

    #       const owner = await ownerConnected.fetchOwnerOf(0);

    #       expect(owner).to.equal(await signer.getAddress());

    #       await ownerConnected.transferFrom(owner, recipient, 0);

    #       const newOwner = await ownerConnected.fetchOwnerOf(0);

    #       expect(newOwner).to.equal(recipient);
    #     });
    #   });