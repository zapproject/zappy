from collections.abc import (
    Mapping,
)
from typing import (
    NamedTuple,
    Union,
)
from eth_utils.curried import (
    to_text,
)
from eth_account._utils.structured_data.hashing import (
    hash_domain,
    hash_message as hash_eip712_message,
    load_and_validate_structured_message,
)
from hexbytes import (
    HexBytes,
)
from src.nft.utils.validation import validate_structured_data

class SignableMessage(NamedTuple):
    """
    A message compatible with EIP-191_ that is ready to be signed.
    The properties are components of an EIP-191_ signable message. Other message formats
    can be encoded into this format for easy signing. This data structure doesn't need to
    know about the original message format. For example, you can think of
    EIP-712 as compiling down to an EIP-191 message.
    In typical usage, you should never need to create these by hand. Instead, use
    one of the available encode_* methods in this module, like:
        - :meth:`encode_structured_data`
        - :meth:`encode_intended_validator`
        - :meth:`encode_defunct`
    .. _EIP-191: https://eips.ethereum.org/EIPS/eip-191
    """
    version: bytes  # must be length 1
    header: bytes  # aka "version specific data"
    body: bytes  # aka "data to sign"


def encode_structured_data(
        primitive: Union[bytes, int, Mapping] = None,
        *,
        hexstr: str = None,
        text: str = None) -> SignableMessage:
    """
    Encode an EIP-712_ message.
    EIP-712 is the "structured data" approach (ie~ version 1 of an EIP-191 message).
    Supply the message as exactly one of the three arguments:
        - primitive, as a dict that defines the structured data
        - primitive, as bytes
        - text, as a json-encoded string
        - hexstr, as a hex-encoded (json-encoded) string
    .. WARNING:: Note that this code has not gone through an external audit, and
        the test cases are incomplete.
        Also, watch for updates to the format, as the EIP is still in DRAFT.
    :param primitive: the binary message to be signed
    :type primitive: bytes or int or Mapping (eg~ dict )
    :param hexstr: the message encoded as hex
    :param text: the message as a series of unicode characters (a normal Py3 str)
    :returns: The EIP-191 encoded message, ready for signing
    .. _EIP-712: https://eips.ethereum.org/EIPS/eip-712
    """
    if isinstance(primitive, Mapping):
        validate_structured_data(primitive)
        structured_data = primitive
    else:
        message_string = to_text(primitive, hexstr=hexstr, text=text)
        structured_data = load_and_validate_structured_message(message_string)
    return SignableMessage(
        HexBytes(b'\x01'),
        hash_domain(structured_data),
        hash_eip712_message(structured_data),
    )