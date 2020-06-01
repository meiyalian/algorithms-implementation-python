import sys

def mirroredBoyerMoore(txt, pat):
    """
       mirrored version of Boyer Moore string searching

       Parameters:
        txt (String): text strings
        pat (String): pattern string

       Returns:
       int[] : an array of starting index in the text that matches the pattern

       Complexity:
       N is the length of text, M is the length of pattern
        best: O(N/M)
        worst: O(M+N)
       """
    if len(pat) > len(txt):
        return []

    pat_index = 0
    txt_index = len(txt) - len(pat)
    matched = []

    z_pat = Zalgorithm(pat)
    shift_table = shiftTable(pat)
    good_prefix = goodPrefix(pat,z_pat)
    matched_suffix = matchedSuffix(pat,z_pat)

    start_index = txt_index # starting index of txt to compare with pat[0...m]
    known_chars = 0 # number of charaters to skip during comparison
    known_chars_start = -1 #starting index of the skipping known characters
    while txt_index >=0:
        while pat_index + known_chars <= len(pat) and txt_index>=0 :

            if pat_index == known_chars_start: # apply galil's optimazation
                pat_index += known_chars
                txt_index += known_chars
                known_chars = 0
                known_chars_start =-1

            if pat_index == len(pat):  # if fully matched
                matched.append(start_index)
                if len(pat) >= 2:  # if pattern length is greater than 1, look at ms[-2] find the max shift
                    known_chars = matched_suffix[-2]
                    txt_index = start_index - (len(pat) - matched_suffix[-2])
                    known_chars_start = len(pat) - known_chars

                if len(pat) < 2:  # if pattern length is 1, compare naively
                    known_chars = 0
                    txt_index = start_index - 1
                start_index = txt_index
                pat_index = 0
                if start_index <0:
                    break

            if pat[pat_index] == txt[txt_index]: #if match
                pat_index +=1
                txt_index +=1

            else: # if mismatch
                bad_char = txt[txt_index]
                bad_char_index = shift_table[ord(bad_char)][pat_index]
                bad_char_skip = max(1, bad_char_index - pat_index)
                good_prefix_skip = good_prefix[pat_index-1]

                if good_prefix_skip == 0: # if good_prefix is 0, apply matched suffix
                    matched_suffix_skip = len(pat) - matched_suffix[pat_index - 1]
                    skip = max(matched_suffix_skip, bad_char_skip)
                    if matched_suffix_skip >= bad_char_skip:
                        known_chars = len(pat) - skip
                        known_chars_start = matched_suffix_skip

                else:
                    skip = max(bad_char_skip, good_prefix_skip) # skip max( bad_char, good_prefix)
                    if good_prefix_skip >= bad_char_skip:
                        known_chars = pat_index
                        known_chars_start = good_prefix_skip
                    else:
                        known_chars = 0
                        known_chars_start = -1
                txt_index = start_index - skip
                start_index = txt_index
                pat_index =0

    return matched

def shiftTable (pat):
    """
       compute shift table of pat to apply bad character shift
       Parameters:
       pat (String): pattern string
       Returns:
       int[]: a 2D array, table[i][k] represents the left most position of chr(i) from index k

       Complexity: O(M) , M is the length of pattern

       """
    table = []
    for i in range (256):
        table.append ([-1]*(len(pat)))

    for j in range (len(pat)):
        pos_i = ord(pat[j])
        table[pos_i][j] = j

    for i in range(256):
        for j in range (len(pat)-2,-1,-1):
            if table[i][j] < table[i][j+1] and table[i][j] == -1:
                table[i][j] = table[i][j+1]
    return table

def goodPrefix(pat,z_pat):
    """
       Compute good prefix value of a string using its z value.

       Parameters:
       pat (String): pattern string
       z_pat ( int[]) : Z values of pat

       Returns:
       int[]: gs[i] stores the left most starting index of a substring that matches the prefix of P[0..i]
              for gp[-1], it should've be the length of the pattern. However, I modify it and store the starting index from pat [0..m]
              that doesn't match pat[0] to use in the case of a mismatching happens in pat[0].
              ( when a mismatch happened in index x, it will always go to gp[x-1] to look for
              its good prefix value. )

       Complexity: O(M), M is the inout string length

       """
    good_prefix = [0]*len(pat)
    is_not_prefix = len(pat)
    for i in range(len(pat)-1,-1,-1):
        index = z_pat[i]-1
        good_prefix[index] = i
        if z_pat[i] == 0 and i>0:
            is_not_prefix = i

    good_prefix[-1] = is_not_prefix
    return good_prefix


def matchedSuffix(pat, z_pat):
    """
       Compute matched suffix value of a string using its z value.

       Parameters:
       pat (String): pattern string
       z_pat ( int[]) : Z values of pat

       Returns:
       int[]: ms[i] stores the length of the longest suffix of P that matches the prefix of P[0..i]

       Complexity: O(M)

       """
    z = z_pat
    z[0] = len(pat)
    ms = [0] * len(pat)

    for i in range(len(pat)):
        if z[i] + i == len(pat):
            ms[z[i] - 1] = z[i]

    for i in range(1, len(pat)):
        if ms[i] == 0:
            ms[i] = ms[i - 1]

    return ms


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
        print("mirrored_boyermoore.py <text file> <pattern file>")
        sys.exit()
    else:
        txt_file = argv[0]
        pat_file = argv[1]
        txt = open(txt_file).read()
        pat = open(pat_file).read()

        matched_patterns = mirroredBoyerMoore(txt,pat)
        output = open("q1/output_mirrored_boyermoore.txt",mode = 'w')
        if matched_patterns >0:

            for index in matched_patterns[::-1]:
                output.write(str(index+1) +'\n')
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
