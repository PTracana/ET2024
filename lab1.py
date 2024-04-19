import math 
import random
import time

def main():
  
    n = int(input("Number of loops\n"))
    l = float(input("Lambda\n"))
    filename = str(n) + "||" + str(l) + ".txt"
    print(1)
    file = open(filename, 'w+')
    print(2)
    for i in range(n):
        random.seed(time.time())
        u = random.random()        
        result = - math.log(1-u)/l
        print(result)
        file.write(str(result) + '\n')
        i -= 1
    file.close()
    return 0 
if __name__== "__main__":
    main()