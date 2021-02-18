from base_contract import BaseContract
from BaseContract import utils
from portedFiles.types import (TransferType, address, txid, NetworkProviderOptions, TransactionCallback, NumType)
from web3._utils. import (toHex)

class ZapToken(BaseConstract):

    def __init__(self, NetworkProviderOptions):
        super().__init__(NetworkProviderOptions or {}, { artifactName: 'ZAP_Token'})

    async def balanceOf(self, address: address):
        return await self.contract.balanceof(adddress)
    
    async def send({to, amount,from, gasPrice, gas = Util.DEFAULT_GAS } : TransferType, cb = TransactionCallback):
        amount = toHex(amount)
        promiEvent = self.contract.transfer(to, amount),send({from, gas, gasPrice})
        if cb:
            #Event
            pass
        return promiEvent

    async def allocate({to, amount,from, gasPrice, gas = Util.DEFAULT_GAS } : TransferType, cb = TransactionCallback):
        amount = toHex(amount)
        promiEvent = self.contract.allocate(to, amount),send({from, gas, gasPrice})
        if cb:
            #Event
            pass
        return promiEvent

    async def approve({to, amount,from, gasPrice, gas = Util.DEFAULT_GAS } : TransferType, cb = TransactionCallback):
        amount = toHex(amount)
        _success = self.contract.approve(to,ammount).send({from, gas, gasPrice})
        if cd:
            #Event
            pass
        success = await _success

        if (not success):
            raise Exception('Failed to approve Bondage transfer')

        return success

    
    


