import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import web3

from src.nft.ZapMedia import ZapMedia
from src.nft.ZapToken import ZapTokenBSC
from src.nft.ZapMarket import ZapMarket

from tests.nft.test_utilities import hh_private_keys

zap_media: ZapMedia = ZapMedia("31337")
zap_token: ZapTokenBSC = ZapTokenBSC("31337")
zap_market: ZapMarket = ZapMarket("31337")


print("""
ZapMedia Info
""")

assert zap_media.address == '0x3Ca8f9C04c7e3E1624Ac2008F92f6F366A869444'
assert zap_media.name() == 'Zap Collection'
assert zap_media.contract_URI() == b'https://bafybeiev76hwk2gu7xmy5h3dn2f6iquxkhu4dhwpjgmt6ookrn6ykbtfi4.ipfs.dweb.link/'
assert zap_media.marketContract() == '0x5FC8d32690cc91D4c39d9d3abcBD16989F875707'


def test_owner_mints_from_Zap_Collection():
    print(
        """
        ("===================================")
        owner of Zap Collention mints
        ("===================================")
        """
    )


    base_url = 'https://gateway.pinata.cloud/ipfs/'
    token_URI = base_url + "woofwoof"
    metadataURI = base_url + "meowmeow"

    mt = zap_media.make_media_data(
        token_URI, 
        metadataURI
    )

    bt = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    tx = zap_media.mint(mt, bt)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    print("receipt_status: ", receipt['status'])
    print("receipt.tx hash: ", receipt['transactionHash'].hex())

    token_id = zap_media.total_supply() - 1
    print("token_id: ", token_id)

    assert zap_media.owner_of(token_id) == zap_media.public_address
    token_uri = zap_media.token_URI(token_id)
    assert token_uri == token_URI

def test_hh_acct_9_mints_from_Zap_Collection():
    print(
        """
        ("===================================")
        hh_acct_9 mints off of Zap Collention
        ("===================================")
        """
    )
    mt = zap_media.make_media_data(
        "woofwoof", 
        "meowmeow"
    )

    bt = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    zap_media.connect(hh_private_keys[9])

    tx = zap_media.mint(mt, bt)
    print('tx: ', tx)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    print("status: ", receipt['status'])
    print("tx hash: ", receipt['transactionHash'].hex())

    token_id = zap_media.total_supply() - 1
    assert zap_media.owner_of(token_id) == '0xa0Ee7A142d267C1f36714E4a8F75612F20a79720'
    token_uri = zap_media.token_URI(0)
    assert token_uri == "woofwoof"


def test_hh_acct_9_set_ask_for_token_0():
    print(
        """
        ("===================================")
        hh_acct_9 sets ask for token 0 of Zap Collention
        ("===================================")
        """
    )
    # connect owner of token because only owner or approved can setAsk.
    zap_media.connect(hh_private_keys[9])
    token_id = 0;

    ask = zap_media.make_ask(
        100,
        zap_token.address
        )

    tx_hash = zap_media.set_ask(token_id, ask)

    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.current_ask_for_token(zap_media.address, token_id)

    assert current_ask[0] == ask["amount"]
    assert current_ask[1] == ask["currency"]

    # overwrite current ask
    new_ask = zap_media.make_ask(
        200, 
        zap_token.address
        )

    tx_hash = zap_media.set_ask(token_id, new_ask)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    assert receipt is not None

    current_ask = zap_market.current_ask_for_token(zap_media.address, token_id)

    assert current_ask[0] == new_ask["amount"]
    assert current_ask[1] == new_ask["currency"]

def test_hh_acct_1_sets_bid_for_token_0():
    
    print(
        """
        ("===================================")
        hh_acct_1 sets bid for token 0 for 50 Zap Tokens
        ("===================================")
        """
    )
    # connect hh_acct_1 to zap_media
    zap_media.connect(hh_private_keys[1])

    bid_amount = 50
    bidder = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    recipient = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

    token_id = 0

    bid = zap_media.make_bid(
        bid_amount,
        zap_token.address,
        bidder,
        bidder,
        10
    )

    # transfer 1000 tokens to make sure hh_acct1 has enough tokens to make a bid
    tx = zap_token.transfer(bidder, 1000)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    assert zap_token.balanceOf(bidder) == 1000

    tx = zap_token.connect(hh_private_keys[1]).approve(zap_market.address, bid_amount)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    tx = zap_media.set_bid(token_id, bid)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    new_bid = zap_market.bid_for_token_bidder(zap_media.address, token_id, bidder)
    assert new_bid[0] == bid["amount"]
    assert new_bid[1] == bid["currency"]
    assert new_bid[2] == bid["bidder"]
    assert new_bid[3] == bid["recipient"]
    assert new_bid[4][0] == bid["sellOnShare"]["value"]

