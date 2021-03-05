from pytest import (
    MonkeyPatch, raises, fixture
)

from unittest.mock import MagicMock, patch


from os.path import join, realpath
import sys
sys.path.insert(0, realpath(join(__file__, "../../../src/")))

from Artifacts.src.index import Artifacts


MockContract = MagicMock(
    abi=['abi'], address="0x000000000000000000", name="MOCKCONTRACT")


@patch('Registry.registry.Web3', autospec=True)
@patch('Registry.registry.NetworkProviderOptions', autospec=True)
@patch('ZapToken.Curve.curve.Curve', autospec=True)
def _ZapRegistry(mock_Curve, mock_npo, mock_Web3):

    mock_Web3.return_value = MagicMock()
    w3 = mock_Web3()

    mock_npo.return_value = {}

    mp = MonkeyPatch()
    # same as setting the return_value of a mock obj
    mp.setattr(w3.eth, "contract", MockContract)

    class MockBaseContract:
        def __init__(self, artifact_name, artifact_dir=None, network_id=None,
                     network_provider=None, coordinator=None,
                     address=None, web3=None):
            self.name = artifact_name
            self.artifact = Artifacts[artifact_name]
            self.provider = web3 or w3
            self.networkId = "1"
            self.coordinator = MockContract
            self.address = self.artifact["networks"][self.networkId]["address"]
            MockContract1 = MagicMock(abi=self.artifact["abi"],
                                      address=self.address)
            self.contract = MockContract1

    # sets the returned class as MockBaseContract
    mp.setattr("Registry.registry.BaseContract", MockBaseContract)
    from Registry.registry import BaseContract
    print(BaseContract("REGISTRY").__dict__)  # ✔️ all good
    from Registry.registry import ZapRegistry

    return(ZapRegistry())  # ❌ uses the original BaseContract


# @fixture()
# def ZapRegistry():
#     return _ZapRegistry()


def test_init(ZapRegistry):
    assert ZapRegistry


print(_ZapRegistry().__dict__)

# def test_init():
#     assert isinstance(_ZapRegistry(), ZapRegistry)
