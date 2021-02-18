from base_contract import BaseContract
from portedFiles.types import (BondageArgs, BondArgs, UnbondArgs, DelegateBondArgs, BondFilter, Filter, txid, NetworkProviderOptions, Constants, NumType, TransactionCallback)
from web3._utils. import (utf8ToHex, toHex)

class ZapBondage(BaseConstract):

    def __init__(self, NetworkProviderOptions):
        super().__init__(NetworkProviderOptions or {}, { artifactName: 'Bondage'})

    async def bond(self, { provider, enssdpoint, dots, address, gasPrice, gas = const.DEFAULT_GAS}: BondageArgs, cb = TransactionCallback):
        assert(dots and dots > 0, 'Dots to bond must be greater than 0.')
        #???
        broker = await self.contract.getEndpointBroker(provider, utf8ToHex(endpoint))
        if broker != const.NULL_ADDRESS:
            if address !== broker:
                raise Error('Broker address {broker} needs to call delegate bonding'.format(broker))
        promiEvent = self.contract.bond(
            provider,
            utf8ToHex(endpoint),
            toHex(dots))
            .send({ address, gas, gasPrice}))
        if cb:
            #Add event
            pass
        return promiEvent

    async def delegateBond(self, { provider, endpoint, dots, subscriber, address, gasPrice, gas = const.DEFAULT_GAS}: DelegateBondArgs, cb = TransactionCallback):
        assert(dots and dots > 0, 'Dots to bond must be greater than 0.')
        dots = toHex(dots)
        broker = await self.contract.getEndpointBroker(provider, utf8ToHex(endpoint))
        if broker != const.NULL_ADDRESS:
            if address != broker:
                raise Error('Broker address {broker} needs to call delegate bonding'.format(broker))
        promiEvent = self.contract.delegateBond(
            subscriber,
            provider,
            utf8ToHex(endpoint),
            dots)
            .send({ address, gas, gasPrice })
        if cb:
            #Add event
            pass
        return promiEvent

    #GETTERS
    async def getBoundDots(self, { subscriber, provider, endpoint }: BondageArgs):
        return await self.contract.getBoundDots(subscriber, provider,utf8ToHex(endpoint))
    
    async def getDotsLimit(self, { provider, endpoint }: BondageArgs):
        return await self.contract.dotLimit(provider, utf8ToHex(endpoint))
    
    async def getDotsIssued(self, { provider, endpoint }: BondageArgs):
        return await self.contract.getDotsIssued(provider, utf8ToHex(endpoint))

    async def getBrokerAddress(self, { provider, endpoint }: BondageArgs):
        return await self.contract.getEndpointBroker(provider, utf8ToHex(endpoint))
    
    async def getZapBound({ provider, endpoint }: BondageArgs):
        return await self.contract.getZapBound(provider, utf8ToHex(endpoint))
    
    async def getNumEscrow( provider, endpoint, subscriber }):
        return await self.contract.getNumEscrow(subscriber, provider, endpoint)

    #EVENTS NEED TO BE ADDED
