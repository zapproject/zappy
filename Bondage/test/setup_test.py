from web3._utils import (utf8ToHex, to toWei, toHex)
#Missing Utils package
from portedFiles.types import Constants

async def bootstrap(zapProvider, accounts, deployedRegistry, deployedBondage, deployedToken):
    #Most of this code depends on Utils
    defaultTx = [accounts[0], 200000]
    tokenOwner = await deployedToken.contract.owner()
    #NOT DONE
