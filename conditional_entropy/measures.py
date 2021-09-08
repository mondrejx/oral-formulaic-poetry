#!/usr/bin/env python3

# An analysis tool to compare different measures over parallel corpora of Slavic texts; Conditional Entropy (CE),
# the Type-Token relationship (TTR), word Unigram entropy (UE) and Bigram entropy (BE) as a measure of predictability.

import time
import os
from os import listdir
import pandas as pd
from itertools import count, product, islice


USER_HOME = os.path.expanduser("~")
RK_HOME = os.path.dirname(__file__)
FILEPATH = os.path.join(RK_HOME, "../files")
RESULTPATH = os.path.join(RK_HOME, "../results")


def cond_entropy(filename, chunk, word_offset):
    """ Call Conditional Entropy class.

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
    file_result = [500000, 0, 0, 0, 0, 0, 0, 0, 0]

    # added filename and chunk to return
    return file_info + file_result


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
    # Initialize dictionary for columns
    dict_for_file = {}

    for item in fields:
        # Generate keys for dictionary (which will be columns in csv).
        for number in list(range((len(chunks)) * 10)):
            dict_for_file[number] = None

    print(dict_for_file)

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
    print(column_index_for_df)

    dictionary = {}
    for index, item in zip(column_index_for_df, list_of_columns):
        dictionary[index] = item

    for item in list_of_columns:
        print(item)
        print(len(item))

    df = pd.DataFrame.from_dict(dictionary)
    return df


# ***********************************************************************
if __name__ == "__main__":

    start_time = time.time()

    print(USER_HOME)
    print(RK_HOME)
    print(FILEPATH)
    
    # READ FILENAMES FROM files DIRECTORY
    file_list = listdir(FILEPATH)
    list_of_groups = [file_list]

    print(list_of_groups)

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
    print(df)

    # ENTER OUTPUT FILE NAME HERE
    result_name = "rukopisy_data_formatted.csv"

    result_filename = os.path.join(RESULTPATH, result_name)
    df.to_csv(result_filename, encoding='utf-8')

    end_time = time.time()
    elapsed = end_time - start_time
    print("Execution time: {:.2f}".format(elapsed) + "s")
