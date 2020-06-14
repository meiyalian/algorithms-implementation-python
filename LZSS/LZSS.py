
import sys
sys.path.append('../')
from .pre_processing import compute_LPS



class LZSS:
    def __init__(self, txt,W,L):
        self.txt = txt
        self.search_window_size = W
        self.buffer_size = L
        self.buffer_pointer = 0 # start of buffer
        self.compressed_msg = []
        self.move = 0

    def  is_buffer_empty(self):
        """
            check if the look ahead buffer is empty
        """
        return self.buffer_pointer + self.move > len(self.txt) - 1

    def shift_window(self):
        """
          shift the look ahead buffer
        """
        self.buffer_pointer += self.move


    def set_next_move(self, match_length):
        """
            set up the next movement for the look ahead buffer
        """
        if match_length ==0:
            self.move = 1
        else:
            self.move = match_length

    def compress(self):
        """
            compress the input txt
        """
        while not self.is_buffer_empty():
            self.shift_window()
            (offset, match_length) = self.find_max_match() # find the max match from the search window
            self.set_next_move(match_length)
            if match_length < 3: #if match less than 3, produce format 1 field
                if match_length ==0:
                    self.compressed_msg.append((1,self.txt[self.buffer_pointer]))
                for i in range(match_length):
                    self.compressed_msg.append((1,self.txt[self.buffer_pointer+i]))
            else:
                #if match greater than 3, produce format 0 field
                self.compressed_msg.append((0, offset, match_length))

    def buffer_window(self):
        """
            return the current look ahead buffer window
        """
        end = self.buffer_pointer + self.buffer_size
        if end > len(self.txt):
            return self.txt[self.buffer_pointer:len(self.txt)]

        else:
            return self.txt[self.buffer_pointer:end]

    def search_window(self):
        """
            return the current search window
        """
        start = self.buffer_pointer - self.search_window_size
        if start < 0:
            return self.txt[0:self.buffer_pointer]
        return self.txt[start: self.buffer_pointer]

    def find_max_match(self):
        """
            using kmp to find the maximum match of the look ahead buffer from the search window
        """
        buffer_win = self.buffer_window()
        search_win = self.search_window()
        search_area = search_win + buffer_win

        lps = compute_LPS(buffer_win)
        prev_match = 0 #starting index of the previous match
        max_match_length = 0 # maximum match length start at index prev_match
        current_match_length = 0
        match_start = 0 # starting index of the current match

        pat_index = 0
        txt_index = 0
        while match_start <= len(search_win)-1 and txt_index < len(search_area): #search within the search window
            if buffer_win[pat_index] == search_area[txt_index]:
                pat_index +=1
                txt_index +=1
                current_match_length +=1

            if current_match_length >= max_match_length: # if current match is greater than the previous match
                prev_match = match_start
                max_match_length = current_match_length

            if pat_index == len(buffer_win): # if fully match
                if txt_index< len(search_area):
                    pat_index = lps[-1]
                    match_start = txt_index - pat_index

                current_match_length = 0

            elif txt_index < len(search_area) and buffer_win[pat_index] != search_area[txt_index]:
                if pat_index != 0:
                    pat_index = lps[pat_index-1]
                    match_start = txt_index - pat_index
                    current_match_length = lps[pat_index-1]
                else:
                    txt_index +=1
                    match_start = txt_index
                    current_match_length = 0

        offset = len(search_win) - prev_match # offset of the starting index of the match from the look ahead buffer
        return offset, max_match_length
