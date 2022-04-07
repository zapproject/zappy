from .base_contract import BaseContract

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


    def deploy_media(self, name: str, symbol: str, marketContractAddr: str, permissive: bool, _collectionMetadata: str, **kwargs):
        """
            Deploys a custom Zap Media contract for user/users to mint as well as interact with the Zap NFT Marketplace.

            :param name: name of collection
            :type name: str
            :param symbol: symbol of collection
            :type symbol: str
            :param marketContractAddr: associated zap market contract address
            :type marketContractAddr: str
            :paraml permissive: permit other users to mint from this collection
            :typel permissive: bool
            :param _collectionMetadata: URI of collection metadata
            :type _collectionMetadata: str
            :kwargs: Arbitrary keyword arguments.
            :return: a tuple that contains the transaction receipt and the newly deployed media address

            - Example::

                args = ['Collection Name', 'CSYM', zap_market.address, True, "https://ExampleCollectionURI.com"]
                (receipt, media_address) = media_factory.deploy_media(*args)        
        """
        tx_deploy_media = self.send_transaction(self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata), **kwargs)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_deploy_media, 180)
        logs = self.contract.events.MediaDeployed.getLogs()
        event = logs[0]
        deployed_media_address = event.args.mediaContract
        return (receipt, deployed_media_address)


            