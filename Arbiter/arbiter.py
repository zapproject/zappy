from base_contract import BaseContract
from portedFiles.types import (Filter, txid, DEFAULT_GAS, NetworkProviderOptions, NumType, SubscriptionInit, SubscriptionEnd, SubscriptionType, ParamsPassedEvent, SubscriptionParams, SubscriptionEndEvent, )
#STILL NEED TransactionCallback to be ported over to types.py
from web3._utils import (isHex, utf8ToHex)
import asyncio
import copy

#@class
#Provides an interface to the Arbiter contract for managing temporal subscriptions to oracles.
#
class ZapArbiter(BaseContract):

    #Initializes a subclass of Basecontract that can access the methods of the Arbiter contract
    #@constructor
    #Takes NetworkProviderOptions as an argument
    #
    def __init__(self, NetworkProviderOptions):
        super().__init__(NetworkProviderOptions or {}, {artifact_name: "ARBITER"})

    #unsure of how to integrate txid into method. please advise.
    async def initiateSubscription(self, {provider, endpoint, endpoint_params, blocks, pubkey, address, gasPrice, gas = DEFAULT_GAS} : SubscriptionInit, callback = TransactionCallback):
        try:
        #changed "from" in ZapJS to "address"
        #necessary to have to do ansynchronously check for hex regex like in zapjs? can refactor
            for i in endpoint_params:
                if not isHex(i):
                    utf8ToHex(endpoint_params[i])
                else:
                    continue
            promiEvent = await self.contract.initiateSubscription(
                provider,
                utf8ToHex(endpoint),
                endpoint_params,
                pubkey,
                blocks).send({address, gas, gasPrice})
            )
            if callback:
            #Do not understand what would be happening here. TransactionCallback not made in types.py
                pass
            return promiEvent
        except Exception as e:
            raise e

    async def endSubscriptionSubscriber(self, {provider, endpoint, address, gasPrice, gas = DEFAULT_GAS}: SubscriptionEnd, callback = TransactionCallback):
        try:
            #necessary to have to do ansynchronously check for hex regex like in zapjs? can refactor
            for i in endpoint_params:
                if not isHex(i):
                    utf8ToHex(endpoint_params[i])
                else:
                    continue
            promiEvent = await self.contract.endSubscriptionSubscriber(
                provider,
                utf8ToHex(endpoint)).send({address, gas, gasPrice})
            )
            if callback:
                #TransactionCallback
                pass
            return promiEvent
        except Exception as e:
            raise e

    async def endSubscriptionProvider(self, {subcriber, endpoint, address, gasPrice, gas = DEFAULT_GAS} : SubscriptionEnd, callback = TransactionCallback):
        try:
            promiEvent = await self.contract.endSubscriptionProvider(
                subscriber,
                utf8ToHex(endpoint)).send({address, gas, gasPrice})
            )
            if callback:
                #TransactionCallback
                pass
            return promiEvent
        except Exception as e:
            raise e

    async def passParams(self, {receiver, endpoint, params, address, gasPrice, gas = DEFAULT_GAS} : SubscriptionParams, callback = TransactionCallback):
        try:
            for i in params:
                if not isHex(i):
                    utf8ToHex(params[i])
                else:
                    continue
            promiEvent = await self.contract.passParams(
                receiver,
                utf8ToHex(endpoint),
                params).send({address, gas, gasPrice})
            )
            if callback:
                #TransactionCallback
                pass
            return promiEvent
        except Exception as e:
            raise e

    #GETTER METHODS
    async def getSubscription(self, {provider, subscriber, endpoint }: SubscriptionType):
        try:
            return await self.contract.getSubscription(provider, subscriber, utf8ToHex(endpoint)).call()
        except Exception as e:
            raise e

    async def getDots(self, {provider, subscriber, endpoint}: SubscriptionType):
        try:
            return await self.contract.getDots(provider, subscriber, endpoint).call()
        except Exception as e:
            raise e

    async def getBlockStart(self, {provider, subscriber, endpoint}: SubscriptionType):
        try:
            return await self.contract.getBlockStart(provider, subscriber, endpoint).call()
        except Exception as e:
            raise e

    async def getPreBlockEnd(self, {provider, subscriber, endpoint}: SubscriptionType):
        try:
            return await self.contract.getPreBlockEnd(provider, subscriber, endpoint).call()
        except Exception as e:
            raise e

    #EVENT METHODS
    def listenSubscriptionEnd(self):
        try:
            pass
        except Exception as e:
            raise e

    def listenDataPurchase(self):
        try:
            pass
        except Exception as e:
            raise e

    def listenParamsPassedEvent(self):
        try:
            pass
        except Exception as e:
            raise e

    def listen(self):
        try:
            pass
        except Exception as e:
            raise e