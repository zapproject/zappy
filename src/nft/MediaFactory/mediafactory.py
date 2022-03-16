from src.nft.base_contract import BaseContract

class MediaFactory(BaseContract):

    def __init__(self, chain_id: str = '31337', custom_contract_address: str = ""):
        super().__init__(chain_id)
        try:
            self.connect_to_contract(MediaFactory.__name__)
        except Exception as e:
            print(e)

    def owner(self):
        return self.contract.functions.owner().call()
        
    # def deploy_media(self, name: str, symbol: str, marketContractAddr: str, permissive: bool, _collectionMetadata: str):
    #     return self.send_transaction(self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata))

    def deploy_media(self, name: str, symbol: str, marketContractAddr: str, permissive: bool, _collectionMetadata: str):
        
        # tx_deploy_media = self.send_transaction(self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata))
        self.send_transaction(self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata))
        # receipt = self.w3.eth.wait_for_transaction_receipt(tx_deploy_media, 180)
        logs = self.contract.events.MediaDeployed.getLogs()
        event = logs[0]
        deployed_media_address = event.args.mediaContract
        print("deployed_media_address: ", deployed_media_address)
        return deployed_media_address

            