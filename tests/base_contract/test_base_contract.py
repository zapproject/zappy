from unittest.mock import MagicMock, patch, AsyncMock, PropertyMock
import pytest
import unittest
from unittest import mock
from anyio import run
import anyio
import sys
import re
import asyncio
from os.path import join, realpath
sys.path.insert(0, realpath(join(__file__, "../../../src/")))

from base_contract import BaseContract, Artifacts, Web3



print(sys.path[0])

mock_abi = {
    'TEST_ARTIFACT': {'abi': [], 'networks':
        {'1': {'address': '0xmainnet'},
         '42': {'address': '0xkovan'},
         '31337': {'address': '0xdevnet'}}},
    'ZAPCOORDINATOR': {'abi': [], 'networks':
        {'1': {'address': '0xcoormainnet'},
         '42': {'address': '0xcoorkovan'},
         '31337': {'address': '0xcoordevnet'}}}
}

@pytest.fixture
@patch('Web3', autospec=True)
def mock_web3(mock_Web3):
    mock_Web3.return_value = MagicMock()
    w3 = mock_Web3()
    w3.eth.contract.return_value = MagicMock()




@patch.dict('Artifacts', mock_abi)
@patch('Web3', autospec=True)
class TestInit:

    def test_instance_name(self, mock_web3):
        """
        Sanity check to ensure the instance runs without errors while mocking web3

        :param mock_Web3: patched web3.
        """
        #mock_Web3.return_value = MagicMock()
        #w3 = mock_Web3()
        #w3.eth.contract.return_value = MagicMock()

        instance = BaseContract(artifact_name='TEST_ARTIFACT')

        assert type(instance.name) == str
        assert instance.name == 'TEST_ARTIFACT'

        with pytest.raises(AssertionError):
            assert type(instance.name) != str
            assert instance.name != 'TEST_ARTIFACT'

    def test_name_without_arg(self, mock_Web3):
        """
        Testing that the contract fails if the artifact_name kwarg is an empty string.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        with pytest.raises(KeyError):
            instance = BaseContract(artifact_name='')
            assert instance


    def test_network_id_default(self, mock_Web3):
        """
        Testing that the default network (1) is assigned to the contract instance.
        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        instance = BaseContract(artifact_name='TEST_ARTIFACT')

        assert type(instance.network_id) == int
        assert instance.network_id == 1

        with pytest.raises(AssertionError):
            assert type(instance.network_id) != int
            assert instance.network_id != 1

    @pytest.mark.parametrize('input', [1, 42, 31337])
    def test_assigned_network_ids(self, mock_Web3, input):
        """
        Testing that the network kwarg gets assigned to the contract network instance.

        :param mock_Web3: patched web3.
        :param input: the relevant networks' corresponding integer.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract
        instance = BaseContract(artifact_name='TEST_ARTIFACT', network_id=input)

        assert instance.network_id == input

        with pytest.raises(AssertionError):
            assert instance.network_id != input

    @pytest.mark.parametrize('wrong_net_id', [11, 16, 47, 118893])
    def test_network_id_should_fail_if_given_unknown_id(self, mock_Web3, wrong_net_id):
        """
        Testing that the contract should fail if given an unknown network id.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        with pytest.raises(KeyError):
            instance = BaseContract(artifact_name='TEST_ARTIFACT', network_id=wrong_net_id)
            assert instance

    def test_network_id_of_zero(self, mock_Web3):
        """
        Testing that the network_id of zero actually uses the default network of '1.'
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        instance = BaseContract(artifact_name='TEST_ARTIFACT', network_id=0)

        assert instance.network_id != 0
        assert instance.network_id == 1


@patch.dict('Artifacts', mock_abi)
@patch('Web3', autospec=True)
class TestAddress:

    def test_address_argument(self, mock_Web3):
        """
        Testing that the address argument is assigned as the instance address.

        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        instance = BaseContract(artifact_name='TEST_ARTIFACT', address='0x_some_address')

        assert type(instance.address) == str
        assert instance.address == '0x_some_address'

        with pytest.raises(AssertionError):
            assert instance.address == '0x_some_other_address'

    @pytest.mark.parametrize('network_input, address_output', [(1, '0xmainnet'), (42, '0xkovan'), (31337, '0xdevnet')])
    def test_address_with_no_argument(self, mock_Web3, network_input, address_output):
        """
        Testing that the address is correctly fetched from the abi when no address arg is given.

        :param mock_Web3: patched web3.
        :param network_input: relevant networks including mainnet, kovan, and devnet.
        :param address_output: the associated address within the mock_abi dictionary.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        instance = BaseContract(artifact_name='TEST_ARTIFACT', network_id=network_input)

        assert type(instance.address) == str
        assert instance.address == address_output

        with pytest.raises(AssertionError):
            assert instance.address == '0x_wrong_address'


@patch.dict('Artifacts', mock_abi)
@patch('Web3', autospec=True)
class TestArtifacts:

    def test_artifact_and_coor_artifact_assignments_from_dictionary(self, mock_Web3):
        """
        Testing that the artifact_name kwarg triggers the artifacts dictionary and populates the artifact
        attribute with the controlled mock abi.

        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        instance = BaseContract(artifact_name='TEST_ARTIFACT')

        """Asserting the artifact attribute is equal to the mock dictionary"""

        assert type(instance.artifact) == dict
        assert instance.artifact['networks']['1']['address'] == '0xmainnet'

        assert type(instance.coor_artifact) == dict
        assert instance.coor_artifact['networks']['1']['address'] == '0xcoormainnet'

        """Ensuring this includes no false positives"""

        with pytest.raises(AssertionError):
            assert type(instance.artifact) != dict
            assert instance.artifact['networks']['1']['address'] == '0x123'

            assert type(instance.coor_artifact) != dict
            assert instance.coor_artifact['networks']['1']['address'] == '0x123'


