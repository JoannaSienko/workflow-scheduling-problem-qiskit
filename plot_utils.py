import json
import matplotlib.pyplot as plt
import numpy as np
from qiskit.quantum_info import Pauli
import matplotlib.patches as mpatches

GREEN = '#4a804f'
RED = '#db4059'
optimal = "0000010101"
correct_solutions = ['0110100011', '0000010101', '0101101010', '0001110001', '0011111000', '0100001110', '0010011100']
font = {'size': 50}
SIZE = 100


def array_contains(h, v):
    for i in range(len(h)):
        if h[i] == True and v[i] == 0:
            return False
    return True

def get_energy(key, d):
    if key in d:
        return d[key]
    else:
        return 0
    
def is_correct(key):
    if key in correct_solutions:
        return True
    return False

def is_ideal(key):
    if key == optimal:
        return True
    return False
    
               
def compute_time(k):
    return int(k[0]) + int(k[1]) * 2 + int(k[2]) * 4 + int(k[3]) * 8 + int(k[4])* 4 + int(k[5]) + int(k[6]) * 2 + int(k[7]) * 12 + int(k[8]) * 3 + int(k[9]) * 6    

def draw_probability_diagram(filename, filenameEnergy, title):
    x = []
    y = []
    index = 0
    corrects_index = []
    correct_res_number = 0
    incorrect_res_number = 0
    ideal = 0
    
    with open(filenameEnergy) as handle:
        ennergies_dict = json.loads(handle.read())
        min_val = min(ennergies_dict.values())
        max_val = max(ennergies_dict.values())

    all_res_number = 0
    with open(filename) as handle:
        results = json.loads(handle.read())
        for key, val in results.items():
            all_res_number += int(val)
        print('all results: ', all_res_number)
        
        for key, val in results.items():    
            energy = get_energy(key, ennergies_dict)
            x.append(energy.real)
            if is_correct(key):
                corrects_index.append(index)
                y.append(val/all_res_number)
                correct_res_number += val
            else:
                y.append(val/all_res_number)
                incorrect_res_number += val
            index += 1
    
        if optimal in results:
            ideal = results[optimal]
            
    print("optimal: ", ideal)
    print('correct res:', correct_res_number)        
    print('incorrect res:', incorrect_res_number)
    print('correct configurations:', len(corrects_index))        
    print('incorrect configurations:', index - len(corrects_index))
    
    x_label = 'energy'
    y_label = 'Probability'
    width = (abs(min_val) + abs(max_val)) * 0.01
    fig, ax = plt.subplots(figsize=(40,20))
    
    barlist = plt.bar(x, y, color=RED, width=width)
    for i in corrects_index:
        barlist[i].set_color(GREEN)
        barlist[i].set_width(width)
     
    ax.set_xlabel(x_label, fontdict=font)
    ax.set_ylabel(y_label, fontdict=font)
    ax.tick_params(axis='y', labelsize='50')
    ax.tick_params(axis='x', labelsize='40', labelrotation=90)
    red_patch = mpatches.Patch(color='r', label='incorrect solutions')
    g_patch = mpatches.Patch(color='g', label='correct solutions')
    plt.xlim(min_val * 1.1 , max_val* 1.1)
    plt.legend(handles=[red_patch, g_patch], fontsize=50)
    ax.set_title(title, fontdict={'fontsize': SIZE, 'fontweight': 'medium'})
    fig.tight_layout()
            
        
def plot_histogram(filename):
    """Exact results in histogram form. """
    with open(filename) as handle:
        dict_res = json.loads(handle.read())
        keys = []
        values = []
        index = 0
        corrects_index = []
        
        for key, val in dict_res.items():
            keys.append(key[::-1])
            values.append(int(val))
            if is_correct(key):
                corrects_index.append(index)
            index += 1
        
        x_label = 'Result'
        y_label = 'Number of shots'
        fig, ax = plt.subplots(figsize=(40,20))
        ax.set_xlabel(x_label, fontdict=font)
        plt.bar(keys, values)
        barlist = plt.bar(keys, values, color=RED)
        for i in corrects_index:
            barlist[i].set_color(GREEN)
     
        ax.set_ylabel(y_label, fontdict=font)
        ax.tick_params(axis='y', labelsize='50')
        ax.tick_params(axis='x', labelsize='40', labelrotation=90)
        fig.tight_layout()


# when the results differs not possible to mark all results, only results with number of shots grater than b are presented.        
def plot_histogram_with_different_res(filename, b):
    with open(filename) as handle:
        dict_res = json.loads(handle.read())
        keys = []
        values = []
        index = 0
        corrects_index = []
        
        for key, val in dict_res.items():
            if int(val) > b:
                keys.append(key[::-1])
                values.append(int(val))
                if is_correct(key):
                    corrects_index.append(index)
                index += 1
        
        x_label = 'result'
        y_label = 'Number of shots'
        fig, ax1 = plt.subplots(figsize=(40,20))
        ax1.set_xlabel(x_label, fontdict=font)
        plt.bar(keys, values)
        barlist = plt.bar(keys, values, color=RED)
        for i in corrects_index:
            barlist[i].set_color(GREEN)
             
        ax1.set_ylabel(y_label, fontdict=font)
        ax1.tick_params(axis='y', labelsize='50')
        ax1.tick_params(axis='x', labelsize='40', labelrotation=90)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped

# draw all energy values for all eigenvalues for the hamiltonian        
def draw_energy_diagram(filename):
    x = []
    y = []
    index = 0
    corrects_index = []
    x1 = []
    x2 = []
    y1 = []
    y2 = []
    with open(filename) as handle:
        ennergies_dict = json.loads(handle.read())
        min_val = min(ennergies_dict.values())
        max_val = max(ennergies_dict.values())

        for key, val in ennergies_dict.items():
            energy = get_energy(key, ennergies_dict)
            x.append(energy.real)
            if is_correct(key):
                x1.append(energy.real)
                y1.append(1)
                corrects_index.append(index)
                y.append(1)
            else:
                x2.append(energy.real)
                y2.append(1)
                y.append(0.5)
            index += 1
            
            
    print('correct:', len(corrects_index))        
    print('incorrect:', index - len(corrects_index))
    
    width = (abs(min_val) + abs(max_val)) * 0.001
    x_label = 'energy'
    y_label = ''
    fig, ax = plt.subplots(figsize=(40,20))
    ax.set_xlabel(x_label, fontdict=font)
    barlist = plt.bar(x1, y1, color=GREEN,width=width)
    barlist2= plt.bar(x2, y2, color=RED, width=width)
    
    ax.tick_params(axis='x', labelsize='40', labelrotation=90)
    ax.axes.get_yaxis().set_visible(False)
    red_patch = mpatches.Patch(color='r', label='incorrect solutions')
    g_patch = mpatches.Patch(color='g', label='correct solutions')
    plt.legend(handles=[red_patch, g_patch], fontsize=50)
    fig.tight_layout()
   