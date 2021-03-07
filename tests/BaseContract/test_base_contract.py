from unittest.mock import MagicMock, patch
import pytest
import base_contract

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



@patch.dict('base_contract.Artifacts', mock_abi)
@patch('base_contract.Web3', autospec=True)
class TestInit:

    def test_instance_name(self, mock_Web3):
        """
        Sanity check to ensure the instance runs without errors while mocking web3

        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT')

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
        w3.eth.contract.return_value = MagicMock()

        with pytest.raises(KeyError):
            instance = base_contract.BaseContract(artifact_name='')


    def test_network_id_default(self, mock_Web3):
        """
        Testing that the default network (1) is assigned to the contract instance.

        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT')

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
        w3.eth.contract.return_value = MagicMock()
        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=input)

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
        w3.eth.contract.return_value = MagicMock()

        with pytest.raises(KeyError):
            instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=wrong_net_id)

    def test_network_id_of_zero(self, mock_Web3):
        """
        Testing that the network_id of zero actually uses the default network of '1.'
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=0)

        assert instance.network_id != 0
        assert instance.network_id == 1


@patch.dict('base_contract.Artifacts', mock_abi)
@patch('base_contract.Web3', autospec=True)
class TestAddress:

    def test_address_argument(self, mock_Web3):
        """
        Testing that the address argument is assigned as the instance address.

        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', address='0x_some_address')

        assert type(instance.address) == str
        assert instance.address == '0x_some_address'

        with pytest.raises(AssertionError):
            assert instance.address == '0xsomeotheraddress'

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
        w3.eth.contract.return_value = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT', network_id=network_input)

        assert type(instance.address) == str
        assert instance.address == address_output

        with pytest.raises(AssertionError):
            assert instance.address == '0xwrongaddress'


@patch.dict('base_contract.Artifacts', mock_abi)
@patch('base_contract.Web3', autospec=True)
class TestArtifacts:

    mock_contract = MagicMock(address="0x000000000000000000", abi=['abi'], name="MOCKCONTRACT")

    def test_artifact_and_coor_artifact_assignments_from_dictionary(self, mock_Web3):
        """
        Testing that the artifact_name kwarg triggers the Artifacts dictionary and populates the artifact
        attribute with the controlled mock abi.

        :param mock_Web3: patched web3.
        """
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = MagicMock()

        instance = base_contract.BaseContract(artifact_name='TEST_ARTIFACT')

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


@patch('base_contract.Web3', autospec=True)
class TestArtifactsDirectory:
    mock_test_abi = {'abi': [], 'networks': {'1': {'address': '0xmainnet'}, '42': {'address': '0xkovan'},
                                             '31337': {'address': '0xdevnet'}}}

    mock_coor_abi = {'abi': [], 'networks': {'1': {'address': '0xcoormainnet'}, '42': {'address': '0xcoorkovan'},
                                             '31337': {'address': '0xcoordevnet'}}}

    mock_dict_dir = {'TEST_ARTIFACT': 'Artifacts/contracts/TestArtifact.json',
                     'ZAPCOORDINATOR': 'Artifacts/contracts/ZapCoordinator.json'}

    @patch('base_contract.Utils.get_artifacts')
    @patch('base_contract.Utils.open_artifact_in_dir')
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
        respectively. Thereafter, the BaseContract instance attribute 'artifact' should be assigned as an object
        (abi). The get_artifacts and open_artifact_in_dir functions are patched and return expected values.

        :param mock_utils_abi: a mocked abi that mimicks what open_artifacts_in_dir function will return.
        :param mock_artifact_dir: a small mocked directory that replicates the return of get_artifacts function.
        :param mock_Web3: patched web3.
        """

        """Mock web3"""
        mock_Web3.return_value = MagicMock()
        w3 = mock_Web3()
        w3.eth.contract.return_value = MagicMock()

        """Mock the relevant function returns"""
        mock_artifact_dir.return_value = self.mock_dict_dir
        mock_utils_abi.side_effect = [self.mock_test_abi, self.mock_coor_abi]

        instance = base_contract.BaseContract(artifact_name=art_input, artifacts_dir='some/path/',
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




