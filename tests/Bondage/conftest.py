from pytest import MonkeyPatch, fixture

from web3 import Web3

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from artifacts.src import Artifacts
from zap_token.curve import Curve

_w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
_abi = {"bondage": Artifacts["BONDAGE"],
        "zap_token": Artifacts["ZAP_TOKEN"]}
coor_artifact = Artifacts["ZAPCOORDINATOR"]

""" Arrange/SetUp Section
"""


@fixture(scope="module")
def w3():
    return _w3


@fixture(scope="module")
def address(w3):
    return {name: Web3.toChecksumAddress(
        abi["networks"]["31337"]["address"])
        for name, abi in _abi.items()}


@fixture(scope="module")
def bond_contract(w3, address):
    _bond_contract = w3.eth.contract(
        address=address["bondage"],
        abi=_abi["bondage"]["abi"])

    return _bond_contract


@fixture(scope="class")
def zt_contract(w3, address):
    _zt_contract = w3.eth.contract(
        address=address["zap_token"],
        abi=_abi["zap_token"]["abi"])

    return _zt_contract


@fixture(scope="module")
def functions(bond_contract):
    return bond_contract.functions


@fixture(scope="module")
def accounts(w3):
    return w3.eth.accounts


@fixture(scope="module")
def owner(accounts):
    return accounts[0]


@fixture(scope="module")
def subscriber(accounts):
    return accounts[1]


@fixture(scope="module")
def oracle(accounts):
    return accounts[8]


@fixture(scope="module")
def broker(accounts):
    return accounts[3]


@fixture(scope="module")
def escrower(accounts):
    return accounts[4]


def _ZapBondage(bond_contract):

    mp = MonkeyPatch()
    # same as setting the return_value of a mock obj

    class MockBaseContract:
        def __init__(self, artifact_name, artifact_dir=None, network_id=None,
                     network_provider=None, coordinator=None,
                     address=None, web3=None):

            self.name = artifact_name
            self.artifact = Artifacts[artifact_name]
            coor_artifact = Artifacts["ZAPCOORDINATOR"]
            self.provider = web3 or _w3
            self.network_id = network_id or "1"
            self.coordinator = self.provider.eth.contract(
                abi=coor_artifact['abi'],
                address=coor_artifact['networks'][self.network_id]['address'])

            self.address =\
                self.artifact["networks"][self.network_id]["address"]
            self.contract = bond_contract

    mp.setattr("bondage.BaseContract", MockBaseContract)
    from bondage import ZapBondage

    try:
        return(ZapBondage({"network_id": "31337"}))
    except Exception as e:
        raise e


@fixture(scope="module")
def Zap_Bondage():

    zap_bond_obj = _ZapBondage
    yield zap_bond_obj
    del zap_bond_obj


@fixture(scope="module")
def provider(oracle):
    return {"pubkey": 108,
            "title": '0x4269616e6361',
            "address": oracle,
            "endpoint_params": ['param1', 'param2'],
            "endpoint": 'Fibonacci',
            "query": 'btcPrice',
            "curve": Curve([2, 5000, 2000, 1000,
                            2, 0, 3000, 10000]),
            "broker": '0x0000000000000000000000000000000000000000'
            }


@fixture(scope="module")
def anyio_backend():
    """ Ensures anyio uses the default, pytest-asyncio plugin
        for running async tests
    """
    return 'asyncio'


@fixture(scope="class")
def instance(Zap_Bondage, bond_contract):
    _instance = Zap_Bondage(bond_contract)
    return _instance
