import os
import json


def load_json(name: str) -> dict:
    path = f"{os.path.dirname(os.path.dirname(__file__))}/contracts/"
    with open(os.path.abspath(path + f"{name}.json")) as f:
        abi_file = json.load(f)
    return abi_file


Artifacts = {
    'ARBITER': load_json('Arbiter'),
    'BONDAGE': load_json('Bondage'),
    'DISPATCH': load_json('Dispatch'),
    'REGISTRY': load_json('Registry'),
    'CurrentCost': load_json('CurrentCost'),
    'ZAP_TOKEN': load_json('ZapToken'),
    'Client1': load_json('Client1'),
    'Client2': load_json('Client2'),
    'Client3': load_json('Client3'),
    'Client4': load_json('Client4'),
    'ZAPCOORDINATOR': load_json('ZapCoordinator'),
    'TOKENDOTFACTORY': load_json('TokenDotFactory'),
}
