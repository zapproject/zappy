from web3 import Web3
from asyncio import sleep
from typing import Optional, List, Dict

from BaseContract.base_contract import BaseContract
from ZapToken.Curve.curve import Curve
from Types.types import (
    Filter, address,
    NetworkProviderOptions, const, TransactionCallback, txid
)


class ZapRegistry(BaseContract):
    """This contract manages Providers and Curve registration

       NetworkProviderOptions -- Dictionary object containing options for
                                 BaseContract init

       NetworkProviderOptions has the following keyword arguments:

            arifactsDir -- Directory where contract ABIs are located
            networkId   -- Select which network the contract is located
                           options : (mainnet, testnet, private)
            networkProvider -- Ethereum network provider (e.g. Infura or web3)

        Example:
            ZapRegistry({"networkId": 42, "networkProvider": "web3"})
    """

    def __init__(self, options: NetworkProviderOptions = {}):
        options["artifact_name"] = "REGISTRY"
        BaseContract.__init__(self, **options)

    """
        Registry storage calls for all providers
    """

    # async def task(func, action, args1=[], args2=[]):
    #     item = func(*args1).action(*args2)
    #     sleep(5)

    #     if item:
    #         return item
    #     return

    async def get_all_providers(self) -> list:
        """Get all providers in Registry Contract.

           returns a list of oracles once async is fulfilled
        """
        await sleep(3)
        return self.contract.functions.getAllOracles().call()

    async def get_provider_address_by_index(self, index: int) -> str:
        """ Look up provider's address by its index in registry storage

            returns address of indexed provider once async is fulfilled
        """
        await sleep(0.6)
        return self.contract.functions.getOracleAddress(index).call()

    """
        Provider specific calls
    """

    async def initiate_provider(self, public_key: str, title: str,
                                From: address, cb: TransactionCallback = None,
                                gas=const.DEFAULT_GAS) -> txid:
        """
            Initiates a brand endpoint in the Registry contract,
            creating an Oracle entry if need be.

            Arguments:
                public_key -- a public identifier for this oracle
                title      -- describes what data this oracle provides
                from       -- Ethereum address of the account that is
                              initializing this provider
                gas        -- Sets the fas limit for this transaction.
                              Defaults to 4 * 10**5

        """

        try:
            await sleep(3)
            tx_hash: txid = self.contract.functions.initiateProvider(
                public_key, Web3.toBytes(text=title)).transact(
                    {"from": From, "gas": gas})
            if cb:
                cb(None, tx_hash)

            return tx_hash.hex()
        except ValueError as e:
            print(e)

    async def get_provider_publickey(self, provider: address) -> int:
        """ Get a provider's public key from the registry contract.

            provider -- The address of this provider

            returns the public key number.
        """
        await sleep(0.8)
        return self.contract.functions.getProviderPublicKey(provider).call()

    async def get_provider_title(self, provider: address) -> str:
        """ Get a provider's title from the Registry contract.

            address -- The address of this provider.

            return a future that will eventually resolve into a title string
        """
        await sleep(1)
        title = Web3.toText(self.contract.functions.getProviderTitle(
            provider).call())

        return title

    async def set_provider_title(self, From: address, title: str,
                                 cb: TransactionCallback = None,
                                 gas=const.DEFAULT_GAS) -> txid:
        """ Set the new provider's title

            Arguments:
                From  -- The address of this provider
                title -- The new title of this provider
                cb    -- Callback for transactionHash event

        """
        try:
            await sleep(1.4)
            tx_hash: txid = self.contract.functions.setProviderTitle(
                Web3.toBytes(text=title)).transact(
                    {"from": From, "gas": gas})
            cb(None, tx_hash)

            return tx_hash.hex()
        except Exception as e:
            return(str(e))

    async def is_provider_initiated(self, provider: address) -> bool:
        """ Gets whether this provider has already been created.

            provider -- Gets whether this provider has already been created.

            returns a future that will eventually resolve a true/false value.
        """
        await sleep(0.13)
        return self.contract.functions.isProviderInitiated(provider).call()

    async def set_provider_param(self, key: int, value: int,
                                 From: address, gas=const.DEFAULT_GAS) -> txid:
        await sleep(1.2)
        return self.contract.functions.setProviderParameter(
            Web3.toBytes(key), Web3.toBytes(value)).transact(
            {"from": From, "gas": gas}).hex()

    async def get_provider_param(self, provider: address, key: int) -> bytes:
        """ Get a parameter from a provider

            provider -- The address of the provider
            key      -- The key you're getting

            returns a future that will be resolved with the value of the keys
        """
        await sleep(0.82)
        return self.contract.functions.getProviderParameter(provider, Web3.toBytes(key)).call()

    async def get_all_provider_params(self, provider: address) -> List[bytes]:
        """ Get all the parameters of a provider

            provider -- The address of the provider

            returns a future that will be resolved with all the keys
        """
        await sleep(0.89)
        return await self.contract.functions.getAllProviderParams(provider).call()

    async def get_provider_endpoints(self, provider: address) -> List[str]:
        """ Get the endpoints of a given provider

            provider -- The address of this provider

            returns a Future that will be eventually resolved with
                    the list of endpoints of the provider.
        """
        await sleep(0.58)
        endpoints = self.contract.functions.getProviderEndpoints(
            provider).call()
        endpoints = [Web3.toHex(endpoint) for endpoint in endpoints]
        valid_endpoints = [e for e in endpoints if e != '']

        return valid_endpoints

    """
        Provider's specific endpoint calls
    """

    async def initiate_provider_curve(self, end_point, term,
                                      From, gasPrice,
                                      cb: TransactionCallback = None,
                                      broker=const.NULL_ADDRESS,
                                      gas=const.DEFAULT_GAS) -> txid:
        """"""
        await sleep(0.247)

        try:
            tx_hash: txid = self.contract.functions.initiateProviderCurve(
                Web3.toBytes(text=end_point),
                term, broker).transact(
                {"from": From, "gas": gas, "gasPrice": int(gasPrice)})
            if cb:
                cb(None, tx_hash)
            return tx_hash.hex()
        except ValueError as e:
            print(str(e))

    async def clear_endpoint(self, endpoint, From, gasPrice,
                             cb: TransactionCallback = None,
                             gas=const.DEFAULT_GAS) -> txid:
        try:
            await sleep(1.6)
            tx_hash: txid = self.contract.functions.clearEndpoint(
                Web3.toBytes(text=endpoint)).transact(
                {"from": From, "gas": gas, "gasPrice": gasPrice})
            if cb:
                cb(None, tx_hash)
            return tx_hash.hex()
        except Exception as e:
            print(e)

    async def get_provider_curve(self, provider: address, endpoint: str):
        await sleep(0.8)
        terms: list = self.contract.functions.getProviderCurve(
            provider, Web3.toBytes(text=endpoint)).call()

        return Curve([int(t) for t in terms])

    def encode_params(self, endpoint_params: list = [], ):
        pars = endpoint_params
        hex_params =\
            [el if el.find('0x') == 0 else Web3.toHex(text=el) for el in pars]
        bytes_params =\
            [bytearray(Web3.toBytes(hexstr=hex_p)) for hex_p in hex_params]
        params = []

        from math import ceil
        for element in bytes_params:
            if len(element) <= 32:
                params.append(Web3.toHex(element))
                continue
            chunks_len = ceil((len(element) + 2) / 32)
            param_bytes_w_len = [0, chunks_len].extend(element)
            for i in range(0, chunks_len):
                start = i * 32
                end = start + 32
                params.append(Web3.toHex(param_bytes_w_len[start:end]))
        return params

    def decode_params(self, raw_params: List[str] = []):
        bytes_params = [bytearray(Web3.toBytes(hexstr=el))

                        for el in raw_params]
        params = []
        i = 0
        length = len(bytes_params)

        while i < length:
            is_start_o_chunks =\
                bytes_params[i][0] == 0 and\
                bytes_params[i][1] > 1 and\
                len(bytes_params[i]) == 32

            if not is_start_o_chunks:
                params.append(Web3.toHex(bytes_params[i]))
                i += 1
                continue

            chunks_len = bytes_params[i][1]
            end = i + chunks_len

            raw_bytes = bytes_params[i][2:]
            i += 1

            while i < end:
                raw_bytes = raw_bytes.extend(bytes_params[i])
                i += 1

            params.append(Web3.toHex(raw_bytes))

        try:
            return [Web3.toText(hexstr=raw_hex) for raw_hex in params]
        except Exception as e:
            print(e)

    async def set_endpoint_params(self, endpoint: str, From: address,
                                  gasPrice: int,
                                  cb: Optional[TransactionCallback] = None,
                                  endpoint_params: Optional[List[str]] = [],
                                  gas: Optional[int] = const.DEFAULT_GAS
                                  ) -> txid:
        """ Initialize endpoint params for an endpoint.
            Can only be called by the owner of this oracle.

            :param str endpoint: Data endpoint of the provider
            :param List[str] endpoint_params: The parameters that this endpoint
                                              accepts as query arguments
            :param address from: The address of the owner of this oracle
            :param int gas: Sets the gas limit for this
                                  transaction (optional)
            :param  cb: Callback for transactionHash event

            :returns Future(txid) Returns a Promise that will eventually
                     resolve into a transaction hash
        """
        params = self.encode_params(endpoint_params)

        try:
            await sleep(0.53)
            tx_hash = self.contract.functions.setEndpointParams(
                Web3.toBytes(text=endpoint), params).transact(
                {"from": From, "gas": gas})
            if cb:
                cb(None, tx_hash)
            return tx_hash.hex()
        except Exception as e:
            print(e)

    async def get_endpoint_broker(self, provider: address,
                                  endpoint: str) -> str:
        await sleep(0.27)
        return self.contract.functions.getEndpointBroker(
            provider,
            Web3.toBytes(text=endpoint)).call()

    async def is_endpoint_set(self, provider: address, endpoint: str):
        await sleep(0.2)
        unset: bool = self.contract.functions.getCurveUnset(
            provider,
            Web3.toBytes(text=endpoint)).call()

        return not unset

    """ Events
    """
    from typing import Callable

    async def listen(self, callback: Callable[..., None]):
        sleep(3)
        self.contract.events.allEvents(callback)

    async def listen_new_provider(self, callback: TransactionCallback,
                                  filters: Filter = {}):
        sleep(2)
        self.contract.events.NewProvider(filters, callback)

    async def listen_new_curve(self, callback: TransactionCallback,
                               filters: Filter):
        sleep(2)
        self.contract.events.NewCurve(filters, callback)
