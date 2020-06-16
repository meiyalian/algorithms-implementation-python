import heapq
import queue



class Node:
    def __init__(self, freq=None, char=None, left=None, right=None, code=None):
        self.freq = freq #frequence
        self.char = char
        self.left = left
        self.right = right
        self.code = None

    def __lt__(self, other):
        return self.freq < other.freq


class Heap:
    def __init__(self):
        self.heap = []

    def push(self, priority, item):
        heapq.heappush(self.heap, (priority, item)) #push the node to heap

    def pop(self):
        if len(self.heap)>0:
            return heapq.heappop(self.heap)[-1] #first in first out
        else:
            return None


def encode(root, code):
    """
        traverse the heap and set up encoding value for the node
    """
    if root is None:
        return
    if code == '' and root.left is None and root.right is None:
        root.code = '0'
        return
    root.code = code
    encode(root.left, code +  '0')
    encode(root.right, code + '1')

def huffman(chars_count):
    """
        Huffman encoding
        Parameters:
         chars_count: a 128 long int list containing characters and their frequency, the index of each element
         is the ascii code of the char, the value of each element is the frequency of that char
         Returns:
         a dictionary contain the huffman code for each char ( frequency > 0 )

         Time Complexity: O(n) n is the number of unique chars ( number of chars whose count > 0 in chars_count)
    """
    heap = Heap()
    unique_chars = 0

    for i in range(len(chars_count)):
        if chars_count[i] > 0:
            unique_chars +=1
            heap.push(chars_count[i], Node(freq=chars_count[i], char=chr(i)))


    for j in range(unique_chars-1):
        left,right = heap.pop(), heap.pop()
        combine = Node(freq=left.freq + right.freq, char=left.char + right.char, left=left, right=right, code=None)
        heap.push(combine.freq, combine)

    root = heap.pop()
    encode(root, '')
    results = dict()
    q = queue.Queue()
    q.put(root)
    while not q.empty():
        node = q.get()
        if len(node.char) == 1: #leaf node
            results[node.char] = node.code
        if node.left:
            q.put(node.left)
        if node.right:
            q.put(node.right)

    return results
