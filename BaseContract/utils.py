import json
import os

# These functions replace the monorepo's artifactDir and negates the need for each 
# artifact's location to be hardcoded in a seperate module.


# Fetches ABI and is a helper function for load_address.
#   @notice: Adjust path below (if changed) to fetch /<name>.json or insert as 2nd arg.
#
#   @params: (name) is the artifact name.
#            (file_path) is used to find artifacts if path is changed.
def load_abi(name: str, file_path = None) -> dict:
    if file_path is not None:
        path = file_path
    else:
        path = f"{os.path.dirname(os.path.dirname(__file__))}/Artifacts/"
    try:
        with open(os.path.abspath(path + f"{name}.json")) as f:
            abi_file = json.load(f)
        return abi_file
    except Exception as e:
        print(e)


#   @notice This function uses the above 'load_abi' function to fetch abi.
#   @params (name) is the name of the artifact.
#           (netId) is the Ethereum network.
#           (abi_file) is used for test.
def load_address(name: str, netId: int or str, abi_file = None) -> str:
    try:
        if abi_file is not None:
            a_dict = abi_file
        else:
            a_dict = load_abi(name)
        network_key = a_dict['networks']
        network_address = network_key[netId]['address']
        return network_address
    except Exception as e:
        print('Error with: ' + str(e))
