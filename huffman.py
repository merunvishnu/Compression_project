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
            frequency[byte] = frequency.get(byte, 0) + 1
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

        # Calculate frequencies
        frequency = self.calculate_frequencies(data)
        self.build_heap(frequency)
        self.make_codes()

        # Encode the data
        encoded_data = ''.join([self.codes[byte] for byte in data])

        # Add padding to ensure it aligns to a byte boundary
        extra_padding = 8 - len(encoded_data) % 8
        encoded_data += '0' * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        encoded_data = padded_info + encoded_data

        # Convert to bytes
        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i + 8]
            byte_array.append(int(byte, 2))

        # Write the compressed data to a new file
        compressed_file = input_file + ".huff"
        with open(compressed_file, 'wb') as file:
            file.write(byte_array)

        # Save the frequency map for decompression
        freq_file = input_file + ".freq"
        with open(freq_file, 'w') as freq_file:
            freq_file.write(str(frequency))

        return compressed_file

    def decompress(self, input_file):
        # Read the compressed file
        with open(input_file, 'rb') as file:
            bit_string = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

        # Remove the padding
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        bit_string = bit_string[8:]
        encoded_data = bit_string[:-extra_padding]

        # Decode the data
        current_code = ''
        decoded_bytes = bytearray()
        for bit in encoded_data:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_bytes.append(self.reverse_codes[current_code])
                current_code = ''

        # Write the decompressed data to a new file
        decompressed_file = input_file.replace('.huff', '')
        with open(decompressed_file, 'wb') as file:
            file.write(decoded_bytes)

        return decompressed_file
