from pytest import MonkeyPatch, fixture

from web3 import Web3
# from Types.types import const, txid

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from Artifacts.src.index import Artifacts
from ZapToken.Curve.curve import Curve

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
abi = Artifacts["REGISTRY"]
coor_artifact = Artifacts["ZAPCOORDINATOR"]
_address = abi["networks"]["31337"]["address"]


""" Arrange/SetUp Section
"""


@fixture(scope="module")
def reg_contract():
    _reg_contract = w3.eth.contract(address=_address,
                                    abi=abi["abi"])
    return _reg_contract


@fixture(scope="module")
def coor():
    _coor = w3.eth.contract(
        abi=coor_artifact['abi'],
        address=coor_artifact['networks']["31337"]['address'])
    return _coor


@fixture(scope="module")
def funcs(reg_contract):
    _funcs = reg_contract.functions.__dict__
    del _funcs['_functions']
    del _funcs['abi']
    return _funcs


@fixture(scope="module")
def coor_funcs(coor):
    _coor_funcs = coor.functions.__dict__
    del _coor_funcs['_functions']
    del _coor_funcs['abi']
    return _coor_funcs


def _ZapRegistry(reg_contract):
    """ WIP: Returns an object representation of ZapRegistry for testing.

        This ZapRegistry object has a mocked BaseContract
        used for its init phase.

        This mocked BaseContract has fixture data, including its contract.

        Contracts (and/or their functions) are asynchronous mock objects.
        Almost everything else is base of Magic mock objects.

    """

    mp = MonkeyPatch()
    # same as setting the return_value of a mock obj

    class MockBaseContract:
        def __init__(self, artifact_name, artifact_dir=None, network_id=None,
                     network_provider=None, coordinator=None,
                     address=None, web3=None):

            self.name = artifact_name
            self.artifact = Artifacts[artifact_name]
            coor_artifact = Artifacts["ZAPCOORDINATOR"]
            self.provider = web3 or w3
            self.network_id = network_id or "1"
            self.coordinator = self.provider.eth.contract(
                abi=coor_artifact['abi'],
                address=coor_artifact['networks'][self.network_id]['address'])

            self.address = self.artifact["networks"][self.network_id]["address"]
            self.contract = reg_contract

    mp.setattr("Registry.registry.BaseContract", MockBaseContract)
    from Registry.registry import ZapRegistry

    try:
        return(ZapRegistry({"network_id": "31337"}))
    except Exception as e:
        raise e


@fixture(scope="module")
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
    del zap_reg_obj


@fixture(scope="module")
def functions(reg_contract):
    return reg_contract.functions


@fixture(scope="module")
def oracle(functions):
    return functions.getOracleAddress(0).call()


@fixture(scope="module")
def account():
    return w3.eth.accounts[11]


@fixture(scope="module")
def curve_values():
    return [3, 0, 0, 3, 100000]


@fixture(scope="module")
def testZapProvider(curve_values):
    _testZapProvider = {
        "pubkey": 111,
        "title": 'testProvider',
        "endpoint_params": ['p1', 'p2'],
        "endpoint": 'testEndpoint',
        "query": 'btcPrice',
        "curve": Curve(curve_values),
        "broker": '0x0000000000000000000000000000000000000000'
    }

    return _testZapProvider


@fixture(scope="module")
def endpoint(testZapProvider):
    return testZapProvider["endpoint"]


@fixture(scope="module")
def endpoint_params(testZapProvider):
    return testZapProvider["endpoint_params"]


@fixture(scope="module")
def broker(testZapProvider):
    return testZapProvider["broker"]


@fixture(scope="module")
def pubkey(testZapProvider):
    return testZapProvider["pubkey"]


@fixture(scope="module")
def title(testZapProvider):
    return testZapProvider["title"]


@fixture(scope="module")
def anyio_backend():
    """ Ensures anyio uses the default, pytest-asyncio plugin
        for running async tests
    """
    return 'asyncio'


@fixture(scope="class")
def instance(Zap_Registry, reg_contract):
    """ SetUp: ZapRegistry instance.

        This instance is cached and can be reused for
        the remainder of the test.
    """
    instance = Zap_Registry(reg_contract)
    return instance
