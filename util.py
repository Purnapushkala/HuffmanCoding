import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    tree = pickle.load(tree_stream)
    return tree


def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    position = tree
    flag = True
    try:
        while flag:
            # If traversing a branch, check if the child node
            # either moves to left or right subbranch
            value = bitreader.readbit()  # Reads 1 bit
            if value:
                position = position.getRight()
            else:
                position = position.getLeft()
            if isinstance(position, huffman.TreeLeaf):
                # Stop if the leaf is found
                flag = False
        return(position.getValue())
    except EOFError:
        pass


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    Returns:
        None
    '''
    root = read_tree(compressed)
    input_stream = bitio.BitReader(compressed)
    output_stream = bitio.BitWriter(uncompressed)
    decodedvalue = decode_byte(root, input_stream)
    flag = True
    try:
        if decodedvalue is not None:
            while flag:
                # Writes decoded symbol with 8 bits and decode the next bits
                output_stream.writebits(decodedvalue, 8)
                decodedvalue = decode_byte(root, input_stream)
                if decodedvalue is None:
                    flag = False
    except EOFError:
        pass
    output_stream.flush()
    compressed.close()


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    Returns:
        None
    '''
    pickle.dump(tree, tree_stream)
    pass


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    Returns:
        None
    '''
    write_tree(tree, compressed)
    writer = bitio.BitWriter(compressed)
    reader = bitio.BitReader(uncompressed)
    table = huffman.make_encoding_table(tree)

    try:
        while True:  # Reads each bit and writes to file until done
            key = reader.readbits(8)  # Reads 8 bits
            if key in table:
                for i in table[key]:
                    writer.writebit(i)
            elif key is None:
                raise EOFError
    except EOFError:
        for j in table[None]:  # Write None to indicate EOF to decompressor
            writer.writebit(j)
        writer.flush()
