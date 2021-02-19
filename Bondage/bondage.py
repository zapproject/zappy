from BaseContract.base_contract import BaseContract
#from Registry.registry import Registry (in hopes this will get ported soon...)
from portedFiles.types import (BondageArgs, BondArgs, UnbondArgs, DelegateBondArgs, BondFilter, Filter, txid, NetworkProviderOptions, Constants, NumType, TransactionCallback)
from web3._utils import (utf8ToHex, toHex)

class ZapBondage(BaseConstract):

    def __init__(self, NetworkProviderOptions):
        super().__init__(self, NetworkProviderOptions or {}, { artifactName: 'Bondage'})

    async def bond(self, bond_args: BondArgs , callback: TransactionCallback):
        assert(dots and dots > 0, 'Dots to bond must be greater than 0.')
        dots = toHex(bond_args['dots'])
        #getEndpointBroker() is part of the Registry code (currently missing)
        broker = await self.contract.getEndpointBroker(bond_args['provider'], utf8ToHex(bond_args['endpoint']))
        if broker != const.NULL_ADDRESS:
            if bond_args['frm'] != broker:
                raise Error('Broker address {broker} needs to call delegate bonding'.format(broker))
        promiEvent = self.contract.bond(
            bond_args['provider'],
            utf8ToHex(bond_args['endpoint']),
            dots)
            .send({ bond_args['frm'], bond_args['gas'], bond_args['gasPrice'] })
        if callback:
            #Add events
            pass
        return promiEvent

    async def delegateBond(self, delegate_bond_args: DelegateBondArgs, callback: TransactionCallback):
        assert(dots and dots > 0, 'Dots to bond must be greater than 0.')
        dots = toHex(delegate_bond_args['dots'])
        broker = await self.contract.getEndpointBroker(delegate_bond_args['provider'], utf8ToHex(delegate_bond_args['endpoint']))
        if broker != const.NULL_ADDRESS:
            if delegate_bond_args['frm'] != broker:
                raise Error('Broker address {broker} needs to call delegate bonding for this endpoint'.format(broker))
        promiEvent = self.contract.delegateBond(
            delegate_bond_args['subscriber'],
            delegate_bond_args['provider'],
            utf8ToHex(delegate_bond_args['endpoint']),
            dots)
            .send({ delegate_bond_args['frm'], delegate_bond_args['gas'], delegate_bond_args['gasPrice'] })
        if callback:
            #Add events
            pass
        return promiEvent

    async def unbond(self, unbond_args: UnbondArgs , callback: TransactionCallback):
        assert(dots and dots > 0, 'Dots to unbond must be greater than 0.')
        dots = toHex(unbond_args['dots'])
        #getEndpointBroker() is part of the Registry code (currently missing)
        broker = await self.contract.getEndpointBroker(unbond_args['provider'], utf8ToHex(unbond_args['endpoint']))
        if broker != const.NULL_ADDRESS:
            if unbond_args['frm'] != broker:
                raise Error('Broker address {broker} needs to call unbonding for this endpoint'.format(broker))
        promiEvent = self.contract.unbond(
            unbond_args['provider'],
            utf8ToHex(unbond_args['endpoint']),
            dots)
            .send({ unbond_args['frm'], unbond_args['gas'], unbond_args['gasPrice'] })
        if callback:
            #Add events
            pass
        return promiEvent

    
    #GETTERS
    async def getBoundDots(self, bondage_args: BondageArgs):
        return await self.contract.getBoundDots(bondage_args['subscriber'], bondage_args['provider'],utf8ToHex(bondage_args['endpoint']))
    
    async def getDotsLimit(self, bondage_args: BondageArgs):
        return await self.contract.dotLimit(bondage_args['provider'], utf8ToHex(bondage_args['endpoint']))
    
    async def getDotsIssued(self, bondage_args: BondageArgs):
        return await self.contract.getDotsIssued(bondage_args['provider'], utf8ToHex(bondage_args['endpoint']))

    async def getBrokerAddress(self, bondage_args: BondageArgs):
        return await self.contract.getEndpointBroker(bondage_args['provider'], utf8ToHex(bondage_args['endpoint']))
    
    async def getZapBound(self, bondage_args: BondageArgs):
        return await self.contract.getZapBound(bondage_args['provider'], utf8ToHex(bondage_args['endpoint']))
    
    async def getNumEscrow(self, bondage_args: BondageArgs):
        return await self.contract.getNumEscrow(bondage_args['subscriber'], bondage_args['provider'], bondage_args['endpoint'])

    
    #EVENTS (Still not sure on these, I'm unaware of what the .events method is referring to)
    def listen(filters: BondFilter = {}, callback: TransactionCallback):
        self.contract.events.allEvents(filters, { 'fromBlock': 0, 'toBlock': 'latest' }, callback)

    def listenBound(filters: BondFilter = {}, callback: TransactionCallback):
        self.contract.events.Bound(filters, { 'toBlock': 'latest' }, callback)

    def listenBound(filters: BondFilter = {}, callback: TransactionCallback):
        self.contract.events.Unbond(filters, {'toBlock': 'latest' }, callback)

    def listenEscrowed(filters: BondFilter = {}, callback: TransactionCallback):
        self.contract.events.Escrowed(filters, { 'toBlock': 'latest' }, callback)

    def listenReleased(filters: BondFilter = {}, callback: TransactionCallback):
        self.contract.events.Released(filters, {'toBlock': 'latest' }, callback)

    def listenReturned(filters: BondFilter = {}, callback: TransactionCallback):
        self.contract.events.Returned(filters, { 'toBlock': 'latest' }, callback)

