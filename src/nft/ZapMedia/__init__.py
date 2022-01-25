from base_contract import BaseContract

class ZapMedia(BaseContract):

    def __init__(self, signer_or_wallet, chainId):
        super().__init__(signer_or_wallet, chainId)

        self.connect_to_contract("ZapMedia")

    def hello(self):
        print("hello")
