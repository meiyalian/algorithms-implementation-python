
def Zalgorithm (str):
    """
         Compute Z value of the str.
         deﬁne Z[i] (for each position i > 1 in str) as the length of the longest substring
         starting at position i of str that matches its prefix

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


def compute_LPS(pat):
    """
           Compute the lps array of a pattern. define each lps[i] as the length of the longest proper suffix
           of pat[1 . . . i] that matches a preﬁx of pat, such that pat[i + 1] != pat[SP i +1].

           Parameters:
           pat(String): the pattern
           Returns:
           int[] : lps array
           Complexity: O(N), N is the length of the pattern
      """
    pat_z = Zalgorithm(pat)
    lps = [0]*len(pat)
    for i in range(len(pat)-1,0,-1):
        index = i + pat_z[i] -1
        lps[index] = pat_z[i]
    return lps
