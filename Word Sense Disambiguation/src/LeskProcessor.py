'''
Created on March 30, 2017
@author: Subhasis
'''

import copy
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

class LeskProcessor(object):
    def __init__(self):
        self.stopwords= stopwords.words('english')
        self.synsets = []
        self.defaults = []
        self.signature = {}
        self.result = []

    def process(self,word,sentense):
        words_in_sentense = sentense.split(" ")

        self.buildData(words_in_sentense)

        self.computeOverlap()

        for i in range(len(words_in_sentense)):
            if self.findStem(word) == self.findStem(words_in_sentense[i]):
                print "WORD: ",words_in_sentense[i]
                print "SYNSET: ",self.result[i]
                if not self.result[i] is None:
                    print "DEFINATION: ", wn.synset(str(self.result[i])[8:-2]).definition()
                    print "EXAMPLE: ", wn.synset(str(self.result[i])[8:-2]).examples()
        return True



    def computeOverlap(self):
        for i in range(len(self.synsets)):
            synset_list=self.synsets[i]
            #ignore words that dont have synset
            if len(synset_list)==0:
                self.result.append(None)
                continue

            #set of all words found except the ones in this synset
            context = set()
            for j in range(len(self.synsets)):
                if i == j:
                    continue
                for s_t in self.synsets[j]:
                    sig = self.signature[s_t]
                    for t in sig:
                        context.add(t)

            #get overlap count
            counts={}
            for syn in synset_list:
                overlap = context.intersection(self.signature[syn])
                counts[syn]=len(overlap)

            max_count = -1
            maxSynset = None
            for syn in synset_list:
                if max_count <  counts[syn]:
                    max_count = counts[syn]
                    maxSynset = syn

            #if max is 0 choose default synset
            if counts[maxSynset] ==0:
                maxSynset = self.defaults[i]

            self.result.append(maxSynset)

    def buildData(self, words_in_sentense):
        for word in words_in_sentense:
            stem = self.findStem(word)
            # if stem/word is a stopword dont bother about finding synset
            if stem in self.stopwords:
                self.synsets.append([])
                self.defaults.append(None)
                continue

            # Get Synset for the word/stem and set synsets and defaults
            synset = wn.synsets(stem)
            if synset is None or len(synset) == 0:
                self.synsets.append([])
                self.defaults.append(None)
                continue

            self.synsets.append(synset)
            self.defaults.append(synset[0])

            # create signature
            for syn in synset:
                defination_example_set = set()
                defination_words = wn.synset(str(syn)[8:-2]).definition().split(" ")
                for d in defination_words:
                    stem_t = self.findStem(d)
                    if stem not in self.stopwords:
                        defination_example_set.add(stem_t)

                example_words = wn.synset(str(syn)[8:-2]).examples()
                if len(example_words) > 0:
                    example_words_split = example_words[0].split(" ")
                    for e in example_words_split:
                        stem_t = self.findStem(d)
                        if stem not in self.stopwords:
                            defination_example_set.add(stem_t)

                self.signature[syn] = defination_example_set

    def findStem(self, word):
        word = word.replace("[\"\\.]", "")
        return word.strip().lower()
