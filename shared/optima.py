import random
import base64

def optima_encode(text_blocks: list[str], seed: str = "") -> str:
    # Encode text blocks
    optima_ints = []
    for block in text_blocks:
        optima_ints += string_to_optima(block, seed) + [SEP]
    # Add seed (it is encoded with seed 0 so it can be decoded)
    optima_ints += string_to_optima(seed, 0)
    # Convert to bits
    optima_bits = optima_to_bits(optima_ints)
    # Now we have all our binary as bits, but it might end in a partial byte
    pad_bits_len = (8 - len(optima_bits) % 8) % 8
    # if we need >5 pad bits, add a SEP to pad first (this will be decoded and dropped)
    if pad_bits_len >= 5:
        pad_char_bits = optima_to_bits([SEP])
        optima_bits += pad_char_bits
        pad_bits_len -= 5
    # now pad with 0s, these won't be decoded (since we decode %5)
    optima_bits += [False] * pad_bits_len

    optima_bytes = bits_to_bytes(optima_bits)
    return base64.urlsafe_b64encode(optima_bytes).decode('ascii')


def optima_decode(optima_string: str):
    import logging
    print(optima_string)
    all_bytes = base64.urlsafe_b64decode(optima_string)
    all_bits = bytes_to_bits(all_bytes)

    # drop pad bits
    if (len(all_bits) % 5) != 0:
        all_bits = all_bits[:-(len(all_bits) % 5)]

    # get optima string
    optima_ints = bits_to_optima(all_bits)

    # drop pad optima
    if optima_ints[-1] == SEP:
        optima_ints = optima_ints[:-1]

    # split by SEP
    optima_blocks = [[]]
    for opt in optima_ints:
        if opt == SEP:
            optima_blocks.append([])
        else:
            optima_blocks[-1].append(opt)

    
    # final block is the seed, which uses the default scramble
    seed_ints = optima_blocks[-1]
    seed = optima_to_string(seed_ints, 0)

    decoded_blocks = [optima_to_string(block, seed) for block in optima_blocks[:-1]]
    return decoded_blocks, seed
        


# These are the only acceptable leters in my names = 31 options, i.e. can fit 2 numbers in base-64
# Has 2 extra options for SEP
SEP = 31
optima_code = "abcdefghijklmnopqrstuvwxyz -'&!"

def shuffled_optima(seed: str) -> dict:
    my_ran = random.Random()
    my_ran.seed(seed)
    my_optima = list(optima_code)
    my_ran.shuffle(my_optima)
    return my_optima

def string_to_optima(block: str, seed: str) -> list[int]:
    decoder = shuffled_optima(seed)
    encoder = dict([(c, i) for i, c in enumerate(decoder)])

    block_text = block.lower()
    block_ints = [encoder[c] for c in block_text]
    return block_ints

def optima_to_string(block_ints: list[int], seed: str) -> str:
    decoder = shuffled_optima(seed)
    return ''.join([decoder[c] for c in block_ints])

def bits_to_optima(optima_bits: list[bool]) -> list[int]:
    assert len(optima_bits) % 5 == 0, "bad bit length"

    optima_chars = list()
    for opt_idx in range(0, len(optima_bits), 5):
        chunk = optima_bits[opt_idx:opt_idx + 5]
        optima_chars.append(b5_to_optima(chunk))
    return optima_chars

def optima_to_bits(optima_32s: list[int]) -> list[bool]:
    bit_list = list()
    for opt in optima_32s:
        bit_list += optima_to_b5(opt)
    return bit_list


def optima_to_b5(optima: int) -> list[bool]:
    assert optima < 32, "bad optima char"
    return [
        optima % 2 >= 1,
        optima % 4 >= 2,
        optima % 8 >= 4,
        optima % 16 >= 8, 
        optima >= 16
    ]


def b5_to_optima(b5: list[bool]) -> int:
    return sum([b * n for b, n in zip(b5, [1, 2, 4, 8, 16])])


def bytes_to_bits(data_bytes: bytes) -> list[bool]:
    # Looping decodes to ints
    bits = []
    for byte in data_bytes:
        bits += [
            byte % 2 >= 1,
            byte % 4 >= 2,
            byte % 8 >= 4,
            byte % 16 >= 8, 
            byte % 32 >= 16,
            byte % 64 >= 32,
            byte % 128 >= 64,
            byte >= 128 
        ]
    return bits
    
def bits_to_bytes(bits: list[bool]) -> bytes:
    assert len(bits) % 8 == 0, "invalid bit count"
    byte_chunks = []
    for bit_idx in range(0, len(bits), 8):
        b8 = bits[bit_idx:bit_idx+8]
        byte_chunks.append(sum([b * n for b, n in zip(b8, [1, 2, 4, 8, 16, 32, 64, 128])]))


    return bytes(byte_chunks)