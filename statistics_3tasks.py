# statistics for workflow with 3 tasks

import numpy as np
import json
import matplotlib.pyplot as plt
from collections import OrderedDict

optimal_key = "0000010101"
time_limit = 19


def sample_most_likely(state_vector):
    if isinstance(state_vector, (OrderedDict, dict)):
        # get the binary string with the largest count
        binary_string = sorted(state_vector.items(), key=lambda kv: kv[1])
        repetitions = int(binary_string[-1][1])
        binary_string = binary_string[-1][0]
        x = np.asarray([int(y) for y in reversed(list(binary_string))])
        return x, repetitions
    return [], 0


def get_stats(filename):
    with open(filename) as handle:
        dict_res = json.loads(handle.read())
        
        optimal = 0
        correct = 0
        incorrect = 0
        correct_config = 0
        
        if optimal_key in dict_res:
            optimal = dict_res[optimal_key]
        for key, val in dict_res.items():
            if is_correct(key):
                correct += val
                correct_config += 1
            else:
                incorrect += val
        
        print('most likely solution: ',sample_most_likely(dict_res))      
        print("optimal: ", optimal)
        print("correct solutions: ", correct)
        print("incorrect solutions: ", incorrect)
        print("correct configs: ", correct_config)


def get_stats_for_result(dict_res):
    optimal = 0
    correct = 0
    incorrect = 0
    correct_config = 0
     
    if optimal_key in dict_res:
        optimal = dict_res[optimal_key]
    for key, val in dict_res.items():
        if is_correct(key):
            correct += val
            correct_config += 1
        else:
            incorrect += val
            
    print('most likely solution: ',sample_most_likely(dict_res))      
    print("optimal: ", optimal)
    print("correct solutions: ", correct)
    print("incorrect solutions: ", incorrect)
    print("correct configs: ", correct_config)

def is_correct(key):
    if solution_vector_correct(key) and execution_time(key) <= time_limit:
        return True
    return False
    
def execution_time(k):
    time = int(k[6]) *8 + int(k[7]) * 4 + int(k[8]) * 2 + int(k[9]) * 1 + int(k[0]) * 6 + int(k[1]) * 3 + int(k[2]) *12 + int(k[3]) * 2 + int(k[4]) * 1 + int(k[5]) * 4
    return time
    
def solution_vector_correct(vector):
    if vector.endswith('000111') or vector.endswith('010101') or vector.endswith('100011') or vector.endswith('001110') or vector.endswith('011100') or vector.endswith('101010') or vector.endswith('110001') or vector.endswith('111000'):
        return True
    return False