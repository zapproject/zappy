from web3 import Web3
import asyncio

import src.artifacts.src.index as index
import src.base_contract.utils as utils


class BaseContract:
    provider: any
    web3: any
    contract: any
    network_id: int
    coordinator: any
    artifact: any
    name: str
    address: str or None

    def __init__(self,
                 artifact_name: str,
                 web3: any = None,
                 network_id: int = 1,
                 network_provider: any = None,
                 artifacts_dir: str = None,
                 coordinator: str = None,
                 address: str = None
                 ):
        try:
            if artifacts_dir is None:
                self.artifact = index.Artifacts[artifact_name]
                self.coor_artifact = index.Artifacts['ZAPCOORDINATOR']
            else:
                artifacts: any = utils.Utils.get_artifacts(artifacts_dir)
                self.artifact = utils.Utils.open_artifact_in_dir(artifacts[artifact_name])
                self.coor_artifact = utils.Utils.open_artifact_in_dir(artifacts['ZAPCOORDINATOR'])

            self.name = artifact_name
            self.provider = web3 or Web3(network_provider or Web3.HTTPProvider("https://cloudflare-eth.com"))
            self.w3 = web3 or Web3(network_provider or Web3.HTTPProvider("https://cloudflare-eth.com"))
            self.network_id = network_id or 1
            self.address = address or self.artifact['networks'][str(self.network_id)]['address']

            if coordinator is not None:
                self.coordinator = self.w3.eth.contract(address=self.w3.toChecksumAddress(coordinator),
                                                        abi=self.coor_artifact['abi'])

                contract_address = self.get_contract()
                self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(contract_address),
                                                     abi=self.artifact['abi'])

            else:
                self.coor_address = self.coor_artifact['networks'][str(self.network_id)]['address']
                self.coordinator = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.coor_address),
                                                        abi=self.coor_artifact['abi'])

                self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.address),
                                                     abi=self.artifact['abi'])

        except Exception as e:
            raise e

    async def _get_contract(self) -> str:
        """
        This async function fetches the contract address from the coordinator abi. Thereafter, the function returns the
        address where it is assigned to the address kwarg in the contract instance.

        :return: the contract address of the coordinator.
        """
        await asyncio.sleep(.5)
        contract_address = self.coordinator.functions.getContract(self.name).call()
        return contract_address

    async def _get_contract_owner(self) -> str:
        """
        This async function fetches the owner of the contract instance.

        :return: the contract owner's address.
        """
        await asyncio.sleep(.5)
        contract_owner = self.contract.functions.owner().call()
        return contract_owner

    def get_contract(self) -> str:
        """
        A synchronous function that wraps the asynchronous _get_contract method. This function returns the contract
        address fetched from the asynchronous _get_contract function.

        :return: the contract address.
        """
        task = self._get_contract()
        contract_address = asyncio.run(task)
        return contract_address

    def get_contract_owner(self) -> str:
        """
        A synchronous function that wraps the asynchronous _get_contract_owner method. This function returns the
        contract owner's address.

        :return: the contract owner's address.
        """
        task = self._get_contract_owner()
        owner = asyncio.run(task)
        return owner
