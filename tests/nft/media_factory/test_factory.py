from msilib.schema import Media
from os import path as os_path
from sys import path as sys_path
from typing import Tuple
sys_path.insert(0, os_path.dirname(os_path.abspath("./__file__")))

from eth_typing import ChecksumAddress
from pytest import raises
from web3.exceptions import SolidityError

from tests.nft.test_utilities import wallets
from src.nft.MediaFactory import MediaFactory
from src.nft.ZapMedia import ZapMedia

class TestMediaFactory:
    """"""

    def test_owner(self, factory: MediaFactory, accounts: Tuple[ChecksumAddress]):
        owner = factory.owner().call()
        assert isinstance(owner, str), "type error: owner is not a string"
        assert owner == accounts[0], "the owner is incorrect"

    def test_renounceOwnership_unauth(self, factory: MediaFactory, accounts: Tuple[ChecksumAddress]):
        assert factory.w3.eth.account.address != accounts[0], "test needs to run with the non-deployer account"
        # factory.sendTransaction(factory.renounceOwnership)
        with raises(SolidityError):
            factory.sendTransaction_unauth(factory.renounceOwnership())

    def test_transferOwnership_unauth(self, factory: MediaFactory, accounts: Tuple[ChecksumAddress]):
        assert factory.w3.eth.account.address != accounts[0], "test needs to run with the non-deployer account"
        with raises(SolidityError):
            factory.sendTransaction(factory.transferOwnership(accounts[1]))

    def test_upgradeMedia_unauth(self, factory: MediaFactory, accounts: Tuple[ChecksumAddress], depl_media: ZapMedia):
        assert factory.w3.eth.account.address != accounts[0], "test needs to run with the non-deployer account"
        with raises(SolidityError):
            factory.sendTransaction(factory.upgradeMedia(depl_media.address))
