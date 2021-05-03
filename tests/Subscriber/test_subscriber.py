from unittest.mock import AsyncMock
from pytest import mark, fixture

from web3 import Web3
from . import encode_params

from os.path import join, realpath
from sys import path
path.insert(0, realpath(join(__file__, "../../../src/")))

from zaptypes import const


""" pytest section
"""

class TestSubscriber:

    query_id = ""

    global tx_meta
    tx_meta = ""

    def test_init(self, instance):
        assert instance

    """ contract patching
    """

    @fixture(scope="class", autouse=True)
    def patch_contracts(self, instance, contracts, oracle):
        instance.zap_registry.contract = contracts["registry"]
        instance.zap_token.contract = contracts["zap_token"]
        instance.zap_bondage.contract = contracts["bondage"]
        instance.zap_dispatch.contract = contracts["dispatch"]

    @fixture(scope="class", autouse=True)
    def patch_all_contract_functions(self, instance, subscriber, w3):
        """ Patches all contract functions before tests
        """

        global tx_meta

        tx_meta = {"From": instance.subscriber_owner,
                   "gas_price": w3.eth.gas_price}

        """ ZapToken Functions
        """

        # ZapToken.balance_of
        def side_effect(acc):
            return\
                instance.zap_token.contract.functions.balanceOf(
                    acc).call()

        instance.zap_token.balance_of = AsyncMock()
        instance.zap_token.balance_of.side_effect = side_effect

        """ Bondage Function
        """

        # Bondage.calc_zap_for_dots
        def side_effect(prov, ep, dots):
            return instance.zap_bondage.contract.functions.calcZapForDots(
                prov, Web3.toBytes(text=ep), dots).call()

        instance.zap_bondage.calc_zap_for_dots = AsyncMock()
        instance.zap_bondage.calc_zap_for_dots.side_effect = side_effect

        # Bondage.get_bound_dots
        def side_effect(sub, prov, ep):
            return instance.zap_bondage.contract.functions.getBoundDots(
                sub, prov, Web3.toBytes(text=ep)).call()

        instance.zap_bondage.get_bound_dots = AsyncMock()
        instance.zap_bondage.get_bound_dots.side_effect = side_effect

        # Bondage.bond
        def side_effect(prov, ep, dts, From, gas_price, gas, cb=None):
            return instance.zap_bondage.contract.functions.bond(
                prov, Web3.toBytes(text=ep), int(dts)).transact(
                {"from": subscriber, "gas": const.DEFAULT_GAS,
                 "gasPrice": w3.eth.gas_price})

        instance.zap_bondage.bond = AsyncMock()
        instance.zap_bondage.bond.side_effect = side_effect

        # Bondage.unbond
        def side_effect(prov, ep, dts, From, gas_price, gas, cb=None):
            return instance.zap_bondage.contract.functions.unbond(
                prov, Web3.toBytes(text=ep), int(dts)).transact(
                {"from": subscriber, "gas": const.DEFAULT_GAS,
                 "gasPrice": w3.eth.gas_price})

        instance.zap_bondage.unbond = AsyncMock()
        instance.zap_bondage.unbond.side_effect = side_effect

    @fixture(scope="class", autouse=True)
    def prepare_tokens(self, instance,
                       subscriber, owner, broker, w3):
        bondage_owner = instance.zap_bondage.contract.address
        instance.zap_token.contract.functions.allocate(
            owner, 1500000000000000000000000000000).transact(
            {"from": owner, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})
        instance.zap_token.contract.functions.allocate(
            subscriber, 50000000000000000000000000000).transact(
            {"from": owner, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        instance.zap_token.contract.functions.allocate(
            broker, 50000000000000000000000000000).transact(
            {"from": owner, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        instance.zap_token.contract.functions.approve(
            bondage_owner, 1000000000000000000000000000000).transact(
            {"from": subscriber, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})

        instance.zap_token.contract.functions.approve(
            bondage_owner, 1000000000000000000000000000000).transact(
            {"from": broker, "gas": const.DEFAULT_GAS,
             "gasPrice": w3.eth.gas_price})


    @mark.anyio
    async def test_get_zap_balance(self, instance):

        balance = await instance.get_zap_balance()

        assert isinstance(balance, int)
        print("Subscriber Balance: ", balance)

    @mark.anyio
    async def test_get_zap_allowance(self, instance, contracts):
        allowance = await instance.get_zap_allowance()

        assert isinstance(allowance, int)
        print("Subscriber allowance: ", allowance)

    @mark.skip("Already approving on SetUp")
    @mark.anyio
    async def test_approve_to_bond(self, instance, oracle,
                                   w3, provider):
        def side_effect(to, amount):
            tx_hash = instance.zap_token.contract.functions.approve(
                to, amount).transact().hex()
            receipt = w3.eth.getTransactionReceipt(tx_hash)
            log = instance.zap_token.contract.events.Approval(
            ).processReceipt(receipt)
            try:
                return not log[0]["errors"]
            except KeyError:
                return True

        instance.zap_token.approve = AsyncMock()
        instance.zap_token.approve.side_effect = side_effect

        approve = await\
            instance.approve_to_bond(1000000000)

        assert approve

    @mark.anyio
    async def test_bond(self, instance, provider,
                        subscriber, oracle, broker):

        await\
            instance.bond(
                oracle,
                provider["endpoint"],
                999, **tx_meta)

        bonded = await instance.zap_bondage.get_bound_dots(
            subscriber,
            oracle,
            provider["endpoint"])

        assert bonded
        assert bonded == 999

        await\
            instance.unbond(
                oracle,
                provider["endpoint"],
                999, **tx_meta)

    @mark.anyio
    async def test_subscribe(self, instance, oracle, provider,
                             subscriber, contracts, w3):

        def side_effect(prov):
            return\
                instance.zap_registry.contract.functions.getProviderPublicKey(
                    prov).call()

        instance.zap_registry.get_provider_publickey = AsyncMock()
        instance.zap_registry.get_provider_publickey.side_effect =\
            side_effect

        instance.zap_arbiter.contract = contracts["arbiter"]

        def side_effect(provider, endpoint,
                        endpoint_params, pubkey,
                        blocks, From, gas_price, gas, cb):
            endpoint_params =\
                [Web3.toBytes(text=param)
                 if not isinstance(param, bytes)
                 else param
                 for param in endpoint_params]
            return\
                instance.zap_arbiter.contract.functions.initiateSubscription(
                    provider, Web3.toBytes(text=endpoint),
                    endpoint_params, pubkey, blocks).transact(
                    {"from": subscriber, "gas": const.DEFAULT_GAS,
                     "gasPrice": w3.eth.gas_price}).hex()

        instance.zap_arbiter.initiate_subscription = AsyncMock()
        instance.zap_arbiter.initiate_subscription.side_effect =\
            side_effect

        bounded = await instance.zap_bondage.get_bound_dots(
            subscriber, oracle, provider["endpoint"])

        if bounded == 0:
            await instance.bond(
                oracle,
                provider["endpoint"],
                100, **tx_meta)

        sub = await instance.subscribe(oracle, provider["endpoint"],
                                       provider["endpoint_params"], 100,
                                       **tx_meta)
        assert isinstance(sub, str)
        assert sub

    @mark.anyio
    async def test_query_data(self, instance, w3,
                              oracle, provider, subscriber):

        global query_id

        def side_effect(prov, q, ep, ep_params, From, gas_price, gas, cb=None):
            return\
                instance.zap_dispatch.contract.functions.query(
                    prov, q, Web3.toBytes(text=ep), ep_params).transact(
                    {"from": subscriber, "gas": const.DEFAULT_GAS,
                     "gasPrice": w3.eth.gas_price})

        instance.zap_dispatch.query_data = AsyncMock()
        instance.zap_dispatch.query_data.side_effect = side_effect

        params = encode_params.encode_params(provider["endpoint_params"])

        bounded = await instance.zap_bondage.get_bound_dots(
            subscriber, oracle, provider["endpoint"])

        if bounded < 999:
            await instance.bond(
                oracle,
                provider["endpoint"],
                999,
                **tx_meta)

        query = await instance.query_data(
            oracle, "query", provider["endpoint"],
            params,
            **tx_meta)

        assert query

        receipt = w3.eth.getTransactionReceipt(query)
        query_id = instance.zap_dispatch.contract.events.Incoming(
        ).processReceipt(
            receipt)[0]["args"]["id"]

    @mark.anyio
    async def test_cancel_query(self, instance, w3, subscriber):

        def side_effect(q_id, From, gas_price, gas, cb):
            return\
                instance.zap_dispatch.contract.functions.cancelQuery(
                    int(q_id)).transact(
                    {"from": subscriber, "gas": const.DEFAULT_GAS,
                     "gasPrice": w3.eth.gas_price})

        instance.zap_dispatch.cancel_query = AsyncMock()
        instance.zap_dispatch.cancel_query.side_effect =\
            side_effect

        await instance.cancel_query(query_id, **tx_meta)

    @mark.anyio
    async def test_delegate_bond(self, instance, w3,
                                 provider, oracle, subscriber):

        def side_effect(sub, ep, dots, prov, From, gas_price, gas, cb=None):
            return\
                instance.zap_bondage.contract.functions.delegateBond(
                    sub, prov, Web3.toBytes(text=ep), dots).transact(
                    {"from": subscriber, "gas": const.DEFAULT_GAS,
                     "gasPrice": w3.eth.gas_price})

        instance.zap_bondage.delegate_bond = AsyncMock()
        instance.zap_bondage.delegate_bond.side_effect =\
            side_effect

        del_bounded = await instance.delegate_bond(
            oracle, instance.zap_bondage.contract.address,
            provider["endpoint"], 1, **tx_meta)

        instance.zap_bondage.functions.unbond

        assert del_bounded
        assert isinstance(del_bounded, int)
        assert del_bounded > 0

        tx_meta2 = tx_meta
        tx_meta2["From"] = instance.zap_bondage.contract.address
        instance.unbond(
            oracle, provider["endpoint"], 1, **tx_meta2)

    @mark.anyio
    async def test_get_num_escrow(self, instance, provider, oracle):

        def side_effect(provider, subscriber, endpoint):
            return\
                instance.zap_bondage.contract.functions.getNumEscrow(
                    provider, subscriber, Web3.toBytes(text=endpoint)).call()

        instance.zap_bondage.get_num_escrow = AsyncMock()
        instance.zap_bondage.get_num_escrow.side_effect =\
            side_effect

        escrowed = await instance.get_num_escrow(
            oracle, provider["endpoint"])

        assert isinstance(escrowed, int)
