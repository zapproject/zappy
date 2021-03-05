from pytest import (
    MonkeyPatch, raises, fixture
)

from unittest.mock import MagicMock, patch, AsyncMock


from os.path import join, realpath
import sys
sys.path.insert(0, realpath(join(__file__, "../../../src/")))

from Artifacts.src.index import Artifacts


MockContract = MagicMock(
    abi=['abi'], address="0x000000000000000000", name="MOCKCONTRACT")

""" Arrange/SetUp Section
"""


@patch('Registry.registry.Web3', autospec=True)
def _ZapRegistry(mock_Web3):
    """ WIP: Returns an object representation of ZapRegistry for testing.

        This ZapRegistry object has a mocked BaseContract
        used for its init phase.

        This mocked BaseContract has fixture data, including its contract.

        Contracts (and/or their functions) are asynchronous mock objects.
        Almost everything else is base of Magic mock objects.

    """

    mock_Web3.return_value = MagicMock()
    w3 = mock_Web3()

    mp = MonkeyPatch()
    # same as setting the return_value of a mock obj
    mp.setattr(w3.eth, "contract", MockContract)

    class MockBaseContract():
        def __init__(self, artifact_name, artifact_dir=None, network_id=None,
                     network_provider=None, coordinator=None,
                     address=None, web3=None):

            self.name = artifact_name
            self.artifact = Artifacts[artifact_name]
            self.provider = web3 or w3
            self.networkId = "1"
            self.coordinator = MockContract
            self.address = self.artifact["networks"][self.networkId]["address"]
            MockContract1 = AsyncMock(abi=self.artifact["abi"],
                                      address=self.address)
            self.contract = MockContract1
            # return value evals to none right now, need to know result of call
            self.contract.functions.getAllOracles.call.return_value = None

    mp.setattr("Registry.registry.BaseContract", MockBaseContract)
    from Registry.registry import ZapRegistry

    try:
        return(ZapRegistry())
    except Exception as e:
        raise e


@fixture()
def Zap_Registry():
    """ yield a ZapRegistry object

        This object stays in pytest cache for the lifespan of the test.
        It is not necessary to have a SetUp class method/function.

        references:
            https://docs.pytest.org/en/stable/xunit_setup.html
            https://docs.pytest.org/en/stable/fixture.html#what-fixtures-are
            https://docs.pytest.org/en/stable/fixture.html#\
                fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached
    """
    zap_reg_obj = _ZapRegistry
    yield zap_reg_obj


""" pytest section
"""


def test_init(Zap_Registry):
    """ WIP: Test if ZapRegistry is initialized

        Also tests if it has an attribute `name` that evaluates to "REGISTRY"
    """
    instance = Zap_Registry()
    assert instance
    assert instance.name == "REGISTRY"


async def task(co_mock):
    """ Will handle awaitables from contract calls/tx
    """
    await co_mock

""" python "direct calls" section
"""

# import pprint
# from asyncio import run
# provs = asyncio.run(_ZapRegistry().get_all_providers())
# zap_reg_obj = _ZapRegistry()
# provs = zap_reg_obj.get_all_providers()

# print(run(task(zap_reg_obj.contract.functions.getAllOracles())))

# pprint(zap_reg_obj.contract.functions.getAllOracles.__dict__)

# def test_init():
#     assert isinstance(_ZapRegistry(), ZapRegistry)
