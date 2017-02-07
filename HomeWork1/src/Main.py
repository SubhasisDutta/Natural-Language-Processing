'''
Created on Jan 30, 2017
@author: Subhasis
'''

import sys
from datetime import datetime
import argparse

from BigramProcessor import BigramProcessor

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())

    parser = argparse.ArgumentParser(description='Process Bigram to find which sentence is more probable.')
    parser.add_argument('-corpus', default='Corpus.txt',
                        help='Location of Corpus File (default: Corpus.txt)')
    parser.add_argument('-s1', default='The chief executive said that the company\'s profit was going down last year.',
             help='Sentence 1 (default: The chief executive said that the company\'s profit was going down last year.)')
    parser.add_argument('-s2', default='The president said the revenue was good last year.',
                        help='Sentence 2 (default: The president said the revenue was good last year.)')

    args = parser.parse_args()

    corpus_location = args.corpus
    sentences = []
    sentences.append(args.s1)
    sentences.append(args.s2)

    processor = BigramProcessor(corpus_location, sentences)

    processComplete = processor.process()

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())
