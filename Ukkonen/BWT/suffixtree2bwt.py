

import sys
sys.path.append('../')
from suffixtree import SuffixTree



def BWT(text):
    """
         Produce Burrows-Wheeler Transform (BWT) of the string using the suffix tree.

          :param text (string)
          :return: bwt (string)
          Time complexity: O(n), n is the length of the text
          Space complexity: O(n), n is the length of the text
    """
    str = text + "$"
    tree = SuffixTree(str)
    tree.build()
    bwt = ""
    sortedIndex = tree.get_leaves()
    for each in sortedIndex:
        bwt += str[each-1]

    return bwt



def main(argv):
    if len(argv)!= 1:
        print("suffixtree2bwt.py <file containing str[1...n]>")
        sys.exit()
    else:
        txt_file = argv[0]
        txt = open(txt_file).read()

        bwt_txt = BWT(txt)
        output = open("output_bwt.txt",mode = 'w')
        output.write(bwt_txt)
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
