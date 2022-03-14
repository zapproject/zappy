import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from src.nft.ZapMedia import ZapMedia
from src.nft.ZapToken import ZapTokenBSC
from src.nft.ZapMarket import ZapMarket

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


print("===================================")
print("===================================")


base_url = 'https://gateway.pinata.cloud/ipfs/'
token_URI = base_url + "QmWVFGFBeH33xYt6na33D9tfR868aybJYuBF2fMWWLaVaE"
metadataURI = base_url + "QmWVFGFBeH33xYt6na33D9tfR868aybJYuBF2fMWWLaVaE"

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
print('tx: ', tx)
receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
print("receipt: ", receipt)

assert zap_media.owner_of(0) == zap_media.public_address
token_uri = zap_media.token_URI(0)
print("token_uri: ", token_uri)
assert token_uri == token_URI

print("===================================")
print("===================================")
mt = zap_media.make_media_data(
    "woof woof", 
    "meow meow"
)

bt = zap_media.make_bid_shares(
    90000000000000000000,
    5000000000000000000,
    [],
    []
)

zap_media.connect("0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6")

tx = zap_media.mint(mt, bt)
print('tx: ', tx)
receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
print("receipt: ", receipt)

assert zap_media.owner_of(1) == '0xa0Ee7A142d267C1f36714E4a8F75612F20a79720'
token_uri = zap_media.token_URI(0)
print("===================================")
print("===================================")

assert zap_media.total_supply() == 2


zap_media.connect('0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d')
wallets = ['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266', '0x70997970C51812dc3A010C7d01b50e0d17dc79C8']
recipient = wallets[0]
bidder = wallets[1]

token_id = 0

bid = zap_media.make_bid(
    100,
    zap_token.address,
    bidder,
    recipient,
    10
)

tx = zap_token.transfer(wallets[1], 100)
receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)


zap_token.connect('0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d')
tx = zap_token.approve(zap_market.address, 100)
receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
assert receipt is not None

# zap_media.connect('0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d')
tx = zap_media.set_bid(token_id, bid)
receipt = zap_media.w3.eth.wait_for_transaction_receipt(tx, 180)
assert receipt is not None

new_bid = zap_market.bidForTokenBidder(zap_media.address, token_id, bidder)
print(new_bid)
assert new_bid[0] == bid["amount"]
assert new_bid[1] == bid["currency"]
assert new_bid[2] == bid["bidder"]
assert new_bid[3] == bid["recipient"]
assert new_bid[4][0] == bid["sellOnShare"]["value"]