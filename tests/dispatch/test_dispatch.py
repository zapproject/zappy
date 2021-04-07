import pytest

from web3 import Web3

from src.dispatch.dispatch import ZapDispatch
from src.types.types import const

"""ZapDispatch contract setup"""

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
options = {
    'web3': web3,
    'network_id': 31337
}
dispatch_wrapper = ZapDispatch(options)


class TestDispatch:

    def test_init(self, dispatch_contract, token_contract, bondage_contract, registry_contract, subscriber,
                  broker, oracle, provider, w3):
        """
        Testing the dispatch, bondage, registry, zap_token initializations.
        """
        assert dispatch_wrapper
        assert type(dispatch_wrapper.address) == str
        assert type(bondage_contract.address) == str
        assert type(registry_contract.address) == str
        assert type(token_contract.address) == str
        assert type(broker) == str
        assert broker == '0x90F79bf6EB2c4f870365E785982E1f101E93b906'

    def test_setup(self, oracle, broker, provider, subscriber, w3, accounts, bondage_contract,
                   registry_contract, token_contract, owner, dispatch_contract):
        """
        Running and testing all prerequisites to ensure the correct allocation and approval of Zap. Further, this
        function fetches the required Zap for dots from the Bondage contract, and finally, bonds the Zap for dots.
        """

        ep = 'endpoint'.encode('utf-8')

        for acct in accounts:
            allocate = token_contract.functions.allocate(acct, 1000).transact(
                {'from': owner, "gas": const.DEFAULT_GAS, "gasPrice": w3.eth.gas_price})
            assert allocate

        dots = 10
        required_zap = bondage_contract.functions.calcZapForDots(owner, ep, dots).call()
        assert type(required_zap) == int

        approve_zap = token_contract.functions.approve(bondage_contract.address, required_zap).transact(
            {'from': oracle, "gas": const.DEFAULT_GAS, "gasPrice": w3.eth.gas_price})
        assert approve_zap

        bonding = bondage_contract.functions.bond(owner, ep, dots).transact(
            {'from': subscriber, "gas": const.DEFAULT_GAS, "gasPrice": w3.eth.gas_price})
        assert bonding

    @pytest.mark.asyncio
    async def test_request_data(self, oracle, provider, subscriber, w3, dispatch_contract, query_config):
        """
        Testing the request_data function. It should return a string.
        """
        res = await dispatch_wrapper.query_data(**query_config)
        assert type(res) == str

        with pytest.raises(AssertionError):
            assert type(res) != str

    @pytest.mark.asyncio
    async def test_cancel_query_with_error(self, subscriber, w3, meta_config):
        """
        Testing the cancel function. Callback error should return a zero.
        """
        config = {
            'query_id': 5
        }

        res = await dispatch_wrapper.cancel_query(**config, **meta_config)
        assert type(res) == int
        assert res == 0

    @pytest.mark.asyncio
    async def test_cancel_query_without_error(self, subscriber, w3, dispatch_contract, oracle, provider,
                                              meta_config, query_config):
        """
        Testing the cancel_query function. First, the query_id is captured from invoking the query_data function. Then,
        the query_id is inserted as the id to cancel in the cancel_query function. It should return an integer of the
        block from whence it was cancelled.
        """

        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming(
        ).processReceipt(
            tx_receipt)[0]["args"]["id"]

        block_number = tx_receipt['blockNumber']
        assert query_id

        config_cancel = {
            'query_id': query_id,
        }
