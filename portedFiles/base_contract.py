import asyncio

class BaseContract:
    def __init__(self, artifactsDir, artifactName, networkId, networkProvider, coordinator, address, web3):
       self.name = artifactName
       try:
            if not artifactsDir:
               self.artifact = artifacts[artifactName]
               coorArtifact = artifacts['ZAPCOORDINATOR']
            else:
                artifacts = Utils.getArtifacts(artifactsDir)
                self.artifact = artifacts[artifactName]
                coorArtifact = artifacts['ZAPCOORDINATOR'] 
            self.provider = web3 or Web3(networkProvider or Web3.providers.HttpProvider("https://cloudflare-eth.com"))
            self.networkId = networkId or 1
            self.coordinator = self.provider.eth.Contract(coorArtifact.abi, coordinator or coorArtifact.networks[self.networkId].address)
            self.contract = None
            if address:
                self.address = address
            else:
                self.address = self.artifact.networks[self.networkId].address
            if coordinator:
                self.getContract() 
                #Question: Missing the cathc promise from the JS code
            else:
                self.contract = self.provider.eth.Contract(self.artifact.abi, self.address)
       except Exception as e:
           raise e
    
    async def getContract(self):
        contractAddress = self.coordinator.getContract(self.name.upper())
        await asyncio.sleep(2)
        self.contract = self.provider.eth.Contract(self.artifact.abi, contractAddress)
        return contractAddress
    
    async def getContractOwner(self):
        contractOwner = self.contract.owner()
        await asyncio.sleep(2)
        return contractOwner
