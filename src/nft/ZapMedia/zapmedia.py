from src.nft.base_contract import BaseContract
import traceback

class ZapMedia(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(ZapMedia.__name__)
        except Exception as e:
            print(e)
        
    # Accepts the specified bid as the token owner or approved user. 
    # Transfer of the token and bid amount is done internally.
    def acceptBid(self, tokenId, bid):
        return self.sendTransaction(self.contract.functions.acceptBid(tokenId, bid))
            
    def appointedOwner(self, ):
        return self.contract.functions.appointedOwner()
            
    # Approves a user for managing the token
    def approve(self, _to, tokenId):
        return self.sendTransaction(self.contract.functions.approve(_to, tokenId))
            
    def approveToMint(self, toApprove):
        return self.contract.functions.approveToMint(toApprove)
            
    # Retrives the number of tokens the user has
    def balanceOf(self, owner):
        try:
            return self.contract.functions.balanceOf(owner).call()
        except Exception as e:
            print(e)
            
    # Burns the specified token id
    def burn(self, tokenId):
        return self.sendTransaction(self.contract.functions.burn(tokenId))
            
    def claimTransferOwnership(self, ):
        return self.contract.functions.claimTransferOwnership()
            
    # Retrieves the contract URI 
    def contractURI(self, ):
        try:
            return self.contract.functions.contractURI().call()
        except Exception as e:
            print(e)
            
    # Retreives the approved address for specified token id
    def getApproved(self, tokenId:int) -> str:
        try:
            return self.contract.functions.getApproved(tokenId).call()
        except Exception as e:
            print(e)
            
    def getOwner(self, ):
        return self.contract.functions.getOwner()
            
    def getPermitNonce(self, _user, _tokenId):
        return self.contract.functions.getPermitNonce(_user, _tokenId)
            
    def getPreviousTokenOwners(self, _tokenId):
        return self.contract.functions.getPreviousTokenOwners(_tokenId)
            
    def getSigNonces(self, _minter):
        return self.contract.functions.getSigNonces(_minter).call()
            
    # Retreives the content URI hash for specified token id
    def getTokenContentHashes(self, _tokenId):
        try:
            return self.contract.functions.getTokenContentHashes(_tokenId).call()
        except Exception as e:
            print(e)
            
    def getTokenCreators(self, _tokenId):
        return self.contract.functions.getTokenCreators(_tokenId)
            
    # Retreives the metadata hash for the specified token id
    def getTokenMetadataHashes(self, _tokenId):
        try:
            return self.contract.functions.getTokenMetadataHashes(_tokenId).call()
        except Exception as e:
            print(e)
            
    # Retreives the metadata URI for the specified token id
    def getTokenMetadataURIs(self, _tokenId):
        try:
            return self.contract.functions.getTokenMetadataURIs(_tokenId).call()
        except Exception as e:
            print(e)
            
    def initTransferOwnership(self, newOwner):
        return self.contract.functions.initTransferOwnership(newOwner)
            
    def initialize(self, name, symbol, marketContractAddr, permissive, collectionURI):
        return self.contract.functions.initialize(name, symbol, marketContractAddr, permissive, collectionURI)
            
    def isApprovedForAll(self, owner, operator):
        return self.contract.functions.isApprovedForAll(owner, operator)
            
    def marketContract(self):
        return self.contract.functions.marketContract()
            
    # Mints a new token
    def mint(self, data, bidShares):
        return self.sendTransaction(self.contract.functions.mint(data, bidShares))
            
    # Mints a new token with ECDSA compliant signatures
    def mintWithSig(self, creator, data, bidShares, sig):
        return self.sendTransaction(self.contract.functions.mintWithSig(creator, data, bidShares, sig))

    def name(self):
        try:
            return self.contract.functions.name().call()
        except Exception as e:
            print(e)
            
    # Retreives the owner of the specified token id
    def ownerOf(self, tokenId):
        try:
            return self.contract.functions.ownerOf(tokenId).call()
        except Exception as e:
            print(e)

    def permit(self, spender, tokenId, sig):
        return self.contract.functions.permit(spender, tokenId, sig)
            
    # Removes the current ask on the specified token id
    def removeAsk(self, tokenId):
        return self.sendTransaction(self.contract.functions.removeAsk(tokenId))
            
    # Removes the current bid on the specified token id
    def removeBid(self, tokenId):
        return self.sendTransaction(self.contract.functions.removeBid(tokenId))
            
    # Removes all approvals on specified token id
    def revokeApproval(self, tokenId):
        return self.sendTransaction(self.contract.functions.revokeApproval(tokenId))
            
    def revokeTransferOwnership(self):
        return self.contract.functions.revokeTransferOwnership()
            
    def safeTransferFrom(self, _from, _to, tokenId):
        return self.contract.functions.safeTransferFrom(_from, _to, tokenId)
            
    def safeTransferFrom(self, _from, _to, tokenId, _data):
        return self.contract.functions.safeTransferFrom(_from, _to, tokenId, _data)
            
    def setApprovalForAll(self, operator, approved):
        return self.contract.functions.setApprovalForAll(operator, approved)
            
    # Creates a new ask for specified token id. Restricted for owner or approved users.
    def setAsk(self, tokenId, ask):
        return self.sendTransaction(self.contract.functions.setAsk(tokenId, ask))
            
    # Creates a new bid for specified token id
    def setBid(self, tokenId, bid):
        return self.sendTransaction(self.contract.functions.setBid(tokenId, bid))
            
    # Determines whether the collection supports the specified interface id
    def supportsInterface(self, interfaceId):
        try:
            return self.contract.functions.supportsInterface(interfaceId).call()
        except Exception as e:
            print(e)
            
    # Retreives the collection symbol
    def symbol(self):
        try:
            return self.contract.functions.symbol().call()
        except Exception as e:
            print(e)
            
    # Retreives the token specified by index
    def tokenByIndex(self, index):
        try:
            return self.contract.functions.tokenByIndex(index).call()
        except Exception as e:
            print(e)
            
    # Retreives the token specified by the owner and index of the owner's tokens
    def tokenOfOwnerByIndex(self, owner, index):
        try:
            return self.contract.functions.tokenOfOwnerByIndex(owner, index).call()
        except Exception as e:
            print(e)
            
    # Retreives the token / content URI for specified token id
    def tokenURI(self, tokenId):
        try:
            return self.contract.functions.tokenURI(tokenId).call()
        except Exception as e:
            print(e)
            
    # Retreives the total supply of token for this collection
    def totalSupply(self, ):
        try:
            return self.contract.functions.totalSupply().call()
        except Exception as e:
            print(e)
            
    def transferFrom(self, _from, _to, tokenId):
        return self.contract.functions.transferFrom(_from, _to, tokenId)
            
    # Updates the metadata URI for specified token id
    def updateTokenMetadataURI(self, tokenId, metadataURI):
        return self.sendTransaction(self.contract.functions.updateTokenMetadataURI(tokenId, metadataURI))
            
    # Updates the token URI for the specified token id
    def updateTokenURI(self, tokenId, tokenURILocal):
        return self.sendTransaction(self.contract.functions.updateTokenURI(tokenId, tokenURILocal))

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