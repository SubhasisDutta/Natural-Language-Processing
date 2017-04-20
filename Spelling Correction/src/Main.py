'''
Created on April 20, 2017
@author: Subhasis
'''

import argparse
import ConfigParser
import time
import logging

from SpellingCorrectService import SpellingCorrectService

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    spelling_correction = SpellingCorrectService()
    logger.info("Spelling Correction Service Loaded")
    logger.info("Test 1")
    sentence_1 = "She is a briliant acress. She wno Tweve Oscar awards but her latest mvie is bad."
    start = time.time()
    result = spelling_correction.process(sentence_1)
    done = time.time()
    elapsed = done - start
    logger.info("Input Text : " + sentence_1)
    logger.info("Result     : " + result)
    logger.info("             " + str(elapsed) + " Seconds to compute")
    logger.info("Test 2")
    start = time.time()
    sentence_2 = "She is a beaiful actress. Her moveie did very well at the box ofice."
    result = spelling_correction.process(sentence_2)
    done = time.time()
    elapsed = done - start
    logger.info("Input Text : " + sentence_2)
    logger.info("Result     : " + result)
    logger.info("             " + str(elapsed) + " Seconds to compute")
