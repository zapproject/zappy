import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from src.nft.ZapMedia import ZapMedia
from src.nft.ZapMarket import ZapMarket
from tests.nft.test_utilities import wallets

from eth_account.messages import encode_structured_data

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

def test_media_mint_w_sig():
    media_data = zap_media.makeMediaData("token-uri", "metadata-uri", b"content-hash2", b"metadata-hash")
    bid_shares = zap_media.makeBidShares(95000000000000000000, 0, [], [])

    # account = zap_media.w3.account.privateKeyToAccount(zap_media.privateKey)

    deadline = time.time() + 60 * 60 * 24
    name = zap_media.name()
    chain_id = zap_media.chainId
    nonce = zap_media.w3.eth.get_transaction_count("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
    
    data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chain_id", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"}
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
            "chain_id": int(chain_id),
            "verifyingContract": zap_media.address
        },
        "message": {
            'contentHash': 'content-hash',
            'metadataHash': 'metadata-hash',
            'creatorShare': 95000000000000000000,
            'nonce': nonce,
            'deadline': deadline
        }
    }

    eip191data = encode_structured_data(data)
    sig_data = zap_media.w3.eth.account.sign_message(eip191data, "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")

    sig = zap_media.makeEIP712Sig(deadline, sig_data.v, sig_data.r, sig_data.s)

    media_data = zap_media.makeMediaData("token-uri", "metadata-uri", b"content-hash", b"metadata-hash")
    bid_shares = zap_media.makeBidShares(95000000000000000000, 0, [], [])

    result = zap_media.mintWithSig("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266", media_data, bid_shares, sig)

def toHex(val):
    return zap_media.w3.toHex(zap_media.w3.toBytes(val).rjust(32, b'\0'))

# test_media_mint()

test_media_mint_w_sig()
