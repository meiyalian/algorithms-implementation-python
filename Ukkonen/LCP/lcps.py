
import math
import sys
sys.path.append('../')
from suffixtree import SuffixTree


#index start from 0
def find_LCP(tree,  index_1, index_2):
    """
      find the longest common prefix of tree.text[index_1:] and tree.text[index_2:]

       :param index_1 (int), index_2 (int)
       :return: LCP (int)
       Time complexity: O(h), h is the maximum depth of the suffix tree
       Space complexity: O(1)
    """

    if index_1 > len(tree.text) -1 or index_2 > len(tree.text) -1 :
        return 0

    node_A = tree.root
    node_B = tree.root


    max_travel_length = len(tree.text) - max(index_1,index_2)

    LCP = 0
    index = 0
    while index < max_travel_length:
        node_A = node_A.get_child(tree.text[index_1+ index])
        node_B = node_B.get_child(tree.text[index_2+ index])

        if node_A != node_B: #node in the previous iteration is their LCA
            return LCP
        else:
            path_length = node_A.get_end(len(tree.text) - 1) - node_A.start + 1
            LCP += path_length
            index += path_length

    # ignore the count of "$"
    if node_A.end == "#":
        LCP -= 1
    return LCP


def find_LCP_optimal(tree, index1, index2):
    level = math.ceil(math.log(tree.max_depth, 2))
    leaf_1 = tree.leafList[index1]
    leaf_2 = tree.leafList[index2]

    if leaf_1.depth > leaf_2.depth:
        leaf_1 = leaf_1.parents_sparse[leaf_1-leaf_2]

    for i in range(level-1, -1,-1 ):
        if leaf_1.parents_sparse[i]!= leaf_2.parents_sparse[i]:
            leaf_1 = leaf_1.parents_sparse[i]
            leaf_2 = leaf_2.parents_sparse[i]

    return leaf_1.parents_sparse[0]





def main(argv):
    if len(argv)!= 2:
        print("lcps.py <string file> <pairs file>")
        sys.exit()
    else:
        txt_file = argv[0]
        txt = open(txt_file).read()
        tree = SuffixTree(txt+"$")
        tree.build()

        pairs_file = open(argv[1])
        output_file = open("output_lcps.txt",mode = 'w')
        while True:
            pairstr = pairs_file.readline()
            if len(pairstr) == 0:
                break
            pair = pairstr.split()

            # the input file assume a string index start with 1 whereas in the program the index start with 0.
            # Hence each index need to minus 1
            LCP = find_LCP(tree, int(pair[0]) - 1, int(pair[1]) - 1)
            output_file.write(pair[0] + " " + pair[1] + " " + str(LCP) + "\n")

        sys.exit()



# def buildSparseTable(tree):
#     leaves = tree.get_leaves()
#     level = math.ceil(tree.number_of_nodes)
#     table = []
#     for i in range (len(leaves)):
#         table.append([-1] * level)
#     for leaf in leaves:
#         table[leaf.index][]
#





if __name__ == "__main__":
    main(sys.argv[1:])
