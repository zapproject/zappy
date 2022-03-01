from eth_typing import Address
from src.nft.base_contract import BaseContract
from py_eth_sig_utils.signing import sign_typed_data
from py_eth_sig_utils.utils import normalize_key


class ZapMedia(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)
        try:
            self.connect_to_contract(ZapMedia.__name__)
        except Exception as e:
            print(e)



    # ================================================================
    #                     GETTER FUNCTIONS
    # ================================================================

    # Retrives the number of tokens the user has
    def balance_of(self, owner):
        try:
            return self.contract.functions.balanceOf(owner).call()
        except Exception as e:
            print(e)
    
        # Retrieves the contract URI 
    def contract_URI(self):
        try:
            return self.contract.functions.contractURI().call()
        except Exception as e:
            print(e)
    # Retreives the approved address for specified token id
    def get_approved(self, tokenId:int) -> str:
        try:
            return self.contract.functions.getApproved(tokenId).call()
        except Exception as e:
            print(e)
            
    def get_owner(self):
        return self.contract.functions.getOwner()
            
    # Retreives the nonce for permit with signature transactions for specified user and token id
    def get_permit_nonce(self, _user, _tokenId):
        return self.contract.functions.getPermitNonce(_user, _tokenId).call()
            
    def getPreviousTokenOwners(self, _tokenId):
        return self.contract.functions.getPreviousTokenOwners(_tokenId)
            
    # Retreives the nonce for mint with signature transactions for specified user and token id
    def get_sig_nonces(self, _minter):
        return self.contract.functions.getSigNonces(_minter).call()
            
    # Retreives the content URI hash for specified token id
    def get_token_content_hashes(self, _tokenId):
        try:
            return self.contract.functions.getTokenContentHashes(_tokenId).call()
        except Exception as e:
            print(e)
            
    def get_token_creators(self, _tokenId):
        return self.contract.functions.getTokenCreators(_tokenId)
            
    # Retreives the metadata hash for the specified token id
    def get_token_metadata_hashes(self, _tokenId):
        try:
            return self.contract.functions.getTokenMetadataHashes(_tokenId).call()
        except Exception as e:
            print(e)
            
    # Retreives the metadata URI for the specified token id
    def get_token_metadata_URIs(self, _tokenId):
        try:
            return self.contract.functions.getTokenMetadataURIs(_tokenId).call()
        except Exception as e:
            print(e)

    # Retreives the name of the media contract
    def name(self):
            try:
                return self.contract.functions.name().call()
            except Exception as e:
                print(e)
            
    # Retreives the owner of the specified token id
    def owner_of(self, tokenId):
        try:
            return self.contract.functions.ownerOf(tokenId).call()
        except Exception as e:
            print(e)

    # Determines whether the collection supports the specified interface id
    def supports_interface(self, interfaceId):
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
            
    def token_by_index(self, index):
        """
        * Returns a token ID at a given `index` of all the tokens stored by the contract.
        """
        try:
            return self.contract.functions.tokenByIndex(index).call()
        except Exception as e:
            print(e)
            
    # Retreives the token specified by the owner and index of the owner's tokens
    def token_of_owner_by_index(self, owner, index):
        try:
            return self.contract.functions.tokenOfOwnerByIndex(owner, index).call()
        except Exception as e:
            print(e)
            
    # Retreives the token / content URI for specified token id
    def token_URI(self, tokenId):
        try:
            return self.contract.functions.tokenURI(tokenId).call()
        except Exception as e:
            print(e)
            
    # Retreives the total supply of token for this collection
    def total_supply(self, ):
        try:
            return self.contract.functions.totalSupply().call()
        except Exception as e:
            print(e)

    def is_approved_for_all(self, owner: str, operator: str):
        return self.contract.functions.isApprovedForAll(owner, operator).call()


    # ================================================================
    #                     WRITER FUNCTIONS
    # ================================================================
        
    # Accepts the specified bid as the token owner or approved user. 
    # Transfer of the token and bid amount is done internally.
    def accept_bid(self, tokenId, bid, **kwargs):
        return self.send_transaction(self.contract.functions.acceptBid(tokenId, bid), **kwargs)
            
    # Approves a user for managing the token
    def approve(self, _to: Address, tokenId: int, **kwargs):
        return self.send_transaction(self.contract.functions.approve(_to, tokenId), **kwargs)
            
    # Burns the specified token id
    def burn(self, tokenId, **kwargs):
        return self.send_transaction(self.contract.functions.burn(tokenId), **kwargs)
                        
    # Mints a new token
    def mint(self, data, bidShares, **kwargs):
        return self.send_transaction(self.contract.functions.mint(data, bidShares), **kwargs)
            
    # Mints a new token with ECDSA compliant signatures
    def mint_with_sig(self, creator, data, bidShares, sig, **kwargs):
        return self.send_transaction(self.contract.functions.mintWithSig(creator, data, bidShares, sig), **kwargs)

    # Approves user with specified signature and token id
    def permit(self, spender, tokenId, sig, **kwargs):
        return self.send_transaction(self.contract.functions.permit(spender, tokenId, sig), **kwargs)
            
    # Removes the current ask on the specified token id
    def remove_ask(self, tokenId, **kwargs):
        return self.send_transaction(self.contract.functions.removeAsk(tokenId), **kwargs)
            
    # Removes the current bid on the specified token id
    def remove_bid(self, tokenId, **kwargs):
        return self.send_transaction(self.contract.functions.removeBid(tokenId), **kwargs)
            
    # Removes all approvals on specified token id
    def revoke_approval(self, tokenId, **kwargs):
        return self.send_transaction(self.contract.functions.revokeApproval(tokenId), **kwargs)
            
    # Creates a new ask for specified token id. Restricted for owner or approved users.
    def set_ask(self, tokenId, ask, **kwargs):
        return self.send_transaction(self.contract.functions.setAsk(tokenId, ask), **kwargs)
            
    # Creates a new bid for specified token id
    def set_bid(self, tokenId, bid, **kwargs):
        return self.send_transaction(self.contract.functions.setBid(tokenId, bid), **kwargs)
    
    # Updates the metadata URI for specified token id
    def update_token_metadata_URI(self, tokenId, metadataURI, **kwargs):
        return self.send_transaction(self.contract.functions.updateTokenMetadataURI(tokenId, metadataURI), **kwargs)
            
    # Updates the token URI for the specified token id
    def update_token_URI(self, tokenId, tokenURILocal, **kwargs):
        return self.send_transaction(self.contract.functions.updateTokenURI(tokenId, tokenURILocal), **kwargs)

    def set_approval_for_all(self, operator: str, approved: bool):
        return self.send_transaction(self.contract.functions.setApprovalForAll(operator, approved))



    # def revokeTransferOwnership(self):
    #     return self.contract.functions.revokeTransferOwnership()
            
    def safeTransferFrom(self, _from, _to, tokenId):
        return self.contract.functions.safeTransferFrom(_from, _to, tokenId)
            
    def safeTransferFrom(self, _from, _to, tokenId, _data):
        return self.contract.functions.safeTransferFrom(_from, _to, tokenId, _data)

    def transferFrom(self, _from, _to, tokenId):
        return self.contract.functions.transferFrom(_from, _to, tokenId)
            
    def marketContract(self):
        return self.contract.functions.marketContract()

            
    



    # ================================================================
    #                     HELPER FUNCTIONS
    # ================================================================

    ## Helper function that builds a dict representing IMedia.MediaData
    def make_media_data(self, tokenURI, metadataURI, contentHash, metadataHash):
        return {
            "tokenURI": tokenURI,
            "metadataURI": metadataURI,
            "contentHash": contentHash,
            "metadataHash": metadataHash
        }

    ## Helper function that build a dict representing IMarket.BidShares
    def make_bid_shares(self, creator, owner, collaborators, collabShares):
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
    def make_ask(self, amount, currency):
        return {
            "amount": amount,
            "currency": currency
        }

    ## Helper function that builds a dict representing IMarket.Bid
    def make_bid(self, amount, currency, bidder, recipient, sellOnShare):
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
                "chainId": int(self.chainId),
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
    def get_permit_signature(self, spender, token_id, deadline):
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
                "chainId": int(self.chainId),
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