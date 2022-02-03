from pytest import fixture

from web3 import Web3

from src.artifacts.src.index import Artifacts
from src.types.types import const

"""Setup"""

_w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
_abi = {'dispatch': Artifacts['DISPATCH'],
        'registry': Artifacts['REGISTRY'],
        'bondage': Artifacts['BONDAGE'],
        'zap_token': Artifacts['ZAP_TOKEN']}


@fixture(scope="module")
def w3():
    return _w3


@fixture(scope="module")
def address(w3):
    return {name: Web3.toChecksumAddress(
        abi["networks"]["31337"]["address"])
        for name, abi in _abi.items()}


@fixture(scope="module")
def dispatch_contract(w3, address):
    _dispatch_contract = w3.eth.contract(
        address=address["dispatch"],
        abi=_abi["dispatch"]["abi"])

    return _dispatch_contract


@fixture(scope="class")
def token_contract(w3, address):
    _token_contract = w3.eth.contract(
        address=address["zap_token"],
        abi=_abi["zap_token"]["abi"])

    return _token_contract


@fixture(scope='class')
def bondage_contract(w3, address):
    bond_contract = w3.eth.contract(
        address=address['bondage'],
        abi=_abi['bondage']['abi'])
    return bond_contract


@fixture(scope='class')
def registry_contract(w3, address):
    reg_contract = w3.eth.contract(
        address=address['registry'],
        abi=_abi['registry']['abi'])
    return reg_contract


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


@fixture(scope="module")
def provider(oracle):
    prov_dict = {
        "pubkey": 108,
        "title": '0x4269616e6361',
        "address": oracle,
        "endpoint_params": ['param1', 'param2'],
        "endpoint": 'Fibonacci',
        "query": 'btcPrice',
        "curve": [2, 5000, 2000, 1000, 2, 0, 3000, 10000],
        "broker": '0x0000000000000000000000000000000000000000'
    }
    return prov_dict


@fixture(scope="module")
def anyio_backend():
    return 'asyncio'


@fixture(scope='module')
def meta_config(subscriber, w3):
    config = {
        'from_address': subscriber,
        'gas': const.DEFAULT_GAS,
        'gas_price': w3.eth.gas_price
    }
    return config


@fixture(scope='module')
def query_config(oracle, provider, subscriber, w3, meta_config):
    config = {
        'provider': oracle,
        'query': provider['query'],
        'endpoint': provider['endpoint'],
        'endpoint_params': provider['endpoint_params'],
        **meta_config
    }
    return config
