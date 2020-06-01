
import sys
import math
class Node:
    def __init__(self,key,parent, start,end):
        self.parent = parent
        self.start = start
        self.end = end
        self.suffixlink = None
        self.child = []
        self.index = -1 #only leaf node will contain proper index, indicating the start index of the suffix
        self.key = key
        for i in range (256):
            self.child.append(None)

        self.depth = -1
        self.parents_sparse = []
        if parent is not None:
            self.parents_sparse.append(parent)
        self.prefix_length = 0


    def to_string(self):
        return "{key: " + self.key +  " start: " + str(self.start) \
               + " end: " + str(self.end) +  " depth: " + str(self.depth) + " index: " + str(self.index) + "sparse: " + \
               str(self.parents_sparse) + " }"

    def get_child(self, char):
        return self.child[ord(char)]

    def set_child(self, node):
        self.child[ord(node.key)] = node

    def get_end(self, current_phase):
        if self.end == '#':
            return current_phase
        else:
            return self.end



class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.root = Node('', None, None, None)
        self.root.index = -1
        self.number_of_nodes = 1
        self.max_depth = 0

        # for building suffix tree
        self.active_node = self.root
        self.active_edge = None
        self.active_length = 0  # remainder
        self.leafList = [None]*len(self.text)


    def build(self):
        """
        Implementation of the Ukkonen's algorithm to build the suffix tree

        :param None
        :return: None
        Time complexity: O(n), n is the length of the text
        Space complexity: O(n)
        """
        remaining = 0

        # start phase
        for i in range (len(self.text)):
            remaining +=1
            last_created_internal_node = None
            char = self.text[i]

            while remaining > 0:

                #if active length is 0, start building from root
                if self.active_length == 0:
                    node = self.root.get_child(char)

                    if node is not None:
                        # get the active path
                        self.active_length +=1
                        self.active_edge = node.start # set the right direction
                        break

                    elif node is None:
                        # create new node
                        new_node = Node(char, self.active_node, i, '#')
                        self.number_of_nodes +=1

                        self.active_node.set_child(new_node)
                        remaining -=1

                elif self.active_length > 0:

                    # find if the next char of the path from active node to direction active_edge with length active_length is equal to char
                    next_char = self.get_next_char(i)
                    if next_char != None:
                        # #rule3 extenion
                        if next_char == char:
                            if last_created_internal_node is not None:
                                last_created_internal_node.suffixlink = self.active_node.get_child(self.text[self.active_edge])
                            self.update_active_node(i)
                            break

                        #create a new internal node and a new leaf node (rule 2)
                        else:
                            node = self.active_node.get_child(self.text[self.active_edge])
                            new_internal = Node(node.key,self.active_node, node.start, node.start + self.active_length-1)


                            node.start = node.start + self.active_length
                            node.parent = new_internal
                            node.key = self.text[new_internal.start+ self.active_length]


                            new_internal.set_child(node)

                            new_leaf = Node(char, new_internal, i, '#')


                            new_internal.set_child(new_leaf)

                            self.active_node.set_child(new_internal)

                            if last_created_internal_node is not None:
                                last_created_internal_node.suffixlink = new_internal

                            last_created_internal_node = new_internal
                            new_internal.suffixlink = self.root

                            self.number_of_nodes +=2

                            if self.active_node != self.root:
                                self.active_node = self.active_node.suffixlink
                            else:
                                self.active_edge +=1
                                self.active_length -=1

                            remaining -=1


                    #already has an internal node, only create a new leaf node ( rule 2 case 2 )
                    elif next_char is None:
                        node = self.active_node.get_child(self.text[self.active_edge])
                        new_leaf = Node(char, node, i, '#')

                        node.set_child(new_leaf)

                        self.number_of_nodes +=1
                        if last_created_internal_node is not None:
                            last_created_internal_node.suffixlink = node

                        last_created_internal_node = node

                        if self.active_node != self.root:
                            self.active_node = self.active_node.suffixlink
                        else:
                            self.active_edge += 1
                            self.active_length -= 1
                        remaining -=1

        # set the starting index of every substring in the leave nodes.
        self.set_index()
        # set depth for each node
        self.setDepth(self.root,0)
        # set prefix length for each node (for task3)
        self.find_prefix_length(self.root)
        self.fill_sparse_list()
        self.set_leaves_list()


    # implement skip/count trick
    def get_next_char(self, current_phase):
        """
        get the next character of the current path

        :param current_phase (int)
        :return: a character, or None if the path is reaching
                 the end which means rule 2 case 2 will happen

        """
        direction_char = self.text[self.active_edge]
        start_node = self.active_node.get_child(direction_char)
        difference = start_node.get_end(current_phase) - start_node.start

        if difference >= self.active_length:
            next_char_index = start_node.start + self.active_length
            return self.text[next_char_index]

        if difference == self.active_length -1:
            if start_node.get_child(self.text[current_phase]) is not None:
                return self.text[current_phase]

            # rule 2 case 2 will return None in this case
            else:
                return None
        else:
            self.active_node = start_node
            self.active_length =self.active_length -  difference-1
            self.active_edge += difference +1
            return self.get_next_char(current_phase)



    def update_active_node(self, current_phase):
        """
        this method is called when rule 3 extension happened, update the active node if there is a skip

        :param current_phase (int)
        :return: None

        """
        current_node = self.active_node.get_child(self.text[self.active_edge])
        difference = current_node.get_end(current_phase) - current_node.start

        if difference < self.active_length:
            self.active_node = current_node
            self.active_length -= difference
            self.active_edge = current_node.get_child(self.text[current_phase]).start
        else:
            self.active_length +=1


    def set_index(self):
        """
             set the index for each leaf node in the tree, the index value is the starting index
             of each suffix

             :param: None
             :return: None

        """
        for node in self.root.child:
            if node is not None:
                self.set_index_aux(node, 0)

    def set_index_aux(self, node, length):
        if node is None:
            return

        length += node.get_end(len(self.text) - 1) - node.start + 1
        if node.end == "#":
            node.index = len(self.text) - length


        for child in node.child:
            self.set_index_aux(child, length)


    def get_all_nodes(self):
        """
             get all the nodes of the tree

             :param: None
             :return: nodes ( a list of node objects)

        """
        nodes = [self.root]
        for node in self.root.child:
            self.get_all_nodes_aux(node, nodes)
        return nodes

    def get_all_nodes_aux(self, node, aList):
        if node is None:
            return
        else:
            if not node in aList:
                aList.append(node)
            for child_node in node.child:
                self.get_all_nodes_aux(child_node, aList)

    def find_all_match(self, pat):
        """
           pattern matching (without wildcard character)

           :param: pat (string)
           :return: match (a list containing the starting index of each matched substring)

        """
        assert len(pat) > 0 and len(pat) <= len(self.text)
        current_node = self.root.get_child(pat[0])
        pat_index = 0
        while current_node is not None:
            path_length = current_node.get_end(len(self.text) - 1) - current_node.start + 1
            path_index = 0
            while pat_index < len(pat) and path_index < path_length:
                if self.text[current_node.start+path_index] == pat[pat_index]:
                    path_index +=1
                    pat_index +=1
                else:
                    break

            if pat_index == len(pat):
                break
            else:
                current_node = current_node.get_child(pat[pat_index])

        if pat_index < len(pat): # no match found
            return []
        else:
            match = []
            self.get_leaves_aux(current_node, match)
            return match

    def set_leaves_list(self,node):
        if node is None:
            return
        if node.end == "#":
            self.leafList[node.index] = node
        else:
            for child in node.child:
                self.get_leaves_aux(child)

    def get_leaves(self):
      """
       get all the leaves node of the tree
         :param node (Node), aList (the list to store the leaves nodes found)
         :return: None

      """
      leaves = []
      for node in self.root.child:
        self.get_leaves_aux(node, leaves)
      return leaves


    def get_leaves_aux(self, node, aList):
        """
             get all the leaves node of a node

             :param node (Node), aList (the list to store the leaves nodes found)
             :return: None

        """
        if node is None:
            return
        if node.end == "#":
            aList.append(node.index)
        else:
            for child in node.child:
                self.get_leaves_aux(child, aList)

    def setDepth(self, node, depth):
        """
               set the depth for each node and set the maximum depth of the tree

               :param node (Node), depth(int)
               :return: None

          """
        if node is not None:
            node.depth = depth
            if node.depth > self.max_depth:
                self.max_depth = node.depth
            for each in node.child:
                self.setDepth(each,depth+1)

    def find_prefix_length(self,node):
        if node is not None and node != self.root:

            if node.parent == self.root:
                node.prefix_length = node.get_end(len(self.text) - 1) - node.start + 1
            else:
                node.prefix_length = node.parent.prefix_length + node.get_end(len(self.text) - 1) - node.start + 1

        if node is not None:
            for child in node.child:
                self.find_prefix_length(child)


    def fill_sparse_list(self):
        for i in range (1,math.ceil(math.log(self.max_depth, 2))):
            self.fill_sparse_list_aux(self.root,i)

    def fill_sparse_list_aux(self,node,i):
        if node is not None:
            if node != self.root:
                parent_node = node.parents_sparse[i-1]
                if parent_node != self.root:
                    node.parents_sparse.append(parent_node.parents_sparse[i-1])
        if node is not None:
            for child in node.child:
                self.fill_sparse_list_aux(child,i)


if __name__ == "__main__":
    tree = SuffixTree("mississipps$")
    tree.build()
    nodes = tree.get_all_nodes()
    for each in nodes:
        print(each.to_string())
    print(len(nodes))
    print(tree.max_depth)
    print(math.ceil(math.log(tree.max_depth, 2)))
