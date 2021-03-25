import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath("./__file__")))

import json

import pprint
pp = pprint.PrettyPrinter(indent=4)


def convertFromBytes32(b32):
    b32 = b32.hex().rstrip("0")
    if len(b32) % 2 != 0:
        b32 = b32 + '0'
    return bytes.fromhex(b32).decode('utf8')


def getArtifact(contract_name: str):
    base_path = os.path.dirname(os.path.abspath("./__file__"))
    artifacts_directory = "src/Artifacts/contracts"
    artifact_path = os.path.join(
        base_path, artifacts_directory, f"{contract_name.capitalize()}.json")
    with open(artifact_path) as f:
        artifact = json.load(f)
        return artifact

def grab_function_name(obj):
    name = obj.get('name')
    if name:
        return name

def get_contract_functions(abi):
    return list(map(grab_function_name, abi))