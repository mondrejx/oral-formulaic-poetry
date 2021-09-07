#!/usr/bin/python3

class CondEntropyUtil:
    """ Pre-processing functions. """

    def __init__(self):
        pass

    @staticmethod
    def word_split(text):
        punctuation = '.,():-—;"!?•$%@“”#<>+=/[]*^\'{}_■~\\|«»©&~`£·'
        text = text.replace('-', ' ')
        # we replace hyphens with spaces because it seems probable that for this purpose
        # we want to count hyphen-divided phrases as separate words
        word_seq = [x.strip(punctuation).lower() for x in text.split()]

        return word_seq


