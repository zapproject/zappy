import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

from typing import Any
from web3 import Web3
import asyncio

from src.BaseContract.utils import Utils
from src.Artifacts.src.index import Artifacts
#from portedFiles.types import base_contract_type


class BaseContract:

    provider: Any
    web3: Any
    contract: Any
    network_id: int
    coordinator: Any
    artifact: Any
    name: str
    address: str = None

    """
    @param {string | null} b.artifacts_dir - Directory where contract ABIs are located
    @param {string} b.artifact_name - Contract name for this contract object
    @param {number | null} b.networkId - Select which network the contract is located on (mainnet, testnet, private)
    @param {any | null} b.network_Provider - Ethereum network provider (e.g. Infura)
    """

    def __init__(self,
                 artifact_name: str,
                 web3: Any = None,
                 network_id: int = 1,
                 network_provider: Any = None,
                 artifacts_dir: str = None,
                 coordinator: str = None,
                 contract: Any = None,
                 address: str = None
                 ):

        self.name = artifact_name
        self.loop = asyncio.get_event_loop()
        try:

            if artifacts_dir is None:
                self.artifact = Artifacts[artifact_name]
                self.coor_artifact = Artifacts['ZAPCOORDINATOR']
            else:
                artifacts: any = Utils.get_artifacts(artifacts_dir)
                self.artifact = Utils.open_artifact_in_dir(
                    artifacts[artifact_name])
                self.coor_artifact = Utils.open_artifact_in_dir(
                    artifacts['ZAPCOORDINATOR'])

            self.provider = web3 or Web3(
                network_provider or Web3.HTTPProvider("https://cloudflare-eth.com"))
            self.w3 = web3 or Web3(network_provider or Web3.HTTPProvider(
                "https://cloudflare-eth.com"))

            """
            #
            #   The added 'self.w3' above looks redundant; however, 'self.provider' was not recognized as a web3 provider. 
            #   Maybe delete provider?
            #
            """

            self.network_id = network_id or 1

            if coordinator is not None:
                checksum_coor_address = self.w3.toChecksumAddress(coordinator)
            else:
                checksum_coor_address = \
                    self.w3.toChecksumAddress(
                        self.coor_artifact['networks'][str(self.network_id)]['address'])

            self.coordinator = self.w3.eth.contract(
                address=checksum_coor_address, abi=self.coor_artifact['abi'])

            if address is not None:
                self.address = address
            else:
                self.address = self.artifact['networks'][str(
                    self.network_id)]['address']

            self.contract = None

            if coordinator is not None:
                """
                #   The get_contract function won't run without proper abi
                """
                asyncio.run(self.get_contract())
            else:
                self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.address),
                                                     abi=self.artifact['abi'])

        except Exception as e:
            raise e

    # Async class methods
    async def get_contract(self):
        contract_address = await self.coordinator.functions.getContract(self.name.upper()).call()
        self.contract = self.w3.eth.contract(
            address=contract_address, abi=self.artifact['abi'])
        return contract_address

    def get_contract_owner(self):
        return self.loop.run_until_complete(self.__async__get_contract_owner())

    async def __async__get_contract_owner(self):
        contract_owner = await self.contract.functions.owner().call()
        return contract_owner