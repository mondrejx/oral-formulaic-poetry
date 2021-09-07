#!/usr/bin/python3

from collections import Counter
from math import log
import sys
import numpy as np
from ofp.conditional_entropy.condentropy_util import CondEntropyUtil


class CondEntropy:
    """ Functions that calculate Unigram Entropy, Bigram Entropy, Conditional Entropy, TTR, and deviations.

    Unigram and Bigram Entropies are entropy calculations based on Shannon's Entropy metric for individual words
    and pairs of consecutive words respectively.

    Conditional entropy is the amount of additional information that would be required to represent the second
    word of each bigram if you already knew the first.

    The Type-Token Ratio (TTR) is the lexical variation within a text calculated as the ratio of types (unique
    words) to tokens (total number of words).

    """

    def __init__(self, filename, chunks, word_offset):
        """ Constructor. Filename and chunks.

        Args:
            filename (str): Input filename including the path.
            chunks (int): Chunks of words.
            word_offset (int): Skip the words in creating bigrams; 1 - consecutive, 2 - skip one word etc.

        """

        try:
            with open(filename, encoding='utf-8') as f:
                text = f.read()
        except OSError:
            sys.exit("File not found: " + filename)

        self.text = text
        self.chunks = chunks
        self.word_offset = word_offset

    def pre_process_text(self):
        # Remove punctuations and format text
        self.text = CondEntropyUtil.word_split(self.text)

    def get_volume_entropy(self):
        # Called from batch report script(s)
        acond_ent, ttr, dev_ttr, word_count, dev_ent, bigram_entropy, unigram_entropy, dev_bigram, dev_unigram = self.measure_by_chunk()

        return [acond_ent, ttr, dev_ttr, word_count, dev_ent, bigram_entropy, unigram_entropy, dev_bigram, dev_unigram]

    def measure_by_chunk(self):
        # This function takes a document, represented as a single string, and returns its conditional,
        # unigram and bigram entropies, and TTR.
        #
        # Since all the measures are related to the length of the text, they are calculated
        # for chunks of a fixed size. Chunk size can be determined as the size of the smallest text in the corpus
        # or according to the needs of the project. A list of different chunk sizes can be implemented in
        # the batch_report.py or batch_report_formatted.py scripts. The calculations are averaged across chunks.

        word_seq = self.text
        chunk_size = self.chunks

        # all words, tokens
        ws_len = len(word_seq)

        # Now we iterate through chunks
        ttrs = []
        cond_ents = []
        bigram_ents = []
        unigram_ents = []

        for pstart in range(0, ws_len, chunk_size):
            pend = pstart + chunk_size

            # If this (final) chunk would overrun the end of the sequence, we adjust it so that it fits,
            # and overlaps with the previous chunk.
            if pend >= ws_len:
                if pend > ws_len:
                    overrun = True

                pend = ws_len
                pstart = pend - chunk_size

                if pstart < 0:
                    # print("In at least one document, chunk size exceeds doc size.")
                    pstart = 0

            act_chunk = word_seq[pstart: pend]

            ttr, cond_ent, bigram_ent, unigram_ent = self.get_all_measures(act_chunk)

            # Collect ttrs and conditional entropies
            ttrs.append(ttr)
            cond_ents.append(cond_ent)

            # Collect bigram and unigram entropies
            bigram_ents.append(bigram_ent)
            unigram_ents.append(unigram_ent)

        # Determine Conditional Entropy and deviation of conditional entropy
        cond_ent = np.round(sum(cond_ents) / len(cond_ents),3)
        dev_ent = np.round(np.std(cond_ents), 3)


        # Determine the bigram and unigram entropies
        bigram_entropy = np.round((sum(bigram_ents) / len(bigram_ents)), 3)
        unigram_entropy = np.round((sum(unigram_ents) / len(unigram_ents)), 3)

        # Determine deviation of bigram, unigram entropies
        dev_bigram = np.round(np.std(bigram_ents), 3)
        dev_unigram = np.round(np.std(unigram_ents), 3)
        
        # Determine ttr and deviation of ttr
        ttr = np.round(sum(ttrs) / len(ttrs), 3)
        dev_ttr = np.round(np.std(ttrs), 3)

        return cond_ent, ttr, dev_ttr, ws_len, dev_ent, bigram_entropy, unigram_entropy, dev_bigram, dev_unigram

    def get_all_measures(self, act_chunk):
        # Given a chunk of text calculates TTR, conditional, bi- and unigram entropies.

        unigram_dist, bigram_dist, unigram_ct, bigram_ct, typect = self.get_distributions(act_chunk)

        ttr = typect / len(act_chunk)

        cond_ent, bigram_entropy, unigram_entropy = self.get_cond_entropy(bigram_dist, unigram_dist,
                                                                          bigram_ct, unigram_ct)

        ttr = np.round(ttr, 3)
        cond_ent = np.round(cond_ent, 3)

        return ttr, cond_ent, bigram_entropy, unigram_entropy

    def get_distributions(self, act_chunk):
        # Calculates distributions over bigrams and unigrams.

        bigram_dist = Counter()
        unigram_dist = Counter()
        unigram_ct = 0
        types = set()
        ws_len = len(act_chunk)

        for idx, word in enumerate(act_chunk):

            unigram_dist[word] += 1
            unigram_ct += 1
            types.add(word)

            # if this is the last word there is no nextword and no bigram to be added!
            if idx > (ws_len - self.word_offset - 1):
                continue
            else:
                next_word = act_chunk[idx + self.word_offset]
                bigram_dist[(word, next_word)] += 1

        # Total number of bigrams as "tokens"
        bigram_ct = unigram_ct - 1

        # Total number of unigram "types"
        typect = len(types)

        return unigram_dist, bigram_dist, unigram_ct, bigram_ct, typect

    def basic_entropy(self, distribution):
        entropy = 0

        for key, keyprob in distribution.items():
            entropy -= keyprob * log(keyprob, 2)

        return entropy

    def get_cond_entropy(self, bigram_dist, unigram_dist, bigram_ct, unigram_ct):
        # Calculate the Conditional Entropy using standard definition.

        # Normalize the distributions so that they're probabilities.
        for key in bigram_dist.keys():
            bigram_dist[key] = bigram_dist[key] / bigram_ct

        for key in unigram_dist.keys():
            unigram_dist[key] = unigram_dist[key] / unigram_ct


        # Standard definition of Conditional Entropy, summing accross
        # the probabilistic space using a simple loop.
        conditional_entropy = 0

        for key, keyprob in bigram_dist.items():
            item_one = key[0]
            unigram_prob = unigram_dist[item_one]
            conditional_entropy -= keyprob * log((keyprob / unigram_prob), 2)

        # Calculate the bigram and unigram entropies on these distributions separately.
        bigram_entropy = self.basic_entropy(bigram_dist)
        unigram_entropy = self.basic_entropy(unigram_dist)

        return conditional_entropy, bigram_entropy, unigram_entropy
