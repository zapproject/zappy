from typing import TypedDict
class AuctionInfo():

    def __init__(self, auctionResponse):
        
            self.token_details = TokenDetails(auctionResponse[0])
            self.approved = auctionResponse[1]
            self.amount = auctionResponse[2]
            self.duration = auctionResponse[3]
            self.first_bid_Time = auctionResponse[4]
            self.reserve_price = auctionResponse[5]
            self.curator_fee_percentage = auctionResponse[6]
            self.token_owner = auctionResponse[7]
            self.bidder = auctionResponse[8]
            self.curator = auctionResponse[9]
            self.auction_currency = auctionResponse[10]
        
class TokenDetails():
    def __init__(self, token_details):
        self.token_id = token_details[0]
        self.media_contract = token_details[1]

# class TokenDetails(TypedDict, total=False):
#     tokenId: int
#     mediaContract: str

# class Auction(TypedDict, total=False):
#     token: TokenDetails
#     approved: bool
#     amount: int
#     duration: int
#     firstBidTime: int
#     reservePrice: int
#     curatorFeePercentage: int 
#     tokenOwner: str
#     bidder: str
#     curator: str
#     auctionCurrency: str