@patch('Web3', autospec=True)
class TestArtifactsDirectory:
    mock_test_abi = {'abi': [], 'networks': {'1': {'address': '0xmainnet'}, '42': {'address': '0xkovan'},
                                             '31337': {'address': '0xdevnet'}}}

    mock_coor_abi = {'abi': [], 'networks': {'1': {'address': '0xcoormainnet'}, '42': {'address': '0xcoorkovan'},
                                             '31337': {'address': '0xcoordevnet'}}}

    mock_dict_dir = {'TEST_ARTIFACT': 'artifacts/contracts/TestArtifact.json',
                     'ZAPCOORDINATOR': 'artifacts/contracts/ZapCoordinator.json'}

    @patch('Utils.get_artifacts')
    @patch('Utils.open_artifact_in_dir')
    @pytest.mark.parametrize(
        'art_input, net_id_input, address_output, coor_address_output', [
            ('TEST_ARTIFACT', 1, '0xmainnet', '0xcoormainnet'), ('TEST_ARTIFACT', 42, '0xkovan', '0xcoorkovan'),
            ('TEST_ARTIFACT', 31337, '0xdevnet', '0xcoordevnet')
        ])
    def test_artifact_instance_from_artifacts_directory_arg(self, mock_utils_abi, mock_artifact_dir, mock_Web3,
                                                            art_input, net_id_input, address_output,
                                                            coor_address_output):
        """
        Testing that the artifacts_dir kwarg passes through both get_artifacts and open_artifact_in_dir functions
        respectively. Thereafter, the base_contract instance attribute 'artifact' should be assigned as an object
        (abi). The get_artifacts and open_artifact_in_dir functions are patched and return expected values.

        :param mock_utils_abi: a mocked abi that mimics what open_artifacts_in_dir function will return.
        :param mock_artifact_dir: a small mocked directory that replicates the return of get_artifacts function.
        :param mock_Web3: patched web3.
        """

        """Mock web3"""
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = w3._utils.datatypes.Contract

        """Mock the relevant function returns"""
        mock_artifact_dir.return_value = self.mock_dict_dir
        mock_utils_abi.side_effect = [self.mock_test_abi, self.mock_coor_abi]

        instance = BaseContract(artifact_name=art_input, artifacts_dir='some/path/',
                                              network_id=net_id_input)

        assert type(instance.artifact) == dict
        assert type(instance.artifact['abi']) == list
        assert instance.artifact['networks'][str(net_id_input)]['address'] == address_output

        """Checking coordinator instance object and coordinator instance address are also set"""

        assert type(instance.coor_address) == str
        assert type(instance.coor_artifact['abi']) == list
        assert instance.coor_address == coor_address_output

        """Assertions regarding the artifact instance that should fail"""

        with pytest.raises(AssertionError):
            assert type(instance.artifact) == list
            assert type(instance.artifact['abi']) == dict
            assert instance.artifact['network'][str(net_id_input)]['address'] == '0xfailingstring'
            assert instance.artifact['abi']['network']

            """Assertions regarding the coordinator artifact instance that should fail"""

            assert type(instance.coor_address) != str
            assert type(instance.coor_artifact['abi']) != dict
            assert instance.coor_address == '0xfailingstring'
            assert instance.coor_artifact['abi']['network']


