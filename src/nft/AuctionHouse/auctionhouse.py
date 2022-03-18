from tokenize import Number
from src.nft.base_contract import BaseContract
from src.nft.AuctionHouse.auctionInfo import AuctionInfo
class AuctionHouse(BaseContract):

    def __init__(self, chain_id: str = '31337', custom_contract_address: str = ""):
        super().__init__(chain_id, custom_contract_address)
        try:
            self.connect_to_contract(AuctionHouse.__name__)
        except Exception as e:
            print(e)


    # ================================================================
    #                     GETTER FUNCTIONS
    # ================================================================


    def auctions(self, auction_Id: int) -> AuctionInfo:
        """
        Get auction detail for a given auction Id.

        :param int auction_Id: auction id number

        :example:
        >>> auction_house.auctions(4)
        
        """

        # get auction data from blockchain
        response = self.contract.functions.auctions(auction_Id).call()
        
        # parse response into usable python class
        return AuctionInfo(response)


    # ================================================================
    #                     WRITER FUNCTIONS
    # ================================================================


    def cancel_auction(self, auction_Id: int):
        """
        Cancels auction for a given auction Id.

        :param int auction_Id: auction id number

        :example:
        >>> auction_house.cancel_auction(4)
        
        """
        return self.send_transaction(self.contract.functions.cancelAuction(auction_Id))
            
    def create_auction(self, token_Id: int, media_contract: str, duration: int, reservePrice: int, curator: str, curatorFeePercentage: int, auctionCurrency: str):
        """
        Creates an auction for a given token Id.

        :param int auction_Id: auction id number
        :param int token_Id: token Id number
        :param str media_contract: media contract address
        :param int duration: token Id number
        :param int reservePrice: token Id number
        :param str curator: curator's address
        :param int curatorFeePercentage: token Id number
        :param str auctionCurrency: address of accepted token for payment

        :example:
            params = [
            token_id, 
            zap_media.address, 
            duration, 
            reservePrice, 
            curator, 
            0, 
            zap_token.address
            ]

        >>> auctionhouse.create_auction(*params)
        
        """
        return self.send_transaction(self.contract.functions.createAuction(token_Id, media_contract, duration, reservePrice, curator, curatorFeePercentage, auctionCurrency))
            
    def create_bid(self, auction_Id: int, amount: int, media_contract: str):
        """
        Creates bid for a given auction Id.

        :param int auction_Id: auction id number
        :param int amount: amount of tokens
        :param str media_contract: media contract address associated with the auction Id

        :example:
        >>> auction_house.create_bid(4, "0x1234567890qwerty")
        
        """
        return self.send_transaction(self.contract.functions.createBid(auction_Id, amount, media_contract))
            
    def end_auction(self, auction_Id: int, media_contract: str):
        """
        End auction for a given auction Id.

        :param int auction_Id: auction id number
        :param str media_contract: media contract address associated with the auction Id

        :example:
        >>> auction_house.end_auction(4, "0x1234567890qwerty")
        
        """
        return self.send_transaction(self.contract.functions.endAuction(auction_Id, media_contract))
            
    def set_auction_reserve_price(self, auction_Id: int, reserve_price: int):
        """
        Set reserve price for a given auction Id.

        :param int auction_Id: auction id number
        :param int reserve_price: minimun price of tokens that need to be met

        :example:
        >>> auction_house.set_auction_reserve_price(4, 300)
        
        """
        return self.send_transaction(self.contract.functions.setAuctionReservePrice(auction_Id, reserve_price))
            
    def start_auction(self, auction_Id: int, approved: bool):
        """
        Starts the auction for a given auction Id.

        :param int auction_Id: auction id number
        :param bool approved: approve auction, starting it up for a bid

        :example:
        >>> auction_house.start_auction(4, True)
        
        """
        return self.send_transaction(self.contract.functions.startAuction(auction_Id, approved))
            
    ## Helper function that builds a dict representing IAuctionHouse.TokenDetails
    def makeTokenDetails(self, token_Id, media_contract):
        return {
            "token_Id": token_Id,
            "media_contract": media_contract
        }