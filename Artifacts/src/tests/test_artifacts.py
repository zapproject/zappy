import pytest
import index

class TestIndex:

    @pytest.fixture
    def artifacts_iterator(self):
        for i in index.Artifacts:
            artifacts = index.Artifacts[i]
        return artifacts

    def test_fetch_artifacts_by_key(self, artifacts_iterator):
            assert type(artifacts_iterator) == dict

            with pytest.raises(AssertionError):
                assert type(artifacts_iterator) != dict


    def test_fetch_arbiter_address(self):
        arbiter_addr = index.Artifacts['ARBITER']['networks']['1']['address']
        assert arbiter_addr == '0x131e22ae3e90f0eeb1fb739eaa62ea0290c3fbe1'

    def test_fetch_zap_coor_kovan_address(self):
        zap_coor_kovan_addr = index.Artifacts['ZAPCOORDINATOR']['networks']['42']['address']
        assert zap_coor_kovan_addr == '0xdbcac7c8bcca78fb05e96d0d2c68efb1c5922539'

    def test_fetch_registry_devnet_address(self):
        registry_devnet_addr = index.Artifacts['REGISTRY']['networks']['31337']['address']
        assert registry_devnet_addr == '0xa513E6E4b8f2a923D98304ec87F64353C4D5C853'

    
    def test_zap_coor_abi(self):
        zap_get_contract = index.Artifacts['ZAPCOORDINATOR']['abi']
        assert type(zap_get_contract) == list