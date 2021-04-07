from typing import Optional
from web3 import Web3
import asyncio

from src.base_contract.base_contract import BaseContract
from src.types.types import (
    Filter, address, TransactionCallback,
    NetworkProviderOptions, const, txid
)


class ZapDispatch(BaseContract):
    """
    The ZapDispatch class provides an interface to the Dispatch contract which enables data queries and responses
    between data providers (oracles) and subscribers. This child class inherits the properties and methods from the
    parent BaseContract class.

    :param NetworkProviderOptions: Dictionary object containing options for BaseContract init
    :param network_id: Select which network the contract is located
                  options : (mainnet, testnet, private)
    :param network_provider: Ethereum network provider (e.g. Infura or web3)
    Example:
            ZapDispatch({"network_id": 42, "network_provider" : 'web3'})
    """
    def __init__(self, options: NetworkProviderOptions = {}):
        options["artifact_name"] = "DISPATCH"
        super().__init__(**options)

    ###### Methods ######

    async def query_data(self,
                         provider: address,
                         query: str,
                         endpoint: str,
                         endpoint_params: list[str],
                         from_address: address,
                         gas: Optional[int] = const.DEFAULT_GAS,
                         gas_price: Optional[int] = Web3().eth.gas_price) -> txid:
        """
        Queries data from a subscriber to a given provider's endpoint. This function passes in both a query string and
        a list of endpoint parameters that will be processed by the oracle.

        :param provider: Address of the data provider (oracle).
        :param query: Data requested from the subscriber.
        :param endpoint: Data endpoint of the data provider which is meant to determine how the query is handled.
        :param endpoint_params: Parameters passed to the data provider's endpoint.
        :param from_address: Address of the subscriber.
        :param gas_price: Price per unit of gas (optional).
        :param gas: The gas limit of this transaction (optional).
        """
        if len(endpoint_params) > 0:
            hex_params = [param if param.find('0x') == 0 else Web3.toHex(text=param) for param in endpoint_params]
            bytes_params = [Web3.toBytes(hexstr=hex_p) for hex_p in hex_params]
            endpoint_params = bytes_params

        try:
            await asyncio.sleep(.5)
            tx: txid = self.contract.functions.query(
                provider, query, Web3.toBytes(text=endpoint), endpoint_params
            ).transact(
                {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
            )

            tx_hash = Web3.toHex(tx)
            return tx_hash

        except Exception as e:
            print(e)

    async def cancel_query(self,
                           query_id: str or int,
                           from_address: address,
                           gas_price: Optional[int] = Web3().eth.gas_price,
                           gas: Optional[int] = const.DEFAULT_GAS) -> str or int:
        """
        This function cancels a query_id. It will return the block number when the query was canceled. If the query
        does not exist, a value error exception wil occur and the returned value will be zero.

        :param query_id: A unique identifier for the query.
        :param from_address: Address of the subscriber.
        :param gas_price: Price per unit of gas (optional).
        :param gas: The gas limit of this transaction (optional).
        """
        try:
            await asyncio.sleep(.5)
            self.contract.functions.cancelQuery(query_id).transact(
                {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
            )
        except ValueError:
            return 0

        else:
            return self.contract.functions.getCancel(query_id).call()

    async def respond(self,
                      query_id: str or int,
                      response_params: list[str],
                      dynamic: bool,
                      from_address: address,
                      gas_price: Optional[int] = Web3().eth.gas_price,
                      gas: Optional[int] = const.DEFAULT_GAS) -> txid:
        """
        This function allows a provider to respond to a subscriber's query. The length and content of the response
        parameters determines the type of response sent back to the subscriber.

        :param query_id: A unique identifier for the query.
        :param response_params: List of responses returned by provider. Length determines the Dispatch response.
        :param dynamic: Determines if the IntArray/Bytes32Array Dispatch response should be used.
        :param from_address: Address of the subscriber.
        :param gas_price: Price per unit of gas (optional).
        :param gas: The gas limit of this transaction (optional).
        """
        if dynamic is not False:
            str_params = [str(param) for param in response_params]
            hex_params = [param.encode('utf-8').hex() for param in str_params]

            if type(response_params[0]) == int:
                int_params = [int(param) for param in hex_params]
                response_params = int_params

                ### Omitted conversion to locale string ###

                tx = self.contract.functions.respondIntArray(
                    query_id, response_params
                ).transact(
                    {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
                )

                await asyncio.sleep(.5)
                tx_hash = Web3.toHex(tx)
                return tx_hash

            else:
                response_params = hex_params

                tx = self.contract.functions.respondBytes32Array(
                    query_id, response_params
                ).transact(
                    {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
                )
                await asyncio.sleep(.5)
                tx_hash = Web3.toHex(tx)
                return tx_hash

        p_length = len(response_params)

        if p_length == 1:
            tx = self.contract.functions.respond1(
                query_id, response_params[0]
            ).transact(
                {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
            )

        elif p_length == 2:
            tx = self.contract.functions.respond2(
                query_id, response_params[0], response_params[1]
            ).transact(
                {'from': from_address, 'gas': gas}
            )

        elif p_length == 3:
            tx = self.contract.functions.respond3(
                query_id, response_params[0], response_params[1], response_params[2]
            ).transact(
                {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
            )

        elif p_length == 4:
            tx = self.contract.functions.respond4(
                query_id, response_params[0], response_params[1], response_params[2], response_params[3]
            ).transact(
                {'from': from_address, 'gas': gas, 'gasPrice': gas_price}
            )

        else:
            raise ValueError('Invalid number of response parameters')

        tx_hash = Web3.toHex(tx)
        return tx_hash

    ###### Getters ######

    async def get_query_id_provider(self, query_id: str or int) -> address:
        """
        Fetches the provider of specified query id.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        return self.contract.functions.getProvider(query_id).call()

    async def get_subscriber(self, query_id: str or int) -> address:
        """
        Fetches the subscriber's address that submitted the query associated with the query id.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        return self.contract.functions.getSubscriber(query_id).call()

    async def get_endpoint(self, query_id: str or int) -> str:
        """
        Fetches the endpoint of the query.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        endpoint = self.contract.functions.getEndpoint(query_id).call()
        return Web3.toText(endpoint)

    async def get_status(self, query_id: str or int) -> int:
        """
        Fetches the status of a query id.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        return self.contract.functions.getStatus(query_id).call()

    async def get_cancel(self, query_id: str or int) -> int:
        """
        Fetches the status of a cancelled query.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        return self.contract.functions.getCancel(query_id).call()

    async def get_user_query(self, query_id: str or int) -> str:
        """
        Fetches the user of the specified query id.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        return self.contract.functions.getUserQuery(query_id).call()

    async def get_subscriber_onchain(self, query_id: str or int) -> bool:
        """
        Fetches information about onchain or offchain subscriber of the specified query id.

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(.1)
        return self.contract.functions.getSubscriberOnchain(query_id).call()

    ###### Events ######

    def listen(self, filters: Filter = {},  cb: TransactionCallback = None, ) -> None:
        """
        Listens for all Dispatch contract events based on the optional filter.

        :param filters: subscriber:address, provider:address, id:int|string, endpoint:bytes32,
                        endpointParams:bytes32[], onchainSubscriber:boolean.
        :param cb: Callback.
        """

        self.contract.events.allEvents(
            filters, {'fromBlock': filters['fromBlock'] or 0, 'toBlock': 'latest'}, cb
        )

    async def listen_incoming(self, filters: Filter = {}, cb: TransactionCallback = None) -> None:
        """
        Listens for "Incoming" Dispatch contract events based on an optional filter. This event listener executes
        a callback when the filter is matched.

        :param filters: subscriber:address, provider:address, endpoint:bytes32.
        :param cb: Callback.
        """

        self.contract.events.Incoming(filters, cb)

    async def listen_fulfill_query(self, filters: Filter = {}, cb: TransactionCallback = None) -> None:
        """
        Listens for "FulfillQuery" Dispatch contract events based on an optional filter.

        :param filters: subscriber:address, provider:address, endpoint:bytes32.
        :param cb: Callback.
        """

        self.contract.events.FulfillQuery(filters, cb)

    async def listen_offchain_response(self, filters: Filter = {}, cb: TransactionCallback = None) -> None:
        """
        Listens for all Offchain responses Dispatch contract events based on an optional filter.

        :param filters: id:number|string, subscriber:address, provider: address, response: bytes32[]|int[],
                        response1:string, response2:string, response3:string, response4:string.
        :param cb: Callback.
        """

        self.contract.events.OffchainResponse(filters, cb)
        self.contract.events.OffchainResponseInt(filters, cb)
        self.contract.events.OffchainResult1(filters, cb)
        self.contract.events.OffchainResult2(filters, cb)
        self.contract.events.OffchainResult3(filters, cb)
        self.contract.events.OffchainResult4(filters, cb)

    async def listen_cancel_request(self, filters: Filter = {}, cb: TransactionCallback = None) -> None:
        """
        Listens for "Cancel" query events.

        :param filters:
        :param cb: Callback.
        """

        self.contract.events.CanceledRequest(filters, cb)
