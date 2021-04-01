from pytest import mark, fixture

from web3 import Web3

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from zap_token.curve import Curve
from artifacts.src import Artifacts
from zaptypes import const


class TestBondage:
    """docstring for TestBondage"""

    global tx_payload, tx_del_payload
    tx_payload = {}
    tx_del_payload = {}

    global required
    required = 0

    def test_init(self, instance, bond_contract, subscriber,
                  oracle, provider, w3):

        global tx_payload

        assert instance
        assert instance.contract.address == bond_contract.address

        tx_payload = {"provider": oracle, "endpoint": provider["endpoint"],
                      "From": subscriber, "gas_price": w3.eth.gas_price}

    @fixture(scope="class", autouse=True)
    def prepare_tokens(self, instance, zt_contract,
                       subscriber, owner, broker, w3):
        bondage_owner = instance.contract.address
        zt_contract.functions.allocate(
            owner, 1500000000000000000000000000000).transact(
            {"from": owner, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        zt_contract.functions.allocate(
            subscriber, 50000000000000000000000000000).transact(
            {"from": owner, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        zt_contract.functions.allocate(
            broker, 50000000000000000000000000000).transact(
            {"from": owner, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        zt_contract.functions.approve(
            bondage_owner, 1000000000000000000000000000000).transact(
            {"from": subscriber, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        zt_contract.functions.approve(
            bondage_owner, 1000000000000000000000000000000).transact(
            {"from": broker, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

    @mark.anyio
    async def test_bond(self, instance):

        print("\n\nTesting bond")
        tx_hash = await instance.bond(dots=999, **tx_payload)

        assert isinstance(tx_hash, str)
        print("✅ Passed\n")

        print("\nTesting get_bound_dots")
        bonded = await instance.get_bound_dots(
            tx_payload["From"], tx_payload["provider"],
            tx_payload["endpoint"])
        print("✅ Passed\n")

        print("\nConfirming dots were bonded")
        assert isinstance(bonded, int)
        assert bonded == 999

    @mark.anyio
    async def test_delegate_bond(self, instance, escrower):

        print("\n\nTesting delegate_bond")
        tx_hash = await instance.delegate_bond(
            subscriber=escrower, dots=999, **tx_payload)

        assert isinstance(tx_hash, str)
        print("✅ Passed\n")

        print("\nConfirming dots were bonded")
        bonded = await instance.get_bound_dots(
            escrower, tx_payload["provider"],
            tx_payload["endpoint"])

        assert isinstance(bonded, int)
        assert bonded == 999

    @mark.anyio
    async def test_calc_zap_for_dots(self, instance):
        global required
        required = await\
            instance.calc_zap_for_dots(
                tx_payload["provider"],
                tx_payload["endpoint"],
                5)

        assert isinstance(required, int)
        assert required > 0

    @mark.anyio
    async def test_current_cost_of_dot(self, instance):
        cost = await\
            instance.current_cost_of_dot(
                tx_payload["provider"],
                tx_payload["endpoint"],
                5)

        assert isinstance(cost, int)
        assert cost > 0

    @mark.anyio
    async def test_get_dots_limits(self, instance):
        limit = await\
            instance.get_dots_limits(
                tx_payload["provider"],
                tx_payload["endpoint"])

        assert isinstance(limit, int)
        assert limit > 0

    @mark.anyio
    async def test_get_dots_issued(self, instance, escrower):
        issued = await\
            instance.get_dots_issued(
                tx_payload["provider"],
                tx_payload["endpoint"])

        bonded = await instance.get_bound_dots(
            tx_payload["From"], tx_payload["provider"],
            tx_payload["endpoint"])

        bonded_del = await instance.get_bound_dots(
            escrower, tx_payload["provider"],
            tx_payload["endpoint"])

        print("\n\nTesting get_bound_dots")
        assert isinstance(issued, int)
        assert issued > 0
        print("✅ Passed\n")
        print("\nConfirming dots issued == total bonded")
        assert issued == bonded + bonded_del
        print("Dots issued: ", issued)

    @mark.anyio
    async def test_get_zap_bound(self, instance):
        zap_bonded = await\
            instance.get_zap_bound(
                tx_payload["provider"],
                tx_payload["endpoint"])

        assert isinstance(zap_bonded, int)
        print("Num of Zap bonded", zap_bonded)
        assert zap_bonded > 0

    @mark.anyio
    async def test_get_num_escrow(self, instance, escrower):

        escrowed = await\
            instance.get_num_escrow(
                tx_payload["provider"],
                escrower,
                tx_payload["endpoint"])

        assert isinstance(escrowed, int)
        print("Num Escrowed: ", escrowed)

        bonded = await instance.get_bound_dots(
            tx_payload["From"], tx_payload["provider"],
            tx_payload["endpoint"])

        bonded_del = await instance.get_bound_dots(
            escrower, tx_payload["provider"],
            tx_payload["endpoint"])

        print("# of bonded dots: ", bonded)
        print("# of bonded dots delegated: ", bonded_del)

        print("\nTesting unbond")
        await instance.unbond(dots=bonded, **tx_payload)
        tx_payload["From"] = escrower
        await instance.unbond(dots=bonded_del, **tx_payload)
