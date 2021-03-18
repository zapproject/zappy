from typing import Optional, List, Dict
from src.base_contract.base_contract import BaseContract
import asyncio
from src.portedFiles.types import (
    Filter, address, TransactionCallback,
    NetworkProviderOptions, const, txid
)
from web3 import Web3


class ZapDispatch(BaseContract):
    """
    NetworkProviderOptions -- Dictionary object containing options for BaseContract init
    network_id -- Select which network the contract is located
                  options : (mainnet, testnet, private)
    networkProvider -- Ethereum network provider (e.g. Infura or web3)
    Example:
            ZapDispatch({"networkId": 42, "networkProvider" : "web3"})
    """
    def __init__(self, options: NetworkProviderOptions = {}):
        options["artifact_name"] = "DISPATCH"
        BaseContract.__init__(self, **options)

    """Methods"""

    async def query_data(self, provider: address, query: str, endpoint: str,
                         endpoint_params: list[str], from_address: str, gas_price: Optional[int], gas: const.DEFAULT_GAS,
                         cb: TransactionCallback = None) -> txid:
        """
        COMMENT HERE

        :param provider:
        :param query:
        :param endpoint:
        :param endpoint_params:
        :param from_address:
        :param gas_price:
        :param gas:
        :param cb:
        """
        try:
            await asyncio.sleep(1)
            if len(endpoint_params) > 0:
                updated_params = [param if param.startswith('0x')
                                  else param.encode('utf-8').hex() for param in endpoint_params]
            else:
                updated_params = endpoint_params

            tx_hash = self.contract.functions.query(
                provider, query, Web3.toBytes(text=endpoint), updated_params
            ).transact({'from': from_address, 'gas': gas, 'gasPrice': gas_price})

            if cb:
                cb(None, tx_hash)
            return tx_hash.hex()
        except Exception as e:
            print(e)


    async def cancel_query(self, query_id: str or int,
                           from_address: address, gas_price: Optional[int],
                           gas: const.DEFAULT_GAS) -> str or int:
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        :param from_address:
        :param gas_price:
        :param gas:
        """
        try:
            await asyncio.sleep(1)
            self.contract.functions.cancelQuery(query_id).transact({'from': from_address, 'gas': gas, 'gasPrice': gas_price})
        except Exception as e:
            return e # return 0?
        else:
            await asyncio.sleep(1)
            return self.contract.functions.getCancel(query_id).call()

    async def respond(self, query_id: str or int, response_params: list[str], dynamic: bool,
                      from_address: address, gas_price: Optional[int], gas: const.DEFAULT_GAS):
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        :param response_params:
        :param dynamic:
        :param from_address:
        :param gas_price:
        :param gas:
        """
        if dynamic is not False:
            if type(response_params[0]) == int:
                big_nums = 'I DONT THINK THIS APPLIES TO PYTHON. FIX ME'
                self.contract.functions.respondIntArray(query_id, big_nums)

            return self.contract.methods.respondBytes32Array(
                    query_id, response_params).send({'from': from_address, 'gas': gas, 'gasPrice': gas_price})

        p_length = len(response_params)

        if p_length == 1:
            return self.contract.functions.respond1(
                query_id,
                response_params[0]).transact({'from': from_address, 'gas': gas, 'gasPrice': gas_price})

        elif p_length == 2:
            return self.contract.functions.respond2(
                query_id,
                response_params[0],
                response_params[1]).transact({'from': from_address, 'gas': gas})

        elif p_length == 3:
            return self.contract.functions.respond3(
                query_id,
                response_params[0],
                response_params[1],
                response_params[2]).transact({'from': from_address, 'gas': gas, 'gasPrice': gas_price})

        elif p_length == 4:
            return self.contract.functions.respond4(
                query_id,
                response_params[0],
                response_params[1],
                response_params[2],
                response_params[3]).transact({'from': from_address, 'gas': gas, 'gasPrice': gas_price})

        else:
            raise ValueError('Invalid number of response parameters')

    """GETTERS"""

    async def get_query_id_provider(self, query_id: str or int) -> str:
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        return self.contract.functions.getProvider(query_id).call()

    async def get_subscriber(self, query_id: str or int) -> str:
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        return self.contract.functions.getSubscriber(query_id).call()

    async def get_endpoint(self, query_id: str or int) -> str:
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        endpoint = self.contract.functions.getEndpoint(query_id).call()
        return Web3.toText(endpoint)

    async def get_status(self, query_id: str or int):
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        return self.contract.functions.getStatus(query_id).call()

    async def get_cancel(self, query_id: str or int):
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        return self.contract.functions.getCancel(query_id).call()

    async def get_user_query(self, query_id: str or int):
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        return self.contract.functions.getUserQuery(query_id).call()

    async def get_subscriber_onchain(self, query_id: str or int) -> bool:
        """
        COMMENT HERE

        :param query_id: A unique identifier for the query.
        """
        await asyncio.sleep(1)
        return self.contract.functions.getSubscriberOnchain(query_id).call()

    """EVENTS"""

    def listen(self, filters: Filter = {}, cb: TransactionCallback = None) -> None:
        """
        COMMENT HERE

        :param filters:
        :param cb:
        """
        self.contract.events.






