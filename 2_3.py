import math 
import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def exponential_distribution(n,l):
    # Generates the sequence of events according to the exponential distribution

    event_timestamp = np.zeros(n)
    time_intervals = np.zeros(n)
    time_ = 0
    
    for i in range(n):
        random.seed(time.time())
        u = random.random()
        deltat = -math.log(1-u)/l
        time_ += deltat
        time_intervals[i] = deltat
        event_timestamp[i] = int(math.floor(time_))
        i -= 1
    return event_timestamp

def plot_histogram(data,n,l):
    # Count how many times each value appears
    value_counts = Counter(data.values())
    # print(value_counts)

    # Calculate total count
    total_count = sum(value_counts.values())
    # print(total_count)

    # Calculate the percentage for each number of events
    percentages = {count: (freq / total_count) for count, freq in value_counts.items()}
    # print(percentages)

    # Plotting sample data histogram
    plt.bar(percentages.keys(), percentages.values(), align='center', alpha=0.5, label='Sample Data')
    
    # Calculating and plotting Theoretical Poisson Distribution
    theoretical_probs = [poisson_pmf(k,sum(l)) for k in range(max(data.values())+1)]
    # print(theoretical_probs)
    plt.plot(range(max(data.values()) + 1), theoretical_probs, marker='o', linestyle='-', color='r', label='Theoretical Distribution')

    plt.xlabel('Number of events')
    plt.ylabel('Percentage / Probability Density')
    plt.title('Superposition of Poisson Processes with λ = ' + str(l) + ' and their respective number of events' + str(n))
    plt.grid(True)
    plt.legend()
    plt.show()
    return 0

def poisson_pmf(k, lambda_):
    # Probability Mass Function (PMF) of the Poisson distribution
    return np.exp(-lambda_) * (lambda_**k) / np.math.factorial(k)

def main():
    # Least Common Multiplier chosen is 1365.
    default_values = [4095,9555,17745,20475]
    n = [value * 1 for value in default_values]
    l = [3,7,13,15]
    
    events = [None] * 4
    for i in range(0,len(l)):
        events[i] = exponential_distribution(n[i],l[i])
    # print(events)
    
    # Count the frequency for each number of events occuring in a unitary time interval
    event_counting = [None] * 4
    for i in range(0,len(events)):
        event_counting[i] = Counter(events[i])
    # print(event_counting)


    # If any value is not present in any of the sequences, add it with a frequency of 0
    index = 0
    for sequence in events:    
        for i in range(int(max(sequence))+1):
            if i not in (event_counting[index]):
                event_counting[index][i] = 0
        index += 1

    # Sort the dictionaries by keys           
    sorted_event_counting = [None] * 4
    index = 0
    for sequence in event_counting:
        sorted_event_counting[index] = dict(sorted(sequence.items()))
        index += 1
    #print(sorted_event_counting[0])

    # Joining all sequences together
    sequence_sum = {}
    for sequence in sorted_event_counting:
        for i in range(int(max(sequence))+1):
            if i not in (sequence_sum):
                sequence_sum[i] = sequence[i]
            else:
                sequence_sum[i] += sequence[i]
    #print(sequence_sum)

    # Plot both histograms for the Sample Data and Theoretical Poisson Distribution with SuperPosition
    plot_histogram(sequence_sum,n,l)
    return 0

if __name__== "__main__":
    main()
   
    