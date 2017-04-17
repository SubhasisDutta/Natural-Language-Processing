'''
Created on March 30, 2017
@author: Subhasis
'''

import argparse
from datetime import datetime

from LeskProcessor import LeskProcessor

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())
    print "Dependency: Install stopwords and wordnet by using the nltk downloader. Use setup.py if required."

    parser = argparse.ArgumentParser(description='Using WordNet implement Simplified LESK algorithim.')
    parser.add_argument('-word', default='flies',
                        help='Word to find Synset (default: flies)')
    parser.add_argument('-sentence', default='Time flies like an arrow',
                        help='Sentence in which to Search (default: Time flies like an arrow)')
    args = parser.parse_args()

    processor = LeskProcessor()
    processComplete = processor.process(args.word, args.sentence)

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())