@patch.dict('Artifacts', mock_abi)
@patch('Web3', autospec=True)
class TestContracts:

    """Side effect function for checking args and kwargs passed"""
    def capture_args(self, *args, **kwargs) -> any:
        return args, kwargs

    @patch('BaseContract.get_contract')
    @pytest.mark.parametrize('net_id', [1, 42, 31337])
    def test_coordinator_contract_args_with_coordinator_address_provided(self, mock_get_contract, mock_Web3, net_id):
        """
        Testing that the coordinator contract object is assigned with the correct args.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.toChecksumAddress.side_effect = self.capture_args
        w3.eth.contract.side_effect = self.capture_args

        """Mocking the get_contract function so the contract instance runs without error"""
        mock_get_contract = MagicMock()

        instance = BaseContract(artifact_name='TEST_ARTIFACT', coordinator='0x_some_address',
                                              network_id=net_id)

        assert type(instance.coordinator) == tuple
        assert instance.coordinator[1]['abi'] == []

        """
        Iterate through the returned tuple to find the passed address. Because of all the mocks, the returned
        kwargs include a lot of unnecessary parenthesis hence the utilization of regexp.
        """

        expected_address = '0x_some_address'

        res = re.search(expected_address, str(instance.coordinator[1]['address']))
        assert res is not None

        """Testing for false positive"""

        with pytest.raises(AssertionError):
            res = re.search('this_should_fail', str(instance.coordinator[1]['address']))
            assert res is not None

    @pytest.mark.parametrize('input_id, expected_output', [(1, '0xcoormainnet'), (42, '0xcoorkovan'),
                                                            (31337, '0xcoordevnet')])
    def test_coordinator_contract_without_coordinator_address_provided(self, mock_Web3, input_id, expected_output):
        """
        Testing that the coordinator contract object is assigned with the correct args.
        """

        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.toChecksumAddress.side_effect = self.capture_args
        w3.eth.contract.side_effect = self.capture_args

        instance = BaseContract(artifact_name='TEST_ARTIFACT', network_id=input_id)

        """Testing that the coordinator instance was assigned"""

        assert type(instance.coordinator) == tuple
        assert instance.coordinator[1]['abi'] == []

        res = re.search(expected_output, str(instance.coordinator[1]['address']))
        assert res is not None

        with pytest.raises(AssertionError):
            res = re.search('this_should_fail', str(instance.coordinator[1]['address']))
            assert res is not None

    @patch('BaseContract.get_contract')
    def test_contract_instance_with_coor_through_get_contract_method(self, mock_get_contract, mock_Web3):

        """
        Testing that the return value from get_contract passes through to the contract instance object.
        """

        test_address = '0x_some_address'

        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.toChecksumAddress.side_effect = self.capture_args
        w3.eth.contract.side_effect = self.capture_args

        """Mocking the get_contract function to return the expected value"""

        mock_get_contract.return_value = test_address

        instance = BaseContract(artifact_name='TEST_ARTIFACT', coordinator=test_address)

        """Actual test that iterates through the returned arguments from the web3 side effect"""

        res = re.search(test_address, str(instance.contract[1]['address']))
        assert res is not None

    @pytest.mark.parametrize('input_id, expected_address', [(1, '0xmainnet'), (42, '0xkovan'), (31337, '0xdevnet')])
    def test_contract_instance_if_no_coor_provided(self, mock_Web3, input_id, expected_address):
        """
        Testing that the contract instance object is assigned with the correct args using the mock_abi with different
        networks.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.toChecksumAddress.side_effect = self.capture_args
        w3.eth.contract.side_effect = self.capture_args

        instance = BaseContract(artifact_name='TEST_ARTIFACT', network_id=input_id)

        assert type(instance.contract) == tuple
        assert instance.contract[1]['abi'] == []

        expected_address = expected_address
        res = re.search(expected_address, str(instance.contract[1]['address']))
        assert res is not None

        with pytest.raises(AssertionError):
            res = re.search('this_will_fail', str(instance.contract[1]['address']))
            assert res is not None


