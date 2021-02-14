import utils
from web3 import Web3

class BaseContract:
    def __init__(self, artifact_name, network_id, network_provider, coordinator, address, web3):
        self.name = artifact_name
        try:
            self.artifact = artifact_name
            self.network_id = network_id or '1'
            coor_artifact_abi = utils.load_abi('ZapCoordinator')
            coor_artifact_address = utils.load_address('ZapCoordinator', self.network_id)
            self.provider = web3 or Web3(network_provider) or Web3(Web3.HTTPProvider('https://cloudflare-eth.com'))
            self.coordinator = self.provider.eth.Contract(coor_artifact_abi, coordinator or coor_artifact_address)
            self.contract = None
            if address:
                self.address = address
            else:
                self.address = self.artifact.networks[self.network_id].address
                if coordinator:
                    self.coordinator.getContract()
                else:
                    self.coordinator = self.provider.eth.Contract(self.artifact.abi, self.address)
        except Exception as e:
            raise e