#!/usr/bin/env python3

# An analysis tool to compare different measures over parallel corpora of Slavic texts; Conditional Entropy (CE),
# the Type-Token relationship (TTR), word Unigram entropy (UE) and Bigram entropy (BE) as a measure of predictability.

import time
import os
from os import listdir
import pandas as pd
from itertools import count, product, islice
from conditional_entropy.condentropy import CondEntropy


USER_HOME = os.path.expanduser("~")
RK_HOME = os.path.dirname(__file__)
FILEPATH = os.path.join(RK_HOME, "../files")
RESULTPATH = os.path.join(RK_HOME, "../results")


def cond_entropy(filename, chunk, word_offset):
    """ Call Conditional Entropy class and arrange the output for csv file formatting.

    Args:
        filename (str): Filename of a text.
        chunk (int): Word chunks for document processing, splicing.
        word_offset (int): Number of words to skip. Default 1.

    Returns:
        list: Results for a single text with Filename, Word chunks, Word_count,
              Average conditional entropy, Average conditional entropy uncertainty,
              Average TTR, Average TTR uncertainty, Bigram entropy, Bigram entropy uncertainty,
              Unigram entropy, Unigram entropy uncertainty

    """
    file_info = [filename, chunk]
    full_path = os.path.join(FILEPATH, filename)

    cent = CondEntropy(full_path, chunk, word_offset)
    cent.pre_process_text()
    file_result = cent.get_volume_entropy()

    # re-arrange outputs for chunk size and word count comparison. Format:
    # Filename, Chunk, Word count,
    # Conditional entropy, Conditional entropy uncertainty,
    # TTR, TTR uncertainty,
    # Bigram entropy, Bigram entropy uncertainty,
    # Unigram entropy, Unigram entropy uncertainty

    # word_count
    file_info.append(file_result[3])
    # avg_cond_ent
    file_info.append(file_result[0])
    # dev_ent
    file_info.append(file_result[4])
    # avg_ttr
    file_info.append(file_result[1])
    # dev_ttr
    file_info.append(file_result[2])
    # bigram_entropy
    file_info.append(file_result[5])
    # dev_bigram
    file_info.append(file_result[7])
    # unigram_entropy
    file_info.append(file_result[6])
    # dev_unigram
    file_info.append(file_result[8])

    return file_info


def multi_letters(seq):
    """Sequence generator.

    Args:
        seq (str): Sequence of letters.

    Yields:
        str: The next letter in the range of "A" to n- 1.

    """
    for n in count(1):
        for s in product(seq, repeat=n):
            yield "".join(s)


def formatted_output(groups, chunks, fields, word_offset):
    """ Process list of files and format the output.

    Args:
        groups (list): Groups of filenames of documents.
        chunks (list): Word chunks for document processing, splicing.
        fields (list): Four methods; Conditional Entropy, Average TTR, Bigram Entropy, Unigram Entropy
                       and corresponding uncertainties. These are used as the column names in results.
        word_offset (int): Number of words to skip. Default 1.

    Returns:
        pd.DataFrame: Resulting values of all four methods.

    """
    # Create first column
    first_column = ["File", None]
    for item in fields:
        for i in range(len(chunks)):
            first_column.append(item)

    # Create second column
    second_column = [None, None]
    for i in range(len(fields)):
        for chunk in chunks:
            second_column.append(chunk)

    # Initialize final list of columns
    list_of_columns = [first_column, second_column]
    for group in groups:
        for file in group:
            print(file)
            data = []
            for chunk in chunks:
                # Convert to list in order to be able to change list items in for-loop (None).
                lst = cond_entropy(file, chunk, word_offset)

                # Append data if chunk size does not exceed word count.
                # Otherwise change data to 'None'
                if lst[1] < lst[2]:
                    data.append(lst)
                else:
                    for item in range(3, len(lst)):
                        lst[item] = None
                    data.append(lst)

            column_list = [file, None]

            for i in range(3, 11, 1):
                for entry in data:
                    column_list.append(entry[i])

            list_of_columns.append(column_list)
        empty_column = [None] * (len(fields) * len(chunks) + 2)
        list_of_columns.append(empty_column)

    column_index_for_df = list(islice(multi_letters("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), len(list_of_columns)))

    dictionary = {}
    for index, item in zip(column_index_for_df, list_of_columns):
        dictionary[index] = item

    df_results = pd.DataFrame.from_dict(dictionary)
    return df_results


# ***********************************************************************
if __name__ == "__main__":

    start_time = time.time()
    
    # READ FILENAMES FROM files DIRECTORY
    file_list = listdir(FILEPATH)
    list_of_groups = [file_list]

    # WORD CHUNK SIZES
    chunks = [100, 300, 500, 1000, 2000, 3000, 5000, 10000, 15000, 20000, 50000, 100000, 300000]
    # OR SPECIFY A RANGE range(first_value, last_value(not included), step)
    # chunks = list(range(1000, 300000, 500))

    # METHODS
    methods = ["1-Conditional Entropy", "2-Cond Ent Deviation", "3-Average TTR", "4-TTR Deviation", 
               "5-Bigram Entropy", "6-Bigram Deviation", "7-Unigram Entropy", "8-Unigram Deviation"]
    # SET WORD-OFFSET
    word_offset = 1

    df = formatted_output(list_of_groups, chunks, methods, word_offset)

    # ENTER OUTPUT FILE NAME HERE
    result_name = "rukopisy_data_formatted.csv"

    result_filename = os.path.join(RESULTPATH, result_name)
    df.to_csv(result_filename, encoding="utf-8")

    end_time = time.time()
    elapsed = end_time - start_time
    print("Execution time: {:.2f}".format(elapsed) + "s")
