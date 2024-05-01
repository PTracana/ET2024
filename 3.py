import random
import numpy as np
import math 
import time

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
        event_timestamp[i] = float(time_)
        i -= 1
    return event_timestamp

def stats(total_waiting_time, num_events, total_queue_time, total_time, idle):
    average_packet_waiting_time = total_waiting_time/num_events
    average_packet_time_in_system =  (total_waiting_time + total_queue_time)/num_events
    total_busy_time = (total_time - idle) / total_time *100
    print("Average packet waiting time: ", average_packet_waiting_time)
    print("Average packet time in system: ", average_packet_time_in_system)
    print("Total busy time: ", total_busy_time)
    return

def processing(arrival_rate, service_rate, event_cap):
    event_list = []
    queue = []
    server_free = True
    total_waiting_time = 0
    total_queue_time = 0
    num_events = 1
    idle = 0
    timer = 0
    event_list.append((0,"in"))
    
    
    while event_list:
        # "reading" packet arrival step 1
        arriving_event = event_list.pop(0)
        
        #step 2
        if arriving_event[1] == "in":
            # add tuple to list
            queue.append(arriving_event)
            # new event generation
            next_event = (arriving_event[0] + exponential_distribution(1,arrival_rate)[0], "in")
            print(next_event)
            event_list.append(next_event)
            
            
        #step 3 
        else:
            # else mark server as free and count the waiting time
            server_free = True
            total_waiting_time += arriving_event[0] - arriving_event[0] 
            
            
        # server is free queue is empty calculate idle time step 4
        if (server_free and not queue):
            idle += arriving_event[0] - timer
            timer = arriving_event[0]
            continue
        
        #process the queue step 5
        if server_free:
            arriving_event = queue.pop(0)
            server_free = False
        
            # add to the event list
            event_list.append((arriving_event[0] + exponential_distribution(1,service_rate)[0], "out"))
            num_events += 1
            total_queue_time += arriving_event[0]- timer
            total_waiting_time += arriving_event[0] - timer
            timer = arriving_event[0]
        
        #num events is over event cap
        if num_events >= event_cap:
            break
    total_time = timer
    
    stats(total_waiting_time, num_events, total_queue_time, total_time, idle)
    return 
    

if __name__== "__main__":
    arrival_lambda = float(input("Arrival rate\n"))
    service_lambda = float(input("Service rate\n"))
    time_cap = int(input("event cap\n"))
    processing(arrival_lambda, service_lambda, time_cap)