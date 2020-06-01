import sys

def wildCharSearch(txt,pat,wild_char):
    """
         string matching with wild card character

          Parameters:
                txt (String): text strings
                pat (String): pattern string
                wild_char (String): wild card character

          Returns:
                int[] : an array of starting index in the text that matches the pattern

        Complexity:
                N is the length of text, M is the length of pattern
                best case: O(M/N) when no charaters in pat matches the whole text
                worst case:  O(MN)
         """
    matched = []
    shiftTable = shiftTableWithWildChar(pat,wild_char)
    shift = 0
    pat_len = len(pat)
    txt_len = len(txt)

    while shift <= (txt_len-pat_len):
        pat_index = pat_len-1
        while pat_index >= 0 and (pat[pat_index] == txt[shift+pat_index] or pat[pat_index] == wild_char) :
            pat_index -=1
        if pat_index < 0: #when fully matched
            matched.append(shift)
            if txt_len > shift+pat_len:
                shift = shift + pat_len - shiftTable[ord(pat[0])][pat_index] #shift the pat to allign with txt_index that corresponding to the last occurance of pat[0]in pat[0..m]
            else:
                shift +=1
        else:
            mismatch = txt[shift+pat_index]
            shift += max(1, pat_index - shiftTable[ord(mismatch)][pat_index])
    return matched



def shiftTableWithWildChar(pat, wild_char):
    """
       compute shift table of pat considering wild card character


       Parameters:
       pat (String): pattern string
       wild_char (String): wild card character

       Returns:
       int[]: a 2D array, table[i][k] represents the right most position of chr(i) from index k considering wild card char

       Complexity: O(M) , M is the length of pattern
"""

    table = []
    for i in range (256):
        table.append ([-1]*len(pat))

    wild_char_val = ord(wild_char)
    for j in range (len(pat)):
        pos_i = ord(pat[j])

        if pos_i == wild_char_val:
            for i in range (256):
                table[i][j] = j
        else:
            table[pos_i][j] = j

    for i in range(256):
        for j in range (1,len(pat)):
            if table[i][j-1] > table[i][j]:
                table[i][j] = table[i][j-1]
    return table


def Zalgorithm (str):
    """
         Compute Z value of the str

         Parameters:
         str (String): the target string

         Returns:
         int[] : a list of Z values for the input string

         Complexity: O(N), N is the length of the str

         """
    Z = [0]*len(str)
    l = 0
    r = 0
    for i in range (1, len(str)):
        if i > r:
            l = i
            r = i
            while r < len(str) and str[r] == str[r-i]:
                r += 1
            r -= 1
            Z[i] = r-l+1
        else:
            if Z[i-l] < r-i+1:
                Z[i] = Z[i-l]
            else:
                l = i
                r = i+1
                while r < len(str) and str[r] == str[r-i]:
                    r +=1
                r -=1
                Z[i] = r -l +1
    return Z


def main(argv):
    if len(argv)!= 2:
        print("wildcard_matching.py <text file> <pattern file>")

        sys.exit()
    else:

        txt_file = argv[0]
        pat_file = argv[1]

        txt = open(txt_file).read()
        pat = open(pat_file).read()

        matched_patterns = wildCharSearch(txt,pat, "?")
        output = open("q2/output_wildcard_matching.txt",mode = 'w')
        if matched_patterns >0:

            for index in matched_patterns:
                output.write(str(index+1) +'\n')

        sys.exit()



if __name__ == "__main__":
    main(sys.argv[1:])
