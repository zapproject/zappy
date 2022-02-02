import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from src.nft.ZapMedia import ZapMedia
from src.nft.ZapMarket import ZapMarket
from src.nft.ZapToken import ZapTokenBSC
from tests.nft.test_utilities import wallets
from src.nft.utils.signature import encode_structured_data

from py_eth_sig_utils.signing import (sign_typed_data, recover_typed_data)
from py_eth_sig_utils.utils import normalize_key

from hexbytes import HexBytes

# from eth_account.messages import encode_structured_data

# ====================================
# SETUP
# ====================================

# create Zap Media
zap_media = ZapMedia('31337')

# create Zap Market
zap_market = ZapMarket('31337')

# create Zap Token
zap_token = ZapTokenBSC('31337')

# ====================================
# END SETUP
# ====================================



def test_connected_to_node():
    assert zap_media.w3.isConnected()

def test_address_matches_deployed_address():
    deployed_zap_media_contract_hardhat_address = "0x3Ca8f9C04c7e3E1624Ac2008F92f6F366A869444"
    assert zap_media.address == deployed_zap_media_contract_hardhat_address

def test_media_mint():
    # mint token
    media_data = zap_media.makeMediaData("token-uri", "metadata-uri", b"content-hash2", b"metadata-hash")
    bid_shares = zap_media.makeBidShares(95000000000000000000, 0, [], [])
    result = zap_media.mint(media_data, bid_shares)
    
    # filter for mint event
    event_filter = zap_market.contract.events.Minted.createFilter(fromBlock="earliest")
    # list of minted events ranged from ealiest to latest
    events = event_filter.get_all_entries()

    assert events[0]["args"]["token"] == 0

    assert events[0]["args"]["mediaContract"] == zap_media.address

    assert zap_media.tokenByIndex(0) == 0

def test_media_mint_w_sig():
    media_data = zap_media.makeMediaData(
        "https://content-uri", 
        "https://metadata-uri", 
        'content-hash'.encode('utf-8'),  
        'metadata-hash'.encode('utf-8'))
    bid_shares = zap_media.makeBidShares(95000000000000000000, 0, [], [])
    print(media_data["contentHash"])
    account = zap_media.w3.eth.account.privateKeyToAccount(zap_media.privateKey)

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
  
    # eip191data = encode_structured_data(data)
    # print("EIP191: ", eip191data)
    # sig_data2 = zap_media.w3.eth.account.sign_message(eip191data, zap_media.privateKey)
    sig_data = sign_typed_data(data, normalize_key(zap_media.privateKey))
    
    print("sig data: ", sig_data)
    # print("sig data 2: ", sig_data2)

    recovered = recover_typed_data(data, sig_data[0], sig_data[1], sig_data[2])
    print("RECOVERED: ", recovered)

    # recovered2 = zap_media.w3.eth.account.recover_message(eip191data, signature=sig_data2.signature)
    # print("RECOVERED2: ", recovered2)

    sig = zap_media.makeEIP712Sig(
        deadline, 
        sig_data[0], 
        # sig_data2[1].to_bytes(32, 'big'),
        # sig_data2[2].to_bytes(32, 'big')
        zap_media.w3.toBytes(sig_data[1]),
        zap_media.w3.toBytes(sig_data[2]),
    )
    print("sig: ", sig)


    result = zap_media.mintWithSig(account.address, media_data, bid_shares, sig)
    print(result)

def toHex(val):
    return zap_media.w3.toHex(zap_media.w3.toBytes(text=val).rjust(32, b'\0'))

