from asyncio import sleep

from web3 import Web3

from base_contract import BaseContract
from registry import ZapRegistry
from zaptypes import (
    BondFilter, txid, NetworkProviderOptions,
    TransactionCallback, const, address
)


class ZapBondage(BaseContract):
    """ Provides an interface to the Bondage contract.
        Enables bonding and unbonding to Oracles.
    """

    def __init__(self, options: NetworkProviderOptions):
        options["artifact_name"] = "BONDAGE"
        BaseContract.__init__(self, **options or {})

    async def bond(self, provider: address, endpoint: str,
                   dots: int, From: address, gas_price: int,
                   gas: int = const.DEFAULT_GAS,
                   cb: TransactionCallback = None) -> txid:
        """ Bonds a number of dots from a subscriber to a provider's endpoint.

            Note: this requires that at least zapNum has been approved from
            the subscriber to be transferred by the Bondage contract.

            :param provider: Provider's address

            :param dots: number of dots to bond to this provider

            :param From: Subscriber's owner (0 broker)  or broker's address

            :param gas: Sets the gas limit for this transaction

            :param cb: Callback for transactionHash event

            :returns
                Coroutine that eventually resolves into a transaction hash.
        """
        assert (dots and dots > 0),\
            "Dots to bond must be greater than 0."

        payload = {"oracleAddress": provider,
                   "endpoint": Web3.toBytes(text=endpoint)}
        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}

        broker =\
            self.contract.functions.getEndpointBroker(**payload).call()

        if broker != const.NULL_ADDRESS:
            if From != broker:
                raise Exception(f"Broker address {broker} needs to call delegate bonding")

        payload["numDots"] = dots

        try:
            await sleep(0)
            tx_hash = self.contract.functions.bond(
                **payload).transact(tx_meta)
            if cb:
                receipt = tx_hash
                logs = self.contract.events.Bound().processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])
            return tx_hash.hex()
        except Exception as e:
            print(e)

    async def delegate_bond(self, provider: address, subscriber: address,
                            endpoint: str, dots: int, From: address,
                            gas_price: int, gas: int = const.DEFAULT_GAS,
                            cb: TransactionCallback = None) -> txid:
        """ Bonds a given number of dots from an account to a subscriber.

            This would be used to bond to a provider
            on behalf of another account, such as a smart contract.

            :param provider: Provider's address

            :param endpoint: Data endpoint of the provider

            :param dots: Number of dots to bond to this provider

            :param subscriber: Address of the intended holder of the dots

            :param From: Address of the data subscriber

            :param gas: Sets the gas limit for this transaction

            :param cb: Callback for transactionHash event

            :returns
                Coroutine that eventually resolves into a transaction hash.
        """

        assert (dots and dots > 0),\
            "Dots to bond must be greater than 0."

        payload = {"oracleAddress": provider,
                   "endpoint": Web3.toBytes(text=endpoint)}
        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}

        broker =\
            self.contract.functions.getEndpointBroker(**payload).call()

        if broker != const.NULL_ADDRESS:
            if From != broker:
                raise Exception(f"Broker address {broker} needs to call delegate bonding")

        payload.update({"numDots": dots, "holderAddress": subscriber})

        try:
            await sleep(0)
            tx_hash = self.contract.functions.delegateBond(
                **payload).transact(tx_meta)

            if cb:
                receipt = tx_hash
                logs = self.contract.events.Bound().processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash.hex()
        except Exception as e:
            print(e)

    async def unbond(self, provider: address,
                     endpoint: str, dots: int, From: address,
                     gas_price: int, gas: int = const.DEFAULT_GAS,
                     cb: TransactionCallback = None) -> txid:
        """ Unbonds a given number of dots.

            It unbonds from a provider's endpoint and transfers the
            appropriate amount of Zap to the subscriber.

            :param provider: Address of the data provider

            :param endpoint: Data endpoint of the provider

            :param dots: The number of dots to unbond from the contract

            :param From : Address of the data subscriber

            :param gas: Sets the gas limit for this transaction (optional)

            :param  cb: Callback for transactionHash event

            :returns
                Coroutine that eventually resolves into a transaction hash.
        """

        assert (dots and dots > 0),\
            "Dots to unbond must be greater than 0."

        payload = {"oracleAddress": provider, "endpoint": Web3.toBytes(text=endpoint)}
        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}

        broker =\
            self.contract.functions.getEndpointBroker(**payload).call()

        if broker != const.NULL_ADDRESS:
            if From != broker:
                raise Exception(f"Broker address {broker} needs to call delegate bonding")

        payload["numDots"] = dots

        try:
            await sleep(0)
            tx_hash = self.contract.functions.unbond(
                **payload).transact(tx_meta)

            if cb:
                receipt = tx_hash
                logs = self.contract.events.Bound().processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash
        except Exception as e:
            print(e)

    """ Getters
    """

    async def get_bound_dots(self, subscriber: address, provider: address,
                             endpoint: str) -> int:
        """ Gets the number of dots that are bounded to a provider's endpoint
            for the current subscriber.

            :param subscriber: Address of the data subscriber

            :param provider: Address of the data provider

            :param endpoint: Data endpoint of the provider

            :returns
                A Coroutine that resolves to the number of
                bound dots to this provider's endpoint
        """
        await sleep(0)
        return self.contract.functions.getBoundDots(
            subscriber, provider, Web3.toBytes(text=endpoint)).call()

    async def calc_zap_for_dots(self, provider: address,
                                endpoint: str, dots: int):
        """ Calculates the amount of Zap required to bond
            a given number of dots to a provider's endpoint.

            :param provider: Address of the data provider

            :param endpoint: Endpoint to calculate zap

            :param dots: Number of dots to calculate the price (in Zap) for

            :returns
                A Coroutine that resolves to the price (in Zap)
                for the given number of dots
        """
        await sleep(0)
        return self.contract.functions.calcZapForDots(
            provider, Web3.toBytes(text=endpoint), dots).call()

    async def current_cost_of_dot(self, provider: address,
                                  endpoint: str, dots: int) -> int:
        """ Calculates the amount of Zap required to bond
            a given number of dots to a provider's endpoint.

            :param provider:  Address of the data provider

            :param endpoint: Data endpoint of the provider

            :param dots:  dots that subscriber want to use

            :returns
                A Coroutine that resolves into the price (in Zap wei)
                for next x dots to bond
        """
        await sleep(0)
        return self.contract.functions.currentCostOfDot(
            provider, Web3.toBytes(text=endpoint), dots).call()

    async def get_dots_limits(self, provider: address, endpoint: str) -> int:
        """ Get Maximum dots that can be bound for an endpoint of a provider

            :param provider: Provider's address

            :param endpoint: Provider's endpoint to get dots limit

            :returns
                A Coroutine that resolves into the number
                of maximum dots that can be bound

        """
        await sleep(0)
        return self.contract.functions.dotLimit(
            provider, Web3.toBytes(text=endpoint)).call()

    async def get_dots_issued(self, provider: address, endpoint: str) -> int:
        """ Gets the total number of dots that have been issued
            by a provider's endpoint.

            :param provider: Address of the data provider

            :param endpoint: Data endpoint of the provider

            :returns A Coroutine that resolves into the number of dots issued

        """
        await sleep(0)
        return self.contract.functions.getDotsIssued(
            provider, Web3.toBytes(text=endpoint)).call()

    async def get_broker_address(self, provider: address, endpoint: str):
        """ Get Broker address for this provider's endpoint
            return NULL_ADDRESS if there is none

            :param provider: Provider's Address

            :param endpoint: Provider's endpoint to get Broker's address

            :returns
                A Coroutine that resolves into a broker's
                address for this endpoint, null address if none

        """
        sleep(0)
        return await\
            self.contract.functions.getEndpointBroker(
                provider, Web3.toBytes(text=endpoint)).call()

    async def get_zap_bound(self, provider: address, endpoint: str) -> int:
        """ Gets the total amount of Zap that has been bonded
            to a provider's endpoint.

            :param provider: Address of the data provider

            :param endpoint: Data endpoint of the provider

            :returns A Coroutine that resolves into the amount of Zaps (wei)
                that are bound to this endpoint

        """
        await sleep(0)
        return self.contract.functions.getZapBound(
            provider, Web3.toBytes(text=endpoint)).call()

    async def get_num_escrow(self, provider: address, subscriber: address,
                             endpoint: str) -> int:
        """ Get Number of dots escrow

            :param provider

            :param endpoint

            :param subscriber

            :returns A Coroutine that resolve into the number of escrow dots

        """
        await sleep(0)
        return self.contract.functions.getNumEscrow(
            subscriber, provider, Web3.toBytes(text=endpoint)).call()

    """ Events
    """

    def listen(self, cb: TransactionCallback,
               filters: BondFilter = {}) -> None:
        self.contract.events.allEvents(
            filters, {"fromBlock": 0, "toBlock": "latest"}, cb)

    def listen_bound(self, cb: TransactionCallback,
                     filters: BondFilter = {}) -> None:
        self.contract.events.Bound(filters, {"toBlock": "latest"}, cb)

    def listen_unbound(self, cb: TransactionCallback,
                       filters: BondFilter = {}) -> None:
        self.contract.events.Unbond(filters, {"toBlock": "latest"}, cb)

    def listen_escrow(self, cb: TransactionCallback,
                      filters: BondFilter = {}) -> None:
        self.contract.events.Escrowed(filters, {"toBlock": "latest"}, cb)

    def listen_released(self, cb: TransactionCallback,
                        filters: BondFilter = {}) -> None:
        self.contract.events.Released(filters, {"toBlock": "latest"}, cb)

    def listen_returned(self, cb: TransactionCallback,
                        filters: BondFilter = {}) -> None:
        self.contract.events.Returned(filters, {"toBlock": "latest"}, cb)
