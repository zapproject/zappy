from base_contract import BaseContract

class AuctionHouse(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(AuctionHouse.__name__)
        except Exception as e:
            print(e)
        
    def auctions(self, ):
        return self.contract.functions.auctions()
            
    def cancelAuction(self, auctionId):
        return self.contract.functions.cancelAuction(auctionId)
            
    def createAuction(self, tokenId, mediaContract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency):
        return self.contract.functions.createAuction(tokenId, mediaContract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency)
            
    def createBid(self, auctionId, amount, mediaContract):
        return self.contract.functions.createBid(auctionId, amount, mediaContract)
            
    def endAuction(self, auctionId, mediaContract):
        return self.contract.functions.endAuction(auctionId, mediaContract)
            
    def hundredPercent(self, ):
        return self.contract.functions.hundredPercent()
            
    def initialize(self, _weth, _marketContract):
        return self.contract.functions.initialize(_weth, _marketContract)
            
    def minBidIncrementPercentage(self, ):
        return self.contract.functions.minBidIncrementPercentage()
            
    def setAuctionReservePrice(self, auctionId, reservePrice):
        return self.contract.functions.setAuctionReservePrice(auctionId, reservePrice)
            
    def startAuction(self, auctionId, approved):
        return self.contract.functions.startAuction(auctionId, approved)
            
    def timeBuffer(self, ):
        return self.contract.functions.timeBuffer()
            
    def wethAddress(self, ):
        return self.contract.functions.wethAddress()
            
    ## Helper function that builds a dict representing IAuctionHouse.TokenDetails
    def makeTokenDetails(self, tokenId, mediaContract):
        return {
            "tokenId": tokenId,
            "mediaContract": mediaContract
        }