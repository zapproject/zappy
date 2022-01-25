from src.nft.base_contract import BaseContract

class ZapMedia(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId)

        self.connect_to_contract("ZapMedia")

    def hello(self):
        print("hello")
