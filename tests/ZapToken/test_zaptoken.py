from pytest import mark
from pprint import pprint


class Test_ZapToken:
    """
    Tests the ZapToken port.

    Tests the following ZapToken Methods:
        - increase_approval
        - allocate
        - allowance
        - balance_of
        - decrease_approval
        - transfer
        - transfer_from
        - finish_minting

    finish_minting can be tested once per test environment deployment.
    """

    @mark.anyio
    async def test_init(self, instance, w3):
        print("\n\nTesting ZapToken object __init__")
        assert instance

    @mark.anyio
    async def test_increase_approval(self, instance, w3, provider_2):
        tx_meta = {"From": provider_2["address"],
                   "gas_price": w3.eth.gas_price}

        tx_hash = await instance.increase_approval(
            provider_2["address"],
            1000, **tx_meta)
        assert tx_hash

        receipt = w3.eth.getTransactionReceipt(tx_hash)
        logs = instance.contract.events.Approval(
        ).processReceipt(receipt)[0]

        assert "error" not in logs

        print("\nTx Logs")
        pprint(dict(logs))

    # @mark.skip
    @mark.anyio
    async def test_allocate(self, instance, provider_1, w3):
        tx_meta = {"gas_price": w3.eth.gas_price}

        tx_hash = await instance.allocate(
            provider_1["address"], 100, **tx_meta)
        assert tx_hash

    @mark.anyio
    async def test_allowance(self, instance,
                             provider_1, provider_2,
                             w3):
        allowance = await instance.allowance(
            provider_1["address"],
            provider_2["address"])

        assert isinstance(allowance, int)

    @mark.anyio
    async def test_balance_of(self, instance, provider_2):
        balance = await instance.balance_of(
            provider_2["address"])

        assert balance
        print("Token Balance: ", balance)
        assert isinstance(balance, int)
        assert balance > 0

    @mark.anyio
    async def test_decrease_approval(self, instance, provider_2, w3):
        tx_meta = {"From": provider_2["address"],
                   "gas_price": w3.eth.gas_price}

        tx_hash = await instance.decrease_approval(
            provider_2["address"], 100, **tx_meta)
        assert(tx_hash)

        receipt = w3.eth.getTransactionReceipt(tx_hash)
        logs = instance.contract.events.Approval(
        ).processReceipt(receipt)[0]

        assert "error" not in logs

        print("\nTx Logs:")
        pprint(dict(logs))

    @mark.anyio
    async def test_transfer(self, instance, provider_2, w3):
        tx_meta = {"From": provider_2["address"],
                   "gas_price": w3.eth.gas_price}

        tx_hash = await instance.send(
            provider_2["address"],
            100, **tx_meta)
        assert tx_hash

        receipt = w3.eth.getTransactionReceipt(tx_hash)
        logs = instance.contract.events.Transfer(
        ).processReceipt(receipt)[0]

        assert "error" not in logs

        print("\nTx Logs:")
        pprint(dict(logs))

    @mark.anyio
    async def test_transfer_from(self, instance,
                                 provider_2, provider_1,
                                 w3):
        tx_meta = {"From": provider_2["address"],
                   "gas_price": w3.eth.gas_price}

        tx_hash = await instance.transfer_from(
            to=provider_2["address"],
            amount=20, **tx_meta)
        assert tx_hash

        receipt = w3.eth.getTransactionReceipt(tx_hash)
        logs = instance.contract.events.Transfer(
        ).processReceipt(receipt)[0]

        assert "error" not in logs

        print("\nTx Logs:")
        pprint(dict(logs))

    @mark.skip("Leave to last; no way to revert once contracts are deployed.")
    @mark.anyio
    async def test_finish_minting(self, instance, w3):
        print("\nTesting if ZapToken can stop minting")
        tx_hash = await instance.finish_minting()
        assert tx_hash

        receipt = w3.eth.getTransactionReceipt(tx_hash)
        logs = instance.contract.events.MintFinished(
        ).processReceipt(receipt)[0]

        assert "error" not in logs

        print("\nTx Logs:")
        pprint(dict(logs))
