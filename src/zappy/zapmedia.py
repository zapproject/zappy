from py_eth_sig_utils.signing import sign_typed_data
from py_eth_sig_utils.utils import normalize_key

from .base_contract import BaseContract


class ZapMedia(BaseContract):
    """
    This class wraps the deployed ZapMedia contract.
    
    :param chain_id: chain Id of network 
    :type chain_id: str
    :param custom_contract_address: optional address for custom ZapMedia contract other than the official Zap Media Collection
    :type custom_contract_address: str

    :return: ZapMedia class connected to contract on given chain Id.

    - Example of connection to Zap Collection on BSC Testnet::
        
        bsc_testnet_chainId: str = "97"
        media = ZapMedia(bsc_testnet_chainId)
    
    - Example of connection to Zap Collection on BSC Testnet::
        
        bsc_testnet_chainId: str = "97"
        custom_media_contract: str = "0xCUSTOM_MEDIA_ADDRESS_FROM_MEDIA_FACTORY"
        media = ZapMedia(bsc_testnet_chainId, custom_media_contract)
    
    """

    def __init__(self, chain_id: str = '31337', custom_contract_address: str = ""):
        super().__init__(chain_id, custom_contract_address)
        try:
            self.connect_to_contract(ZapMedia.__name__)
        except Exception as e:
            print(e)
    
    # ================================================================
    #                     GETTER FUNCTIONS
    # ================================================================

    def balance_of(self, owner_address: str):
        """
            Retrives the number of tokens the user has
            
            :param owner_address: address of wallet
            :type owner_address: str
            :return: number of NFTs owned by given address

            - Example::

                balance = zap_media.balance_of(signers[1].address)
            
        """
        return self.contract.functions.balanceOf(owner_address).call()
    
    def contract_URI(self):
        """
            Retrives the contract URI used for the collection

            :return: base URI of contract 

            - Example::

                uri = zap_media.contract_URI()
            
        """
        return self.contract.functions.contractURI().call()

    def get_approved(self, token_id: int):
        """
            Retrives the approved address for a given token id
            
            :param token_id: Id of NFT token
            :type token_id: int
            :return: address of approved 

            - Example::
                token_id: int = 3
                balance = zap_media.get_approved(token_id)
            
        """
        return self.contract.functions.getApproved(token_id).call()
            
    def get_owner(self):
        """
            Retrives the owner address for the deploy media contract
            
            :return: address of contract owner 

            - Example::

                owner_address = zap_media.get_owner()
            
        """
        return self.contract.functions.getOwner().call()
             
    def get_permit_nonce(self, _user: str, token_id: int):
        """
            Retrives nonce of a particular NFT to create a permit. Used when creating a signature.

            :param _user: address of user
            :type _user: str
            :param token_id: Id of NFT token
            :type token_id: int
            :return: latest nonce of a given address and token id

            - Example::
                user: str = "0xUserAddress"
                token_id: int = 5
                nonce = zap_media.get_permit_nonce(user, token_id)
            
        """
        return self.contract.functions.getPermitNonce(_user, token_id).call()
            
    def get_previous_token_owners(self, token_id: int):
        """
            Retrieves the previous owner of an NFT

            :param token_id: Id of NFT token
            :type token_id: int
            :return: address of previous owner of given NFT

            - Example::
                token_id: int = 5
                prev_owner = zap_media.getPreviousTokenOwners(token_id)
            
        """
        return self.contract.functions.get_previous_token_owners(token_id).call
             
    def get_sig_nonces(self, _minter: str):
        """
            Retrives nonce of a particular NFT to create a signature. Used when creating a signature.

            :param _minter: address of user
            :type _minter: str
            :return: latest nonce of a given address and token id

            - Example::
                minter: str = "0xUserAddress"
                sig_nonce = zap_media.get_sig_nonces(minter)
            
        """
        return self.contract.functions.getSigNonces(_minter).call()
             
    def get_token_content_hashes(self, token_id: int):
        """
            Retrives the content hash of the NFT

            :param token_id: Id of NFT token
            :type token_id: int
            :return: content hash 

            - Example::

                content_hash = zap_media.get_token_content_hashes(7)
            
        """
        return self.contract.functions.getTokenContentHashes(token_id).call()
            
    def get_token_creators(self, token_id: int):
        """
            Retrives the creator of the NFT

            :param token_id: Id of NFT token
            :type token_id: int
            :return: base URI of contract 

            - Example::

                content_hash = zap_media.get_token_content_hashes(7)
            
        """
        return self.contract.functions.getTokenCreators(token_id).call()
             
    def get_token_metadata_hashes(self, token_id: int):
        """
            Retrives the metadata hash of the NFT

            :param token_id: Id of NFT token
            :type token_id: int
            :return: metadata hash 

            - Example::

                content_hash = zap_media.get_token_metadata_hashes(7)
            
        """
        return self.contract.functions.getTokenMetadataHashes(token_id).call()
             
    def get_token_metadata_URIs(self, token_id: int):
        """
            Retrives the metadata URI of the NFT

            :param token_id: Id of NFT token
            :type token_id: int
            :return: metadata URI 

            - Example::

                content_hash = zap_media.get_token_metadata_URIs(7)
            
        """
        return self.contract.functions.getTokenMetadataURIs(token_id).call()

    def is_approved_for_all(self, owner: str, operator: str):
        """
            Retrives the approved address for all of a user's NFTs
            
            :param owner: owner address of the NFTs
            :type owner: str
            :param token_id: Id of NFT token
            :type token_id: int
            :return: address of approved 

            - Example::
                owner: str = "0xOwnerAddress"
                token_id: int = 3
                balance = zap_media.is_approved_for_all(owner, token_id)
            
        """
        return self.contract.functions.isApprovedForAll(owner, operator).call()
        
    def market_contract(self):
        """
            Retrieves the Zap Market contract address

            :return: address of Zap Market contract

            - Example::
                zap_market_address = zap_media.market_contract(owner, token_id)
        """
        return self.contract.functions.marketContract().call()
 
    def name(self):
        """
            Retrieves the name of the NFT collection

            :return: collection name

            - Example::
                collection_name = zap_media.name()
        """
        return self.contract.functions.name().call()
         
    def owner_of(self, token_id: int):
        """
            Retrieves the name of the NFT collection

            :param token_id: Id of NFT token
            :type token_id: int
            :return: collection name

            - Example::
                collection_name = zap_media.name()
        """
        return self.contract.functions.ownerOf(token_id).call()
 
    def supports_interface(self, interface_id: str):
        """
            Checks if the contract support a particular interface

            :param interface_id: interface id to check
            :type interface_id: string
            :return: collection name

            - Example::
                collection_name = zap_media.name()
        """
        return self.contract.functions.supportsInterface(interface_id).call()
     
    def symbol(self):
        """
            Retrieves the symbol of the NFT collection
            :return: symbol of collection

            - Example::
                symbol = zap_media.symbol()
        """
        return self.contract.functions.symbol().call()
            
    def token_by_index(self, index: int):
        """
            Retrieves the token_id of the NFT in Zap Media

            :param index: Id of NFT token
            :type index: int
            :return: corresponsing token id of a given index

            - Example::
                token_id = zap_media.token_by_index(3)
        """
        return self.contract.functions.tokenByIndex(index).call()
             
    def token_of_owner_by_index(self, owner: str, index: int):
        """
            Retrieves the token_id of the NFT in Zap Media

            :param owner: address of token owner
            :type owner: str
            :param index: Id of NFT token
            :type index: int
            :return: corresponsing token id of a given addressa and index

            - Example::
                token_id = zap_media.token_of_owner_by_index("0xOWNERADDRES", 3)
        """
        return self.contract.functions.tokenOfOwnerByIndex(owner, index).call()
             
    def token_URI(self, token_id: int):
        """
            Retrieves the URI of an NFT

            :param token_id: Id of NFT token
            :type token_id: int
            :return: URI of minted NFT

            - Example::
                token_id = zap_media.token_URI(3)
        """
        return self.contract.functions.tokenURI(token_id).call()
             
    def total_supply(self):
        """
            Retrieves the total supply of the media contract

            :return: Total supply. Subtract by 1 to get the latest token Id.

            - Example::
                token_id = zap_media.total_supply()
        """
        return self.contract.functions.totalSupply().call()


    # ================================================================
    #                     WRITER FUNCTIONS
    # ================================================================
        
    # Accepts the specified bid as the token owner or approved user. 
    # Transfer of the token and bid amount is done internally.
    def accept_bid(self, token_id: int, bid, **kwargs):
        """
            Owner of an approved user can use this function to accept a submitted bid for an NFT.
            Once accepted, payment and NFT are both transferred to it's new wallet/owner.

            :param token_id: Id of NFT token
            :type token_id: int
            :param bid: dictionary of the bid. 
            :type bid: dict[int, str, str, str, dict[int]]
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash 
            

            .. seealso:: 

                Helper function ``zap_media.make_bid(...)``

            - bid param::

                bid = {
                        "amount": int,
                        "currency": str,
                        "bidder": str,
                        "recipient": str,
                        "sellOnShare": {"value": int}
                    }

            - Example using make_bid helper function::

                bid = make_bid(
                        50,
                        zap_token.address, 
                        "0xBIDDER_ADDRESS",
                        "0xRECIPIENT_ADDRESS", 
                        10
                        )
                token_id = zap_media.accept_bid(3, bid)
        """
        return self.send_transaction(self.contract.functions.acceptBid(token_id, bid), **kwargs)
            
    def approve(self, to: str, token_id: int, **kwargs):
        """
            NFT owner can approve a user address, to help manage the token.

            :param to: address
            :type to: str
            :param token_id: Id of NFT token
            :type token_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            .. seealso:: 
            
                'ZapMedia.set_approval_for_all(...)'

            - Example::

                tx = zap_media.accept_bid(3, bid)
        """
        return self.send_transaction(self.contract.functions.approve(to, token_id), **kwargs)
            
    def burn(self, token_id: int, **kwargs):
        """
            Owner or approved can burns the specified token id.

            :param token_id: Id of NFT token
            :type token_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::

                tx = zap_media.burn(3)
        """
        return self.send_transaction(self.contract.functions.burn(token_id), **kwargs)

    def claim_transfer_ownership(self, **kwargs):
        """
            Deployer can use this function to claim ownership of a custom media contract deployed through the Media Factory.
            The Media Factory will be the owner of the contract until claimed.

            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash
            

            - Example::

                media_factory = MediaFactory()
                
                args = [
                    'CUSTOM COLLECTION', 
                    'CCT', 
                    zap_market.address,
                    True, 
                    'https://customcollection.com'
                    ]
                
                (receipt, deployed_media_address) = media_factory.deploy_media(*args)                
                my_media = ZapMedia("chainId", deployed_media_address)
                tx = my_media.claim_transfer_ownership()
        """
        return self.send_transaction(self.contract.functions.claimTransferOwnership(), **kwargs)
                        
    # Mints a new token
    def mint(self, data, bid_shares, **kwargs):
        """
            Mints a new token. Once minted, should in the owner's wallet.

            :param data: dictionary of media metadata
            :type data: dict[str, str, bytes(32), bytes(32)]
            :param bid_shares: dictionary of the bidShare
            :type bid_shares: dict[dict[int], dict[int], List[str], List[int]]
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            
            .. seealso::
                
                :Helper function: ZapMedia.make_media_data(...)
                :Helper function: ZapMedia.make_bid_shares(...)
                    
                For simplicity, use the helper functions to create the data and bid_shares parameters.


            - Example::

                media_data = zap_media.make_media_data(...)
                bid_shares = zap_media.make_bid_shares(...)
                             
                tx = zap_media.mint(media_data, bid_shares)
        """
        return self.send_transaction(self.contract.functions.mint(data, bid_shares), **kwargs)
            
    def mint_with_sig(self, creator: str, data, bidShares, sig, **kwargs):
        """
            Mints a new token with ECDSA compliant signatures. Once minted, should in the owner's wallet.

            :param creator: public address of creator
            :type creator: str
            :param data: dictionary of media metadata
            :type data: dict[str, str, bytes(32), bytes(32)]
            :param bid_shares: dictionary of the bidShare
            :type bid_shares: dict[dict[int], dict[int], List[str], List[int]]
            :param sig: ECDSA compliant signature
            :type sig: string
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            
            .. seealso::
                
                :Helper function: zap_media.make_media_data(...)
                :Helper function: zap_media.make_bid_shares(...)
                :Helper function: zap_media.get_mint_signature(...)
                    
                For simplicity, use the helper functions to create the data, bid_shares, and sig parameters.


            - Example::

                media_data = zap_media.make_media_data(...)
                bid_shares = zap_media.make_bid_shares(...)
                sig = zap_media.get_mint_signature_shares(...)
                             
                tx = zap_media.mint_with_sig(creator_address, media_data, bid_shares, sig)
        """
        return self.send_transaction(self.contract.functions.mintWithSig(creator, data, bidShares, sig), **kwargs)

    def permit(self, spender: str, token_id: int, sig, **kwargs):
        """
            Approves user with specified signature and token id
            
            :param spender: public address of spender
            :type spender: str
            :param token_id: Id of NFT token
            :type token_id: int
            :param sig: ECDSA compliant signature
            :type sig: string
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            
            .. seealso::
                
                :Helper function: zap_media.get_permit_signature(...)
                    
                For simplicity, use the helper function to create the sig parameter.


            - Example::

                sig = zap_media.get_permit_signature(...)
                             
                tx = zap_media.permit(spender_address, 3, sig)
        """
        return self.send_transaction(self.contract.functions.permit(spender, token_id, sig), **kwargs)
            
    def remove_ask(self, token_id: int, **kwargs):
        """
            Removes the current ask on the specified token id
            
            :param token_id: Id of NFT token
            :type token_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash


            - Example::
                            
                tx = zap_media.remove_ask(3)
        """
        return self.send_transaction(self.contract.functions.removeAsk(token_id), **kwargs)
            
    def remove_bid(self, token_id: int, **kwargs):
        """
            Removes the current bid on the specified token id            
            :param token_id: Id of NFT token
            :type token_id: int
            :return: transaction hash

            :kwargs: Arbitrary keyword arguments.

            - Example::
                            
                tx = zap_media.remove_bid(3)
        """
        return self.send_transaction(self.contract.functions.removeBid(token_id), **kwargs)
            
    def revoke_approval(self, token_id: int, **kwargs):
        """
            Removes all approvals on specified token id            
            :param token_id: Id of NFT token
            :type token_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash


            - Example::
                            
                tx = zap_media.revoke_approval(3)
        """
        return self.send_transaction(self.contract.functions.revokeApproval(token_id), **kwargs)

    def set_ask(self, token_id: int, ask, **kwargs):
        """
            Creates a new ask for specified token id.
            Restricted to owner or approved users.

            :param token_id: Id of NFT token
            :type token_id: int
            :param ask: dictionary of ask data
            :type ask: dict[int, str]
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash


            .. seealso::
                
                :Helper function: zap_media.make_ask(...)
                    
                For simplicity, use the helper function to create the ask parameter.

            - Example::
                            
                ask = zap_media.make_ask(
                    100,
                    zap_token.address
                    )

                tx_hash = zap_media.set_ask(3, ask)
        """
        return self.send_transaction(self.contract.functions.setAsk(token_id, ask), **kwargs)
            
    def set_bid(self, token_id: int, bid, **kwargs):
        """
            Creates a new bid for specified token id.
            
            :param token_id: Id of NFT token
            :type token_id: int
            :param bid: dictionary of bid data
            :type bid: dict[int, str, str, str, int]
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash


            .. seealso:: 
                
                Helper function 'zap_media.make_bid(...)'


            - Example::
                            
                bid = zap_media.make_bid(
                    100,
                    zap_token.address,
                    bidder,
                    wallets[1],
                    10
                    )

                tx_hash = zap_media.set_bid(3, bid)
        """
        return self.send_transaction(self.contract.functions.setBid(token_id, bid), **kwargs)
    
    def update_token_metadata_URI(self, token_id: int, metadataURI: str, **kwargs):
        """
            Updates the metadata URI for specified token id.
            
            :param token_id: Id of NFT token
            :type token_id: int
            :param metadataURI: URI to updated metadata
            :type metadataURI: str
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::

                token_id = 3
                new_URI = "https://newURI.com"     
                tx_hash = zap_media.update_token_metadata_URI(token_id, new_URI)
        """
        return self.send_transaction(self.contract.functions.updateTokenMetadataURI(token_id, metadataURI), **kwargs)
            
    def update_token_URI(self, token_id: int, token_URI_Local: str, **kwargs):
        """
            Updates the token URI for the specified token id

            :param token_id: Id of NFT token
            :type token_id: int
            :param token_URI_Local: URI to updated metadata
            :type token_URI_Local: str
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::
            
                token_id = 3
                new_URI = "https://newURI.com"     
                tx_hash = zap_media.update_token_URI(token_id, new_URI)
        """
        return self.send_transaction(self.contract.functions.updateTokenURI(token_id, token_URI_Local), **kwargs)

    def set_approval_for_all(self, operator: str, approved: bool, **kwarg):
        """
            NFT owner can approve a user address, to help manage all tokens in collection.

            :param operator: address to give approval for all
            :type operator: str
            :param approved: True or False
            :type approved: bool
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            .. seealso:: 
                
                Helper function 'ZapMedia.approve(...)'

            - Example::

                user_to_approve: "0xUSERADDRESS"
                permission: True

                tx = zap_media.set_approval_for_all(user_to_approve, permission)
        """
        return self.send_transaction(self.contract.functions.setApprovalForAll(operator, approved), **kwarg)

    def safe_transfer_from(self, _from: str, _to: str, token_id: int, **kwarg):
        """
            Executes a SafeTransfer of the given tokenId to the specified address if and only if it adheres to the ERC721-Receiver Interface

            :param _from: address of the owner
            :type _from: str
            :param _to: address of the recipient
            :type _to: str
            :param token_id: Id of NFT token
            :type token_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::

                owner = "0xOWNERADDRESS"
                recipient = "0xRECIPIENTADDRESS"
                token_id = 3

                tx = zap_media.safe_transfer_from(owner, recipient, token_id)
        """
        return self.send_transaction(self.contract.functions.safeTransferFrom(_from, _to, token_id), **kwarg)

    def transfer_from(self, _from: str, _to: str, token_id: int):
        """
            Transfers the specified tokenId to the specified to address

            :param _from: address of the owner
            :type _from: str
            :param _to: address of the recipient
            :type _to: str
            :param token_id: Id of NFT token
            :type token_id: int
            :kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::

                owner = "0xOWNERADDRESS"
                recipient = "0xRECIPIENTADDRESS"
                token_id = 3
                tx = zap_media.transfer_from(owner, recipient, token_id)
        """
        return self.send_transaction(self.contract.functions.transferFrom(_from, _to, token_id))   
    
               



    # ================================================================
    #                     HELPER FUNCTIONS
    # ================================================================

    def make_media_data(self, token_URI: str, metadata_URI: str):
        """
            Helper function that builds a dict representing IMedia.MediaData struct.

            :param token_URI: link to the media/resource that is representated by the NFT token
            :type token_URI: str
            :param metadata_URI: address of the recipient
            :type metadata_URI: str
            :kwargs: Arbitrary keyword arguments.
            :return: dict[str, str, bytes, bytes]

            - Example::

                # if using Pinata
                base_url = 'https://gateway.pinata.cloud/ipfs/'
                token_URI = base_url + "CID_FROM_PINATA"
                metadata_URI = base_url + "ANOTHER_CID_FROM_PINATA"

                media_data = zap_media.transfer_from(token_URI, metadata_URI)
        """
        return {
            "tokenURI": token_URI,
            "metadataURI": metadata_URI,
            "contentHash": self.generate_hash_from_string(token_URI),
            "metadataHash": self.generate_hash_from_string(metadata_URI)
        }

    def make_bid_shares(self, creator: int, owner: int, collaborators, collabShares):
        """
            Helper function that build a dict representing IMarket.BidShares struct.
            Used when minting a new token and defines the creator, owner, and collaborators of the media being minted.
            Also defines the each member's share of the media.

            :param creator: creator share
            :type creator: int
            :param owner: owner share
            :type owner: int
            :param collaborators: a list of address that represents collaborators on the media
            :type collaborators: List[str]
            :param collabShares: a list of integers that represents each collaborator's share of the media
            :type collabShares: List[int]
            :kwargs: Arbitrary keyword arguments.
            :return: dict[dict[int], dict[int], List[str], List[int]]

            .. note:: 
                Total shares should add up to 95% since the platform automatically get 5%.


            - Example::
                
                creator_share = 10
                owner_share = 75
                collaborators = ["0xFIRSTCOLLABORATOR", "0xSECONDCOLLABORATOR"]
                collab_shares = [5,5]
                # total shares: 10 + 75 + 5 + 5 = 95

                bid_shares = zap_media.make_bid_shares(creator_share, owner_share, collaborators, collab_shares)
        """
        return {
            "creator": {"value": creator},
            "owner": {"value": owner},
            "collaborators": collaborators,
            "collabShares": collabShares
        }

    def make_ask(self, amount: int, currency: str):
        """
            Helper function that builds a dict representing IMarket.Ask struct

            :param amount: the price of the token
            :type amount: int
            :param currency: address of ERC20 token being used to pay
            :type currency: str
            :kwargs: Arbitrary keyword arguments.
            :return: dict[int, str]

            - Example::
                
                amount = 250
                currency = "0xTOKENCONTRACTADDRESS"
                
                bid = zap_media.make_ask(amount, currency)
        """

        return {
            "amount": amount,
            "currency": currency
        }


    def make_bid(self, amount: int, currency: str, bidder: str, recipient: str, sell_on_share: int):
        """
            Helper function that builds a dict representing IMarket.Bid

            :param amount: amount willing to bid
            :type amount: int
            :param currency: address of ERC20 token being used to pay
            :type currency: str
            :param bidder: address of bidder
            :type bidder: str
            :param recipient: address of recipient
            :type recipient: str
            :param sell_on_share: % of the next sale to award the current owner
            :type sell_on_share: int
            :kwargs: Arbitrary keyword arguments.
            :return: dict[int, str, str, str, dict[int]]

            - Example::
                
                amount = 250
                currency = "0xTOKENCONTRACTADDRESS"
                bidder = "0xBIDDERADDRESS"
                recipient = "0xRECIPIENTADDRESS"
                sell_on_share = 10
                
                bid = zap_media.make_bid(amount, currency, bidder, recipient, sell_on_share)
        """
        return {
            "amount": amount,
            "currency": currency,
            "bidder": bidder,
            "recipient": recipient,
            "sellOnShare": {"value": sell_on_share}
        }
    
    def make_EIP712_Sig(self, deadline, v, r, s):
        """
            Helper function that builds a dict representing IMedia.EIP712Signature.
            Mainly used internally to create the signature or a permit signature.

            :param deadline: amount willing to bid
            :type deadline: int
            :param v: a component of the signature
            :type v: str
            :param r: a component of the signature
            :type r: str
            :param s: a component of the signature
            :type s: str
            :kwargs: Arbitrary keyword arguments.
            :return: dict[int, str, str, int]

            - Example::
                
                sig = zap_media.make_EIP712_Sig(deadline, v, r, s)
        """
        return {
            "deadline": deadline,
            "v": v,
            "r": r,
            "s": s
        }

    # Creates the ECDSA compliant signature for minting
    def get_mint_signature(self, media_data, bid_share, deadline):
        """
            Helper function to creates the ECDSA compliant signature for minting

            :param media_data: media data dict
            :type media_data: dict
            :param bid_share: bid_share dict
            :type bid_share: dict
            :param deadline: deadline in unixtime
            :type deadline: int
            :kwargs: Arbitrary keyword arguments.
            :return: dict[int, int, str, str]

            - Example::
                
                media_data = zap_media.make_media_data(
                                            token_URI, 
                                            metadataURI
                                            )
                bid_shares = zap_media.make_bid_shares(
                                            90000000000000000000,
                                            5000000000000000000,
                                            [],
                                            []
                                            )
                deadline = int(time.time() + 60 * 60 * 24)
                
                sig = zap_media.get_mint_signature(media_data, bid_shares, deadline) 
        """
        # EIP191 data structure which specifies EIP712 versioning
        data = {
            "types": {
                "EIP712Domain": [
                    { "name": "name", "type": "string" },
                    { "name": "version", "type": "string" },
                    { "name": "chainId", "type": "uint256" },
                    { "name": "verifyingContract", "type": "address" }
                ],
                "MintWithSig": [
                    { "name": 'contentHash', "type": 'bytes32' },
                    { "name": 'metadataHash', "type": 'bytes32' },
                    { "name": 'creatorShare', "type": 'uint256' },
                    { "name": 'nonce', "type": 'uint256' },
                    { "name": 'deadline', "type": 'uint256' }
                ]
            },
            "primaryType": "MintWithSig",
            "domain": {
                "name": self.name(),
                "version": "1",
                "chainId": int(self.chain_id),
                "verifyingContract": self.address
            },
            "message": {
                'contentHash': media_data["contentHash"],
                'metadataHash': media_data["metadataHash"],
                'creatorShare': bid_share["creator"]["value"],
                'nonce': self.get_sig_nonces(self.public_address),
                'deadline': deadline
            }
        }

        # signs the data
        sig_data = sign_typed_data(data, normalize_key(self.private_key))

        # builds the signature struct for solidity
        return self.make_EIP712_Sig(
            deadline, 
            sig_data[0], 
            self.w3.toHex(sig_data[1]),
            self.w3.toHex(sig_data[2]),
        )

    def get_permit_signature(self, spender: str, token_id: int, deadline: int):
        """
            Helper function to creates the ECDSA compliant signature for approving

            :param spender: address to give approval
            :type spender: str
            :param token_id: Id of NFT token
            :type token_id: int
            :param deadline: deadline in unixtime
            :type deadline: int
            :kwargs: Arbitrary keyword arguments.
            :return: dict[int, int, str, str]

            - Example::
                
                spender = "0xSPENDERADDRESS"
                token_id = 4
                deadline = int(time.time() + 60 * 60 * 24)
                
                sig = zap_media.get_permit_signature(spender, token_id, deadline) 
        """



        # EIP191 data structure which specifies EIP712 versioning
        data = {
            "types": {
                "EIP712Domain": [
                    { "name": "name", "type": "string" },
                    { "name": "version", "type": "string" },
                    { "name": "chainId", "type": "uint256" },
                    { "name": "verifyingContract", "type": "address" }
                ],
                "Permit": [
                    { "name": 'spender', "type": 'address' },
                    { "name": 'tokenId', "type": 'uint256' },
                    { "name": 'nonce', "type": 'uint256' },
                    { "name": 'deadline', "type": 'uint256' },
                ]
            },
            "primaryType": "Permit",
            "domain": {
                "name": self.name(),
                "version": "1",
                "chainId": int(self.chain_id),
                "verifyingContract": self.address
            },
            "message": {
                'spender': spender,
                'tokenId': token_id,
                'nonce': self.get_permit_nonce(self.public_address, token_id),
                'deadline': deadline
            }
        }

        # signs the data
        sig_data = sign_typed_data(data, normalize_key(self.private_key))

        # builds the signature struct for solidity
        return self.make_EIP712_Sig(
            deadline, 
            sig_data[0], 
            self.w3.toHex(sig_data[1]),
            self.w3.toHex(sig_data[2]),
        )


    def generate_hash_from_string(self, string_input: str):
        """
            Helper function to creates a str that's compatible with bytes32 in Solidity.
            This function helps with strings that are too long and not compatible with bytes32.
            Mainly used in helper function `make_media_data()`.

            :param string_input: string input
            :type string_input: str
            :return: bytes

            - Example::
                
                base_url = 'https://gateway.pinata.cloud/ipfs/'
                token_URI = base_url + "CID_FROM_PINATA"
                
                hash = self.get_permit_signature(token_URI) 
        """
        hex = self.w3.toHex(text=string_input)
        hash = self.w3.solidityKeccak(['bytes32'], [hex])
        return hash
