from web3 import Web3


def encode_params(self, endpoint_params: list = [], ):
    """ needed for
    """
    pars = endpoint_params
    hex_params =\
        [el if el.find('0x') == 0 else Web3.toHex(text=el) for el in pars]
    bytes_params =\
        [Web3.toBytes(hexstr=hex_p) for hex_p in hex_params]
    params = []

    from math import ceil
    for element in bytes_params:
        if len(element) <= 32:
            params.append(Web3.toHex(element))
            continue
        chunks_len = ceil((len(element) + 2) / 32)
        param_bytes_w_len = [0, chunks_len].extend(element)
        for i in range(0, chunks_len):
            start = i * 32
            end = start + 32
            params.append(Web3.toHex(param_bytes_w_len[start:end]))
    return params
