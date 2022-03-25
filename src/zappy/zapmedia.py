from py_eth_sig_utils.signing import sign_typed_data
from py_eth_sig_utils.utils import normalize_key

from .base_contract import BaseContract


class ZapMedia(BaseContract):

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
        """
        return self.contract.functions.balanceOf(owner_address).call()
    
    def contract_URI(self):
        """
        Retrieves the collection URI
        """
        return self.contract.functions.contractURI().call()

    def get_approved(self, token_id: int):
        """
        Retrieves the approved address for specified token id
        """
        return self.contract.functions.getApproved(token_id).call()
            
    def get_owner(self):
        """
        Returns the owner of the media contract.
        """
        return self.contract.functions.getOwner().call()
             
    def get_permit_nonce(self, _user: str, token_id: int):
        """
        Retrieves the nonce for permit with signature transactions for specified user and token id
        """
        return self.contract.functions.getPermitNonce(_user, token_id).call()
            
    def getPreviousTokenOwners(self, token_id: int):
        return self.contract.functions.getPreviousTokenOwners(token_id).call
             
    def get_sig_nonces(self, _minter: str):
        """
        Retrieves the nonce for mint with signature transactions for specified user and token id
        """
        return self.contract.functions.getSigNonces(_minter).call()
             
    def get_token_content_hashes(self, token_id: int):
        """
        Retrieves the content URI hash for specified token id
        """
        return self.contract.functions.getTokenContentHashes(token_id).call()
            
    def get_token_creators(self, token_id: int):
        return self.contract.functions.getTokenCreators(token_id).call()
             
    def get_token_metadata_hashes(self, token_id: int):
        """
        Retrieves the metadata hash for the specified token id
        """
        return self.contract.functions.getTokenMetadataHashes(token_id).call()
             
    def get_token_metadata_URIs(self, token_id: int):
        """
        Retrieves the metadata URI for the specified token id
        """
        return self.contract.functions.getTokenMetadataURIs(token_id).call()

    def is_approved_for_all(self, owner: str, operator: str):
        """
        Retrieves the approved address for all of a user's token
        """
        return self.contract.functions.isApprovedForAll(owner, operator).call()
        
    def marketContract(self):
        """
        Retrieves the Zap Market contract address
        """
        return self.contract.functions.marketContract().call()
 
    def name(self):
        """
        Retrieves the name of the media contract
        """
        return self.contract.functions.name().call()
         
    def owner_of(self, token_id: int):
        """
        Retrieves the owner of the specified token id
        """
        return self.contract.functions.ownerOf(token_id).call()
 
    def supports_interface(self, interfaceId: str):
        """
        Determines whether the collection supports the specified interface id
        """
        return self.contract.functions.supportsInterface(interfaceId).call()
     
    def symbol(self):
        """
        Retrieves the collection symbol
        """
        return self.contract.functions.symbol().call()
            
    def token_by_index(self, index: int):
        """
        * Returns a token ID at a given `index` of all the tokens stored by the contract.
        """
        return self.contract.functions.tokenByIndex(index).call()
             
    def token_of_owner_by_index(self, owner: str, index: int):
        """
        Retrieves the token specified by the owner and index of the owner's tokens
        """
        return self.contract.functions.tokenOfOwnerByIndex(owner, index).call()
             
    def token_URI(self, token_id: int):
        """
        Retrieves the token / content URI for specified token id
        """
        return self.contract.functions.tokenURI(token_id).call()
             
    def total_supply(self):
        """
        Retrieves the total supply of token for this collection
        """
        return self.contract.functions.totalSupply().call()


    # ================================================================
    #                     WRITER FUNCTIONS
    # ================================================================
        
    # Accepts the specified bid as the token owner or approved user. 
    # Transfer of the token and bid amount is done internally.
    def accept_bid(self, token_id: int, bid, **kwargs):
        return self.send_transaction(self.contract.functions.acceptBid(token_id, bid), **kwargs)
            
    # Approves a user for managing the token
    def approve(self, _to: str, token_id: int, **kwargs):
        return self.send_transaction(self.contract.functions.approve(_to, token_id), **kwargs)
            
    # Burns the specified token id
    def burn(self, token_id: int, **kwargs):
        return self.send_transaction(self.contract.functions.burn(token_id), **kwargs)

    def claim_transfer_ownership(self):
        return self.send_transaction(self.contract.functions.claimTransferOwnership())
                        
    # Mints a new token
    def mint(self, data, bidShares, **kwargs):
        return self.send_transaction(self.contract.functions.mint(data, bidShares), **kwargs)
            
    # Mints a new token with ECDSA compliant signatures
    def mint_with_sig(self, creator: str, data, bidShares, sig, **kwargs):
        return self.send_transaction(self.contract.functions.mintWithSig(creator, data, bidShares, sig), **kwargs)

    # Approves user with specified signature and token id
    def permit(self, spender: str, token_id: int, sig, **kwargs):
        return self.send_transaction(self.contract.functions.permit(spender, token_id, sig), **kwargs)
            
    # Removes the current ask on the specified token id
    def remove_ask(self, token_id: int, **kwargs):
        return self.send_transaction(self.contract.functions.removeAsk(token_id), **kwargs)
            
    # Removes the current bid on the specified token id
    def remove_bid(self, token_id: int, **kwargs):
        return self.send_transaction(self.contract.functions.removeBid(token_id), **kwargs)
            
    # Removes all approvals on specified token id
    def revoke_approval(self, token_id: int, **kwargs):
        return self.send_transaction(self.contract.functions.revokeApproval(token_id), **kwargs)
            
    # Creates a new ask for specified token id. Restricted to owner or approved users.
    def set_ask(self, token_id: int, ask, **kwargs):
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
    def make_bid_shares(self, creator: str, owner: str, collaborators, collabShares):
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
