from web import Web3
from asyncio import sleep

from BaseContract.base_contract import BaseContract
from registry import ZapRegistry
from dispatch import ZapDispatch
from bondage import ZapBondage
from arbiter import ZapArbiter
from zaptoken import ZapToken

from typing import Any

from zaptypes import (
    NetworkProviderOptions, const,
    TransactionCallback
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

    async def get_zap_balance(self) -> str or int:
        """ Gets the Zap balance of the current ZapSubscriber.

            :return a Future that will resolve into the Zap Balance in wei.
        """
        await sleep()
        return self.zap_token.balance_of(self.subscriber_owner)

    async def get_zap_allowance(self) -> int or float:
        """ Gets the Zap allowance of the current ZapSubscriber to Bondage.

            :return a Future that will resolve into the Zap Allowance in wei
        """
        await sleep()
        return self.zap_token.contract.methods.allowance(
            self.subscriber_owner,
            self.zap_bondage.methods)

    async def appove_to_bond(self, provider, zap_num,
                             gas_price, gas: const.DEFAULT_GAS) -> None:
        """ Approve number of zap to a provider

            :param str provider : Provider's address
            :param int zap_num  : Number of Zap to approve
            :param int gas      : Number of gas limit
        """
        await sleep()
        return self.zap_token.approve({
            "to": self.zap_bondage.contract._address,
            "amount": zap_num,
            "gas": gas,
            "gapPrice": gas_price
        })

    async def bond(self, provider, endpoint,
                   dots, gas_price, gas: const.DEFAULT_GAS,
                   cb: TransactionCallback = None) -> str:
        """ Bonds `zap_num` amount of Zap to the given provider's endpoint,
            yielding dots that enable this subscriber to send queries.

            :param str provider: Provider's address
            :param str endpoint : Endpoint that this client wants to query from
            :param int dots : Amount of dots to bond
            :param class:`TransactionCallback` cb : Callback for transactionHash event
            :returns str a Future that will eventually resolve into a transaction hash
        """
        await sleep()
        approved: int =\
            self.zap_token.contract.methods.allowance(
                self.subscriber_owner,
                self.zap_bondage.contract._address.call())

        required: int = await\
            self.zap_bondage.calc_zap_for_dots(provider, endpoint, dots)
        await sleep()
        zap_balance = await self.get_zap_balance()

        assert (approved >= required), "You don\'t have enough ZAP approved."
        assert (zap_balance >= required), "Balance insufficent."

        bonded = await self.zap_bondage.bond(
            provider, endpoint,
            dots, gas,
            gas_price, From=self.subscriber_owner,
            cb=cb)

        return bonded

    async def delegate_bond(self, provider, subscriber,
                            endpoint, dots,
                            cb: TransactionCallback = None) -> Any:
        """ Delegate bond zapNum amount of Zap to provider's endpoint.

            Thereby yielding dots that enable the given subscriber
            to send queries.
            
          :param address provider: Provider's address
          :param address subscriber: subscriber's address that will bond with provider's endpoint
          :param string endpoint: Endpoint that this client wants to query from
          :param number dots: Amount of dots to bond
          :param TransactionCallback cb: Callback for transactionHash event
          :return Future that will resolve into a tx_hash
            """
        await sleep()
        approved: int =\
            self.zap_token.contract.methods.allowance(
                self.subscriber_owner,
                self.zap_bondage.contract._address.call())

        required: int = await\
            self.zap_bondage.calc_zap_for_dots(provider, endpoint, dots)
        await sleep()
        zap_balance = await self.get_zap_balance()

        assert (approved >= required), "You don\'t have enough ZAP approved."
        assert (zap_balance >= required), "Balance insufficent."

        bonded = await self.zap_bondage.bond(
            provider, endpoint,
            dots, subscriber, gas,
            gas_price, From=self.subscriber_owner,
            cb=cb)

        return bonded

    async def unbond(self, provider, endpoint,
                     dots, gas_price,
                     gas=const.DEFAULT_GAS,
                     cb: TransactionCallback = None) -> None:
        """ Unbonds a given number of dots from a given oracle.

            Returns Zap to this subscriber based on the bonding curve.

            :param UnbondType u. {provider, endpoint, dots}
            :param str provider - Oracle's address
            :param str endpoint - Endpoint that the client has already bonded to
            :param str or int u.dots - Number of dots to unbond (redeem) from this provider and endpoint
            :param class:`TransactionCallback` cb - Callback for transactionHash event
            :returns {Promise<txid>} Transaction hash
        """
        await sleep()
        return None

    async def function(self) -> None:
        """
        """
        await sleep()
        return None

    async def function(self) -> None:
        """
        """
        await sleep()
        return None
