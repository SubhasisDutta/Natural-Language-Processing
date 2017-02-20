'''
Created on Feb 20, 2017
@author: Subhasis
'''

import argparse

from Viterbi import Viterbi

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply Viterbi Algorithm to Hot and Cold Problem.')
    parser.add_argument('-sequence', default='331122313',
                        help='A sequence of Icecream count[1-3] (default: 331122313)')
    args = parser.parse_args()
    sequence = args.sequence

    states = ['HOT', 'COLD']
    initial = {
        'HOT': 0.8,
        'COLD': 0.2
    }
    transition = {
        'HOT': {
            'HOT': 0.7,
            'COLD': 0.3
        },
        'COLD': {
            'HOT': 0.4,
            'COLD': 0.6
        }
    }
    emission = {
        'HOT': {
            '1': 0.2,
            '2': 0.4,
            '3': 0.4
        },
        'COLD': {
            '1': 0.5,
            '2': 0.4,
            '3': 0.1
        }
    }
    processor = Viterbi(sequence, states, initial, transition, emission)
    result = processor.process()
    resultString = ''
    for r in result:
        if r == 'HOT':
            resultString += 'H'
        if r == 'COLD':
            resultString += 'C'

    print "The Weather forecast for Observation : ", sequence, "is", resultString