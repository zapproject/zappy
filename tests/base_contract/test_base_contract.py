"""
    This module tests the different possible branches of execution within the Zap base contract.

    The following unit tests require minimal dependencies. Because the base contract embodies the constructor role for
    the entire Python interface of Zap (Zappy), the focus here lies in testing the instantiated dynamic attributes
    of the base contract class.
"""

from unittest.mock import MagicMock, patch
import pytest
import re
import src.base_contract.base_contract as base_contract


"""Default setup"""


MOCK_ABI = {
    'TEST_ARTIFACT': {'abi': [], 'networks':
        {'1': {'address': '0xmainnet'},
         '42': {'address': '0xkovan'},
         '31337': {'address': '0xdevnet'}}},
    'ZAPCOORDINATOR': {'abi': [], 'networks':
        {'1': {'address': '0xcoormainnet'},
         '42': {'address': '0xcoorkovan'},
         '31337': {'address': '0xcoordevnet'}}}
}

def capture_args(*args, **kwargs) -> any:
    """Side effect function for checking args and kwargs passed"""
    return args, kwargs


@patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True)
@patch('src.base_contract.Web3', autospec=True)
class TestInit:

    """Setup"""

    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = MagicMock()

    def test_instance_name(self, mock_Web3, instance):
        """
        Sanity check to ensure the instance runs without errors while mocking web3.
        """
        assert type(instance.name) == str
        assert instance.name == 'TEST_ARTIFACT'

        with pytest.raises(AssertionError):
            assert type(instance.name) != str
            assert instance.name != 'TEST_ARTIFACT'

    def test_name_without_arg(self, mock_Web3):
        """
        Testing that the contract fails if the artifact_name kwarg is an empty string.
        """
        with pytest.raises(KeyError):
            instance = base_contract.BaseContract(artifact_name='', web3=self.w3)
            assert instance

    def test_network_id_default(self, mock_Web3, instance):
        """
        Testing that the default network (1) is assigned to the contract instance.
        """
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
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=input, web3=self.w3)

        assert instance.network_id == input

        with pytest.raises(AssertionError):
            assert instance.network_id != input

    @pytest.mark.parametrize('wrong_net_id', [11, 16, 47, 118893, 'string'])
    def test_network_id_should_fail_if_given_unknown_id(self, mock_Web3, wrong_net_id):
        """
        Testing that the contract fails if given an unknown network id.
        """
        with pytest.raises(KeyError):
            instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=wrong_net_id, web3=self.w3)
            assert instance

    def test_network_id_of_zero(self, mock_Web3):
        """
        Testing that the network_id of zero actually uses the default network of '1.'
        """
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=0, web3=self.w3)

        assert instance.network_id != 0
        assert instance.network_id == 1


@patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True)
@patch('src.base_contract.Web3', autospec=False)
class TestAddress:

    """Setup"""

    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = MagicMock()

    def test_address_argument(self, mock_Web3):
        """
        Testing that the address argument is assigned as the instance address.
        """
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', address='0x_some_address', web3=self.w3)

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
        :param address_output: the associated address within the MOCK_ABI dictionary.
        """
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=network_input, web3=self.w3)

        assert type(instance.address) == str
        assert instance.address == address_output

        with pytest.raises(AssertionError):
            assert instance.address == '0x_wrong_address'


@patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True)
@patch('src.base_contract.Web3', autospec=True)
class TestArtifacts:

    """Setup"""

    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = MagicMock()

    def test_artifact_and_coor_artifact_assignments_from_dictionary(self, mock_Web3, instance):
        """
        Testing that the artifact_name kwarg triggers the artifacts dictionary and populates the artifact
        attribute with the controlled mock abi.

        :param mock_Web3: patched web3.
        """
        assert type(instance.artifact) == dict
        assert instance.artifact['networks']['1']['address'] == '0xmainnet'

        assert type(instance.coor_artifact) == dict
        assert instance.coor_artifact['networks']['1']['address'] == '0xcoormainnet'

        with pytest.raises(AssertionError):
            assert type(instance.artifact) != dict
            assert instance.artifact['networks']['1']['address'] == '0x123'

            assert type(instance.coor_artifact) != dict
            assert instance.coor_artifact['networks']['1']['address'] == '0x123'


@patch('src.base_contract.Web3', autospec=False)
class TestArtifactsDirectory:

    """Setup"""

    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.side_effect = MagicMock()

    mock_test_abi = {'abi': [], 'networks': {'1': {'address': '0xmainnet'}, '42': {'address': '0xkovan'},
                                             '31337': {'address': '0xdevnet'}}}

    mock_coor_abi = {'abi': [], 'networks': {'1': {'address': '0xcoormainnet'}, '42': {'address': '0xcoorkovan'},
                                             '31337': {'address': '0xcoordevnet'}}}

    mock_dict_dir = {'TEST_ARTIFACT': 'artifacts/contracts/TestArtifact.json',
                     'ZAPCOORDINATOR': 'artifacts/contracts/ZapCoordinator.json'}

    @patch('src.base_contract.utils.Utils.get_artifacts')
    @patch('src.base_contract.utils.Utils.open_artifact_in_dir')
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

        """Mock the relevant function returns"""
        mock_artifact_dir.return_value = self.mock_dict_dir
        mock_utils_abi.side_effect = [self.mock_test_abi, self.mock_coor_abi]

        instance = base_contract.BaseContract(artifact_name=art_input, artifacts_dir='some/path/',
                                              network_id=net_id_input, web3=self.w3)

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


@patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True)
@patch('src.base_contract.Web3', autospec=False)
class TestContracts:

    """Setup"""

    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.toChecksumAddress.side_effect = capture_args
        w3.eth.contract.side_effect = capture_args

    @patch('src.base_contract.base_contract.BaseContract.get_contract')
    @pytest.mark.parametrize('net_id', [1, 42, 31337])
    def test_coordinator_contract_args_with_coordinator_address_provided(self, mock_get_contract, mock_Web3, net_id):
        """
        Testing that the coordinator contract object is assigned with the correct args. This test first mocks the
        get_contract function so the contract instance runs without errors.
        """
        mock_get_contract = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', coordinator='0x_some_address',
                                              network_id=net_id, web3=self.w3)

        assert type(instance.coordinator) == tuple
        assert instance.coordinator[1]['abi'] == []

        """
        Iterate through the returned tuple to find the passed address. Because of all the mocks, the returned
        kwargs include a lot of unnecessary punctuation--hence the use of regexp.
        """

        expected_address = '0x_some_address'

        res = re.search(expected_address, str(instance.coordinator[1]['address']))
        assert res is not None

        with pytest.raises(AssertionError):
            res = re.search('this_should_fail', str(instance.coordinator[1]['address']))
            assert res is not None

    @pytest.mark.parametrize('input_id, expected_output', [(1, '0xcoormainnet'), (42, '0xcoorkovan'),
                                                            (31337, '0xcoordevnet')])
    def test_coordinator_contract_without_coordinator_address_provided(self, mock_Web3, input_id, expected_output):
        """
        Testing that the coordinator contract object is assigned with the correct args. The first assertions test that
        the coordinator instance was correctly assigned.
        """
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=input_id, web3=self.w3)

        assert type(instance.coordinator) == tuple
        assert instance.coordinator[1]['abi'] == []

        res = re.search(expected_output, str(instance.coordinator[1]['address']))
        assert res is not None

        with pytest.raises(AssertionError):
            res = re.search('this_should_fail', str(instance.coordinator[1]['address']))
            assert res is not None

    @patch('src.base_contract.base_contract.BaseContract.get_contract')
    def test_contract_instance_with_coor_through_get_contract_method(self, mock_get_contract, mock_Web3):
        """
        Testing that the return value from get_contract passes through to the contract instance object. This test
        mocks the get_contract function to return the expected value.
        """
        test_address = '0x_some_address'
        mock_get_contract.return_value = test_address

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', coordinator=test_address, web3=self.w3)

        res = re.search(test_address, str(instance.contract[1]['address']))
        assert res is not None

    @pytest.mark.parametrize('input_id, expected_address', [(1, '0xmainnet'), (42, '0xkovan'), (31337, '0xdevnet')])
    def test_contract_instance_if_no_coor_provided(self, mock_Web3, input_id, expected_address):
        """
        Testing that the contract instance object is assigned with the correct args using the MOCK_ABI with
        different networks.
        """
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=input_id, web3=self.w3)

        assert type(instance.contract) == tuple
        assert instance.contract[1]['abi'] == []

        expected_address = expected_address
        res = re.search(expected_address, str(instance.contract[1]['address']))
        assert res is not None

        with pytest.raises(AssertionError):
            res = re.search('this_will_fail', str(instance.contract[1]['address']))
            assert res is not None


@patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True)
@patch('src.base_contract.Web3', autospec=False)
class TestWrapperMethods:

    """Setup"""

    with patch('src.base_contract.Web3') as mock_Web3:
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.toChecksumAddress.side_effect = capture_args
        w3.eth.contract.side_effect = capture_args

    @patch('src.base_contract.base_contract.BaseContract._get_contract')
    def test_sync_get_contract(self, mock_async_get_contract, mock_Web3):
        """
        Testing that the get_contract function returns the proper values from the _get_contract async function. This
        test mocks the async _get_contract function and gives it a return value to check that the get_contract
        wrapper returns the proper value.
        """
        mock_async_get_contract.return_value = 'test_get_contract_address'

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', coordinator='some_address', web3=self.w3)

        assert type(instance.get_contract()) == str
        assert instance.get_contract() == 'test_get_contract_address'

        """Test false positive"""

        with pytest.raises(AssertionError):
            assert instance.get_contract() == 'this_should_fail'


    @patch('src.base_contract.base_contract.BaseContract._get_contract_owner')
    def test_sync_get_contract_owner(self, mock_async_owner, mock_Web3, instance):
        """
        Testing that the get_contract_owner returns the proper values from the async _get_contract_owner function.
        The test mocks the async _get_contract_owner function and gives it a return value to check that the
        get_contract_owner wrapper returns the proper value.
        """
        mock_async_owner.return_value = 'test_owner_address'

        assert type(instance.get_contract_owner()) == str
        assert instance.get_contract_owner() == 'test_owner_address'

        with pytest.raises(AssertionError):
            assert instance.get_contract_owner() == 'this_should_fail'


class TestAsyncMethods:

    """
    The following asynchronous functions should not be called directly; rather, the wrapper function should be
    called instead. The following unit tests require the somewhat hacky functions mock_owner_abi and mock_coor_abi
    in order to ensure the async functions were called. The mock abi functions are returned as a side effect from
    the web3.eth.contract call. While patching both Web3 and the artifacts dictionary, these functions proved
    difficult to test (hence, the creative workaround). The Pythonic syntax of these side effects are, nevertheless,
    exactly the same:
        _get_contract_owner() = <mock_object>.functions.owner().call()
        _get_contract() = <mock_object>.functions.getContract(self.name).call()
    """

    """Setup"""


    def mock_owner_abi(self, *args, **kwargs):
        """Function mimicking abi"""
        return_val = '0x_owner_address'
        class mimicked_abi:
            class functions:
                class owner:
                    def call(self):
                        return return_val
        return mimicked_abi


    def mock_coor_abi(self, *args, **kwargs):
        """Function mimicking abi"""
        return_val = '0x_artifact_address'

        class mimicked_coordinator:
            class functions:
                class getContract:
                    def __init__(self, name):
                        self.name = name
                    def call(self):
                        return return_val
        return mimicked_coordinator

    @pytest.mark.anyio
    async def test_async_get_contract_owner(self):
        """
        Testing the asynchronous _get_contract_owner function.
        """
        with patch('src.base_contract.Web3') as mock_Web3:
            mock_Web3.return_value = MagicMock()
            w3 = mock_Web3()
            w3.eth.contract.side_effect = self.mock_owner_abi
            w3.toChecksumAddress.side_effect = MagicMock()

            with patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True):

                instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', web3=w3)
                res = await instance._get_contract_owner()
                assert res == '0x_owner_address'

                with pytest.raises(AssertionError):
                    assert res == 'this_should_fail'

    @pytest.mark.anyio
    async def test_async_get_contract(self):
        """
        Testing the asynchronous _get_contract function.
        """
        with patch('src.base_contract.Web3') as mock_Web3:
            mock_Web3.return_value = MagicMock()
            w3 = mock_Web3()
            w3.eth.contract.side_effect = self.mock_coor_abi
            w3.toChecksumAddress.side_effect = MagicMock()

            with patch.dict(base_contract.index.Artifacts, MOCK_ABI, clear=True):

                instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', web3=w3)
                res = await instance._get_contract()
                assert res == '0x_artifact_address'

                with pytest.raises(AssertionError):
                    assert res == 'this_should_fail'
