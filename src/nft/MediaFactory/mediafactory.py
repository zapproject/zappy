from base_contract import BaseContract

class MediaFactory(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(MediaFactory.__name__)
        except Exception as e:
            print(e)
        
    def deployMedia(self, name, symbol, marketContractAddr, permissive, _collectionMetadata):
        return self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata)
            
    def initialize(self, _zapMarket, zapMediaInterface):
        return self.contract.functions.initialize(_zapMarket, zapMediaInterface)
            
    def owner(self, ):
        return self.contract.functions.owner()
            
    def renounceOwnership(self, ):
        return self.contract.functions.renounceOwnership()
            
    def transferOwnership(self, newOwner):
        return self.contract.functions.transferOwnership(newOwner)
            
    def upgradeMedia(self, newInterface):
        return self.contract.functions.upgradeMedia(newInterface)
            