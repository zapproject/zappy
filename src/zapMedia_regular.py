from base_contract import BaseContract

class ZapMedia(BaseContract):

    def __init__(self, signer_or_wallet, chainId):
        super().__init__(signer_or_wallet, chainId)

        try:
            self.connect_to_contract("ZapMedia")            
        except Exception:
            print(Exception)

    
    def hello(self):
        print(f"hello, {'World'}")

    def call_function(self, function_name:str):
        func = self.contract.get_function_by_name(function_name)
        return func().call()


params = ["signer", '31337']

# connecting to Zap Media PROXY instance
zap_media = ZapMedia(*params)
print(zap_media.chainId)
print(zap_media.address)
print(zap_media.w3)
# print(zap_media.connect_to_contract())
print(dir(zap_media.contract.functions))
print(zap_media.contract.functions.getOwner().call())
print(zap_media.call_function("getOwner"))