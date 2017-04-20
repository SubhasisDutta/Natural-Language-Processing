'''
Created on April 20, 2017
@author: Subhasis
'''
import ConfigParser
import ast
import logging
import editdistance

class WordCorrectionService(object):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self, gram_service):
        self.config = ConfigParser.ConfigParser()
        self.config.read('../config/config.cnf')
        self.gram_service = gram_service
        self.loadConfusionMatrix()
        self.createDictionaryCache(self.loadDictionary())
        self.word_dictionary = sorted(set(self.gram_service.training_corpus_words))

    def createDictionaryCache(self,dict_list):
        self.english_word_dictionary = {}
        for word in dict_list:
            if len(word) < 2:
                self.english_word_dictionary[word] = [word]
            else:
                two_char = word[0:2]
                if not two_char in self.english_word_dictionary.keys():
                    self.english_word_dictionary[two_char] = []
                self.english_word_dictionary[two_char].append(word)
        for k,v in self.english_word_dictionary.items():
            word_set = set(v)
            self.english_word_dictionary[k] = word_set


    def presentInDictionary(self,token):
        key = ""
        if len(token) < 2:
            key = token
        else:
            key = token[0:2]
        try:
            bucket = self.english_word_dictionary[key]
            if token in bucket:
                return True
            else:
                return False
        except KeyError:
            return False



    def loadConfusionMatrix(self):
        """Load Confusion Matrix from external data file."""
        f = open(self.config.get('WordCorrectionService', 'File.InsersionData'), 'r')
        data = f.read()
        f.close()
        self.insertion_matrix = ast.literal_eval(data)

        f = open(self.config.get('WordCorrectionService', 'File.DeletionData'), 'r')
        data = f.read()
        f.close()
        self.deletion_matrix = ast.literal_eval(data)

        f = open(self.config.get('WordCorrectionService', 'File.SubstitutionData'), 'r')
        data = f.read()
        f.close()
        self.substitution_matrix = ast.literal_eval(data)

        f = open(self.config.get('WordCorrectionService', 'File.TranspositionData'), 'r')
        data = f.read()
        f.close()
        self.transposition_matrix = ast.literal_eval(data)

    def loadDictionary(self):
        """Load dictionary from external data file."""
        logging.info("Loading dictionary from data file ...")
        f = open(self.config.get('WordCorrectionService', 'File.DictionaryData'), 'r')
        return f.read().split("\n")

    def generateCandidates(self, word):
        """Generate set of candidates for a given word using Damerau-Levenshtein Edit Distance."""
        candidates = dict()
        for item in self.word_dictionary:
            distance = int(editdistance.eval(word,item))#self.calculateEditDistance(word, item)
            if distance <= 1:
                candidates[item] = distance
        return sorted(candidates, key=candidates.get, reverse=False)

    def editType(self, candidate, word):
        """Calculate edit type for single edit errors."""
        edit = [False] * 4
        correct = ""
        error = ""
        x = ''
        w = ''
        for i in range(min([len(word), len(candidate)]) - 1):
            if candidate[0:i + 1] != word[0:i + 1]:
                if candidate[i:] == word[i - 1:]:
                    edit[1] = True
                    correct = candidate[i - 1]
                    error = ''
                    x = candidate[i - 2]
                    w = candidate[i - 2] + candidate[i - 1]
                    break
                elif candidate[i:] == word[i + 1:]:

                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#' + error
                    else:
                        w = word[i - 1]
                        x = word[i - 1] + error
                    edit[0] = True
                    break
                if candidate[i + 1:] == word[i + 1:]:
                    edit[2] = True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i + 1] and candidate[i + 2:] == word[i + 2:]:
                    edit[3] = True
                    correct = candidate[i] + candidate[i + 1]
                    error = word[i] + word[i + 1]
                    x = error
                    w = correct
                    break
        candidate = candidate[::-1]
        word = word[::-1]
        for i in range(min([len(word), len(candidate)]) - 1):
            if candidate[0:i + 1] != word[0:i + 1]:
                if candidate[i:] == word[i - 1:]:
                    edit[1] = True
                    correct = candidate[i - 1]
                    error = ''
                    x = candidate[i - 2]
                    w = candidate[i - 2] + candidate[i - 1]
                    break
                elif candidate[i:] == word[i + 1:]:

                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#' + error
                    else:
                        w = word[i - 1]
                        x = word[i - 1] + error
                    edit[0] = True
                    break
                if candidate[i + 1:] == word[i + 1:]:
                    edit[2] = True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i + 1] and candidate[i + 2:] == word[i + 2:]:
                    edit[3] = True
                    correct = candidate[i] + candidate[i + 1]
                    error = word[i] + word[i + 1]
                    x = error
                    w = correct
                    break
        if word == candidate:
            return "None", '', '', '', ''
        if edit[1]:
            return "DELETION", correct, error, x, w
        elif edit[0]:
            return "INSERTION", correct, error, x, w
        elif edit[2]:
            return "SUBSTITUTION", correct, error, x, w
        elif edit[3]:
            return "TRANSPOSITION", correct, error, x, w

    def channelProbability(self, x, y, edit):
        """Method to calculate channel model probability for errors."""
        corpus = ' '.join(self.gram_service.training_corpus_words)
        if edit == 'INSERTION':
            if x == '#':
                return self.insertion_matrix[x + y] / corpus.count(' ' + y)
            else:
                return self.insertion_matrix[x + y] / corpus.count(x)
        if edit == 'SUBSTITUTION':
            return self.substitution_matrix[(x + y)[0:2]] / corpus.count(y)
        if edit == 'TRANSPOSITION':
            return self.transposition_matrix[x + y] / corpus.count(x + y)
        if edit == 'DELETION':
            return self.deletion_matrix[x + y] / corpus.count(x + y)

# help(WordCorrectionService)