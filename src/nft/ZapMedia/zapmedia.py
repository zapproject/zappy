from base_contract import BaseContract

class ZapMedia(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId) 
        try:
            self.connect_to_contract("ZapMedia")            
        except Exception as e:
            print(e)
        