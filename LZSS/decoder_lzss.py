import sys

class LZSSDecoder:
    def __init__(self, read_file):
        self.source = open(read_file,"rb") # source file
        self.current_byte = ''
        self.decoded_msg = ''
        self.bit_pointer = 0 # current bit
        self.dictionary = dict() # dictionary for storing the huffman encoding
        # read in 1 byte
        self.get_next_byte()


    def decode(self):
        """
           decode the body of the file
        """
        self.process_header()
        num_of_fields = self.decoding_elias()
        for _ in range(num_of_fields):
            first_bit = self.get_next_bit()
            if first_bit == '1':
                code = self.get_next_bit()
                decoded_char = self.dictionary.get(code,None)
                while decoded_char is None:
                    code += self.get_next_bit()
                    decoded_char = self.dictionary.get(code,None)
                self.decoded_msg += decoded_char

            elif first_bit == '0':
                offset = self.decoding_elias()
                length = self.decoding_elias()
                start_pointer = len(self.decoded_msg)-offset
                for _ in range (length):
                    self.decoded_msg += self.decoded_msg[start_pointer]
                    start_pointer +=1


    def process_header(self):
        """
            process the header to get the huffman encoding of the file
        """
        unique_chars = self.decoding_elias() # number of unique characters

        for _ in range(unique_chars):
            char_code = ''
            for _ in range(7):
                char_code += self.get_next_bit()

            char = chr(int(char_code,2)) #get char
            huffman_code = ''
            huffman_length = self.decoding_elias() # get length of the following huffman

            #get huffman code of the char
            for _ in range(huffman_length):
                huffman_code += self.get_next_bit()

            self.dictionary[huffman_code] = char


    def decoding_elias(self):
        """
            decode a number encoded by elias code
        """

        read_length = 1
        component = self.get_next_bit()
        while component[0] != '1':
            read_len_bin = '1'
            if len(component) >1:
                read_len_bin += component[1:]
            read_length = int(read_len_bin,2) +1

            component = ''
            for _ in range(read_length):
                component += self.get_next_bit()

        return int(component,2)



    def get_next_byte(self):
        """
            read in one byte from source
        """
        byte = self.source.read(1)
        if len(byte) == 0:
            self.current_byte = ''
        else:
            bits = bin(byte[0])[2:] # when convert int to binary string, it might not be 8 bits
            left_padding = (8-len(bits))*'0' # pad to make each byte 8 bits
            self.current_byte = left_padding + bits

    def get_next_bit(self):
        """
            read next bit from the current byte
        """
        if self.has_read_all():
            return ''
        else:
            bit = self.current_byte[self.bit_pointer]
            if self.bit_pointer == 7: # prepare for the next read
                self.get_next_byte()
                self.bit_pointer = 0
            else:
                self.bit_pointer +=1 # point to next bit of the current byte
            return bit


    def has_read_all(self):
        """
            check if we have process all the bytes in the source file
        """
        if self.current_byte == '':
            self.source.close()
            return True
        return False


def main(argv):
    if len(argv) != 1:
        print("decoder lzss.py <output encoder lzss.bin>")
        sys.exit()
    else:
        decoder = LZSSDecoder(argv[0])
        decoder.decode()
        with open('output_decoder_lzss.txt', 'w') as output:
            output.write(decoder.decoded_msg)


if __name__ =="__main__":

    main(sys.argv[1:])
    # decoder = LZSSDecoder("output_encoder_lzss.bin")
    # decoder.decode()
    # with open('output_decoder_lzss.txt', 'w') as output:
    #     output.write(decoder.decoded_msg)
    #
    # msg = open("input.txt", "r").read()
    # print(decoder.decoded_msg == msg)
