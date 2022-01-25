from base_contract import BaseContract


class ZapMedia(BaseContract):

    def __init__(self, signer_or_wallet, chainId):
        super().__init__(signer_or_wallet, chainId)

        try:
            # artifact = self.get_contract_info("ZapMedia")
            # self.address = artifact[self.chainId]["address"]
            # self.abi = artifact["abi"]
            self.connect_to_contract("ZapMedia")            
        except Exception:
            print(Exception)

    
    def hello(self):
        print("hello")

params = ["signer", '31337']
zap_media = ZapMedia(*params)
print(zap_media.chainId)
print(zap_media.address)
print(zap_media.w3)
# print(zap_media.connect_to_contract())
print(dir(zap_media.contract.functions))
print(zap_media.contract.functions.getOwner().call())