def test_hh_acct_3_sets_bid_for_token_0():
    
    print(
        """
        ("===================================")
        hh_acct_1 sets bid for token 0 for 50 Zap Tokens
        ("===================================")
        """
    )
    # connect hh_acct_1 to zap_media
    zap_media.connect(hh_private_keys[3])

    bid_amount = 50
    bidder = "0x90F79bf6EB2c4f870365E785982E1f101E93b906"
    recipient = "0x90F79bf6EB2c4f870365E785982E1f101E93b906"

    token_id = 0

    bid = zap_media.make_bid(
        bid_amount,
        zap_token.address,
        bidder,
        bidder,
        10
    )

    # transfer 1000 tokens to make sure hh_acct1 has enough tokens to make a bid
    tx = zap_token.transfer(bidder, 1000)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    assert zap_token.balanceOf(bidder) == 1000

    tx = zap_token.connect(hh_private_keys[3]).approve(zap_market.address, bid_amount)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    print("Owner of token 0 before bidding: ", zap_media.owner_of(0))

    tx = zap_media.set_bid(token_id, bid)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    print("Owner of token 0 after bidding: ", zap_media.owner_of(0))

    new_bid = zap_market.bid_for_token_bidder(zap_media.address, token_id, bidder)
    print(new_bid)
    assert new_bid[0] == bid["amount"]
    assert new_bid[1] == bid["currency"]
    assert new_bid[2] == bid["bidder"]
    assert new_bid[3] == bid["recipient"]
    assert new_bid[4][0] == bid["sellOnShare"]["value"]

def test_hh_acct_2_sets_bid_for_token_0_matching_ask():
    
    print(
        """
        ("===================================")
        hh_acct_2 sets bid for token 0 for 200 Zap Tokens.
        This will match the ask price, automatially transferring Zap and NFT to token owner and bidder respectively.
        ("===================================")
        """
    )

    hh_acct2 = {
        "pa": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
        "pk": hh_private_keys[2]
    }

    token_id = 0

    # connect hh_acct_1 to zap_media
    zap_media.connect(hh_acct2['pk'])

    current_ask = zap_market.connect(hh_acct2['pk']).current_ask_for_token(zap_media.address, token_id)

    bid_amount = current_ask[0]
    bidder = hh_acct2['pa']
    recipient = hh_acct2['pa']

    bid = zap_media.make_bid(
        bid_amount,
        zap_token.address,
        bidder,
        bidder,
        10
    )

    # transfer 1000 tokens to make sure hh_acct2 has enough tokens to make a bid as owner of contract
    zap_token.connect(hh_private_keys[0])
    tx = zap_token.transfer(bidder, 1000)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    assert zap_token.balanceOf(bidder) == 1000

    tx = zap_token.connect(hh_acct2['pk']).approve(zap_market.address, bid_amount)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    owner_before_matching_bid = zap_media.owner_of(token_id)
    assert owner_before_matching_bid == "0xa0Ee7A142d267C1f36714E4a8F75612F20a79720"

    tx = zap_media.set_bid(token_id, bid)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    assert receipt is not None

    # assert new owner
    owner_after_matching_bid = zap_media.owner_of(token_id)
    assert owner_after_matching_bid == bidder

    bid_is_reset = zap_market.bid_for_token_bidder(zap_media.address, token_id, bidder)
    assert bid_is_reset[0] == 0
    assert bid_is_reset[1] == "0x0000000000000000000000000000000000000000"
    assert bid_is_reset[2] == "0x0000000000000000000000000000000000000000"
    assert bid_is_reset[3] == "0x0000000000000000000000000000000000000000"

