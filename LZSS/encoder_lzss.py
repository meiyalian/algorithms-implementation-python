
import sys
from bitarray import bitarray
sys.path.append('../')

from task2 import huffman_code
from task2 import LZSS



def elias(integer):
    """
        encoding integer using Elias' code
        Parameter: integer: int
        Return: b'', binary code

        Time Complexity: O(logn) where n is the number of bits of the integer
        Space Complexity: O(1)
    """
    min_binary_code = bitarray(bin(integer)[2:])
    length_component = bitarray()
    L= len(min_binary_code)-1
    if L >=1:
        while L>1:
            encode = bitarray('0') +bitarray( bin(L)[3:])
            length_component = encode + length_component
            L = len(encode)-1

        length_component = bitarray('0')+ length_component
    return length_component + min_binary_code


def LZSS_encoder(txt, W, L):
    """
        encoder implementing LZSS
        Parameter: txt: texts to encode, W: search window size, L: look ahead buffer size
        Return: encoding binary string
    """
    chars_count = [0]*128 # count the appearance of each char
    for i in range(len(txt)):
        chars_count[ord(txt[i])] = chars_count[ord(txt[i])] +1
    huffman_codes = huffman_code.huffman(chars_count)
    unique_char = len(huffman_codes)

    #construct file header
    header = elias(unique_char)
    for char in huffman_codes.keys():
        code = bitarray(huffman_codes[char])
        ascill_char = bitarray(bin(ord(char))[2:])
        if len(ascill_char) <7:
            ascill_char = bitarray('0'*(7-len(ascill_char))) + ascill_char # pad to length 7
        header += ascill_char + elias(len(code)) + code

    #construct file data
    encoder = LZSS.LZSS(txt,W,L)
    encoder.compress()

    data = elias(len(encoder.compressed_msg)) # total number of format (0/1) fields
    for field in encoder.compressed_msg:
        if len(field) == 2:
            data += bitarray('1') + bitarray(huffman_codes[field[1]])

        elif len(field) == 3:
            data += bitarray('0') + elias(field[1]) + elias(field[2])

    return header + data

def pack_to_bytes(binary_str):
    """
        packing the binary string into bytes
        Parameter: binary_str: binary string
        Return: byte array
        Time Complexity: O(n), n is the length of the binary string
    """
    bytes_arr = bytearray()
    pointer = 0
    while pointer < len(binary_str):
        if pointer+7 > len(binary_str)-1:
            byte = binary_str[pointer:]
            padding = bitarray((8 - len(byte))*'0')
            byte = byte + padding
            bytes_arr += byte.tobytes()
            break
        else:
            byte = binary_str[pointer:pointer+8]

            bytes_arr += byte.tobytes()
            pointer +=8
    return bytes_arr

def main(argv):
    if len(argv) != 3:
        print("encoder lzss.py <input text file> <W> <L>")
        sys.exit()
    else:
        try:
            txt = open(argv[0]).read()
            W = int(argv[1])
            L = int(argv[2])
        except ValueError:
            print("encoder lzss.py <input text file> <W> <L>")
            sys.exit()

        compressed_binary = LZSS_encoder(txt,W,L)
        bytes = pack_to_bytes(compressed_binary)
        with open('output_encoder_lzss.bin', 'wb') as output:
            output.write(bytes)


if __name__ =="__main__":

    main(sys.argv[1:])
