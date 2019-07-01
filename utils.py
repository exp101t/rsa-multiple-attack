from base64 import b64encode, b64decode
from re import match

# Mathematical algorithms
def egcd(a: int, b: int) -> (int, int, int):
    prelast_u, prelast_v = 1, 0
    last_u, last_v = 0, 1

    while True:
        q, r = a // b, a % b

        if r == 0:
            return (last_u, last_v, b)

        prelast_u, last_u = last_u, prelast_u - q * last_u
        prelast_v, last_v = last_v, prelast_v - q * last_v

        a, b = b, r

def gcd(a: int, b: int) -> int:
    while True:
        if b == 0:
            return a
        a, b = b, a % b

def mod_inv(a: int, b: int) -> int:
    return egcd(a, b)[0] % b

def solve_chinese_problem(modules: list, remainders: list) -> int:
    mult = 1

    for i in modules:
        mult *= i

    result = sum(
        r * mult * mod_inv(mult // m, m) // m
        for r, m in zip(remainders, modules)
    )

    return result % mult

# Conversion algorithms
def int_as_bytes(n: int) -> bytes:
    bit_length = n.bit_length()

    if bit_length == 0:
        length = 1
    else:
        length = (bit_length + 7) // 8

    return n.to_bytes(length, 'big')

def bytes_as_int(b: bytes) -> int:
    return int.from_bytes(b, 'big')

def transform_to_int(s: str) -> int:
    if match(r'^\d+$', s):
        return int(s)
    elif s.startswith('0x'):
        return int(s, 16)
    elif match(r'^[\w+/=\r\n]+$', s):
        b = b64decode(s.encode('utf-8'))
        return bytes_as_int(b)