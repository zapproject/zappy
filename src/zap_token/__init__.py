from asyncio import sleep

from base_contract import BaseContract
from zaptypes import (
    address, txid, NetworkProviderOptions,
    TransactionCallback, const
)


class ZapToken(BaseContract):
    """docstring for ZapToken"""

    def __init__(self, options: NetworkProviderOptions = None):
        options["artifact_name"] = "ZAP_TOKEN"
        BaseContract.__init__(self, **options)

    async def balance_of(self, address: address) -> int:

        return self.contract.functions.balanceOf(address).call()

    async def send(self, to: address, amount: int, From: address,
                   gas_price: int,
                   gas: int = const.DEFAULT_GAS,
                   cb: TransactionCallback = None,
                   node=None) -> txid:
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
