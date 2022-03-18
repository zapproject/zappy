from src.nft.base_contract import BaseContract

class ZapMarket(BaseContract):

    def __init__(self, chain_id: str = '31337', custom_contract_address: str = ""):
        super().__init__(chain_id)
        try:
            self.connect_to_contract(ZapMarket.__name__)
        except Exception as e:
            print(e)
        
    def acceptBid(self, mediaContractAddress, tokenId, expectedBid):
        return self.contract.functions.acceptBid(mediaContractAddress, tokenId, expectedBid)
            
    def appointedOwner(self, ):
        return self.contract.functions.appointedOwner()
            
    def bid_for_token_bidder(self, mediaContractAddress, tokenId, bidder):
        return self.contract.functions.bidForTokenBidder(mediaContractAddress, tokenId, bidder).call()
            
    def bidSharesForToken(self, mediaContractAddress, tokenId):
        return self.contract.functions.bidSharesForToken(mediaContractAddress, tokenId).call()
            
    def claimTransferOwnership(self, ):
        return self.contract.functions.claimTransferOwnership()
            
    def configure(self, deployer, mediaContract, name, symbol):
        return self.contract.functions.configure(deployer, mediaContract, name, symbol)
            
    def current_ask_for_token(self, mediaContractAddress: str, tokenId: int):
        return self.contract.functions.currentAskForToken(mediaContractAddress, tokenId).call()
            
    def get_owner(self):
        return self.contract.functions.getOwner().call()
            
    def initTransferOwnership(self, newOwner):
        return self.contract.functions.initTransferOwnership(newOwner)
            
    def isConfigured(self, media_contract_address: str) -> bool:
        return self.contract.functions.isConfigured(media_contract_address).call()
            
    def isRegistered(self, media_contract_address: str) -> bool:
        return self.contract.functions.isRegistered(media_contract_address).call()
            
    def isValidBid(self, mediaContractAddress, tokenId, bidAmount):
        return self.contract.functions.isValidBid(mediaContractAddress, tokenId, bidAmount).call()
            
    def isValidBidShares(self, bidShares):
        return self.contract.functions.isValidBidShares(bidShares)
            
    def mediaContracts(self, deployerAddress, index):
        return self.contract.functions.mediaContracts(deployerAddress, index).call()
            
    def mintOrBurn(self, isMint, tokenId, mediaContract):
        return self.contract.functions.mintOrBurn(isMint, tokenId, mediaContract)
            
    def registerMedia(self, mediaContract):
        return self.contract.functions.registerMedia(mediaContract)
            
    def registeredMedias(self, ):
        return self.contract.functions.registeredMedias()
            
    def removeAsk(self, tokenId):
        return self.contract.functions.removeAsk(tokenId)
            
    def removeBid(self, tokenId, bidder):
        return self.contract.functions.removeBid(tokenId, bidder)
            
    def revokeRegistration(self, mediaContract):
        return self.contract.functions.revokeRegistration(mediaContract)
            
    def revokeTransferOwnership(self, ):
        return self.contract.functions.revokeTransferOwnership()
            
    def setAsk(self, tokenId, ask):
        return self.contract.functions.setAsk(tokenId, ask)
            
    def setBid(self, tokenId, bid, spender):
        return self.contract.functions.setBid(tokenId, bid, spender)
            
    def setBidShares(self, tokenId, bidShares):
        return self.contract.functions.setBidShares(tokenId, bidShares)
            
    def setFee(self, newFee):
        return self.contract.functions.setFee(newFee)
            
    def setMediaFactory(self, _mediaFactory):
        return self.contract.functions.setMediaFactory(_mediaFactory)
            
    def splitShare(self, sharePercentage, amount):
        return self.contract.functions.splitShare(sharePercentage, amount)
            
    def viewFee(self, ):
        return self.contract.functions.viewFee()
            
    ## Helper function that builds a dict representing IMedia.MediaData
    def makeMediaData(self, tokenURI, metadataURI, contentHash, metadataHash):
        return {
            "tokenURI": tokenURI,
            "metadataURI": metadataURI,
            "contentHash": contentHash,
            "metadataHash": metadataHash
        }

    ## Helper function that build a dict representing IMarket.BidShares
    def makeBidShares(self, creator, owner, collaborators, collabShares):
        return {
            "creator": {"value": creator},
            "owner": {"value": owner},
            "collaborators": collaborators,
            "collabShares": collabShares
        }

    ## Helper function that builds a dict representing IMedia.EIP712Signature
    def makeEIP712Sig(self, deadline, v, r, s):
        return {
            "deadline": deadline,
            "v": v,
            "r": r,
            "s": s
        }

    ## Helper function that builds a dict representing IMarket.Ask
    def makeAsk(self, amount, currency):
        return {
            "amount": amount,
            "currency": currency
        }

    ## Helper function that builds a dict representing IMarket.Bid
    def makeBid(self, amount, currency, bidder, recipient, sellOnShare):
        return {
            "amount": amount,
            "currency": currency,
            "bidder": bidder,
            "recipient": recipient,
            "sellOnShare": {"value": sellOnShare}
        }