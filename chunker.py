import itertools
import math
import re

from separators import sentence_split, spaces


def chunk(text, chunks_number):
    # split the sentences and strip any spaces
    text_sentences = [sentence.strip(spaces) for sentence in re.split(sentence_split, text)]
    # compute the number of sentence per chunk
    chunk_size = math.ceil(len(text_sentences) / chunks_number)
    # join the sentences in chunks
    itertools_chunks = itertools.zip_longest(*[iter(text_sentences)] * chunk_size, fillvalue="")
    return [".".join(chunk) for chunk in itertools_chunks]