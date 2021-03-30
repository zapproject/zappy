from asyncio import sleep

from registry import ZapRegistry
from dispatch import ZapDispatch
from bondage import ZapBondage
from arbiter import ZapArbiter
from zap_token import ZapToken

from typing import Any, List, Optional

from zaptypes import (
    NetworkProviderOptions, const,
    TransactionCallback, txid,
    address
)


class ZapSubscriber:
    """ Represents an offchain Subscriber.

        Also provides an interface to the appropriate smart contracts.
    """

    def __init__(self, owner: str,
                 options: NetworkProviderOptions):
        assert owner, "owner address is required"
        self.subscriber_owner = owner
        self.zap_token = ZapToken(**options)
        self.zap_dispatch = ZapDispatch(**options)
        self.zap_bondage = ZapBondage(**options)
        self.zap_arbiter = ZapArbiter(**options)
        self.zap_registry = ZapRegistry(**options)

    async def get_zap_balance(self) -> int:
        """ Gets the Zap balance of the current ZapSubscriber.

            :return a Coroutine that will resolve into the Zap Balance in wei.
        """
        balance: int = await\
            self.zap_token.balance_of(self.subscriber_owner)
        return balance

    async def get_zap_allowance(self) -> int:
        """ Gets the Zap allowance of the current ZapSubscriber to Bondage.

            :return a Coroutine that will resolve into the Zap Allowance in wei
        """
        owner = self.zap_bondage.contract.address

        await sleep(1.5)
        allowance: int = self.zap_token.contract.functions.allowance(
            self.subscriber_owner, owner).call()

        return allowance

    async def approve_to_bond(self, zap_num: int,
                              From: address, gas_price: int,
                              gas: Optional[int] = const.DEFAULT_GAS) -> txid:
        """ Approve number of zap to a provider

            :param provider: Provider's address

            :param zap_num: Number of Zap to approve

            :param gas: Number of gas limit
        """
        return await self.zap_token.approve(
            self.zap_bondage.contract.address,
            zap_num,
            From, gas_price, gas)

    async def bond(self, provider: address, endpoint: str, dots: int,
                   From: address, gas_price: int,
                   gas: Optional[int] = const.DEFAULT_GAS,
                   cb: Optional[TransactionCallback] = None) -> txid:
        """ Bonds `zap_num` amount of Zap to the given provider's endpoint,
            yielding dots that enable this subscriber to send queries.

            :param provider: Provider's address

            :param endpoint: Endpoint that this client wants to query from

            :param dots: Amount of dots to bond

            :param cb: Callback for transactionHash event

            :returns
                a Coroutine that will eventually resolve
                into a transaction hash
        """
        await sleep(1.5)
        approved: str =\
            self.zap_token.contract.functions.allowance(
                self.subscriber_owner,
                self.zap_bondage.contract.address).call()

        required: int = await\
            self.zap_bondage.calc_zap_for_dots(
                provider, endpoint, dots)

        zap_balance = await self.get_zap_balance()

        assert (approved >= required),\
            "You don\'t have enough ZAP approved."
        assert (zap_balance >= required),\
            "Balance insufficient."

        bonded = await self.zap_bondage.bond(
            provider, endpoint,
            dots,
            From, gas_price, gas,
            cb=cb)

        return bonded

    async def delegate_bond(self, provider: address, subscriber: address,
                            endpoint: str, dots: int,
                            From: address, gas_price: int,
                            gas: Optional[int] = const.DEFAULT_GAS,
                            cb: Optional[TransactionCallback] = None) -> txid:
        """ Delegate bond zapNum amount of Zap to provider's endpoint.

            Thereby yielding dots that enable the given subscriber
            to send queries.

          :param provider: Provider's address

          :param subscriber:
            subscriber's address that will bond with provider's endpoint

          :param endpoint: Endpoint that this client wants to query from

          :param dots: Amount of dots to bond

          :param cb: Callback for transactionHash event

          :return Coroutine that will resolve into a txid
            """
        await sleep(1.5)
        approved: int =\
            self.zap_token.contract.functions.allowance(
                self.subscriber_owner,
                self.zap_bondage.contract.address).call()

        required: int = await\
            self.zap_bondage.calc_zap_for_dots(provider, endpoint, dots)
        zap_balance = await self.get_zap_balance()

        assert approved >= required,\
            "You don\'t have enough ZAP approved."
        assert (zap_balance >= required),\
            "Balance insufficient."

        bonded = await self.zap_bondage.delegate_bond(
            subscriber, endpoint,
            dots, provider, From,
            gas_price, gas,
            cb=cb)

        return bonded

    async def unbond(self, provider: address, endpoint: address, dots: int,
                     From: address, gas_price: int,
                     gas: Optional[int] = const.DEFAULT_GAS,
                     cb: Optional[TransactionCallback] = None) -> txid:
        """ Unbonds a given number of dots from a given oracle.

            Returns Zap to this subscriber based on the bonding curve.

            :param provider: Oracle's address

            :param endpoint: Endpoint that the client has already bonded to

            :param dots:
                Number of dots to unbond (redeem) from
                this provider and endpoint

            :param cb: Callback for transactionHash event

            :returns a Coroutine that will resolve into a transaction hash
        """
        bound_dots = await\
            self.zap_bondage.get_bound_dots(
                self.subscriber_owner,
                provider,
                endpoint)

        assert (bound_dots >= dots),\
            "dots to unbond is less than requested"

        return await self.zap_bondage.unbond(
            provider, endpoint, dots,
            From, gas_price, gas, cb)

    async def subscribe(self, provider: address, endpoint: address,
                        endpoint_params: List[str], dots: int,
                        From: address, gas_price: int,
                        gas: Optional[int] = const.DEFAULT_GAS,
                        cb: Optional[TransactionCallback] = None) -> str:
        """ Initializes a temporal subscription to an oracle.

            Defined in terms of # of blocks.

            :param  provider: Oracle's address

            :param  endpoint: Endpoint that the client will query from

            :param  endpointParams: The parameters passed to the oracle

            :param  dots:
                Number of dots to subscribe for, determining the number of
                blocks this temporal subscription will last for

            :returns a Coroutine that will resolve into a transaction hash
        """
        provider_pubkey = await\
            self.zap_registry.get_provider_publickey(provider)
        zap_required = await\
            self.zap_bondage.calc_zap_for_dots(provider, endpoint, dots)
        zap_balance = await\
            self.get_zap_balance()

        if zap_balance < zap_required:
            raise Exception(
                f"Insufficient balance; Requires {zap_required} Zap for {dots} dots")

        bound_dots = await\
            self.zap_bondage.get_bound_dots(
                self.subscriber_owner,
                provider,
                endpoint)

        if bound_dots < dots:
            raise Exception(
                f"Insufficient bound dots; Please bond {dots} dots to subscribe")
        blocks = dots
        sub = await\
            self.zap_arbiter.initiate_subscription(
                provider, endpoint, endpoint_params,
                provider_pubkey, blocks,
                From, gas_price, gas, cb)

        return sub

    async def query_data(self, provider: address, query: str,
                         endpoint: str, endpoint_params: List[str],
                         From: address, gas_price: int,
                         gas: Optional[int] = const.DEFAULT_GAS,
                         cb: Optional[TransactionCallback] = None) -> txid:
        """ Queries data from a subscriber to a given provider's endpoint.

            Parses a query string and endpoint parameters which will be
            processed by the oracle.

            :param provider: Oracle's address

            :param query: Query string given to be handled by provider

            :param endpoint:
                Data endpoint of provider, determines how query is handled

            :param endpointParams:
                Parameters passed to data provider's endpoint

            :returns Coroutine Transaction hash
        """
        bound_dots = await\
            self.zap_bondage.get_bound_dots(
                self.subscriber_owner,
                provider, endpoint)

        if not bound_dots:
            raise Exception("Insufficient balance of bound dots to query")

        return\
            await self.zap_dispatch.query_data(
                provider, query, endpoint,
                endpoint_params,
                From, gas_price, gas, cb)

    async def cancel_query(self, query_id,
                           From: address, gas_price: int,
                           gas: Optional[int] = const.DEFAULT_GAS,
                           cb: Optional[TransactionCallback] = None) -> txid:
        """ Cancel a query_id

            :param queryId: string representation of the query id
        """
        try:
            await self.zap_dispatch.cancel_query(
                query_id,
                From, gas_price, gas, cb)
        except Exception as e:
            raise e

    async def get_num_escrow(self, provider: address, endpoint: str) -> int:
        """ Get Number of dots in escrow

            :param provider

            :param endpoint

            :returns Number of escrow dots
        """
        return\
            await self.zap_bondage.get_num_escrow(
                provider,
                self.subscriber_owner,
                endpoint)

    async def get_bound_dots(self, provider: address, endpoint: str) -> int:
        """ Gets the number of dots that are bounded to a provider's endpoint
            for the current subscriber.

            :param provider: Address of the data provider

            :param endpoint: Data endpoint of the provider

            :returns
                a Coroutine that resolves into the number of bound dots
                to this provider's endpoint
        """
        return\
            await self.zap_bondage.get_bound_dots(
                self.subscriber_owner,
                provider, endpoint)

    async def listen_to_offchain_response(
            self,
            cb: Optional[TransactionCallback] = None,
            Filter: Optional[dict] = {}) -> Any:
        """ Listen to all Offchain responses events

            :param filter

            :param callback
        """
        if not Filter["subscriber"]:
            Filter.update({"subscriber": self.subscriber_owner})

        self.zap_dispatch.listen_offchain_response(Filter, cb)

    """ Helpers
    """
    async def hasEnoughZap(self, zap_required: int) -> bool:
        """ Compares Zap Balance of Subscriber to a given amount.

            :param zap_required: Number of zap to check for

            :returns
                a Coroutine that will resolve into a boolean
                true if there is enough Zap
        """
        balance: int = await\
            self.zap_token.balance_of(self.subscriber_owner)
        return balance >= zap_required
