from src.nft.base_contract import BaseContract

class ZapTokenBSC(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(ZapTokenBSC.__name__)
        except Exception as e:
            print(e)
        
    def allocate(self, _to, amount):
        return self.contract.functions.allocate(_to, amount)
            
    def allowance(self, _owner, _spender):
        return self.contract.functions.allowance(_owner, _spender)
            
    def approve(self, _spender, _value):
        return self.sendTransaction(self.contract.functions.approve(_spender, _value))
        
    def balanceOf(self, _owner):
        return self.contract.functions.balanceOf(_owner).call()
            
    def decimals(self, ):
        return self.contract.functions.decimals()
            
    def decreaseApproval(self, _spender, _subtractedValue):
        return self.contract.functions.decreaseApproval(_spender, _subtractedValue)
            
    def finishMinting(self, ):
        return self.contract.functions.finishMinting()
            
    def getOwner(self, ):
        return self.contract.functions.getOwner()
            
    def increaseApproval(self, _spender, _addedValue):
        return self.contract.functions.increaseApproval(_spender, _addedValue)
            
    def mint(self, _to, _amount):
        return self.contract.functions.mint(_to, _amount)
            
    def mintingFinished(self, ):
        return self.contract.functions.mintingFinished()
            
    def name(self, ):
        return self.contract.functions.name()
            
    def owner(self, ):
        return self.contract.functions.owner()
            
    def symbol(self, ):
        return self.contract.functions.symbol()
            
    def totalSupply(self, ):
        return self.contract.functions.totalSupply()
            
    def transfer(self, _to, _value):
        return self.sendTransaction(self.contract.functions.transfer(_to, _value))
            
    def transferFrom(self, _from, _to, _value):
        return self.contract.functions.transferFrom(_from, _to, _value)
            
    def transferOwnership(self, newOwner):
        return self.contract.functions.transferOwnership(newOwner)
            