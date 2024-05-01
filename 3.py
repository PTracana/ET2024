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

def stats(total_waiting_time, num_events, total_queue_time, total_time, idle, arrival_rate, service_rate):
    
    rho = arrival_rate / service_rate
    Lq = rho**2 / (1 - rho)
    print("Theoretical Average Queue Size",Lq)
    # falta calcular do experimental
    
    print ("------------------------------------")

    average_packet_time_in_system =  (total_waiting_time + total_queue_time)/num_events
    print("Average packet time in system: ", average_packet_time_in_system)
    Ws = 1 / (service_rate - arrival_rate)
    print("Theoretical Average Packet Time in the system: ", Ws)
    
    print ("------------------------------------")
    average_packet_time_in_queue = total_waiting_time/num_events
    print("Average packet waiting time: ", average_packet_time_in_queue)
    Wq = Ws - (1 / service_rate)
    print("Theoretical Average Packet Time in the queue",Wq)

    #falta o teorico
    total_busy_time = (total_time - idle) / total_time *100
  #  print("Total busy time: ", total_busy_time)
    
    return

def processing(arrival_rate, service_rate, event_cap):
    event_list = []
    queue = []
    server_free = True
  
    total_waiting_time = 0

    total_queue_time = 0
    num_events = 1
    #
    idle = 0
    timer = 0
    event_list.append((0,"in"))
    
    idle_since = 0
    
    while event_list:
        # "reading" packet arrival step 1
        arriving_event = event_list.pop(0)
        
        #step 2
        if arriving_event[1] == "in":
            # add tuple to list
            queue.append(arriving_event)
            # new event generation
            next_event = (arriving_event[0] + exponential_distribution(1,arrival_rate)[0], "in")
            event_list.append(next_event)
            
            
        #step 3 
        else:
            # else mark server as free and count the waiting time
            server_free = True
            idle_since += arriving_event[0]
            
            total_waiting_time += arriving_event[0] - timer 
            
        #step 4
        # server is free queue is empty calculate idle time 
        if (server_free and not queue):
            timer = arriving_event[0]

        elif  server_free and queue:
            leaving_event = queue.pop(0)
            server_free = False
        
            if idle_since != 0:
                idle += leaving_event[0] - idle_since
                idle_since = 0
                
            # add to the event list
            leaving_time = leaving_event[0] + exponential_distribution(1,service_rate)[0]
            event_list.append((leaving_time, "out"))
            num_events += 1
            total_queue_time += arriving_event[0]- timer
            total_waiting_time += arriving_event[0] - timer
            timer = arriving_event[0]

        
        #num events is over event cap
        if num_events >= event_cap:
            break
        
        
    total_time = timer
    
    stats(total_waiting_time, num_events, total_queue_time, total_time, idle, arrival_rate, service_rate)
    return 
    

if __name__== "__main__":
    arrival_lambda = float(input("Arrival rate\n"))
    service_lambda = float(input("Service rate\n"))
    time_cap = int(input("event cap\n"))
    processing(arrival_lambda, service_lambda, time_cap)