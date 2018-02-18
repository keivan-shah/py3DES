# DES Algorithm implemented in Python3

__version__ = '1.0'
__author__ = 'Keivan Shah'

# character size of utf-8 character in bits
UTF_CHAR_SIZE = 16


def str_to_bin(data):
    # ENCODE STRING TO BINARY
    bin_data = ""
    for x in str(data):
        text = bin(ord(x))[2:]
        while len(text) % UTF_CHAR_SIZE != 0:
            text = '0' + text
        bin_data += text
    return bin_data


def bin_to_str(data):
    # DECODE BINARY TO STRING
    text = ""
    for i in range(len(data) // UTF_CHAR_SIZE):
        char_byte = data[i * UTF_CHAR_SIZE: (i +1) * UTF_CHAR_SIZE]
        text += chr(int(char_byte, 2))
    return text


def create_blocks(data):
    # convert data to binary
    bin_data = str_to_bin(str(data))

    # convert string to be divisible by size 64
    if len(bin_data) % 64 > 0:
        bin_data += '0' * (64 - len(bin_data) % 64)

    blocks = []

    for i in range(0, len(bin_data) // 64):
        blocks.append(bin_data[i * 64:(i + 1) * 64])

    return blocks


# KEY GENERATION


PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63,
       55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

round_shift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]


def permutate_string(string, permutation):
    if len(string) < max(permutation):
        print(len(string))
        raise Exception("INVALID PERMUTATION")
    else:
        new_key = ""
        for i in permutation:
            new_key += string[i - 1]
        # print(len(new_key))
        return new_key


def shift(s, k):
    return s[k:] + s[:k]


def generate_keys(str_key, string=True):

    if string:
        key = str_to_bin(str_key)
    else:
        key = str_key

    if len(key) < 64:
        raise Exception("INVALID BLOCK SIZE")
    else:
        c, d, keys = {}, {}, {}
        keys[0] = permutate_string(key, PC1)

        c[0] = keys[0][:28]
        d[0] = keys[0][28:]

        for i in range(1, 17):
            c[i] = shift(c[i - 1], round_shift[i - 1])
            d[i] = shift(d[i - 1], round_shift[i - 1])
            keys[i] = permutate_string(c[i] + d[i], PC2)
        return keys


# ENCRYPTION AND DECRYPTION


IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32,
      24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47,
      39, 31, 23, 15, 7]

E_BIT = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20,
         21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

S_BOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

INV_IP = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]


def xor(a, b):
    if len(a) == len(b):
        ans = ""
        for i in range(0, len(a)):
            ans += str(int(a[i], 2) ^ int(b[i], 2))
        return ans
    else:
        raise Exception("XOR Error")


def function_f(right, key):
    e = permutate_string(right, E_BIT)
    ans = xor(key, e)
    ri = ""
    for i in range(0, 8):
        ri += function_s(ans[i * 6:(i + 1) * 6], S_BOX[i])
    return permutate_string(ri, P)


def function_s(s, sbox):
    row = int(s[0] + s[5], 2)
    col = int(s[1:5], 2)
    text = bin(sbox[row][col])[2:]
    while len(text) % 4 != 0:
        text = '0' + text
    return text


def des_encrypt_block(block, key, string=True):
    if len(block) != 64:
        raise Exception("INVALID BLOCK SIZE")
    else:

        keys = generate_keys(key, string)
        r, l = {}, {}
        message = permutate_string(block, IP)

        l[0] = message[:32]
        r[0] = message[32:]

        for i in range(1, 17):
            l[i] = r[i - 1]
            r[i] = xor(l[i - 1], function_f(r[i - 1], keys[i]))

        return permutate_string(r[16] + l[16], INV_IP)


def des_encrypt(data, key, string=True):
    blocks = create_blocks(data)

    encrypted_data = ""

    for block in blocks:
        encrypted_data += des_encrypt_block(block, key, string)

    return encrypted_data


def des_decrypt_block(block, key, string=True):
    if len(block) != 64:
        raise Exception("INVALID BLOCK SIZE")
    else:
        keys = generate_keys(key, string)
        r, l = {}, {}
        message = permutate_string(block, IP)

        l[0] = message[:32]
        r[0] = message[32:]

        for i in range(1, 17):
            l[i] = r[i - 1]
            r[i] = xor(l[i - 1], function_f(r[i - 1], keys[17 - i]))
        return permutate_string(r[16] + l[16], INV_IP)


def des_decrypt(data, key, string=True):
    decrypted_data = ""
    for i in range(0, len(data) // 64):
        decrypted_data += des_decrypt_block(data[i * 64:(i + 1) * 64], key, string)

    return bin_to_str(decrypted_data)


if __name__ == '__main__':
    KEY = '0001001100110100010101110111100110011011101111001101111111110001'

    STRING = "Hello World★"

    STRING_KEY = "BUZZWORD"

    print("ORIGINAL TEXT: " + STRING)

    e = des_encrypt(STRING, STRING_KEY)

    print("ENCRYPTED TEXT: " + e)

    d = des_decrypt(e, STRING_KEY)

    print("DECRYPTED TEXT: " + d)

    e = des_encrypt(STRING, KEY, False)

    print("ENCRYPTED TEXT: " + e)

    d = des_decrypt(e, KEY, False)

    print("DECRYPTED TEXT: " + d)
