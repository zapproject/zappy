import os
import json


class Utils:

    """
    # @ignore
    # @params {string} buildDir
    # @returns {any}
    """

    @staticmethod
    def get_artifacts(build_dir: str) -> dict:
        artifacts = {
            'ARBITER': os.path.join(build_dir, 'Arbiter.json'),
            'BONDAGE': os.path.join(build_dir, 'Bondage.json'),
            'DISPATCH': os.path.join(build_dir, 'Dispatch.json'),
            'REGISTRY': os.path.join(build_dir, 'Registry.json'),
            'CurrentCost': os.path.join(build_dir, 'CurrentCost.json'),
            'PiecewiseLogic': os.path.join(build_dir, 'PiecewiseLogic.json'),
            'ZAP_TOKEN': os.path.join(build_dir, 'ZapToken.json'),
            'Client1': os.path.join(build_dir, 'Client1.json'),
            'Client2': os.path.join(build_dir, 'Client2.json'),
            'Client3': os.path.join(build_dir, 'Client3.json'),
            'Client4': os.path.join(build_dir, 'Client4.json'),
            'ZAPCOORDINATOR': os.path.join(build_dir, 'ZapCoordinator.json'),
            'TOKENDOTFACTORY': os.path.join(build_dir, 'TokenDotFactory.json'),
        }
        return artifacts

    """
    # @ignore
    # @params {string} artifact
    # @returns {dict}
    """

    @staticmethod
    def open_artifact_in_dir(artifact: str) -> dict:
        with open(artifact) as f:
            abi = json.load(f)
            return abi
