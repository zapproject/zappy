from base_contract import BaseContract

class ZapMedia(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(ZapMedia.__name__)
        except Exception as e:
            print(e)
        
    def acceptBid(self, tokenId, bid):
        return self.contract.functions.acceptBid(tokenId, bid)
            
    def appointedOwner(self, ):
        return self.contract.functions.appointedOwner()
            
    def approve(self, _to, tokenId):
        return self.contract.functions.approve(_to, tokenId)
            
    def approveToMint(self, toApprove):
        return self.contract.functions.approveToMint(toApprove)
            
    def auctionTransfer(self, tokenId, recipient):
        return self.contract.functions.auctionTransfer(tokenId, recipient)
            
    def balanceOf(self, owner):
        return self.contract.functions.balanceOf(owner)
            
    def burn(self, tokenId):
        return self.contract.functions.burn(tokenId)
            
    def claimTransferOwnership(self, ):
        return self.contract.functions.claimTransferOwnership()
            
    def contractURI(self, ):
        return self.contract.functions.contractURI()
            
    def getApproved(self, tokenId):
        return self.contract.functions.getApproved(tokenId)
            
    def getOwner(self, ):
        return self.contract.functions.getOwner()
            
    def getPermitNonce(self, _user, _tokenId):
        return self.contract.functions.getPermitNonce(_user, _tokenId)
            
    def getPreviousTokenOwners(self, _tokenId):
        return self.contract.functions.getPreviousTokenOwners(_tokenId)
            
    def getSigNonces(self, _minter):
        return self.contract.functions.getSigNonces(_minter)
            
    def getTokenContentHashes(self, _tokenId):
        return self.contract.functions.getTokenContentHashes(_tokenId)
            
    def getTokenCreators(self, _tokenId):
        return self.contract.functions.getTokenCreators(_tokenId)
            
    def getTokenMetadataHashes(self, _tokenId):
        return self.contract.functions.getTokenMetadataHashes(_tokenId)
            
    def getTokenMetadataURIs(self, _tokenId):
        return self.contract.functions.getTokenMetadataURIs(_tokenId)
            
    def initTransferOwnership(self, newOwner):
        return self.contract.functions.initTransferOwnership(newOwner)
            
    def initialize(self, name, symbol, marketContractAddr, permissive, collectionURI):
        return self.contract.functions.initialize(name, symbol, marketContractAddr, permissive, collectionURI)
            
    def isApprovedForAll(self, owner, operator):
        return self.contract.functions.isApprovedForAll(owner, operator)
            
    def marketContract(self, ):
        return self.contract.functions.marketContract()
            
    def mint(self, data, bidShares):
        return self.contract.functions.mint(data, bidShares)
            
    def mintWithSig(self, creator, data, bidShares, sig):
        return self.contract.functions.mintWithSig(creator, data, bidShares, sig)
            
    def name(self, ):
        return self.contract.functions.name()
            
    def ownerOf(self, tokenId):
        return self.contract.functions.ownerOf(tokenId)
            
    def permit(self, spender, tokenId, sig):
        return self.contract.functions.permit(spender, tokenId, sig)
            
    def removeAsk(self, tokenId):
        return self.contract.functions.removeAsk(tokenId)
            
    def removeBid(self, tokenId):
        return self.contract.functions.removeBid(tokenId)
            
    def revokeApproval(self, tokenId):
        return self.contract.functions.revokeApproval(tokenId)
            
    def revokeTransferOwnership(self, ):
        return self.contract.functions.revokeTransferOwnership()
            
    def safeTransferFrom(self, _from, _to, tokenId):
        return self.contract.functions.safeTransferFrom(_from, _to, tokenId)
            
    def safeTransferFrom(self, _from, _to, tokenId, _data):
        return self.contract.functions.safeTransferFrom(_from, _to, tokenId, _data)
            
    def setApprovalForAll(self, operator, approved):
        return self.contract.functions.setApprovalForAll(operator, approved)
            
    def setAsk(self, tokenId, ask):
        return self.contract.functions.setAsk(tokenId, ask)
            
    def setBid(self, tokenId, bid):
        return self.contract.functions.setBid(tokenId, bid)
            
    def supportsInterface(self, interfaceId):
        return self.contract.functions.supportsInterface(interfaceId)
            
    def symbol(self, ):
        return self.contract.functions.symbol()
            
    def tokenByIndex(self, index):
        return self.contract.functions.tokenByIndex(index)
            
    def tokenMetadataURI(self, tokenId):
        return self.contract.functions.tokenMetadataURI(tokenId)
            
    def tokenOfOwnerByIndex(self, owner, index):
        return self.contract.functions.tokenOfOwnerByIndex(owner, index)
            
    def tokenURI(self, tokenId):
        return self.contract.functions.tokenURI(tokenId)
            
    def totalSupply(self, ):
        return self.contract.functions.totalSupply()
            
    def transferFrom(self, _from, _to, tokenId):
        return self.contract.functions.transferFrom(_from, _to, tokenId)
            
    def updateTokenMetadataURI(self, tokenId, metadataURI):
        return self.contract.functions.updateTokenMetadataURI(tokenId, metadataURI)
            
    def updateTokenURI(self, tokenId, tokenURILocal):
        return self.contract.functions.updateTokenURI(tokenId, tokenURILocal)
            
    ## Helper function that builds a dict representing IMedia.MediaData
    def makeMediaData(tokenURI, metadataURI, contentHash, metadataHash):
        return {
            "tokenURI": tokenURI,
            "metadataURI": metadataURI,
            "contentHash": contentHash,
            "metadataHash": metadataHash
        }

    ## Helper function that build a dict representing IMarket.BidShares
    def makeBidShares(creator, owner, collaborators, collabShares):
        return {
            "creator": {"value": creator},
            "owner": {"value": owner},
            "collaborators": collaborators,
            "collabShares": collabShares
        }

    ## Helper function that builds a dict representing IMedia.EIP712Signature
    def makeEIP712Sig(deadline, v, r, s):
        return {
            "deadline": deadline,
            "v": v,
            "r": r,
            "s": s
        }

    ## Helper function that builds a dict representing IMarket.Ask
    def makeAsk(amount, currency):
        return {
            "amount": amount,
            "currency": currency
        }

    ## Helper function that builds a dict representing IMarket.Bid
    def makeBid(amount, currency, bidder, recipient, sellOnShare):
        return {
            "amount": amount,
            "currency": currency,
            "bidder": bidder,
            "recipient": recipient,
            "sellOnShare": {"value": sellOnShare}
        }