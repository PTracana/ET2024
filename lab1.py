import math 
import random
import time
import numpy as np


def generate_poisson(N=120, lam=3):
    rng = np.random.default_rng()
    print( rng.poisson(lam=lam, size=N))
    return rng.poisson(lam=lam, size=N)

def main():
  
    n = int(input("Number of loops\n"))
    l = float(input("Lambda\n"))
# filename = str(n) + "||" + str(l) + ".txt"
#    file = open(filename, 'w+')
    random_times  = np.zeros(n)
    event_timestamp = np.zeros(n)
    
    
    realtimestamp = 0
    for i in range(n):
        random.seed(time.time())
        u = random.random()        
        result = - math.log(1-u)/l
        realtimestamp += result
        random_times[i] = result
        event_timestamp[i] = realtimestamp
        i -= 1
        
    print(random_times)
    print(event_timestamp)
 #   file.close()
    return 0 
if __name__== "__main__":
    generate_poisson()
    