@patch.dict('Artifacts', mock_abi)
@patch('Web3', autospec=True)
class TestMethods:

    """Side effect function for checking args and kwargs passed"""

    def capture_args(self, *args, **kwargs) -> any:
        return args, kwargs

    @patch('BaseContract._get_contract')
    def test_sync_get_contract(self, mock_async_get_contract, mock_Web3):
        """
        Testing that the get_contract function returns the proper values from the _get_contract async function.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = self.capture_args
        w3.toChecksumAddress.side_effect = self.capture_args

        """
        Mock the async _get_contract function and give it a return value to check that the get_contract
        wrapper returns the proper value.
        """
        mock_async_get_contract.return_value = 'test_get_contract_address'

        instance = BaseContract(artifact_name='ARBITER', coordinator='some_address')

        assert type(instance.get_contract()) == str
        assert instance.get_contract() == 'test_get_contract_address'

        """Test false positive"""

        with pytest.raises(AssertionError):
            assert instance.get_contract() == 'this_should_fail'


    @patch('BaseContract._get_contract_owner')
    def test_sync_get_contract_owner(self, mock_async_owner, mock_Web3):
        """
        Testing that the get_contract_owner returns the proper values from the async _get_contract_owner function.
        """
        mock_Web3.return_value = MagicMock()

        """
        Mock the async _get_contract_owner function and give it a return value to check that the get_contract_owner
        wrapper returns the proper value.
        """
        mock_async_owner.return_value = 'test_owner_address'

        instance = BaseContract(artifact_name='TEST_ARTIFACT')

        assert type(instance.get_contract_owner()) == str
        assert instance.get_contract_owner() == 'test_owner_address'

@pytest.fixture
def anyio_backend():
    """ Ensures anyio uses the default, pytest-asyncio plugin
        for running async tests
    """
    return 'asyncio'
@patch.dict('Artifacts', mock_abi)

@patch('Web3', autospec=True)
class TestAsyncs:


    def capture_args(self, *args, **kwargs) -> any:
        """Side effect function for checking args and kwargs passed"""
        return args, kwargs


    def mock_owner_abi(self, *args, **kwargs):
        """
        A mocked abi for the async _get_contract_owner to fetch from without being read by web3--hence it being
        a class and not a dictionary.
        """
        return_val = 'some_string'

        class Irrelevant:
            class functions:
                class owner:
                    def call(self):
                        return return_val
        return Irrelevant

    def test_get_contract_owner_type(self, mock_Web3):
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = self.capture_args
        w3.toChecksumAddress.side_effect = self.capture_args

        """Create instance to allow the coordinator attribute to be visible"""
        instance = BaseContract(artifact_name='TEST_ARTIFACT')
        async_owner = instance._get_contract_owner()
        isinstance(async_owner, type(object))
        assert asyncio.iscoroutine(async_owner) is True

    @pytest.mark.anyio
    async def test_get_contract_type(self, mock_Web3):
        mock_Web3.return_value = MagicMock()

        instance = BaseContract(artifact_name='TEST_ARTIFACT')
        async_contract = await instance._get_contract()

        isinstance(async_contract, type(object))
        assert asyncio.iscoroutine(async_contract) is True





    def test_async_get_contract_owner(self, mock_Web3):
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = self.mock_owner_abi
        w3.toChecksumAddress.side_effect = self.mock_owner_abi

        instance = BaseContract(artifact_name='TEST_ARTIFACT')

        assert instance.get_contract_owner() == 'some_string'
















