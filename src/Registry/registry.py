from web3 import Web3
# from Web3 import Web3.toHex, Web3.toText, Web3.toBytes

from BaseContract.base_contract import BaseContract
from ZapToken.Curve.curve import Curve
from Types.types import (
    Filter, address,
    NetworkProviderOptions, const, TransactionCallback
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
        super().__init__(**options)

    """
        Registry storage calls for all providers
    """

    # async def task(func, action, args1=[], args2=[]):
    #     item = func(*args1).action(*args2)
    #     asyncio.sleep(5)

    #     if item:
    #         return item
    #     return

    async def get_all_providers(self):
        """Get all providers in Registry Contract.

           returns a list of oracles once async is fulfilled
        """
        await self.contract.functions.getAllOracles().call()

    async def get_provider_address_by_index(self, index: int):
        """ Look up provider's address by its index in registry storage

            returns address of indexed provider once async is fulfilled
        """
        await self.contract.functions.getOracleAddress(index).call()

    """
        Provider specific calls
    """

    async def initiate_provider(self, public_key: str, title: str,
                                From: address, cb: TransactionCallback,
                                gas=const.DEFAULT_GAS):
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
            tx_hash = await self.contract.functions.InitiateProvider(
                str(public_key), Web3.toHex(title)).transact(
                    {"from": From, "gas": gas})

            cb(None, tx_hash)
        except Exception as e:
            cb(e)

        return tx_hash

    async def get_provider_publickey(self, provider: address):
        """ Get a provider's public key from the registry contract.

            provider -- The address of this provider

            returns the public key number.
        """
        pub_key: str = await\
            self.contract.functions.getProviderPublicKey(provider).call()

        return pub_key

    async def get_providertitle(self, provider: address):
        title = await\
            self.contract.functions.getProviderTitle(provider).call()

        return Web3.toText(title)

    async def set_provider_title(self, From: address, title: str,
                                 cb: TransactionCallback, gas=const.DEFAULT_GAS):
        """ Set the new provider's title
            
            Arguments:
                From  -- The address of this provider
                title -- The new title of this provider
                cb    -- Callback for transactionHash event   

        """
        try:
            tx_hash = await\
                self.contract.functions.setProviderTitle(Web3.toHex(title)).transact(
                    {"from": From, "gas": gas})
            cb(None, tx_hash)

        except Exception as e:
            cb(e, None)

        return tx_hash

    async def is_provider_initiated(self, provider: address):
        return await self.contract.is_provider_initiated(provider)

    async def get_provider_param(self, provider: address, key: str):
        return await self.contract.functions.getProviderParameter(provider, Web3.toHex(key))

    async def get_all_provider_params(self, provider: address):
        return await self.contract.functions.getAllProviderParams(provider).call()

    async def get_provider_endpoints(self, provider: address):
        endpoints = await\
            self.contract.functions.getProviderEndpoints(provider).call()
        endpoints = [Web3.toText(endpoint) for endpoint in endpoints]
        valid_endpoints = [e for e in endpoints if e != '']

        return valid_endpoints

    """
        Provider's specific endpoint calls
    """

    async def initiate_provider_curve(self, end_point, term,
                                      From, gasPrice, cb,
                                      broker=const.NULL_ADDRESS,
                                      gas=const.DEFAULT_GAS):
        """"""
        hex_terms = [Web3.toHex(t) for t in term]

        try:
            tx_hash = await\
                self.contract.functions.initiateProviderCurve(Web3.toHex(end_point),
                                                              hex_terms, broker)
            cb(None, tx_hash)
        except Exception as e:
            cb(e)

        return tx_hash

    async def clear_endpoint(self, endpoint, From, gasPrice,
                             cb: TransactionCallback, gas=const.DEFAULT_GAS):
        try:
            tx_hash = await\
                self.contract.functions.clearEndpoint(Web3.toHex(endpoint)).send(
                    {"from": From, "gas": gas})
            cb(None, tx_hash)
        except Exception as e:
            cb(e)

        return tx_hash

    async def get_provider_curve(self, provider: address, endpoint: str):
        terms: list = await\
            self.contract.functions.getProviderCurve(
                provider, Web3.toHex(endpoint)).call()

        return Curve([int(t) for t in terms])

    def encode_params(endpoint_params: list = [], ):
        pars = endpoint_params
        hex_params =\
            [el if el.find('0x') == 0 else Web3.toHex(el) for el in pars]
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

    def decode_params(self, raw_params: list = []):
        bytes_params = [bytearray(Web3.toBytes(hexstr=el)) for el in raw_params]
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

    async def set_endpoint_params(self, endpoint, From, gasPrice,
                                  cb, endpoint_params=[],
                                  gas=const.DEFAULT_GAS):
        params = self.encode_params(endpoint_params)

        try:
            tx_hash = await\
                self.contract.functions.setEndpointParams(
                    Web3.toHex(text=endpoint), params).transact(
                        {"from": From, "gas": gas})
            cb(None, tx_hash)
        except Exception as e:
            cb(e)

        return tx_hash

    async def get_endpoint_broker(self, provider: address, endpoint: str):
        return\
            await self.contract.functions.getEndpointBroker(provider,
                                                            Web3.toHex(text=endpoint)).call()

    async def is_endpoint_set(self, provider: address, endpoint: str):
        unset: bool = await\
            self.contract.functions.getCurveUnset(provider,
                                                  Web3.toHex(text=endpoint)).call()
        return not unset

    """ Events
    """
    from typing import Callable

    async def listen(self, callback: Callable[..., None]):
        self.contract.events.allEvents(callback)

    async def listen_new_provider(self, callback: TransactionCallback,
                                  filters: Filter = {}):
        self.contract.events.NewProvider(filters, callback)

    async def listen_new_curve(self, callback: TransactionCallback,
                               filters: Filter):
        self.contract.events.NewCurve(filters, callback)
