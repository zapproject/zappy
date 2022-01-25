from base_contract import BaseContract

class ZapMedia(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)

        try:
            self.connect_to_contract("ZapMedia")            
        except Exception:
            print(Exception)

    
    def hello(self):
        print(f"hello, {'World'}")

    def call_function(self, function_name:str):
        func = self.contract.get_function_by_name(function_name)
        return func().call()


params = ['31337']
# connecting to Zap Media PROXY instance
zap_media = ZapMedia(*params)
print(zap_media.chainId)
print(zap_media.address)
print(zap_media.w3)
# print(zap_media.connect_to_contract())
print(dir(zap_media.contract.functions))
print(zap_media.contract.functions.getOwner().call())
print(zap_media.call_function("getOwner"))

nonce = zap_media.w3.eth.getTransactionCount("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")

private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

tx = zap_media.contract.functions.mint(
        {
            "tokenURI": "token-uri",
            "metadataURI": "metadata-uri",
            "contentHash": b'1',
            "metadataHash": b'2',
        },
        {
            "creator": {"value": 95000000000000000000},
            "owner": {"value": 0},
            "collaborators": [],
            "collabShares": []
        }
    ).buildTransaction({
        'chainId': 31337,
        'gas': 1400000,
        'gasPrice': zap_media.w3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

signed_txn = zap_media.w3.eth.account.signTransaction(tx, private_key)

result = zap_media.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

tx_receipt = zap_media.w3.eth.getTransactionReceipt(result)
print(tx_receipt)