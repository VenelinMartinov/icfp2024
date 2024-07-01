BASE = 94

# pylint: disable=line-too-long
STRING_ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"


def ascii_to_index(msg: str) -> list[int]:
    msg_bytes = msg.encode("ascii")
    res: list[int] = []
    for char in msg_bytes:
        index = char - 33
        res.append(index)

    return res


def index_to_string(msg: list[int]) -> str:
    res = ""
    for elem in msg:
        res += STRING_ASCII[elem]

    return res


def string_to_index(msg: str) -> list[int]:
    res: list[int] = []
    for char in msg:
        index = STRING_ASCII.index(char)
        res.append(index)

    return res


def index_to_ascii(msg: list[int]) -> str:
    res = b""
    for elem in msg:
        res += bytes([elem + 33])

    return res.decode("ascii")


def decode_integer(body: str) -> int:
    indices = ascii_to_index(body)
    result = 0

    for i, elem in enumerate(reversed(indices)):
        result += (BASE**i) * elem

    return result


def decode_string(body: str) -> str:
    indices = ascii_to_index(body)

    return index_to_string(indices)


def encode_string(msg: str) -> str:
    indices = string_to_index(msg)

    return index_to_ascii(indices)


def encode_integer(num: int) -> str:
    res: list[int] = []
    while num > 0:
        res.append(num % BASE)
        num //= BASE

    return index_to_ascii(res)
