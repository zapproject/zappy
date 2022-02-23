from tokenize import Number
from src.nft.base_contract import BaseContract
from src.nft.AuctionHouse.auctionInfo import AuctionInfo
from typing import TypedDict

class TokenDetails(TypedDict, total=False):
    tokenId: int
    mediaContract: str

class Auction(TypedDict, total=False):
    token: TokenDetails
    approved: bool
    amount: int
    duration: int
    firstBidTime: int
    reservePrice: int
    curatorFeePercentage: int 
    tokenOwner: str
    bidder: str
    curator: str
    auctionCurrency: str


class AuctionHouse(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(AuctionHouse.__name__)
        except Exception as e:
            print(e)
        
    def auctions(self, auctionId: int) -> AuctionInfo:
        response = self.contract.functions.auctions(auctionId).call()
        return AuctionInfo(response)

    def cancelAuction(self, auctionId: int):
        return self.contract.functions.cancelAuction(auctionId)
            
    def create_auction(self, tokenId, mediaContract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency):
        return self.sendTransaction(self.contract.functions.createAuction(tokenId, mediaContract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency))
            
    def createBid(self, auctionId, amount, mediaContract):
        return self.contract.functions.createBid(auctionId, amount, mediaContract)
            
    def endAuction(self, auctionId, mediaContract):
        return self.contract.functions.endAuction(auctionId, mediaContract)
            
    def hundredPercent(self):
        return self.contract.functions.hundredPercent()
            
    def initialize(self, _weth, _marketContract):
        return self.contract.functions.initialize(_weth, _marketContract)
            
    def minBidIncrementPercentage(self):
        return self.contract.functions.minBidIncrementPercentage()
            
    def setAuctionReservePrice(self, auctionId: int, reservePrice: int):
        return self.sendTransaction(self.contract.functions.setAuctionReservePrice(auctionId, reservePrice))
            
    def start_auction(self, auctionId: int, approved:bool):
        return self.sendTransaction(self.contract.functions.startAuction(auctionId, approved))
            
    def timeBuffer(self):
        return self.contract.functions.timeBuffer()
            
    def wethAddress(self):
        return self.contract.functions.wethAddress()
            
    ## Helper function that builds a dict representing IAuctionHouse.TokenDetails
    def makeTokenDetails(self, tokenId, mediaContract):
        return {
            "tokenId": tokenId,
            "mediaContract": mediaContract
        }