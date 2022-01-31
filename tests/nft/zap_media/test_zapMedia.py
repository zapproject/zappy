import os
from platform import platform
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import pytest
import time

from eth_account.messages import encode_structured_data
from web3 import (
    EthereumTesterProvider,
    Web3,
)
from eth_tester import EthereumTester

from unittest.mock import patch


import tests.nft.test_utilities as utils
from src.nft.ZapMedia import ZapMedia

import pprint
pp = pprint.PrettyPrinter(indent=4)

from src.nft.utils.signature import encode_structured_data
from py_eth_sig_utils.signing import (sign_typed_data, recover_typed_data)
from py_eth_sig_utils.utils import normalize_key

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
    abi = artifact['abi']

    # return ZapMedia(str(w3.eth.chain_id))
    zap_media = ZapMedia(str(w3.eth.chain_id))
    zap_media.w3 = w3
    zap_media.contract = w3.eth.contract(address=zap_media_address, abi=abi)
    return zap_media
    
    


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
    assert zap_media.totalSupply().call() == 0



def test_media_mint(w3, wallets, zap_media):
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
    bidShares = {
        "creator" : {"value":90000000000000000000},
        "owner" : {"value":5000000000000000000},
        "collaborators": [],
        "collabShares": []
    }


    zap_media.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    nonce = zap_media.w3.eth.get_transaction_count(wallets[0].address)

    assert zap_media.chainId

    tx = {
        'chainId':61,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': zap_media.w3.toWei('50', 'gwei'),
    }

    tx_hash = zap_media.mint(mediaData, bidShares)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    after_mint = zap_media.totalSupply().call()
    assert after_mint == before_mint + 1

def test_media_mint2(w3, wallets, zap_media):
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
    bidShares = {
        "creator" : {"value":90000000000000000000},
        "owner" : {"value":5000000000000000000},
        "collaborators": [],
        "collabShares": []
    }


    zap_media.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    nonce = zap_media.w3.eth.get_transaction_count(wallets[0].address)

    assert zap_media.chainId

    tx = {
        'chainId':61,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': zap_media.w3.toWei('50', 'gwei'),
    }

    tx_hash = zap_media.mint(mediaData, bidShares)
    w3.eth.wait_for_transaction_receipt(tx_hash, 180)

    after_mint = zap_media.totalSupply().call()
    assert after_mint == before_mint + 1


def test_media_mint_w_sig(w3, wallets, eth_tester ,zap_media):
    zap_media.privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    before_mint = zap_media.totalSupply().call()
    media_data = zap_media.makeMediaData(
        "https://content-uri", 
        "https://metadata-uri", 
        "content-hash".encode('utf-8'), 
        "metadata-hash".encode('utf-8'))
    bid_shares = zap_media.makeBidShares(95000000000000000000, 0, [], [])

    account = w3.eth.account.privateKeyToAccount(zap_media.privateKey)

    deadline = int(time.time() + 60 * 60 * 24)
    name = zap_media.name()
    chain_id = zap_media.chainId
    nonce = zap_media.getSigNonces(account.address)
    data = {
        "types": {
            "EIP712Domain": [
                { "name": "name", "type": "string" },
                { "name": "version", "type": "string" },
                { "name": "chainId", "type": "uint256" },
                { "name": "verifyingContract", "type": "address" }
            ],
            "MintWithSig": [
                { "name": 'contentHash', "type": 'bytes32' },
                { "name": 'metadataHash', "type": 'bytes32' },
                { "name": 'creatorShare', "type": 'uint256' },
                { "name": 'nonce', "type": 'uint256' },
                { "name": 'deadline', "type": 'uint256' }
            ]
        },
        "primaryType": "MintWithSig",
        "domain": {
            "name": name,
            "version": "1",
            "chainId": int(chain_id),
            "verifyingContract": zap_media.address
        },
        "message": {
            'contentHash': media_data["contentHash"],
            'metadataHash': media_data["metadataHash"],
            'creatorShare': bid_shares["creator"]["value"],
            'nonce': nonce+1,
            'deadline': deadline
        }
    }
  
    eip191data = encode_structured_data(data)
    print("EIP191: ", eip191data)

    # sig_data = w3.eth.sign_typed_data("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266", data)

    sig_data2 = w3.eth.account.sign_message(eip191data, zap_media.privateKey)
    sig_data3 = sign_typed_data(data, normalize_key(zap_media.privateKey))
    
    # print("sig data: ", sig_data)
    print("sig data 2: ", sig_data2)
    print("sig data 3: ", sig_data3)

    recovered = recover_typed_data(data, sig_data3[0], sig_data3[1], sig_data3[2])
    print("RECOVERED: ", recovered)

    recovered2 = w3.eth.account.recover_message(eip191data, signature=sig_data2.signature)
    print("RECOVERED2: ", recovered2)

    sig = zap_media.makeEIP712Sig(
        deadline, 
        sig_data3[0], 
        w3.toHex(sig_data3[1]),
        w3.toHex(sig_data3[2])
    )
    print("sig: ", sig)


    result = zap_media.mintWithSig(account.address, media_data, bid_shares, sig)
    w3.eth.wait_for_transaction_receipt(result, 180)
    after_mint = zap_media.totalSupply().call()
    assert account.address == "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    assert after_mint == before_mint + 1