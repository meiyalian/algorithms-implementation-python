import sys


def spTable (pat):
    """
         Compute sp table for pat

         Parameters:
         pat (String): the target string

         Returns:
         int[] : a 2d array, table[i][j] denotes the right most position of chr(i) from pat[j]

         Complexity: O(M), M is the length of the str

         """
    sp_arr = []
    z = Zalgorithm(pat)
    for i in range(256):
        sp_arr.append([0]*len(pat))

    for i in range(len(pat)-1,0,-1):
        index = i + z[i]-1
        char = pat[z[i]]
        sp_arr[ord(char)][index] = z[i]

    return sp_arr


def KMP(txt,pat):
    """
         modified kmp search function

          Parameters:
                txt (String): text strings
                pat (String): pattern string

          Returns:
                int[] : an array of starting index in the text that matches the pattern

        Complexity:
                worst case O(M+N), M is pattern length and N is the text length

         """
    matched = []
    pat_len = len(pat)
    txt_len = len(txt)
    sp = spTable(pat)
    txt_index = 0
    pat_index = 0

    while txt_index < txt_len :
        if pat[pat_index] == txt[txt_index]:
            pat_index += 1
            txt_index += 1

        if pat_index == pat_len:
            matched.append(txt_index - pat_index)
            if txt_index < txt_len :
                pat_index = sp[ord(txt[txt_index])][pat_index-1] # find the right most position in the pat that
                # matches to the current corresponding text character


        elif txt_index < txt_len and pat[pat_index] != txt[txt_index]:

            if pat_index != 0:
                shift = sp[ord(txt[txt_index])][pat_index-1]
                pat_index = sp[ord(txt[txt_index])][pat_index-1]

                if shift > 0:
                    pat_index +=1
                    txt_index += 1
                    if pat_index == pat_len:
                        matched.append(txt_index - pat_index)
                        if txt_index < txt_len:
                            pat_index = sp[ord(txt[txt_index])][pat_index - 1]
            else:
                txt_index += 1
    return matched


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
        print("modified_kmp.py <text file> <pattern file>")
        sys.exit()
    else:
        txt_file = argv[0]
        pat_file = argv[1]
        txt = open(txt_file).read()
        pat = open(pat_file).read()

        matched_patterns = KMP(txt,pat)
        output = open("q3/output_kmp.txt",mode = 'w')
        if matched_patterns >0:

            for index in matched_patterns:
                output.write(str(index+1) +'\n')
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
