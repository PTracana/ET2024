import random
from statistics import mean
from matplotlib import pyplot as plt
import numpy as np
import math 
import time
import queue as qu

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

def stats( total_queue_time, total_processing_time,packets_served ,ending_timer,system_idle_time, arrival_rate, service_rate,queue_size_array):
    
    rho = arrival_rate / service_rate
    
    print ("------------------------------------")
    total_waiting_time =  total_queue_time + total_processing_time
    average_packet_time_in_system =  total_waiting_time/packets_served if packets_served > 0 else 0
    print("Average packet time in system: ", average_packet_time_in_system)
    try:
        Ws = 1 / (service_rate - arrival_rate)
    except ZeroDivisionError:
        Ws = float('inf')
    print("Theoretical Average Packet Time in the system: ", Ws)
    
    print ("------------------------------------")
    average_packet_time_in_queue = total_queue_time / packets_served if packets_served > 0 else 0
    print("Average packet waiting time: ", average_packet_time_in_queue)
    Wq = Ws - (1 / service_rate)
    print("Theoretical Average Packet Time in the queue",Wq)

    print ("------------------------------------")
    average_size = average_queue_size(queue_size_array)
    print("Average queue size: ", average_size)
    Lq = arrival_rate * Wq
    print("Theoretical Average Queue Size",Lq)

    print ("------------------------------------")
    total_busy_time =  (ending_timer - system_idle_time)/ending_timer *100
    print("Percentage of time busy % : ", total_busy_time)
    print("Theoretical busy time % :",rho*100 )

    
    return

def average_queue_size(queue_size_array):
    sizes = [size[1] for size in queue_size_array]
    return mean(sizes)

def processing(arrival_rate, service_rate, event_cap):
    event_list = []
    queue = qu.Queue()
    server_free = True
    total_queue_time = float(0)
    total_processing_time = float(0)
    system_idle_time = float(0)
    packet_arrived = 0
    packets_served = 0
    block_in_creation = False
    # This list storages tuples that allow to understand the size of queue overtime per timestamp - tuple (timestamp,len(queue))
    queue_size_array = []
    timer = 0
    event_list.append((0,"in"))
    idle_since = float(0)
    
    while event_list:
        # If number of events is the maximum value of events
        if packets_served >= event_cap:
            break
            
        # Step 1 - Read the next tuple from the event list
        current_event = event_list.pop(0)
    
        # Step 2 - If the event type is an arrival
        if current_event[1] == "in" and not block_in_creation:
            # Add new arrival to the queue and generate new arrival event to append into the list
            if packets_served <= event_cap:
                queue.put(current_event)
                next_event = (current_event[0] + exponential_distribution(1,arrival_rate)[0], "in")
                event_list.append(next_event)
                packet_arrived += 1
                event_list = sorted(event_list, key=lambda x: x[0])
            # Jump to Step 4
            else: 
                block_in_creation = True
                continue
            
        # Step 3 - If the event type is a processing 
        else:
            # Mark server as free and count the waiting time
            server_free = True
            idle_since = current_event[0]
            packets_served += 1
        
        # Step 4 - if the server is free and the queue is empty
        if (server_free and queue.empty()):
            timer = current_event[0]
            queue_size_array.append((current_event[0],queue.qsize()))
            continue
 
        if not server_free:
            timer = current_event[0]
            queue_size_array.append((current_event[0],queue.qsize()))
            continue
        
        # Step 5 - Process the packet inside the queue  
        leaving_event = queue.get()
        server_free = False
        # If the previous event was a processing, calculate the idle time in between
        if idle_since is not None:
            system_idle_time += current_event[0] - idle_since
            #system_idle_time += leaving_event[0] - idle_since
            idle_since = None
        
        time_in_processing = current_event[0] + exponential_distribution(1,service_rate)[0]
        event_list.append((time_in_processing, "out"))
        event_list = sorted(event_list, key=lambda x: x[0])
        # Count the time the leaving packet was inside the queue
        total_queue_time += current_event[0]- leaving_event[0]
        # Count the processing time for the leaving packet
        total_processing_time += time_in_processing - current_event[0]
        timer = current_event[0]
        queue_size_array.append((current_event[0],queue.qsize()))

    ending_timer = timer
    stats(total_queue_time, total_processing_time, packets_served, ending_timer, system_idle_time, arrival_rate, service_rate,queue_size_array)

    #Plot the queue size over time
    x_axis = [value[0] for value in queue_size_array]
    y_axis = [value[1] for value in queue_size_array]
    plt.plot(x_axis,y_axis)
    plt.xlabel('Time(Seconds)')
    plt.ylabel('Queue Size')
    plt.title('Queue Size over time with λ = ' + str(arrival_rate) + ' , μ = ' + str(service_rate) + ' for N = ' + str(event_cap))
    plt.grid(True)
    plt.show()
    return 
    

if __name__== "__main__":
    #Lq = 1 -> rho ≃ 0.61803 -> lambda = 6.1803 and miu = 10
    #Lq = 10 -> rho ≃ 0.91608 -> lambda = 9.1608 and miu = 10
    #Lq = 100 -> rho ≃ 0.99020 -> lambda = 9.9020 and miu = 10
    #Lq = 1000 -> rho ≃ 0.99900 -> lambda = 9.9900 and miu = 10
    arrival_lambda = float(input("Arrival rate\n"))
    service_lambda = float(input("Service rate\n"))
    event_cap = int(input("event cap\n"))
    processing(arrival_lambda, service_lambda, event_cap)