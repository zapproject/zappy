import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from src.zappy.zapmedia import ZapMedia
from src.zappy.zaptokenbsc import ZapTokenBSC
from src.zappy.zapmarket import ZapMarket
from src.zappy.mediafactory import MediaFactory

from tests.nft.test_utilities import hh_private_keys

zap_media: ZapMedia = ZapMedia()
zap_token: ZapTokenBSC = ZapTokenBSC()
zap_market: ZapMarket = ZapMarket()
media_factory: MediaFactory = MediaFactory()


print("""
Media Factory Info
""")

assert media_factory.address == '0xB7f8BC63BbcaD18155201308C8f3540b07f84F5e'
assert media_factory.owner() == '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'

def test_deploy_custom_media():
    args = ['TEPPY COLLECTION', 'TEP', zap_market.address, True, 'https://teppycollection.com']

    # hh_acct_1 is deploying a custom collection
    (receipt, deploy_media_address) = media_factory.connect(hh_private_keys[1]).deploy_media(*args)
    assert receipt['status'] == 1
    
    is_registered = zap_market.isRegistered(deploy_media_address)
    assert is_registered == True
    
    is_configured = zap_market.isConfigured(deploy_media_address)
    assert is_configured == True
    return deploy_media_address


def test_deployed_media():
    # get deployed address from above
    my_media_address = test_deploy_custom_media()
    # connect to deployed contract with chain id and address
    my_media: ZapMedia = ZapMedia("31337", my_media_address)

    hh_acct_1 = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

    # media factory still owns the contract since hh_acct_1 did not claim yet
    assert my_media.get_owner() == media_factory.address

    # need to connect for testing purposes
    my_media.connect(hh_private_keys[1])

    # hh_acct_1 claims ownership of deployed media
    tx = my_media.connect(hh_private_keys[1]).claim_transfer_ownership()
    receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)

    # after claiming ownership, get_owner should return hh_acct_1
    assert my_media.get_owner() == hh_acct_1

    assert my_media.address == my_media_address
    assert my_media.chain_id == media_factory.chain_id, "Should be the same chain id as the media factory that deployed it."
    assert my_media.name() == "TEPPY COLLECTION"
    assert my_media.symbol() == "TEP"
    assert my_media.contract_URI() == b"https://teppycollection.com"
    assert my_media.total_supply() == 0, "Total supply should be zero since it's newly deployed."

def test_owner_mints_from_Teppy_Collection():
    print(
        """
        ("===================================")
        owner of TEPPY Collention mints
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
    print("receipt - status: ", receipt['status'])
    print("receipt - tx hash: ", receipt['transactionHash'].hex())

    token_id = zap_media.total_supply() - 1
    print("token_id: ", token_id)

    assert zap_media.owner_of(token_id) == zap_media.public_address
    token_uri = zap_media.token_URI(token_id)
    assert token_uri == token_URI


test_deployed_media()
test_owner_mints_from_Teppy_Collection()
