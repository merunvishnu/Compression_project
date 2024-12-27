import heapq
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    def calculate_frequencies(self, data):
        frequency = {}
        for byte in data:
            if byte in frequency:
                frequency[byte] += 1
            else:
                frequency[byte] = 1
        return frequency

    def build_heap(self, frequency):
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(self.heap, node)

    def build_tree(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)
        return self.heap[0]

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_codes[current_code] = root.char
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = self.build_tree()
        self.make_codes_helper(root, "")

    def compress(self, input_file):
        with open(input_file, 'rb') as file:
            data = file.read()

        frequency = self.calculate_frequencies(data)
        self.build_heap(frequency)
        self.make_codes()

        compressed_data = ''.join([self.codes[byte] for byte in data])
        extra_padding = 8 - len(compressed_data) % 8
        compressed_data += '0' * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        compressed_data = padded_info + compressed_data

        byte_array = bytearray()
        for i in range(0, len(compressed_data), 8):
            byte = compressed_data[i:i + 8]
            byte_array.append(int(byte, 2))

        compressed_file = input_file + ".huff"
        output_path = os.path.join("static", "compressed", compressed_file)
        with open(output_path, 'wb') as file:
            file.write(byte_array)

        return compressed_file
