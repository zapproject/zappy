from base_contract import BaseContract

class MediaFactory(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(MediaFactory.__name__)
        except Exception as e:
            print(e)

    def owner(self):
        return self.contract.functions.owner().call()
        
    def deploy_media(self, name: str, symbol: str, marketContractAddr: str, permissive: bool, _collectionMetadata: str):
        return self.send_transaction(self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata))

            


            