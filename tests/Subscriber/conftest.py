from pytest import MonkeyPatch, fixture
from unittest.mock import Mock

from web3 import Web3

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from artifacts.src import Artifacts
from zap_token import Curve
from zaptypes import const


_w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
abi_dir = {"registry": Artifacts["REGISTRY"],
           "dispatch": Artifacts["DISPATCH"],
           "bondage": Artifacts["BONDAGE"],
           "arbiter": Artifacts["ARBITER"],
           "zap_token": Artifacts["ZAP_TOKEN"]
           }


@fixture(scope="module")
def w3():
    return _w3


# @fixture(scope="module")
# def zt():
#     zt_abi = Artifacts["ZAP_TOKEN"]
#     zt_address =\
#         _w3.toChecksumAddress(
#             zt_abi["networks"]["development"]["address"])

#     return (zt_abi, zt_address)


coor_artifact = Artifacts["ZAPCOORDINATOR"]
_address_dir = {contract:
                Web3.toChecksumAddress(
                    abi["networks"]["31337"]["address"])
                for contract, abi in abi_dir.items()}

""" Arrange/SetUp Section
"""


@fixture(scope="module")
def contracts():
    _contracts = {name: _w3.eth.contract(address=address,
                                         abi=abi_dir[name]["abi"])
                  for name, address in _address_dir.items()}
    return _contracts


@fixture(scope="module")
def coor():
    _coor = _w3.eth.contract(
        abi=coor_artifact['abi'],
        address=coor_artifact['networks']["31337"]['address'])
    return _coor


@fixture(scope="module")
def funcs(contracts):
    _funcs = {}
    for name, contract in contracts.items():
        _funcs[name] = contract.functions.__dict__
        del _funcs[name]['_functions']
        del _funcs[name]['abi']
    return _funcs


@fixture(scope="module")
def coor_funcs(coor):
    _coor_funcs = coor.functions.__dict__
    del _coor_funcs['_functions']
    del _coor_funcs['abi']
    return _coor_funcs


@fixture(scope="module")
def accounts():
    return _w3.eth.accounts


@fixture(scope="class")
def owner(accounts):
    return accounts[0]


@fixture(scope="class")
def subscriber(accounts):
    return accounts[1]


@fixture(scope="class")
def oracle(accounts):
    return accounts[2]


@fixture(scope="class")
def broker(accounts):
    return accounts[3]


def _ZapSubscriber(contracts, funcs, subscriber):

    mp = MonkeyPatch()

    """ Mocked Contract classes

        These mocked objects have defined constants within this body
        and will have variables to test various correct and erroneous
        test cases within the test module.

        constants:
            ContractClass.contact: the Solidty contract
    """

    # ZapBondage
    mock_Bondage = Mock()

    # ZapToken
    mock_ZapToken = Mock()
    # print(mock_ZapToken.contract)
    # mock_ZapToken.contract =

    mock_Dispatch = Mock()  # ZapDispatch
    mock_Arbiter = Mock()  # ZapArbiter
    mock_Registry = Mock()  # ZapRegistry

    mp.setattr("subscriber.ZapBondage", mock_Bondage)
    mp.setattr("subscriber.ZapToken", mock_ZapToken)
    mp.setattr("subscriber.ZapDispatch", mock_Dispatch)
    mp.setattr("subscriber.ZapArbiter", mock_Arbiter)
    mp.setattr("subscriber.ZapRegistry", mock_Registry)

    # reminder: might need to run the Mock.configure_mock(**attrs)
    # before running subscriber tests

    from subscriber import ZapSubscriber

    try:
        return(
            ZapSubscriber(
                subscriber,
                {"network_id.return_value": "31337"}))
    except Exception as e:
        raise e


@fixture(scope="module")
def Zap_Subscriber():
    zap_sub_obj = _ZapSubscriber
    yield zap_sub_obj
    del zap_sub_obj


@fixture(scope="module")
def hardhat_provider():
    return "http://localhost:8545"


@fixture(scope="module")
def provider(accounts):
    return {"pubkey": 102,
            "title": '0x426f72676573697573',
            "address": accounts[2],
            "endpoint_params": ['param1', 'param2'],
            "endpoint": 'Wiles',
            "query": 'btcPrice',
            "curve": Curve([3, 0, 0, 1, 1222]),
            "broker": '0x0000000000000000000000000000000000000000'
            }


@fixture(scope="module")
def function():
    pass


@fixture(scope="module")
def anyio_backend():
    """ Ensures anyio uses the default, pytest-asyncio plugin
        for running async tests
    """
    return 'asyncio'


@fixture(scope="class")
def instance(Zap_Subscriber, contracts, funcs, subscriber):
    return Zap_Subscriber(contracts, funcs, subscriber)


# @fixture(scope="module")
# def function():
#     return None


# @fixture(scope="module")
# def function():
#     return None


# @fixture(scope="module")
# def function():
#     return None


# @fixture(scope="module")
# def function():
#     return None
