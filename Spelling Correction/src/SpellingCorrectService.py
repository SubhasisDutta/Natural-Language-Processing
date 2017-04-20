'''
Created on April 20, 2017
@author: Subhasis
'''
import math as calc
from BiGramService import BiGramService
from WordCorrectionService import WordCorrectionService
import logging


class SpellingCorrectService(object):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.gram_service = BiGramService()
        self.word_service = WordCorrectionService(self.gram_service)

    def process_sentence(self, sentence):
        """Get the sentence and return the corrected sentence"""
        input_tokens = self.gram_service.tokenize(sentence)
        logging.info("    Input Token : " + str(input_tokens))
        correct_sentence = ""
        for index, token in enumerate(input_tokens):
            # Word is a valid word no need to search for correction
            if self.word_service.presentInDictionary(token):  # candidates:
                logging.info("        Found Correct : " + token)
                correct_sentence += token + ' '
                continue
            candidates = self.word_service.generateCandidates(token)
            if token in candidates:
                logging.info("        Found Correct in Candidates : ", token)
                correct_sentence += token + ' '
                continue
            logging.info("        All Candidates for " + token + " : " + str(candidates))
            # Incorrect Word : Need to Select best candidate by using Channel Model
            logging.debug("        Error Detected: " + token + ": " + str(candidates))
            if len(candidates) < 1:
                correct_sentence += token + ' '
                continue
            NP = dict()
            P = dict()
            for candidate in candidates:
                logging.debug("        Before Edit Type: " + str(candidate) + ": "
                             + str(self.gram_service.uni_grams[candidate]) + ": "
                             + str(self.gram_service.probability(candidate)))
                edit = self.word_service.editType(candidate, token)
                logging.info("        Edit Type : " + str(candidate) + ': ' + str(edit))
                if edit is None:
                    continue
                elif edit[0] == "INSERTION":
                    NP[candidate] = self.word_service.channelProbability(edit[3][0], edit[3][1], 'INSERTION')
                elif edit[0] == 'DELETION':
                    NP[candidate] = self.word_service.channelProbability(edit[4][0], edit[4][1], 'DELETION')
                elif edit[0] == 'TRANSPOSITION':
                    NP[candidate] = self.word_service.channelProbability(edit[4][0], edit[4][1], 'TRANSPOSITION')
                elif edit[0] == 'SUBSTITUTION':
                    NP[candidate] = self.word_service.channelProbability(edit[3], edit[4], 'SUBSTITUTION')
                else:
                    continue
            for item in NP:
                channel = NP[item]
                bi_gram = 1
                if len(input_tokens) - 1 != index:
                    bi_gram = calc.pow(calc.e, self.gram_service.sentenceprobability(
                        input_tokens[index - 1] + ' ' + item + ' ' + input_tokens[index + 1], 'bi_gram'))
                else:
                    bi_gram = calc.pow(calc.e,
                                       self.gram_service.sentenceprobability(input_tokens[index - 1] + ' ' + item,
                                                                             'bi_gram'))
                logging.debug(str(channel) + ": " + str(bi_gram))
                P[item] = channel * bi_gram * calc.pow(10, 9)
            P = sorted(P, key=P.get, reverse=True)
            if P == []:
                P.append('')
            correct_sentence += P[0] + ' '
        correct_sentence = self.correctCase(sentence, correct_sentence)
        return correct_sentence

    def correctCase(self, sentence, correct_sentence):
        words_sentence = sentence.split()
        words_correct_sentence = correct_sentence.split()
        correct = []
        for index, word in enumerate(words_sentence):
            if word.isupper():
                correct.append(words_correct_sentence[index].upper())
            elif word.islower():
                correct.append(words_correct_sentence[index].lower())
            elif word.istitle():
                correct.append(words_correct_sentence[index].title())
            else:
                correct.append(words_correct_sentence[index])
        logging.debug(correct)
        return " ".join(correct)

    def process(self, text):
        sentences = text.split(".")
        sentences = [x for x in sentences if x]
        correct_sentences = []
        for sentence in sentences:
            logging.debug("    Each Sentence: " + sentence)
            correct_sentence = self.process_sentence(sentence)
            correct_sentences.append(correct_sentence)
            logging.debug("    Each Correct : ", correct_sentence)
        return ". ".join(correct_sentences) + "."

# help(SpellingCorrectService)