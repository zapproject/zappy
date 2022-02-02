from base_contract import BaseContract
from hexbytes import HexBytes
from web3.contract import ContractFunction

class MediaFactory(BaseContract):
    """
    Smart Contract wrapper for the Zap MediaFactory.

    The MediaFactory deploys ZapMedia ERC721 Smart Contracts to be used on the
    Zap NFT Marketplace.
    """

    def __init__(self, chainId: str):
        super().__init__(chainId)
        try:
            self.connect_to_contract(MediaFactory.__name__)
        except Exception as e:
            print(e)
        
    def deployMedia(self, name: str, symbol: str, marketContractAddr: str, permissive: bool, _collectionMetadata: str) -> HexBytes:
        """Deploys ZapMedia ERC721 contracts to be used on the Zap NFT Marketplace.

        This is the contract factory function, it deploys a proxy contract,
        then a ZapMedia contract, then sets the implementation and initializes ZapMedia.

        Parameters
        ----------
        name : str
            Name of the collection
        symbol : str
            Collection's symbol
        marketContractAddr : str
            ZapMarket contract to attach to, this can not be updated
        permissive : bool
            Whether or not you would like this contract to be minted by everyone or just the owner
        _collectionMetadata : str
            The metadata URI of the collection

        Returns
        ----------
        HexBytes
            The transaction hash
        """
        return self.sendTransaction(self.contract.functions.deployMedia(name, symbol, marketContractAddr, permissive, _collectionMetadata))
            
    def owner(self, ) -> ContractFunction:
        return self.contract.functions.owner()

    def renounceOwnership(self, ) -> ContractFunction:
        return self.contract.functions.renounceOwnership()
            
    def transferOwnership(self, newOwner: str) -> ContractFunction:
        return self.contract.functions.transferOwnership(newOwner)
            
    def upgradeMedia(self, newInterface: str) -> ContractFunction:
        """Upgrades ZapMedia contracts

        Calls `upgrateTo` on the Beacon contract to upgrade/replace the implementation contract.

        Can only be called by the owner of this `MediaFactory`.

        Parameters
        ----------
        newInterface : str
            The Address of the the new ZapMedia Interface
        """
        return self.contract.functions.upgradeMedia(newInterface)
