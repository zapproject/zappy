import json
import os


# These functions replace the monorepo's artifactDir and negates the need for each 
# artifact's location to be hardcoded in a seperate module.
#
# Helper function for load_abi and load_address.
def load_json(name: str) -> str:
    # Adjust path below to fetch Artifacts/<name>.json.
    path = "./Artifacts/"
    with open(os.path.abspath(path + f"{name}.json")) as f:
        json_file = json.load(f)
    return json_file


def load_abi(name: str) -> dict:
    obj = load_json(name)
    abi = obj['abi']
    return abi

def load_address(name: str, netId: int or str) -> dict:
    try:
        a_dict = load_json(name)
        addr = a_dict['networks']
        network_address = addr[netId]['address']
        return network_address
    except Exception as e:
        print('Error with: ' + str(e))