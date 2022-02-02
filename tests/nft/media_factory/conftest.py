from typing import Tuple

from pytest import fixture
from eth_typing import ChecksumAddress

from src.nft.MediaFactory import MediaFactory
from src.nft.ZapMarket import ZapMarket
from src.nft.ZapMedia import ZapMedia

@fixture(scope="module")
def market():
    market_obj = ZapMarket('31337')
    yield market_obj
    del market_obj

@fixture(scope="module")
def factory_init():
    factory_obj = MediaFactory('31337')
    yield factory_obj
    del factory_obj

@fixture(scope="module")
def accounts(factory_init: MediaFactory):
    return factory_init.w3.eth.accounts

@fixture(scope="module")
def deployer(accounts: Tuple[ChecksumAddress]):
    return accounts[0]

@fixture(scope="module")
def tester(accounts):
    return accounts[5]


@fixture(scope="module")
def factory(tester):
    factory_obj = MediaFactory('31337')
    factory_obj.w3.eth.default_account = tester

    yield factory_obj
    del factory_obj

@fixture(scope="module")
def depl_media():
    media_obj = ZapMedia('31337')

    yield media_obj
    del media_obj

@fixture(scope="module")
def media(factory: MediaFactory, market: ZapMarket) -> str:
    tx_hash = factory.deployMedia(
        "Test Media 1",
        "TM1",
        market.address,
        True,
        "https://ipfs.moralis.io:2053/ipfs/QmeWPdpXmNP4UF9Urxyrp7NQZ9unaHfE2d43fbuur6hWWV"
    )

    tx_receipt = factory.w3.eth.wait_for_transaction_receipt(tx_hash)

    deployed_filter = factory.contract.events.MediaDeployed.createFilter(
        from_block=tx_receipt.blockNumber
    )

    deployed_event = deployed_filter.get_all_entries()[-1]
    return deployed_event["args"]["mediaContract"]