#
        res = await dispatch_wrapper.cancel_query(**config_cancel, **meta_config)
        assert type(res) == int
        assert res != 0
        assert res == block_number + 1


    @pytest.mark.asyncio
    @pytest.mark.parametrize('failing_params', [[], ['res1', 'res2', 'res3', 'res4', 'res5', 'res6']])
    async def test_respond_dynamic_false_should_fail(self, failing_params, subscriber, w3, meta_config,
                                                     dispatch_contract, query_config, oracle):
        """
        Testing the respond function. The response_params should cause the function to fail with a value error.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming(
        ).processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        config = {
            'query_id': query_id,
            'response_params': failing_params,
            'dynamic': False,
            'from_address': oracle,
            'gas': const.DEFAULT_GAS,
            'gas_price': w3.eth.gas_price
        }

        with pytest.raises(ValueError):
            response = await dispatch_wrapper.respond(**config)
            assert response
            assert type(response) == str

    @pytest.mark.asyncio
    @pytest.mark.parametrize('response_params', [['res1'],
                                                 ['res1', 'res2'],
                                                 ['res1', 'res2', 'res3'],
                                                 ['res1', 'res2', 'res3', 'res4']])
    async def test_respond_dynamic_false(self, dispatch_contract, query_config, w3, oracle, response_params):
        """
        Testing that each set of parameters goes through without an error.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming().processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        config = {
            'query_id': query_id,
            'response_params': response_params,
            'dynamic': False,
            'from_address': oracle,
            'gas': const.DEFAULT_GAS,
            'gas_price': w3.eth.gas_price
        }

        response = await dispatch_wrapper.respond(**config)

        assert response
        assert type(response) == str

    @pytest.mark.asyncio
    @pytest.mark.parametrize('input_res', [[1, 2],
                                           [10293847566574839201, 1029384756574839201],
                                           [1, 999999999999999999999],
                                           [9999999, 8888888888888888, 3874, 1293847566, 5555555551]])
    async def test_response_dyanmic_int_array(self, dispatch_contract, query_config, w3, oracle, input_res):
        """
        Testing that the respond function conditional runs as expected using varied cominations of integers.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming().processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        config = {
            'query_id': query_id,
            'response_params': input_res,
            'dynamic': True,
            'from_address': oracle,
            'gas': const.DEFAULT_GAS,
            'gas_price': w3.eth.gas_price
        }

        response = await dispatch_wrapper.respond(**config)
        assert response

    @pytest.mark.asyncio
    @pytest.mark.parametrize('fail_res', [[-1, 2],
                                           [1, 9.999999],
                                           [9999999, 8888888888888888, 3874, 1293.847566, -5555555551]])
    async def test_response_dyanmic_int_array_should_fail(self, dispatch_contract, query_config, w3, oracle, fail_res):
        """
        Testing that a value exception is raised for negative and floating-point integers within the response parameters.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming().processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        config = {
            'query_id': query_id,
            'response_params': fail_res,
            'dynamic': True,
            'from_address': oracle,
            'gas': const.DEFAULT_GAS,
            'gas_price': w3.eth.gas_price
        }

        with pytest.raises(ValueError):
            response = await dispatch_wrapper.respond(**config)
            assert response

    @pytest.mark.asyncio
    async def test_bytes32_array(self, query_config, w3, dispatch_contract, oracle):
        """
        Testing that the respond function conditional runs as expected.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming().processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        config = {
            'query_id': query_id,
            'response_params': ['p1', 'p2'],
            'dynamic': True,
            'from_address': oracle,
            'gas': const.DEFAULT_GAS,
            'gas_price': w3.eth.gas_price
        }

        response = await dispatch_wrapper.respond(**config)
        assert response
        assert type(response) == str



class TestGetters:

    @pytest.mark.asyncio
    async def test_getters(self, provider, oracle, subscriber, w3, dispatch_contract, query_config):
        """
        Testing the getter functions in one test, as they're fairly straightforward.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming().processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        """Test get_query_id_provider"""

        id_provider = await dispatch_wrapper.get_query_id_provider(query_id)
        assert type(id_provider) == str
        assert id_provider == '0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f'

        """Test get_subscriber"""

        sub = await dispatch_wrapper.get_subscriber(query_id)
        assert type(sub) == str
        assert sub == subscriber

        """Test get_endpoint"""

        get_ep = await dispatch_wrapper.get_endpoint(query_id)
        assert type(get_ep) == str
        assert 'Fibonacci' in get_ep

        """Test get_status"""
        # Further testing required
        status = await dispatch_wrapper.get_status(query_id)
        st = dispatch_contract.functions.getStatus(query_id).call()
        assert status == st

        """Test get_user_query"""

        user_query = await dispatch_wrapper.get_user_query(query_id)
        assert type(user_query) == str
        assert user_query == provider['query']

        """Test get_subscriber_onchain"""
        # Further testing required
        sub_on_chain = await dispatch_wrapper.get_subscriber_onchain(query_id)
        assert sub_on_chain is False

    @pytest.mark.asyncio
    async def test_get_cancel(self, provider, oracle, subscriber, w3, dispatch_contract, meta_config, query_config):
        """
        Testing that the get_cancel function returns the cancelled query's block number during cancellation.
        """
        tx_hash = await dispatch_wrapper.query_data(**query_config)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        query_id = dispatch_contract.events.Incoming().processReceipt(
            tx_receipt)[0]["args"]["id"]

        assert query_id

        block_number = tx_receipt['blockNumber']

        config_cancel = {
            'query_id': query_id,
        }

        cancel = await dispatch_wrapper.cancel_query(**config_cancel, **meta_config)
        assert cancel

        get_cancel = await dispatch_wrapper.get_cancel(query_id)
        assert get_cancel == block_number + 1
