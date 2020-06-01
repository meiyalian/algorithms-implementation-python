
"""
name: Meiya Lian
studentID: 29617111
"""

import sys
sys.path.append('../')
from suffixtree import SuffixTree


def match_with_wildcard(tree, pat, wild_card_char):
    """
         pattern matching with wildcard character

         :param pat (string), wild_card_char (string)
         :return: leafList(a list stores the starting index of all the matched substring)
         Time complexity: O(n), n is the length of the text
         Space complexity: O(n), n is the length of the text
    """
    if len(pat) == 0:
        return []

    endNodes = []  # all the leaf nodes from these nodes are the leaf nodes of substrings that matches the pattern

    if pat[0] == wild_card_char and len(pat) == 1:
        for each in tree.root.child:
            if each is not None and each.key != "$":
                endNodes.append(each)

    elif pat[0] == wild_card_char:
        for child in tree.root.child:
            if child is not None and child.key != "$":
                match_with_wildcard_aux(tree, pat, 0, child, endNodes, wild_card_char)
    else:
        start_node = tree.root.get_child(pat[0])
        match_with_wildcard_aux(tree, pat, 0, start_node, endNodes, wild_card_char)

    leafList = []
    for node in endNodes:
        # get all the leaf nodes of each node
        tree.get_leaves_aux(node, leafList)
    return leafList


def match_with_wildcard_aux(tree, str, pat_i, node, nodeList, wildCard):
    if node is None:
        return

    else:
        path_length = node.get_end(len(tree.text) - 1) - node.start + 1
        path_index = 0
        pat_index = pat_i
        while pat_index < len(str) and path_index < path_length:
            if str[pat_index] == wildCard and path_index == path_length - 1:
                for each in node.child:
                    if each is not None:
                        match_with_wildcard_aux(tree, str, pat_index + 1, each, nodeList, wildCard)
                return
            if tree.text[node.start + path_index] == str[pat_index] or (
                    str[pat_index] == wildCard and tree.text[node.start + path_index] != "$"):
                pat_index += 1
                path_index += 1

            elif tree.text[node.start + path_index] != str[pat_index]:
                return

        # if pat_index is the length of the pattern, all the leaf nodes from this node are the substring that matches the pattern
        if pat_index == len(str):
            nodeList.append(node)
            return
        else:
            if path_index == path_length:
                next_char = str[pat_index]
                if next_char == "?":
                    for child in node.child:
                        if child is not None:
                            match_with_wildcard_aux(tree, str, pat_index, child, nodeList, wildCard)
                else:
                    start_node = node.get_child(next_char)
                    if start_node is not None:
                        match_with_wildcard_aux(tree, str, pat_index, start_node, nodeList, wildCard)


def main(argv):
    if len(argv)!= 2:
        print("wildcard suffixtree matching.py <text file> <pattern file>")
        sys.exit()
    else:

        txt = open(argv[0]).read()
        tree = SuffixTree(txt + "$")

        pat = open(argv[1]).read()
        tree.build()
        match = match_with_wildcard(tree, pat, "?")
        output = open("output_wildcard_matching.txt", mode='w')
        for value in match:
            output.write(str(value+1) + '\n')

        sys.exit()






if __name__ == "__main__":
    main(sys.argv[1:])






