'''
Created on April 20, 2017
@author: Subhasis
'''
import re
# import os.path
import math as calc
import ConfigParser
from collections import Counter
import logging

class BiGramService(object):
    """Find the Unigram and Bigram Probability.
        Finds the Probability of a Sentence.


    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('../config/config.cnf')
        self.training_corpus_words = self.loadTrainingCorpus()
        logging.debug("training_corpus_words: " + str(len(self.training_corpus_words)))
        self.uni_grams = self.create_unigram(self.training_corpus_words)
        self.bi_grams = self.create_bigram(self.training_corpus_words)

    def tokenize(self, text):
        return re.findall('[a-z]+', text.lower())  # training_data.split(' ')

    def loadTrainingCorpus(self):
        """Read a collection of word and build the training corpus"""
        logging.info("Loading Training Data to build word corpus ...")
        corpus_file = open(self.config.get('BiGramService', 'File.TrainingData'), 'r')
        training_data = corpus_file.read()
        corpus_file.close()
        logging.info("Processing Training Corpus")
        tokens = self.tokenize(training_data)
        return tokens

    def create_unigram(self, words):
        """Create Unigram Model for words loaded."""
        logging.info("Creating Uni-gram count model ...")
        # store_file_location = self.config.get('BiGramService', 'File.UniGramStore')
        # if os.path.isfile(store_file_location):
        #     unigram_file = open(self.config.get('BiGramService', 'File.TrainingData'), 'r')
        #     unigram_data = unigram_file.read()
        #     unigram_file.close()
        #     #convert file read to unigram dictionary
        # else:
        # unigramfile = open('unigram.data', 'w')
        uni_gram = Counter(words)
        logging.info("Calculated Count for Unigram Model")
        # unigramfile.write(str(unigram))
        # unigramfile.close()
        return uni_gram

    def create_bigram(self, words):
        """Create Unigram Model for words loaded."""
        logging.info("Creating Bi-gram Count Model ...")
        bi_words = []
        for index, item in enumerate(words):
            if index == len(words) - 1:
                break
            bi_words.append(item + ' ' + words[index + 1])
        bi_gram = Counter(bi_words)
        logging.info("Calculated Count for Bigram Model")
        return bi_gram

    def probability(self, word, words="", type='uni_gram'):
        """Calculate the Maximum Likelihood Probability of n-Grams. With Add 1 Laplace Coefficient."""
        logging.debug(word + "   " + words)
        if type == 'uni_gram':
            logging.debug("self.uni_grams[word]: " + word + " " + str(self.uni_grams[word]))
            logging.debug("len(self.training_corpus_words): " +str(len(self.training_corpus_words)))
            logging.debug("len(self.uni_grams): " + str(len(self.uni_grams)))
            return calc.log((self.uni_grams[word] + 1) / float(len(self.training_corpus_words) + len(self.uni_grams)))
        elif type == 'bi_gram':
            logging.debug("self.bi_grams[words]: " + words + " " + str(self.bi_grams[words]))
            logging.debug("self.uni_grams[word]: " + word + " " + str(self.uni_grams[word]))
            logging.debug("len(self.uni_grams): " + str(len(self.uni_grams)))
            return calc.log((self.bi_grams[words] + 1) / float(self.uni_grams[word] + len(self.uni_grams)))

    def sentenceprobability(self, sentence, type='uni_gram', form='anti-log'):
        """Calculate Maximum Likelihood Probability of a sentence."""
        logging.debug("            Bigram sentence: " + sentence)
        tokens = self.tokenize(sentence)
        accumulator = 0
        if type == 'uni_gram':
            for index, item in enumerate(tokens):
                accumulator += self.probability(item)
        if type == 'bi_gram':
            for index, item in enumerate(tokens):
                if index == len(tokens) - 1: break
                accumulator += self.probability(item, item + ' ' + tokens[index + 1], 'bi_gram')
        logging.debug( "            Sentence Probability : " + str(accumulator))
        if form == 'log':
            return accumulator
        elif form == 'anti-log':
            anti_log = calc.pow(calc.e, accumulator)
            logging.debug(anti_log)
            return anti_log

# help(BiGramService)