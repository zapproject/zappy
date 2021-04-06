from pytest import MonkeyPatch, fixture

from web3 import Web3

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from artifacts.src import Artifacts
from zap_token.curve import Curve

_w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
abi = Artifacts["ZAP_TOKEN"]
coor_artifact = Artifacts["ZAPCOORDINATOR"]
_address = Web3.toChecksumAddress(abi["networks"]["31337"]["address"])


@fixture(scope="module")
def w3():
    return _w3


@fixture(scope="module")
def zt_contract(w3):
    _zt_contract = w3.eth.contract(address=_address,
                                   abi=abi["abi"])
    return _zt_contract


@fixture(scope="module")
def coor():
    _coor = _w3.eth.contract(
        abi=coor_artifact['abi'],
        address=coor_artifact['networks']["31337"]['address'])
    return _coor


def _ZapToken(zt_contract, coor):

    mp = MonkeyPatch()

    class MockBaseContract:
        def __init__(self, artifact_name, artifact_dir=None, network_id=None,
                     network_provider=None, coordinator=None,
                     address=None, web3=None):

            self.name = artifact_name
            self.artifact = Artifacts[artifact_name]
            self.provider = web3 or _w3
            self.network_id = network_id or "1"
            self.coordinator = coor or coordinator
            self.address =\
                self.artifact["networks"][self.network_id]["address"]
            self.contract = zt_contract

    mp.setattr("zap_token.BaseContract", MockBaseContract)
    from zap_token import ZapToken

    try:
        return(ZapToken({"network_id": "31337"}))
    except Exception as e:
        raise e


@fixture(scope="module")
def Zap_Token():
    zap_tok_obj = _ZapToken
    yield zap_tok_obj
    del zap_tok_obj


@fixture(scope="module")
def functions(reg_contract):
    return reg_contract.functions


@fixture(scope="module")
def accounts():
    return _w3.eth.accounts


@fixture(scope="class")
def owner(accounts):
    return accounts[0]


@fixture(scope="module")
def subscriber_1(accounts):
    return accounts[1]


@fixture(scope="class")
def oracle(accounts):
    return accounts[2]


@fixture(scope="module")
def subscriber_2(accounts):
    return accounts[3]


@fixture(scope="module")
def provider_1(subscriber_1):
    return {"pubkey": 101,
            "title": '0x426c696365726f',
            "address": subscriber_1,
            "endpoint_params": ['param1', 'param2'],
            "endpoint": 'Wiles',
            "query": 'btcPrice',
            "curve": Curve([3, 0, 0, 1, 1222]),
            "broker": '0x0000000000000000000000000000000000000000'
            }


@fixture(scope="module")
def provider_2(subscriber_2):
    return {"pubkey": 103,
            "title": '0x456e7a69616e',
            "address": subscriber_2,
            "endpoint_params": ['param1', 'param2'],
            "endpoint": 'Jacobi',
            "query": 'btcPrice',
            "curve": Curve([1, 100, 1000]),
            "broker": '0x0000000000000000000000000000000000000000'
            }


@fixture(scope="module")
def anyio_backend():
    """ Ensures anyio uses the default, pytest-asyncio plugin
        for running async tests
    """
    return 'asyncio'


@fixture(scope="class")
def instance(Zap_Token, zt_contract, coor):
    """ SetUp: ZapRegistry instance.

        This instance is cached and can be reused for
        the remainder of the test.
    """
    instance = Zap_Token(zt_contract, coor)
    return instance
