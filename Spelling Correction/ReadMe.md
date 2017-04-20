# Spelling Error Detection and Correction

This program takes in a bunch of sentences. Identifies non-word spelling errors and correct them 
Using :
1. Bi-gram model
2. Noisy Channel Model
3. Kernighan Error Confusion Matrix
4. Damerau-Levenshtein Edit Distance


```
Help on class BiGramService in module BiGramService:

class BiGramService(__builtin__.object)
 |  Find the Unigram and Bigram Probability.
 |  Finds the Probability of a Sentence.
 |  
 |  Methods defined here:
 |  
 |  __init__(self)
 |  
 |  create_bigram(self, words)
 |      Create Unigram Model for words loaded.
 |  
 |  create_unigram(self, words)
 |      Create Unigram Model for words loaded.
 |  
 |  loadTrainingCorpus(self)
 |      Read a collection of word and build the training corpus
 |  
 |  probability(self, word, words='', type='uni_gram')
 |      Calculate the Maximum Likelihood Probability of n-Grams. With Add 1 Laplace Coefficient.
 |  
 |  sentenceprobability(self, sentence, type='uni_gram', form='anti-log')
 |      Calculate Maximum Likelihood Probability of a sentence.
 |  
 |  tokenize(self, text)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  logger = <logging.Logger object>

Help on class WordCorrectionService in module WordCorrectionService:

class WordCorrectionService(__builtin__.object)
 |  Methods defined here:
 |  
 |  __init__(self, gram_service)
 |  
 |  channelProbability(self, x, y, edit)
 |      Method to calculate channel model probability for errors.
 |  
 |  createDictionaryCache(self, dict_list)
 |  
 |  editType(self, candidate, word)
 |      Calculate edit type for single edit errors.
 |  
 |  generateCandidates(self, word)
 |      Generate set of candidates for a given word using Damerau-Levenshtein Edit Distance.
 |  
 |  loadConfusionMatrix(self)
 |      Load Confusion Matrix from external data file.
 |  
 |  loadDictionary(self)
 |      Load dictionary from external data file.
 |  
 |  presentInDictionary(self, token)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  logger = <logging.Logger object>

Help on class SpellingCorrectService in module SpellingCorrectService:

class SpellingCorrectService(__builtin__.object)
 |  Methods defined here:
 |  
 |  __init__(self)
 |  
 |  correctCase(self, sentence, correct_sentence)
 |  
 |  process(self, text)
 |  
 |  process_sentence(self, sentence)
 |      Get the sentence and return the corrected sentence
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  logger = <logging.Logger object>
 ```
 