'''
Created on Jan 30, 2017
@author: Subhasis
'''

import tokenize
import cStringIO


class BigramProcessor(object):
    '''
    This Class takes a corpus data in a file, buikds a model and estimates the prediction for sentences.
    '''

    def __init__(self, corpus_location, sentences):
        self.corpus_location = corpus_location
        self.sentences = sentences
        self.prob_without_smoothing = []
        self.prob_add_one_smoothing = []
        self.prob_good_turing_discounting = []
        self.no_of_tokens = 0
        self.vocab_size = 0
        self.token_count = {}
        self.tokens = []
        self.token_fequency_count = {}
        self.bi_gram_count = {}

    def process(self):
        self.findAllCorpusTokens()
        print ""
        print "The number of Tokens is : ", self.no_of_tokens
        # Find count of each distinct Tokens
        self.findCountOfEachToken()
        print "The Vocabulary size is : ", self.vocab_size
        print ""
        # Iterate over each sentence and process for each
        for i, s in enumerate(self.sentences):
            print "SENTENCE ", i + 1, " : ", s
            sentence_tokens = self.getSentenceTokenCount(s, i)
            self.processBiGramCount(sentence_tokens, i, 'NO_SMOOTHING')
            self.calculateProbability(list(sentence_tokens), 'NO_SMOOTHING', self.prob_without_smoothing)
            print ""
            self.processBiGramCount(sentence_tokens, i, 'ADD_ONE_SMOOTHING')
            self.calculateProbability(list(sentence_tokens), 'ADD_ONE_SMOOTHING', self.prob_add_one_smoothing)
            print ""
            self.processBiGramCount(sentence_tokens, i, 'GOOD_TURING_DISCOUNTING')
            self.calculateProbability(list(sentence_tokens), 'GOOD_TURING_DISCOUNTING',
                                      self.prob_good_turing_discounting)
            print ""
            print ""

        # Print No-Smoothing Probability
        self.displayResults(self.prob_without_smoothing, 'NO SMOOTHING')
        self.displayResults(self.prob_add_one_smoothing, 'ADD ONE SMOOTHING')
        self.displayResults(self.prob_good_turing_discounting, 'GOOD TURING DISCOUNTING')

        return True

    def displayResults(self, list, type):
        print ""
        print "Result for ------ ", type
        max_i = 0
        max_val = list[0]
        for i, p in enumerate(list):
            print "For Sentence ", i + 1, " Probability : ", p
            if max_val < p:
                max_val = p
                max_i = i
        print "Sentence ", max_i + 1, " is more probable."
        print ""

    def findAllCorpusTokens(self):
        corpus_string = open(self.corpus_location).read()
        # Read the file and extract all the tokens
        g = tokenize.generate_tokens(cStringIO.StringIO(corpus_string).readline)
        for toknum, tokval, _, _, _ in g:
            i_token = tokval.lower()
            self.tokens.append(i_token)
            if toknum == 1 and len(i_token) > 1:
                if i_token in self.token_count:
                    self.token_count[i_token] += 1
                else:
                    self.token_count[i_token] = 1
                self.no_of_tokens += 1

    def findCountOfEachToken(self):
        self.vocab_size = len(self.token_count)
        for k, v in self.token_count.iteritems():
            if v in self.token_fequency_count:
                self.token_fequency_count[v] += 1
            else:
                self.token_fequency_count[v] = 1

    def getSentenceTokenCount(self, sentence, index):
        sentence_tokens = tokenize.generate_tokens(cStringIO.StringIO(sentence).readline)
        s_t = []
        for n, v, _, _, _ in sentence_tokens:
            if n == 1 and len(v) > 1:
                s_t.append(v.lower())
        return s_t

    def processBiGramCount(self, sentence_tokens, index, table_type):
        print "    ", table_type, "    "
        print "Sentence ", index + 1, " ------ BIGRAM COUNT TABLE (C)"
        print_sentence = "".ljust(10)
        for i in sentence_tokens:
            print_sentence += i.ljust(10)
        print print_sentence

        for i in sentence_tokens:
            print_sentence = i.ljust(10)
            self.bi_gram_count[i] = {}
            for j in sentence_tokens:
                self.bi_gram_count[i][j] = self.findBiGramCount(i, j)
                print_sentence += str(self.getBiGramCount(i, j, table_type)).ljust(10)
            print print_sentence
        print ""
        if table_type == 'GOOD_TURING_DISCOUNTING':
            print "Sentence ", index + 1, " ------ BIGRAM COUNT TABLE (C PLUS)"
            print_sentence = "".ljust(10)
            for i in sentence_tokens:
                print_sentence += i.ljust(10)
            print print_sentence
            for i in sentence_tokens:
                print_sentence = i.ljust(10)
                for j in sentence_tokens:
                    print_sentence += str(round(self.getConditionalProbability(i, j, table_type+'_cplus'), 6)).ljust(10)
                print print_sentence
        print ""
        print "Sentence ", index + 1, " ------ BIGRAM PROBABILITY TABLE"
        print_sentence = "".ljust(10)
        for i in sentence_tokens:
            print_sentence += i.ljust(10)
        print print_sentence
        for i in sentence_tokens:
            print_sentence = i.ljust(10)
            for j in sentence_tokens:
                print_sentence += str(round(self.getConditionalProbability(i, j, table_type), 6)).ljust(10)
            print print_sentence

    def findBiGramCount(self, word1, word2):
        count = 0
        indices = [i for i, x in enumerate(self.tokens) if x == word1]
        for i in indices:
            if self.tokens[i + 1] == word2:
                count += 1
        return count

    def calculateProbability(self, sentence_tokens, table_type, prob_list):
        sentence_probability = 1.0
        sentence_tokens.append('XXXXXXXX')
        for i, s in enumerate(sentence_tokens[:-1]):
            conditional_probability = self.getConditionalProbability(s, sentence_tokens[i + 1], table_type)
            if conditional_probability > 0:
                sentence_probability *= conditional_probability
        prob_list.append(sentence_probability)

    def getBiGramCount(self, token1, token2, table_type):
        if table_type == 'NO_SMOOTHING':
            return self.bi_gram_count[token1].get(token2, 0)
        elif table_type == 'ADD_ONE_SMOOTHING':
            return self.bi_gram_count[token1].get(token2, 0) + 1
        elif table_type == 'GOOD_TURING_DISCOUNTING':
            return self.bi_gram_count[token1].get(token2, 0)
        return 0

    def getConditionalProbability(self, token1, token2, table_type):
        unigram_count = float(self.token_count[token1])
        bi_gram_count = self.bi_gram_count[token1].get(token2, 0)
        conditional_probability = 0
        if table_type == 'NO_SMOOTHING':
            if bi_gram_count > 0:
                conditional_probability = bi_gram_count / unigram_count
        elif table_type == 'ADD_ONE_SMOOTHING':
            conditional_probability = (bi_gram_count + 1) / (unigram_count + self.vocab_size)
        elif table_type == 'GOOD_TURING_DISCOUNTING_cplus':
            c = bi_gram_count
            n_c_frequency = self.token_fequency_count.get(c, 1)
            n_c_frequency_plus_1 = self.token_fequency_count.get(c + 1, 1)
            c_star = (c + 1) * n_c_frequency_plus_1 / float(n_c_frequency)
            conditional_probability = c_star
        elif table_type == 'GOOD_TURING_DISCOUNTING':
            c = bi_gram_count
            n_c_frequency = self.token_fequency_count.get(c, 1)
            n_c_frequency_plus_1 = self.token_fequency_count.get(c + 1, 1)
            c_star = (c + 1) * n_c_frequency_plus_1 / float(n_c_frequency)
            conditional_probability = c_star / self.no_of_tokens
        return conditional_probability
