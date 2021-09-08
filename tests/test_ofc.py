#!/usr/bin/env python3

import sys
import os
from os import listdir

from conditional_entropy.measures import formatted_output

RK_HOME = os.path.dirname(__file__)
FILEPATH = os.path.join(RK_HOME, "../files")


def test_cond_entropy():

    # READ FILENAMES FROM files DIRECTORY
    file_list = listdir(FILEPATH)
    list_of_groups = [file_list]

    # WORD CHUNK SIZES
    chunks = [100, 300, 500, 1000, 2000, 3000, 5000, 10000, 15000, 20000, 50000, 100000, 300000]
    # METHODS
    methods = ["1-Conditional Entropy", "2-Cond Ent Deviation", "3-Average TTR", "4-TTR Deviation",
               "5-Bigram Entropy", "6-Bigram Deviation", "7-Unigram Entropy", "8-Unigram Deviation"]
    # SET WORD-OFFSET
    word_offset = 1

    df = formatted_output(list_of_groups, chunks, methods, word_offset)
    result_csv = df.to_csv(encoding="utf-8")

    # Formatted master file
    test_filename = "rukopisy_data_formatted_fin.csv"

    try:
        with open(test_filename, "r") as file:
            test_csv = file.read()
    except IOError:
        sys.exit("File " + test_filename + " is not accessible!")

    assert test_csv == result_csv
