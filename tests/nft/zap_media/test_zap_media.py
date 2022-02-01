import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from src.nft.ZapMedia import ZapMedia
from src.nft.ZapMarket import ZapMarket
from src.nft.ZapToken import ZapTokenBSC
from tests.nft.test_utilities import wallets


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

    assert zap_media.totalSupply() == 1

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



    # restore wallet to first account
    zap_token.privateKey = wallets[0].key.hex()
    zap_token.publicAddress = wallets[0].address

    zap_media.privateKey = wallets[0].key.hex()
    zap_media.publicAddress = wallets[0].address

def test_media_set_ask():
    tokenURI = "https://test1"
    metadataURI = "http://test1"

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

    # # filter for mint event
    # event_filter = zap_market.contract.events.AskCreated.createFilter(fromBlock="earliest")
    # # list of minted events ranged from ealiest to latest
    # events = event_filter.get_all_entries()
    # events = events[0]["args"]

    # assert events["mediaContract"] == zap_media.address

    # assert events["tokenId"] == token_id

    # assert events["ask"]["amount"] == ask["amount"]

    # assert events["ask"]["currency"] == ask["currency"]

test_media_mint()
test_media_set_bid()
test_media_set_ask()