def test_hh_acct_9_permits_hh_acct_1_for_token_0():
    print(
        """
        ("===================================")
        hh_acct_9 permits hh_acct_1 for token 0.
        ("===================================")
        """
    )

    zap_media.connect(hh_private_keys[9])
    hh_acct_1 = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    token_id = zap_media.total_supply() - 1
    deadline = int(time.time() + 60 * 60 * 24)

    sig = zap_media.get_permit_signature(hh_acct_1, token_id, deadline)
    
    # make sure wallets[1] is not already approved
    assert zap_media.get_approved(token_id) == web3.constants.ADDRESS_ZERO
    zap_media.w3

    tx = zap_media.permit(hh_acct_1, token_id, sig)
    zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    approved_address = zap_media.get_approved(token_id)
    assert approved_address == hh_acct_1

def test_hh_acct_9_revokes_approval_for_hh_acct_1_for_token_0():
    print(
        """
        ("===================================")
        hh_acct_9 revokes hh_acct_1 approval for token 0.
        ("===================================")
        """
    )
    zap_media.connect(hh_private_keys[9])
    hh_acct_1 = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

    token_id = zap_media.total_supply() - 1

    # don't need to approve like below since we ran zap_media.permit(...) in the test above
    # tx = zap_media.approve(hh_acct_1, token_id)
    # w3.eth.wait_for_transaction_receipt(tx, 180)

    postApprovedStatus = zap_media.get_approved(token_id)
    assert postApprovedStatus == hh_acct_1

    tx = zap_media.revoke_approval(token_id)
    zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    assert zap_media.get_approved(token_id) == web3.constants.ADDRESS_ZERO

def test_burn_token_0():
    # if the owner is also the creator, owner/creator can burn
    # if owner is NOT the creator, owner cannot burn and creator cannot burn 
    hh_acct_2 = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
    hh_acct_9 = "0xa0Ee7A142d267C1f36714E4a8F75612F20a79720"
    token_id = zap_media.total_supply() - 1
    token_owner = zap_media.owner_of(0)
    print("token_owner: ", token_owner)
    token_creator = zap_media.get_token_creators(0)
    print("token_creator: ", token_creator)
    
    tx = zap_media.connect(hh_private_keys[2]).approve(hh_acct_9, 0)
    zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    
    # zap_media.connect(hh_private_keys[2])
    before_bal = zap_media.balance_of(zap_media.public_address)

    tx = zap_media.burn(token_id)
    zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    after_bal = zap_media.balance_of(zap_media.public_address)
    assert after_bal == before_bal - 1
    assert after_bal == 0

    assert zap_media.total_supply() == 0

def test_hh_acct_9_mints_another_token_from_Zap_Collection():
    print(
        """
        ("===================================")
        hh_acct_9 mints another token from Zap Collention
        ("===================================")
        """
    )
    mt = zap_media.make_media_data(
        "ruffruff", 
        "yaowyaow"
    )

    bt = zap_media.make_bid_shares(
        90000000000000000000,
        5000000000000000000,
        [],
        []
    )

    zap_media.connect(hh_private_keys[9])

    tx = zap_media.mint(mt, bt)
    print('tx: ', tx)
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    print("status: ", receipt['status'])
    print("tx hash: ", receipt['transactionHash'].hex())

    token_id = zap_media.total_supply() - 1
    print("token_id: ", token_id)

    assert zap_media.owner_of(token_id) == '0xa0Ee7A142d267C1f36714E4a8F75612F20a79720'
    token_uri = zap_media.token_URI(0)

def test_creator_owner_burn_token_1():
    # if the owner is also the creator, owner/creator can burn
    # if owner is NOT the creator, owner cannot burn and creator cannot burn 
    token_id = zap_media.total_supply() - 1
   
    # tx = zap_media.connect(hh_private_keys[9]).approve(hh_acct_9, 0)
    # zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
    
    zap_media.connect(hh_private_keys[9])
    before_bal = zap_media.balance_of(zap_media.public_address)

    tx = zap_media.burn(token_id)
    zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    after_bal = zap_media.balance_of(zap_media.public_address)
    print(after_bal)
    assert after_bal == before_bal - 1
    assert after_bal == 0


# test_owner_mints_from_Zap_Collection()

test_hh_acct_9_mints_from_Zap_Collection()
test_hh_acct_9_set_ask_for_token_0()

test_hh_acct_1_sets_bid_for_token_0()
test_hh_acct_9_permits_hh_acct_1_for_token_0()
test_hh_acct_9_revokes_approval_for_hh_acct_1_for_token_0()
test_hh_acct_2_sets_bid_for_token_0_matching_ask()
test_hh_acct_9_mints_another_token_from_Zap_Collection()
test_creator_owner_burn_token_1()


# test_burn_token_0()