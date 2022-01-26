from ..base_contract import BaseContract

class MediaFactory(BaseContract):
    def __init__(self, signer_or_wallet: any, chainId: str = '31337'):
        super().__init__(signer_or_wallet, chainId)

        self.connect_to_contract("MediaFactory")

    def hello(self):
        print("hello")
