from utils import *
from random import randint

def chosen_plaintext(n: int, e: int, c: int) -> bytes:
    p = randint(2, 1000)
    q = mod_inv(p, n)

    to_decrypt = c * pow(p, e, n) % n
    b = int_as_bytes(to_decrypt)

    print('Send data for decrypting in one of the following forms:')
    print('As decimal integer:', to_decrypt)
    print('As hexidecimal integer:', hex(to_decrypt))
    print('As Base64 encoded bytes:', b64encode(b).decode('ascii'))

    result = input('Provide decrypted data: ')
    result = transform_to_int(result)

    m = result * q % n
    print('Result is:', int_as_bytes(m))

def common_divisor(n1: int, n2: int, e1: int, c1: int) -> bytes:
    assert gcd(n1, n2) > 1

    p = gcd(n1, n2)
    q = n1 // p

    d = mod_inv(e1, (p - 1) * (q - 1))
    m = pow(c1, d, n1)

    return int_as_bytes(m)

def common_modulus(n: int, e1: int, e2: int, c1: int, c2: int) -> bytes:
    assert gcd(e1, e2) == 1

    p1, p2, _ = egcd(e1, e2)

    if p1 < 0:
        c1 = mod_inv(c1, n)
        p1 *= -1
    else:
        c2 = mod_inv(c2, n)
        p2 *= -1

    m = pow(c1, p1, n) * pow(c2, p2, n) % n

    return int_as_bytes(m)

def common_exponent(e: int, modules: list, ciphertexts: list) -> bytes:
    assert len(modules) == e

    solution = solve_chinese_problem(modules, ciphertexts)

    left, right = 1, min(modules)

    while right - left > 1:
        middle = (left + right) // 2

        if middle ** e == solution:
            return int_as_bytes(middle)

        if middle ** e < solution:
            left = middle
        else:
            right = middle

    return b''