def test_media_set_bid():
    tokenURI = "https://test"
    metadataURI = "http://test"

    mediaData = {
        "tokenURI": tokenURI,
        "metadataURI": metadataURI,
        "contentHash": zap_media.w3.toBytes(text=tokenURI),
        "metadataHash": zap_media.w3.toBytes(text=metadataURI)
    }

    bidShares = {
        "creator" : {"value":90000000000000000000},
        "owner" : {"value":5000000000000000000},
        "collaborators": [],
        "collabShares": []
    }

    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    zap_media.privateKey = wallets[1].key.hex()
    zap_media.publicAddress = wallets[1].address
    bidder = zap_media.publicAddress
    bid = zap_media.makeBid(
        100,
        zap_token.address,
        bidder,
        wallets[0].address,
        10
    )
    
    token_id = zap_media.totalSupply() - 1

    current_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    assert current_bid[0] == 0
    assert current_bid[1] == '0x0000000000000000000000000000000000000000'
    assert current_bid[2] == '0x0000000000000000000000000000000000000000'
    assert current_bid[3] == '0x0000000000000000000000000000000000000000'
    assert current_bid[4][0] == 0

    tx = zap_token.transfer(wallets[1].address, 300)
    receipt = zap_token.w3.eth.wait_for_transaction_receipt(tx, 180)

    zap_token.privateKey = wallets[1].key.hex()
    zap_token.publicAddress = wallets[1].address
    
    # First bid 
    tx = zap_token.approve(zap_market.address, 100)
    receipt = zap_token.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.setBid(token_id, bid)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    new_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    assert new_bid[0] == bid["amount"]
    assert new_bid[1] == bid["currency"]
    assert new_bid[2] == bid["bidder"]
    assert new_bid[3] == bid["recipient"]
    assert new_bid[4][0] == bid["sellOnShare"]["value"]

    # 2nd bid - should overwrite previous one
    bid["amount"] = 200

    tx = zap_token.approve(zap_market.address, 200)
    receipt = zap_token.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.setBid(token_id, bid)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    new_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
    assert new_bid[0] == bid["amount"]
    assert new_bid[1] == bid["currency"]
    assert new_bid[2] == bid["bidder"]
    assert new_bid[3] == bid["recipient"]
    assert new_bid[4][0] == bid["sellOnShare"]["value"]

    ### For events that return a struct, current open issue https://github.com/ethereum/web3.py/pull/2211
    #skipping event test until resolved
    # # filter for mint event
    # event_filter = zap_market.contract.events.BidCreated.createFilter(fromBlock="earliest")
    # # list of minted events ranged from ealiest to latest
    # events = event_filter.get_all_entries()

    # events = events[0]["args"]

    # restore wallet to first account
    zap_token.privateKey = wallets[0].key.hex()
    zap_token.publicAddress = wallets[0].address

    zap_media.privateKey = wallets[0].key.hex()
    zap_media.publicAddress = wallets[0].address

def test_media_set_ask():
    tokenURI = "https://test2"
    metadataURI = "http://test2"

    mediaData = {
        "tokenURI": tokenURI,
        "metadataURI": metadataURI,
        "contentHash": zap_media.w3.toBytes(text=tokenURI),
        "metadataHash": zap_media.w3.toBytes(text=metadataURI)
    }

    bidShares = {
        "creator" : {"value":90000000000000000000},
        "owner" : {"value":5000000000000000000},
        "collaborators": [],
        "collabShares": []
    }

    tx_hash = zap_media.mint(mediaData, bidShares)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    token_id = zap_media.totalSupply() - 1

    ask = zap_media.makeAsk(
        100,
        zap_token.address
    )

    tx = zap_media.setAsk(token_id, ask)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.currentAskForToken(zap_media.address, token_id)

    assert current_ask[0] == ask["amount"]

    assert current_ask[1] == ask["currency"]

    #### For events that return a struct, there exists an open issue regarding this https://github.com/ethereum/web3.py/pull/2211
    ## skipping event test until resolved
    # # filter for mint event
    # event_filter = zap_market.contract.events.AskCreated.createFilter(fromBlock="earliest")
    # # list of minted events ranged from ealiest to latest
    # events = event_filter.get_all_entries()
    # print(events)

    # events = events[0]["args"]

    # assert events["mediaContract"] == zap_media.address

    # assert events["tokenId"] == token_id

    # assert events["ask"]["amount"] == ask["amount"]

    # assert events["ask"]["currency"] == ask["currency"]

test_media_mint_w_sig()
# test_media_mint()
# test_media_set_bid()
# test_media_set_ask()
