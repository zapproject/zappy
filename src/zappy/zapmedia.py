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
            **kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            .. seealso:: Helper function 'ZapMedia.make_bid(...)'

            - bid param::

                bid = {
                        "amount": int,
                        "currency": str,
                        "bidder": str,
                        "recipient": str,
                        "sellOnShare": {"value": int}
                    }

            - Example using make_bid helper function::

                bid = make_bid(50, zap_token.address, "0xBIDDER_ADDRESS", "0xRECIPIENT_ADDRESS", 10)
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
            **kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            .. seealso:: Helper function 'ZapMedia.set_approval_for_all(...)'

            - Example::

                tx = zap_media.accept_bid(3, bid)
        """
        return self.send_transaction(self.contract.functions.approve(to, token_id), **kwargs)
            
    def burn(self, token_id: int, **kwargs):
        """
            Owner or approved can burns the specified token id.

            :param token_id: Id of NFT token
            :type token_id: int
            **kwargs: Arbitrary keyword arguments.
            :return: transaction hash

            - Example::

                tx = zap_media.burn(3)
        """
        return self.send_transaction(self.contract.functions.burn(token_id), **kwargs)

    def claim_transfer_ownership(self, **kwargs):
        """
            Deployer can use this function to claim ownership of a custom media contract deployed through the Media Factory.
            The Media Factory will be the owner of the contract until claimed.

            :return: transaction hash
            **kwargs: Arbitrary keyword arguments.
            

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
            :return: transaction hash

            **kwargs: Arbitrary keyword arguments.
            
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
            :return: transaction hash

            **kwargs: Arbitrary keyword arguments.
            
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
            :return: transaction hash

            **kwargs: Arbitrary keyword arguments.
            
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
            :return: transaction hash

            **kwargs: Arbitrary keyword arguments.

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

            **kwargs: Arbitrary keyword arguments.

            - Example::
                            
                tx = zap_media.remove_bid(3)
        """
        return self.send_transaction(self.contract.functions.removeBid(token_id), **kwargs)
            
    def revoke_approval(self, token_id: int, **kwargs):
        """
            Removes all approvals on specified token id            
            :param token_id: Id of NFT token
            :type token_id: int
            :return: transaction hash

            **kwargs: Arbitrary keyword arguments.

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
            :return: transaction hash

            **kwargs: Arbitrary keyword arguments.

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
            
    # Creates a new bid for specified token id
    def set_bid(self, token_id: int, bid, **kwargs):
        return self.send_transaction(self.contract.functions.setBid(token_id, bid), **kwargs)
    
    # Updates the metadata URI for specified token id
    def update_token_metadata_URI(self, token_id: int, metadataURI: str, **kwargs):
        return self.send_transaction(self.contract.functions.updateTokenMetadataURI(token_id, metadataURI), **kwargs)
            
    # Updates the token URI for the specified token id
    def update_token_URI(self, token_id: int, tokenURILocal: str, **kwargs):
        return self.send_transaction(self.contract.functions.updateTokenURI(token_id, tokenURILocal), **kwargs)

    def set_approval_for_all(self, operator: str, approved: bool, **kwarg):
        return self.send_transaction(self.contract.functions.setApprovalForAll(operator, approved), **kwarg)

    def safe_transfer_from(self, _from: str, _to: str, token_id: int, **kwarg):
        return self.send_transaction(self.contract.functions.safeTransferFrom(_from, _to, token_id), **kwarg)

    def transfer_from(self, _from: str, _to: str, token_id: int):
        return self.send_transaction(self.contract.functions.transferFrom(_from, _to, token_id))

    
    
    
    
    # def revokeTransferOwnership(self):
    #     return self.contract.functions.revokeTransferOwnership()

    # def safeTransferFrom(self, _from, _to, token_id, _data):
    #     return self.contract.functions.safeTransferFrom(_from, _to, token_id, _data)



            



    # ================================================================
    #                     HELPER FUNCTIONS
    # ================================================================

    ## Helper function that builds a dict representing IMedia.MediaData
    # def make_media_data(self, tokenURI, metadataURI, contentHash, metadataHash):
    def make_media_data(self, tokenURI: str, metadataURI: str):
        return {
            "tokenURI": tokenURI,
            "metadataURI": metadataURI,
            "contentHash": self.generate_hash_from_string(tokenURI),
            "metadataHash": self.generate_hash_from_string(metadataURI)
        }

    ## Helper function that build a dict representing IMarket.BidShares
    def make_bid_shares(self, creator: int, owner: int, collaborators, collabShares):
        return {
            "creator": {"value": creator},
            "owner": {"value": owner},
            "collaborators": collaborators,
            "collabShares": collabShares
        }

    ## Helper function that builds a dict representing IMedia.EIP712Signature
    def make_EIP712_Sig(self, deadline, v, r, s):
        return {
            "deadline": deadline,
            "v": v,
            "r": r,
            "s": s
        }

    ## Helper function that builds a dict representing IMarket.Ask
    def make_ask(self, amount: int, currency_address: str):
        return {
            "amount": amount,
            "currency": currency_address
        }

    ## Helper function that builds a dict representing IMarket.Bid
    def make_bid(self, amount: int, currency: str, bidder: str, recipient: str, sellOnShare: int):
        return {
            "amount": amount,
            "currency": currency,
            "bidder": bidder,
            "recipient": recipient,
            "sellOnShare": {"value": sellOnShare}
        }

    # Creates the ECDSA compliant signature for minting
    def get_mint_signature(self, media_data, bid_share, deadline):
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

    
    # Creates the ECDSA compliant signature for approving
    def get_permit_signature(self, spender: str, token_id: int, deadline: int):
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
        hex = self.w3.toHex(text=string_input)
        hash = self.w3.solidityKeccak(['bytes32'], [hex])
        return hash
