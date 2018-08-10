import os
from os import walk


def read_text_corpus(directory_path):
    absolute_path = os.path.abspath(directory_path)
    corpus = {}
    for (dirpath, dirnames, filenames) in walk(absolute_path):
        for name in filenames:
            text_file_path = (os.path.join(dirpath, name))
            with open(text_file_path, "rb") as text_file:
                corpus[name] = text_file.read()
    return corpus