from src.nft.base_contract import BaseContract

class ZapToken(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(ZapToken.__name__)
        except Exception as e:
            print(e)
        
    def balanceOf(self, _owner: str):
        return self.contract.functions.balanceOf(_owner).call()

    def name(self):
        return self.contract.functions.name().call()
            
    def owner(self):
        return self.contract.functions.owner().call()
            
    def symbol(self):
        return self.contract.functions.symbol().call()
            
    def total_supply(self):
        return self.contract.functions.totalSupply().call()
    
    

            
    def allowance(self, _owner, _spender):
        return self.send_transaction(self.contract.functions.allowance(_owner, _spender))
            
    def approve(self, _spender, _value):
        return self.send_transaction(self.send_transaction(self.contract.functions.approve(_spender, _value)))
        
    def decreaseApproval(self, _spender, _subtractedValue):
        return self.send_transaction(self.contract.functions.decreaseApproval(_spender, _subtractedValue))
            
    def increaseApproval(self, _spender, _addedValue):
        return self.send_transaction(self.contract.functions.increaseApproval(_spender, _addedValue))

    def transfer(self, _to, _value):
        return self.send_transaction(self.send_transaction(self.contract.functions.transfer(_to, _value)))
            
    def transfer_from(self, _from, _to, _value):
        return self.send_transaction(self.contract.functions.transferFrom(_from, _to, _value))


    # def allocate(self, _to, amount):
    #     return self.contract.functions.allocate(_to, amount)

    # def decimals(self, ):
    #     return self.contract.functions.decimals()
            
    # def finishMinting(self, ):
    #     return self.contract.functions.finishMinting()
            
    # def mint(self, _to, _amount):
    #     return self.contract.functions.mint(_to, _amount)
            
    # def mintingFinished(self, ):
    #     return self.contract.functions.mintingFinished()
    
    # def transfer_ownership(self, newOwner):
    #     return self.contract.functions.transferOwnership(newOwner)
            