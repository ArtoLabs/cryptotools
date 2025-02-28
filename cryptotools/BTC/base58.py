from cryptotools.transformations import bytes_to_int, int_to_bytes
from cryptotools.BTC.error import Base58DecodeError

ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE = len(ALPHABET)


def encode(bts: bytes) -> str:
    n = bytes_to_int(bts)
    leading_zero_bytes = len(bts) - len(bts.lstrip(b'\x00'))
    int_digits = []
    while n:
        int_digits.append(int(n % BASE))
        n //= BASE
    for _ in range(leading_zero_bytes):
        int_digits.append(0)
    return ''.join(ALPHABET[i] for i in reversed(int_digits))


def decode(b58: str) -> bytes:
    print(f"Input Base58 string: {b58}")  # Debugging
    partial_sum = 0
    exponent = 0
    for digit in reversed(b58):
        try:
            index = ALPHABET.index(digit)
            print(f"Digit: {digit}, Index: {index}, Exponent: {exponent}")  # Debugging
            partial_sum += index * BASE**exponent
        except ValueError:
            raise Base58DecodeError('Bad Byte') from None
        exponent += 1
    print(f"Partial sum: {partial_sum}")  # Debugging
    result = int_to_bytes(partial_sum)
    print(f"Decoded bytes: {result}")  # Debugging
    return result
