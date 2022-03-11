import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))
from src.nft.ZapMedia import ZapMedia
from src.nft.ZapMarket import ZapMarket
from web3 import (
    Web3,
)


zap_media:ZapMedia = ZapMedia("31337")
zap_market: ZapMarket = ZapMarket("31337")
# print(zap_media.name())
# print(zap_media.address)
# print(zap_media.public_address)
def test_media_mint():
    # mint token
    media_data = zap_media.make_media_data("token-uri", "metadata-uri", b"content-hash2", b"metadata-hash")
    bid_shares = zap_media.make_bid_shares(95000000000000000000, 0, [], [])
    result = zap_media.mint(media_data, bid_shares)

    # filter for mint event
    event_filter = zap_market.contract.events.Minted.createFilter(fromBlock="earliest")
    # list of minted events ranged from ealiest to latest
    events = event_filter.get_all_entries()

    assert events[0]["args"]["token"] == 0

    assert zap_media.token_by_index(0) == 0



test_media_mint()

# def test_mint_w_sig():
#     token_URI = "https://test"
#     metadataURI = "http://test"

#     media_data = zap_media.make_media_data(
#         token_URI, 
#         metadataURI,
#         Web3.toBytes(text=token_URI),
#         Web3.toBytes(text=metadataURI)
#     )
#     bid_shares = zap_media.make_bid_shares(
#         90000000000000000000,
#         5000000000000000000,
#         [],
#         []
#     )
#     deadline = int(time.time() + 60 * 60 * 24)

#     sig = zap_media.get_mint_signature(media_data, bid_shares, deadline) 

#     tx = zap_media.mint_with_sig(zap_media.public_address, media_data, bid_shares, sig)
#     zap_media.w3.eth.wait_for_transaction_receipt(tx, 360)

#     assert zap_media.total == 1

#     assert zap_media.balanceOf(zap_media.public_address) == 1


# def test_permit():
#     token_URI = "https://tokenURI1.com"
#     metadataURI = "https://metadataURI1.com"

#     mediaData = zap_media.make_media_data(
#         token_URI, 
#         metadataURI,
#         Web3.toBytes(text=token_URI),
#         Web3.toBytes(text=metadataURI)
#     )
#     bidShares = zap_media.make_bid_shares(
#         90000000000000000000,
#         5000000000000000000,
#         [],
#         []
#     )

#     tx_hash = zap_media.mint(mediaData, bidShares)
#     zap_media.w3.eth.wait_for_transaction_receipt(tx_hash, 180)

#     token_id = zap_media.total_supply() - 1
#     deadline = int(time.time() + 60 * 60 * 24)

#     sig = zap_media.get_permit_signature("0x2546BcD3c84621e976D8185a91A922aE77ECEc30", token_id, deadline)
    
#     # make sure wallets[1] is not already approved
#     assert zap_media.get_approved(token_id) == "0x0000000000000000000000000000000000000000"

#     tx = zap_media.permit("0x2546BcD3c84621e976D8185a91A922aE77ECEc30", token_id, sig)
#     zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

#     assert zap_media.get_approved(token_id) == "0x2546BcD3c84621e976D8185a91A922aE77ECEc30"

# test_mint_w_sig()
# test_permit()