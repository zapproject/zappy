""" Tests the setting up, transactions, and calls of the Zap Registry contract.

    This is an integration test that uses the Zap Hardhat testing environment
    to test the output and side effects of Zap Registry.

    Web3 is initialized and used to make calls and transactions to Hardhat and
    receive events from the testing environment.

    Uses Pytest's fixture decorators to facilitate the setup of this test.
    Fixtures are ran once the first time they're requested and their return
    values are cached for the remainder of the test.
"""
from pytest import mark

from web3 import Web3

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from zap_token.curve import Curve
from artifacts.src import Artifacts


""" pytest section
"""


class TestRegistry:
    """ Tests the initialization and functionality of Zap's Registry Contract
    """

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
    async def test_initiate_provider(self, instance, pubkey, account, title):
        opt = {"public_key": pubkey, "title": title,
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
    async def test_initiate_provider_curve(self, instance, account,
                                           endpoint, curve_values):
        term = curve_values
        opts = {"end_point": endpoint, "term": term,
                "From": account, "gas_price": int(5e4)}

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

    @mark.anyio
    async def test_get_provider_curve(self, instance,
                                      account, endpoint):
        e = endpoint
        curve = await instance.get_provider_curve(account, e)

        assert curve
        print(curve.values)
        assert isinstance(curve, Curve)

    def decode_params(self, instance, params):
        return(instance.decode_params(params))

    def encode_params(self, instance, params):
        return(instance.encode_params(params))

    @mark.anyio
    async def test_set_endpoint_params(self, instance, account,
                                       endpoint, endpoint_params):
        tx = await instance.set_endpoint_params(
            endpoint, account,
            int(5e4),
            endpoint_params=endpoint_params)

        assert tx
        assert isinstance(tx, str)

    @mark.anyio
    async def test_get_endpoint_broker(self, instance, broker):
        broker = await instance.get_endpoint_broker(broker, "123")

        assert broker
        assert isinstance(broker, str)

    @mark.anyio
    async def test_is_endpoint_set(self, instance, account, endpoint):
        isSet = await instance.is_endpoint_set(account, endpoint)

        assert isSet is True
        assert isinstance(isSet, bool)

    @mark.anyio
    async def test_clear_endpoint(self, instance,
                                  endpoint,
                                  account):
        e = endpoint
        tx = await instance.clear_endpoint(
            e, account, int(5e3))

        assert tx
        print(tx)
        assert isinstance(tx, str)

    # @mark.anyio
    # async def test_(self, instance):
    #     get = await instance.something()

    #     assert get
    #     print(get)
    #     assert isinstance(get, bytes)


# async def task(co_mock):
#     """ Will handle awaitables from contract calls/tx
#     """
#     await co_mock

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
