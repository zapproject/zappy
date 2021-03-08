from web3 import Web3
from src.index import Artifacts
from utils import Utils
import asyncio


class BaseContract:
    provider: any
    web3: any
    contract: any
    network_id: int
    coordinator: any
    artifact: any
    name: str
    address: str = None

    def __init__(self,
                 artifact_name: str,
                 web3: any = None,
                 network_id: int = 1,
                 network_provider: any = None,
                 artifacts_dir: str = None,
                 coordinator: str = None,
                 contract: any = None,
                 address: str = None
                 ):
        try:
            if artifacts_dir is None:
                self.artifact = Artifacts[artifact_name]
                self.coor_artifact = Artifacts['ZAPCOORDINATOR']
            else:
                artifacts: any = Utils.get_artifacts(artifacts_dir)
                self.artifact = Utils.open_artifact_in_dir(artifacts[artifact_name])
                self.coor_artifact = Utils.open_artifact_in_dir(artifacts['ZAPCOORDINATOR'])

            self.name = artifact_name
            self.provider = web3 or Web3(network_provider or Web3.HTTPProvider("https://cloudflare-eth.com"))
            self.w3 = web3 or Web3(network_provider or Web3.HTTPProvider("https://cloudflare-eth.com"))
            self.network_id = network_id or 1
            self.address = address or self.artifact['networks'][str(self.network_id)]['address']

            if coordinator is not None:
                self.coordinator = self.w3.eth.contract(address=self.w3.toChecksumAddress(coordinator),
                                                        abi=self.coor_artifact['abi'])
                call_get_contract = self.get_contract()
                asyncio.run(call_get_contract)
            else:
                self.coor_address = self.coor_artifact['networks'][str(self.network_id)]['address']
                self.coordinator = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.coor_address),
                                                        abi=self.coor_artifact['abi'])
                self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.address),
                                                     abi=self.artifact['abi'])

            call_contract_owner = self.get_contract_owner()
            asyncio.run(call_contract_owner)

        except Exception as e:
            raise e

    async def get_contract(self) -> str:
        """
        This function fetches the contract address from coordinator and assigns the 'self.contract' contract object.
        :return: the contract address of the coordinator.
        """
        await asyncio.sleep(1)
        contract_address = self.coordinator.functions.getContract.address
        print('address is:' + contract_address)     #DELETE: For demo purposes!!!
        self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(contract_address),
                                             abi=self.artifact['abi'])
        return contract_address

    async def get_contract_owner(self) -> str:
        """
        This function fetches the owner of the contract instance.
        :return: the contract owner's address.
        """
        await asyncio.sleep(1)
        contract_owner = self.contract.functions.owner().call()
        print('owner is:' + contract_owner)     #DELETE: For demo purposes!!!
        return contract_owner
