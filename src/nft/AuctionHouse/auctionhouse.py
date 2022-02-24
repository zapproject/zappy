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
        # get info from contract
        response = self.contract.functions.auctions(auctionId).call()
        # parse response into usable python class
        return AuctionInfo(response)

    def cancel_auction(self, auctionId: int):
        return self.send_transaction(self.contract.functions.cancelAuction(auctionId))
            
    def create_auction(self, tokenId, mediaContract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency):
        return self.send_transaction(self.contract.functions.createAuction(tokenId, mediaContract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency))
            
    def create_bid(self, auctionId: int, amount: int, mediaContract: str):
        return self.send_transaction(self.contract.functions.createBid(auctionId, amount, mediaContract))
            
    def end_auction(self, auctionId: int, mediaContract: str):
        return self.send_transaction(self.contract.functions.endAuction(auctionId, mediaContract))
            
    def set_auction_reserve_price(self, auctionId: int, reservePrice: int):
        return self.send_transaction(self.contract.functions.setAuctionReservePrice(auctionId, reservePrice))
            
    def start_auction(self, auctionId: int, approved:bool):
        return self.send_transaction(self.contract.functions.startAuction(auctionId, approved))
            
    ## Helper function that builds a dict representing IAuctionHouse.TokenDetails
    def makeTokenDetails(self, tokenId, mediaContract):
        return {
            "tokenId": tokenId,
            "mediaContract": mediaContract
        }