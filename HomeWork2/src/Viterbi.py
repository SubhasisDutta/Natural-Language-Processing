'''
Created on Feb 20, 2017
@author: Subhasis
'''
from collections import deque

class Viterbi(object):
    '''
    This class takes the states, observation sequence and transition and emission values and decides
    to find the most probable hidden sequence.
    '''

    def __init__(self, sequence, states, initial, transition, emission):
        self.observation_sequence = sequence
        self.states = states
        self.initial = initial
        self.transition = transition
        self.emissions = emission
        self.no_of_states = len(self.states)
        self.no_of_observation = len(self.observation_sequence)
        self.v_values = {}
        self.backtrack_values = {}
        for state in states:
            self.v_values[state] = [0.0 for t in range(self.no_of_observation)]
            self.backtrack_values[state] = ['' for t in range(self.no_of_observation)]

    def process(self):
        # Initilization
        for state in self.states:
            self.v_values[state][0] = self.initial[state] * self.emissions[state][self.observation_sequence[0]]
        # Recursion
        for index, observation in enumerate(self.observation_sequence):
            if index == 0:
                continue
            for state in self.states:
                self.v_values[state][index], self.backtrack_values[state][index] = self.findMax_Argmax(state, index)
        # Termination
        max_value = float('-inf')
        best_state = ''
        for finalState in self.states:
            for state in self.states:
                v = self.v_values[state][-1] * self.transition[state][finalState]
                if v > max_value:
                    max_value = v
                    best_state = finalState

        result = deque(())
        result.append(best_state)
        for i in range(self.no_of_observation-1, 0, -1):
            best_state = self.backtrack_values[best_state][i]
            result.appendleft(best_state)
        return result

    def findMax_Argmax(self, state, index):
        values = {}
        for s in self.states:
            values[s] = self.v_values[s][index - 1] * self.transition[s][state] * self.emissions[state][
                self.observation_sequence[index]]
        max_value = float('-inf')
        max_arg = ''
        for index, key in enumerate(values):
            if values[key] > max_value:
                max_value = values[key]
                max_arg = key
        return max_value, max_arg
