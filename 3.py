import random
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

def stats( total_queue_time, total_processing_time,packets_served ,ending_timer,system_idle_time, arrival_rate, service_rate):
    
    rho = arrival_rate / service_rate
    Lq = rho**2 / (1 - rho)
    print("Theoretical Average Queue Size",Lq)
    
    # falta calcular do experimental
    
    total_waiting_time =  total_queue_time + total_processing_time
    print ("------------------------------------")

    average_packet_time_in_system =  total_waiting_time/packets_served if packets_served > 0 else 0
    print("Average packet time in system: ", average_packet_time_in_system)
    Ws = 1 / (service_rate - arrival_rate)
    print("Theoretical Average Packet Time in the system: ", Ws)
    
    print ("------------------------------------")
    average_packet_time_in_queue = total_queue_time / packets_served if packets_served > 0 else 0
    print("Average packet waiting time: ", average_packet_time_in_queue)
    Wq = Ws - (1 / service_rate)
    print("Theoretical Average Packet Time in the queue",Wq)

    #falta o teorico
    print ("------------------------------------")
    total_busy_time =  (ending_timer - system_idle_time)/ending_timer
    print("Total busy time: ", total_busy_time)
    
    return

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
    
    
    #
    timer = 0
    event_list.append((0,"in"))
    
    idle_since = float(0)
    
    while event_list:
        # "reading" packet arrival step 1
        current_event = event_list.pop(0)
    
        #step 2
        if current_event[1] == "in" and not block_in_creation:
            # add tuple to list
            
            # new event generation
            if packet_arrived <= event_cap:
                queue.put(current_event)
                next_event = (current_event[0] + exponential_distribution(1,arrival_rate)[0], "in")
                event_list.append(next_event)
                packet_arrived += 1
                sorted(event_list, key=lambda x: x[0])
            #jump to 4
            else: 
                block_in_creation = True
                continue
            
        #step 3 
        else:
            # else mark server as free and count the waiting time
            server_free = True
            idle_since = current_event[0]
            packets_served += 1
            

            
        #step 4
        # server is free queue is empty 
        if (server_free and queue.empty()):
            timer = current_event[0]
            continue
 
        if not server_free:
            timer = current_event[0]
            continue
        
        leaving_event = queue.get()
        server_free = False
    
        if idle_since is not None:
            system_idle_time += leaving_event[0] - idle_since
            idle_since = None
            
            
        # add to the event list (é preciso guardar o timestamp para manter o tempo de processamento)
        time_in_processing = current_event[0] + exponential_distribution(1,service_rate)[0]
        event_list.append((time_in_processing, "out"))
        event_list = sorted(event_list, key=lambda x: x[0])
        
        
        total_queue_time += current_event[0]- leaving_event[0]
        total_processing_time += time_in_processing - current_event[0]
        timer = current_event[0]

        
        #num events is over event cap
        if timer > event_cap and packets_served == packet_arrived:
            break
            
    ending_timer = timer
    
    stats(total_queue_time, total_processing_time, packets_served, ending_timer, system_idle_time, arrival_rate, service_rate)
    return 
    

if __name__== "__main__":
    arrival_lambda = float(input("Arrival rate\n"))
    service_lambda = float(input("Service rate\n"))
    time_cap = int(input("event cap\n"))
    processing(arrival_lambda, service_lambda, time_cap)