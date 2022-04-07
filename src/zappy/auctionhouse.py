from .base_contract import BaseContract

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


    def auctions(self, auction_id: int) -> AuctionInfo:
        """
            Get auction detail for a given auction Id.

            :param auction_id: Id of auction
            :type auction_id: int
            :return: transaction hash

            - Example::

                auction_info = auction_house.auctions(4)
        
        """

        # get auction data from blockchain
        response = self.contract.functions.auctions(auction_id).call()
        
        # parse response into usable python class
        return AuctionInfo(response)


    # ================================================================
    #                     WRITER FUNCTIONS
    # ================================================================


    def cancel_auction(self, auction_id: int, **kwargs):
        """
            Cancel an auction of a given auction Id.

            :param auction_id: Id of auction
            :type auction_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::

                tx = auction_house.cancel_auction(4)
            
        """
        return self.send_transaction(self.contract.functions.cancelAuction(auction_id),  **kwargs)
            
    def create_auction(self, token_id: int, media_contract: str, duration: int, reserve_price: int, curator: str, curator_fee_percentage: int, auction_currency: str, **kwargs):
        """
            Creates an auction for a given token Id.

            :param token_id: token Id number
            :type token_id: int
            :param media_contract: media contract address
            :type media_contract: str
            :param duration: duration of auctionhouse
            :type duration: int
            :param reserve_price: minimum accepted price
            :type reserve_price: int
            :param curator: curator's address
            :type curator: str
            :param curator_fee_percentage: curator fee
            :type curator_fee_percentage: int
            :param auction_currency: token address of accepted token
            :type auction_currency: str
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::
                
                params = {
                    token_id: 3, 
                    media_contract: zap_media.address, 
                    duration: duration, 
                    reserve_price: reserve_price, 
                    curator: curator, 
                    curator_fee_percentage: curator_fee_percentage, 
                    auction_currency: zap_token.address
                    }

                tx = auctionhouse.create_auction(**params)
        
        """
        return self.send_transaction(self.contract.functions.createAuction(token_id, media_contract, duration, reserve_price, curator, curator_fee_percentage, auction_currency), **kwargs)
            
    def create_bid(self, auction_id: int, amount: int, media_contract: str, **kwargs):
        """
            Create a bid on a token, with a given amount.

            :param auction_id: Id of auction
            :type auction_id: int
            :param amount: bid amount
            :type amount: int
            :param media_contract: contract address of collection the NFT belongs to
            :type media_contract: str
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::
            
                tx = auction_house.create_bid(4, 500, "0xMEDIACONTRACTADDRESS")
            
        """
        return self.send_transaction(self.contract.functions.createBid(auction_id, amount, media_contract), **kwargs)
            
    def end_auction(self, auction_id: int, media_contract: str, **kwargs):
        """
            End an auction, finalizing the bid on Zap NFT Marketplace if applicable and paying out the respective parties.

            :param auction_id: Id of auction
            :type auction_id: int
            :param media_contract: contract address of collection the NFT belongs to
            :type media_contract: str
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::
            
                tx = auction_house.end_auction(4, "0xMEDIACONTRACTADDRESS")
            
        """
        return self.send_transaction(self.contract.functions.endAuction(auction_id, media_contract), **kwargs)
            
    def set_auction_reserve_price(self, auction_id: int, reserve_price: int, **kwargs):
        """
            Set a reserve price of an auction.

            :param auction_id: Id of auction
            :type auction_id: int
            :param reserve_price: minimum accepted price
            :type reserve_price: str
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::
            
                tx = auction_house.set_auction_reserve_price(4, 650)
            
        """
        return self.send_transaction(self.contract.functions.setAuctionReservePrice(auction_id, reserve_price), **kwargs)
            
    def start_auction(self, auction_id: int, approved: bool, **kwargs):
        """
            Approve an auction, opening up the auction for bids.

            :param auction_id: Id of auction
            :type auction_id: int
            :param approved: approve auction
            :type approved: bool
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::
            
                tx = auction_house.start_auction(4, True)
            
        """
        return self.send_transaction(self.contract.functions.startAuction(auction_id, approved), **kwargs)
            
