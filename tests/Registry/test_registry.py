""" Tests the setting up, transactions and calls of the Zap Registry contract.

    This is an integration test that uses the Zap Hardhat testing environment
    to test the output and side effects of Zap Registry.

    Web3 is initialized and used to make calls and transactions to Hardhat and
    receive events from the testing environment.

    Uses Pytest's fixture decorators to facilitate the setup of this test.
    Fixtures are ran once the first time they're requested and their return
    values are cached for the remainder of the test.
"""
from pytest import (
    MonkeyPatch, raises, fixture, mark
)

from web3 import Web3

from os.path import join, realpath
import sys
from subprocess import run
sys.path.insert(0, realpath(join(__file__, "../../../src/")))


from Artifacts.src.index import Artifacts
from Types.types import const, txid
from ZapToken.Curve.curve import Curve


# @fixture
# def test_provider():
#     return EthereumTesterProvider()


# @fixture
# def tester(test_provider):
#     return test_provider.ethereum_tester


# @fixture
# def w3(test_provider):
#     return Web3(test_provider)

# @fixture(autouse=True)
# def prepare_hh():
#     run(["wsl", "-d Ubuntu", "-e", "killall node"], shell=True)
#     run(["wsl", "-d Ubuntu", "-e",
#          "~/projects/zap-hardhat/start.sh"], shell=True)


w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
abi = Artifacts["REGISTRY"]
coor_artifact = Artifacts["ZAPCOORDINATOR"]
_address = abi["networks"]["31337"]["address"]


@fixture
def reg_contract():
    _reg_contract = w3.eth.contract(address=_address,
                                    abi=abi["abi"])
    return _reg_contract


@fixture
def coor():
    _coor = w3.eth.contract(abi=coor_artifact['abi'],
                            address=coor_artifact['networks']["31337"]['address'])
    return _coor


@fixture
def funcs(reg_contract):
    _funcs = reg_contract.functions.__dict__
    del _funcs['_functions']
    del _funcs['abi']
    return _funcs


@fixture
def coor_funcs(coor):
    _coor_funcs = coor.functions.__dict__
    del _coor_funcs['_functions']
    del _coor_funcs['abi']
    return _coor_funcs


""" Arrange/SetUp Section
"""


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
            self.coordinator = self.provider.eth.contract(abi=coor_artifact['abi'],
                                                          address=coor_artifact['networks'][self.network_id]['address'])
            self.address = self.artifact["networks"][self.network_id]["address"]
            self.contract = reg_contract

    mp.setattr("Registry.registry.BaseContract", MockBaseContract)
    from Registry.registry import ZapRegistry

    try:
        return(ZapRegistry({"network_id": "31337"}))
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
    del zap_reg_obj


@fixture
def functions(reg_contract):
    return reg_contract.functions


# @fixture
# def all_oracles(functions):
#     return functions.getAllOracles().call()


@fixture
def oracle(functions):
    return functions.getOracleAddress(0).call()


@fixture
def account():
    return w3.eth.accounts[11]


@fixture
def pubkey(functions, account):
    return functions.getPublicKey(account).call()


@fixture
def anyio_backend():
    """ Ensures anyio uses the default, pytest-asyncio plugin
        for running async tests
    """
    return 'asyncio'


""" pytest section
"""


