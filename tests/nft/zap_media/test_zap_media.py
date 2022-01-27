import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from src.nft.ZapMedia import ZapMedia
from src.nft.ZapMarket import ZapMarket
from tests.nft.test_utilities import wallets


# ====================================
# SETUP
# ====================================

# create Zap Media
zap_media = ZapMedia('31337')

# create Zap Market
zap_market = ZapMarket('31337')

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

    assert zap_media.tokenByIndex(0) == 0



# test_media_mint()
