from typing import TypedDict, Callable, Any, NewType
from collections import namedtuple

address = NewType("address", str)
txid = NewType("txid", str)
NumType = NewType("NumType", float)  # need confirmation on this datatype

"""
    Python has a builtin called the TypedDict that
    is structured and can be accessed in a similar way
    to a TypeScript interface

    Py also lacks constants, but named tuples behaves
    the same way
"""


class defaultTx(TypedDict, total=False):
    From: str
    gas: float
    gasPrice: float


class Filter(TypedDict, total=False):
    fromBlock: float
    toBlock: float
    provider: str
    subscriber: str
    terminator: str
    endpoint: str
    ID: float


class listenEvent(TypedDict, total=False):
    filtr: Filter
    callback: Callable[..., Any]  # accepts a function, takes any # of args


class Artifact(TypedDict, total=False):
    contract_name: str
    abi: dict
    networks: dict = {"networkId": {"address": str}}


class BaseContractType(TypedDict, total=False):
    """ Base Contract """
    artifactsDir: str
    artifactName: str
    networkId: int
    networkProvider: Any or None
    contract: Any
    coordinator: str
    address: str
    web3: Any


class NetworkProviderOptions(TypedDict, total=False):
    artifactsDir: str
    networkId: int
    networkProvider: Any
    coordinator: str
    address: str
    web3: Any


class TransferType(defaultTx, TypedDict):
    to: str
    amount: float


Constants = namedtuple("Constants", ["DEFAULT_GAS", "NULL_ADDRESS"])
const = Constants(4e5, "0x0000000000000000000000000000000000000000")
"""
    accessed by const.DEFAULT_GAS and const.NULL_ADDRESS
"""


class SubscriptionInit(defaultTx, TypedDict, total=False):
    provider: str
    endpoint: str
    endpoint_params: list
    blocks: NumType
    pubkey: NumType


class SubscriptionEnd(defaultTx, TypedDict, total=False):
    provider: str


class SubscriptionType(TypedDict):
    provider: str
    subscriber: str
    endpoint: str


############# BONDAGE #############

class TokenBondType(defaultTx, TypedDict):
    endpoint: str
    dots: NumType


class BondType(defaultTx, TypedDict, total=False):
    subscriber: str
    provider: str
    endpoint: str
    dots: NumType


class DelegateBondType(BondType, TypedDict):
    subscriber: str


class UnbondType(defaultTx, TypedDict):
    provider: str
    endpoint: str
    dots: NumType


class SubscribeType(defaultTx, TypedDict):
    provider: str
    endpoint: str
    dots: NumType
    endpoint_params: list  # need confirmation on this data type


class SubscriberHandler(TypedDict, total=False):
    """
        Callable types accepts a function, takes any # of args
    """
    handleResponse: Callable[..., Any]
    handleUnsubscription: Callable[..., Any]
    handleSubscription: Callable[..., Any]


class ApproveType(defaultTx, TypedDict):
    provider: str
    zapNum: float


class BondArgs(defaultTx, TypedDict):
    provider: str
    endpoint: str
    dots: NumType


class UnbondArgs(defaultTx, TypedDict):
    provider: str
    endpoint: str
    dots: NumType


class DelegateBondArgs(defaultTx, TypedDict):
    provider: str
    endpoint: str
    dots: NumType
    subscriber: str


class BondageArgs(TypedDict, total=False):
    subscriber: str
    provider: str
    endpoint: str
    dots: NumType
    zapNum: NumType


class CalcBondRateType(TypedDict):
    provider: str
    endpoint: str
    zapNum: NumType


class BondFilter(Filter, TypedDict, total=False):
    numDots: NumType
    numZap: NumType


############# TOKEN DOT FACTORY #############

# accepts a function, takes error and hash as args
TransactionCallback = NewType(
    "TransactionCallback", Callable[str, str], None)


############# PROVIDER #############

class InitProvider(defaultTx, TypedDict):
    public_key: str
    title: str


class InitCurve(defaultTx, TypedDict, total=False):
    endpoint: str
    term: list
    broker: address


class NextEndpoint(TypedDict):
    provider: address
    endpoint: str


class EndpointParams(defaultTx, TypedDict):
    endpoint: str
    endpoint_params: list


class SetProviderParams(defaultTx, TypedDict):
    key: str
    value: str


class SetProviderTitle(defaultTx, TypedDict):
    From: address
    title: str


class Endpoint(defaultTx, TypedDict):
    endpoint: str