class TestRegistry:
    """ Tests the initialization and functionality of Zap's Registry Contract
    """

    @fixture
    def instance(self, Zap_Registry, reg_contract):
        """ SetUp: ZapRegistry instance.

            This instance is cached and can be reused for
            the remainder of the test.
        """
        instance = Zap_Registry(reg_contract)
        return instance

    def test_init(self, instance, funcs, coor_funcs):
        """ Test if ZapRegistry is initialized

            Tests is the static attributes are all present and are valid
        """
        contract = instance.contract
        coor = instance.coordinator
        functions_dict = contract.functions.__dict__
        coordinator_dict = coor.functions.__dict__

        assert instance
        assert instance.name == "REGISTRY"
        assert instance.artifact == Artifacts["REGISTRY"]
        assert isinstance(instance.artifact, dict)
        assert isinstance(instance.provider, Web3)
        assert instance.provider == instance.contract.web3
        assert instance.network_id == "31337"
        assert instance.address == "0xa513E6E4b8f2a923D98304ec87F64353C4D5C853"
        assert instance.address == instance.contract.address

        for func, coor_func in zip(funcs, coor_funcs):
            assert func in functions_dict
            assert coor_func in coordinator_dict

    # @mark.skip(reason="Provider already initialized.")
    @mark.anyio
    async def test_initiate_provider(self, instance, pubkey, account):
        opt = {"public_key": pubkey, "title": "Registry",
               "From": account, "gas": 4 * 10**5}
        tx = await instance.initiate_provider(**opt)

        assert isinstance(tx, str)

    @mark.anyio
    async def test_get_provider_publickey(self, instance, pubkey, account):
        pubkey_instance = await instance.get_provider_publickey(account)

        assert pubkey_instance
        assert isinstance(pubkey_instance, int)
        assert pubkey_instance == pubkey

    @mark.anyio
    async def test_get_provider_title(self, instance, account):
        title_instance = await instance.get_provider_title(account)

        assert title_instance
        assert isinstance(title_instance, str)
        # assert title_instance ==

    @mark.anyio
    async def test_is_provider_initiated(self, instance, account):
        isInit = await instance.is_provider_initiated(account)

        assert isInit is True
        assert isinstance(isInit, bool)

    @mark.anyio
    async def test_set_provider_title(self, instance, account):
        title_test = "REGISTRY"

        tx = await instance.set_provider_title(account, title_test)

        assert tx
        print(tx)
        assert isinstance(tx, str)

    @mark.anyio
    async def test_set_provider_param(self, instance, pubkey, account):
        tx = await instance.set_provider_param(pubkey, 11, account)

        assert tx
        assert isinstance(tx, str)

    @mark.anyio
    async def test_get_provider_param(self, instance, account, pubkey):
        param = await instance.get_provider_param(
            account, Web3.toBytes(pubkey))

        assert param
        print(param)
        assert isinstance(param, bytes)

    @mark.anyio
    async def test_get_all_providers(self, instance):
        provs = await instance.get_all_providers()
        assert provs
        assert isinstance(provs, list)

    @mark.anyio
    async def get_all_provider_params(self, instance, address, pubkey):
        params = await instance.get_provider_param(
            address, pubkey)

        assert params
        print(params)
        assert isinstance(params, list)

    # @mark.skip(reason="Possible error with python types")
    @mark.anyio
    async def test_initiate_provider_curve(self, instance, account):
        term = [3, 0, 0, 3, 100000]
        opts = {"end_point": 'hi', "term": term,
                "From": account, "gasPrice": int(5e4)}

        curve = await instance.initiate_provider_curve(**opts)

        assert curve
        assert isinstance(curve, str)

    @mark.anyio
    async def test_get_provider_address_by_index(self, instance):
        addy = await instance.get_provider_address_by_index(0)
        assert addy
        assert isinstance(addy, str)

    @mark.anyio
    async def test_get_provider_endpoints(self, instance, account):
        e = await instance.get_provider_endpoints(account)

        assert e
        print(e)
        assert isinstance(e, list)

        return e

    @fixture
    async def endpoints(self, instance, account):
        e = await instance.get_provider_endpoints(account)

        return e

    @mark.anyio
    async def test_get_provider_curve(self, instance,
                                      account, endpoints):
        e = endpoints
        curve = await instance.get_provider_curve(account, e[-1])

        assert curve
        print(curve.values)
        assert isinstance(curve, Curve)

    @mark.anyio
    async def test_clear_endpoint(self, instance,
                                  endpoints, 
                                  account):
        e = endpoints
        tx = await instance.clear_endpoint(
            e[-1], account, int(5e3))

        assert tx
        print(tx)
        assert isinstance(tx, str)

    # @mark.anyio
    # async def test_(self, instance):
    #     get = await instance.something()

    #     assert get
    #     print(get)
    #     assert isinstance(get, bytes)


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
