from asyncio import sleep

from base_contract import BaseContract
from zaptypes import (
    address, txid, NetworkProviderOptions,
    TransactionCallback, const
)


class ZapToken(BaseContract):
    """
    Represents an interface to the Zap Token ERC20 contract.
    
    Enables token transfers, balance lookups, and approvals.

    :param arifactsDir: Directory where contract ABIs are located

    :param networkId:
        Select which network the contract is located
        options - (mainnet, testnet, private)

    :param networkProvider:
        Ethereum network provider (e.g. Infura or web3)
    """

    def __init__(self, options: NetworkProviderOptions = None):
        options["artifact_name"] = "ZAP_TOKEN"
        BaseContract.__init__(self, **options)

    async def balance_of(self, address: address) -> int:
        """
            Get the Zap Token balance of a given address.

            :param {address} address  Address to check

            :returns {Promise<number>} Returns a Promise that will eventually resolve into a Zap balance (wei)
        """

        return self.contract.functions.balanceOf(address).call()

    async def send(self, to: address, amount: int, From: address,
                   gas_price: int,
                   gas: int = const.DEFAULT_GAS,
                   cb: TransactionCallback = None,
                   node=None) -> txid:
        """
            Transfers Zap from an address to another address.

            :param to: Address of the recipient

            :param amount: Amount of Zap to transfer (wei)

            :param from: Address of the sender

            :param gas: Sets the gas limit for this transaction (optional)

            :param cb: Callback for transactionHash event

            :returns a Coroutine that will eventually resolve into a transaction hash
        """
        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}
        try:

            tx_hash = self.contract.functions.transfer(
                to, amount).transact(tx_meta)

            if cb and node:
                receipt = node.getTransactionReceipt(tx_hash)
                logs = self.contract.events.Transfer(
                ).processReceipt(receipt)[0]

                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash.hex()
        except Exception as e:
            raise e

    async def allocate(self, to, amount: int,
                       gas_price: int,
                       gas: int = const.DEFAULT_GAS):
        """
            Allocates Zap Token from the Zap contract owner to an address (ownerOnly).

            :param to: Address of the recipient

            :param amount: Amount of Zap to allocate (wei)

            :param from: Address of the sender (must be owner of the Zap contract)

            :param gas: Sets the gas limit for this transaction (optional)

            :param cb: Callback for transactionHash event

            :returns a Coroutine that will eventually resolve into a transaction hash
        """

        tx_meta = {"gas": gas, "gasPrice": gas_price}
        try:

            tx_hash = self.contract.functions.allocate(
                to, amount).transact(tx_meta)

            return tx_hash.hex()
        except Exception as e:
            raise e

    async def approve(self, to: address, amount: int,
                      From: address, gas_price: int,
                      gas: int = const.DEFAULT_GAS,
                      cb: TransactionCallback = None,
                      node=None) -> txid:
        """
            Approves the transfer of Zap Token from a holder to another account.
            Enables the bondage contract to transfer Zap during the bondage process.

            :param to: Address of the recipient

            :param amount: Amount of Zap to approve (wei)

            :param from: Address of the sender

            :param gas: Sets the gas limit for this transaction (optional)

            :param cb: Callback for transactionHash event

            :returns a Coroutine that will eventually resolve into a transaction hash
        """

        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}
        try:

            tx_hash = self.contract.functions.approve(
                to, amount).transact(tx_meta)

            if cb and node:
                receipt = node.getTransactionReceipt(tx_hash)
                logs = self.contract.events.Approval(
                ).processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash.hex()
        except Exception as e:
            raise e

    async def transfer_from(self, to: address, From: address, amount: int,
                            gas_price: int,
                            gas: int = const.DEFAULT_GAS,
                            cb: TransactionCallback = None,
                            node=None) -> txid:

        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}
        try:

            tx_hash = self.contract.functions.transferFrom(
                From, to, amount).transact(tx_meta)

            if cb and node:
                receipt = node.getTransactionReceipt(tx_hash)
                logs = self.contract.events.Transfer(
                ).processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash.hex()
        except Exception as e:
            raise e

    async def allowance(self, owner: address, spender: address) -> int:

        return\
            self.contract.functions.allowance(owner, spender).call()

    async def finish_minting(self, cb: TransactionCallback = None,
                             node=None):
        try:
            tx_hash = self.contract.functions.finishMinting().transact()

            if cb and node:
                receipt = node.eth.getTransactionReceipt(tx_hash)
                logs = self.contract.events.MintFinished(
                ).processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])
            return tx_hash.hex()
        except Exception as e:
            print(e)

    async def increase_approval(self, spender: address, added_value: int,
                                From: str, gas_price: int,
                                gas: int = const.DEFAULT_GAS,
                                cb: TransactionCallback = None,
                                node=None) -> txid:

        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}
        try:

            tx_hash = self.contract.functions.increaseApproval(
                spender, added_value).transact(tx_meta)

            if cb and node:
                receipt = node.getTransactionReceipt(tx_hash)
                logs = self.contract.events.Approval(
                ).processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash.hex()
        except Exception as e:
            raise e

    async def decrease_approval(self, spender: address, subtracted_value: int,
                                From: str, gas_price: int,
                                gas: int = const.DEFAULT_GAS,
                                cb: TransactionCallback = None,
                                node=None) -> txid:

        tx_meta = {"from": From, "gas": gas, "gasPrice": gas_price}
        try:

            tx_hash = self.contract.functions.decreaseApproval(
                spender, subtracted_value).transact(tx_meta)

            if cb and node:
                receipt = node.getTransactionReceipt(tx_hash)
                logs = self.contract.events.Approval(
                ).processReceipt(receipt)[0]
                if "error" in logs:
                    cb(logs["error"])
                cb(None, logs["args"]["transactionHash"])

            return tx_hash.hex()
        except Exception as e:
            raise e
