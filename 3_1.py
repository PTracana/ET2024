import numpy as np
import queue as qu
import math 
import random
import time

class MM1Queue:
    # Generate an instance of the class MM1Queue
    def __init__(self, lambda_, miu_,arrivals):
        self.lambda_ = lambda_
        self.miu_ = miu_
        self.rho = lambda_ / miu_
        self.system_clock = 0  
        self.server_free = True
        self.event_list = qu.Queue()
        self.packet_queue = qu.Queue()
        self.arrivals_processed = 0
        self.num_arrivals = arrivals

    def simulation_loop(self):
        while self.arrivals_processed < self.num_arrivals:
            event_time, event_type = self.event_list.get()
            self.system_clock = event_time # Update the system clock

            if event_type == 'arrival':
                self.handle_arrival(event_time)
                if self.server_free:
                    self.handle_processing(event_time)
            else:
                self.handle_processing(event_time)

    def schedule_event(self, event_time, event_type):
        self.event_list.put((event_time, event_type))


    def handle_arrival(self,event_time):
        self.packet_queue.put(event_time)
        next_time_arrival = self.arrival_exponential_distribution()
        if self.arrivals_processed < self.num_arrivals:
            self.schedule_event(next_time_arrival, 'arrival')
            self.arrivals_processed += 1
        
        
    def handle_processing(self,event_time):
        self.server_free = True # First thing to do to process the next departure is to declare the server's state as Free
        if not self.packet_queue.empty():
            next_departure_time = event_time + self.processing_exponential_distribution()
            self.schedule_event(next_departure_time, 'processing')
            self.server_free = False # Server is now gonna process the first element in the FIFO queue

            self.total_time_in_queue += event_time - self.last_event_time
            self.last_event_time = event_time

            self.packet_queue.get() # Remove first element in queue

    def arrival_exponential_distribution(self):
        # Generates a random time t according to the exponential distribution
        random.seed(time.time())
        u = random.random()
        delta_t = -math.log(1-u)/self.lambda_
        next_arrival_time = self.system_clock + delta_t
        return next_arrival_time
    
    def processing_exponential_distribution(self):
        # Generates a random time t according to the exponential distribution
        random.seed(time.time())
        u = random.random()
        delta_t = -math.log(1-u)/self.miu_
        return delta_t

    def print_statistics(self):
        # Theoretical Utilization Factor
        print("Utilization Factor",self.rho)
        
        # Theoretical Average Queue Size (Lq)
        Lq = self.rho**2 / (1 - self.rho)
        print("Theoretical Average Queue Size",Lq)
        '''
        # Theoretical Average Packet Time in the system
        Ws = 1 / (self.miu_ - self.lambda_)
        print("Theoretical Average Packet Time in the system",Ws)
        # Theoretical Average Packet Time in the Queue
        Wq = Ws - (1 / self.miu_)
        print("Theoretical Average Packet Time in the queue",Wq)
        # Theoretical number of events in the system
        Ls = Ws * self.lambda_
        print("Theoretical number of events in the system",Ls)
        '''
        average_queue_size= self.packet_queue.qsize()/ (self.num_arrivals + 1)
        print("Experimental Average queue size:",average_queue_size)

def main():
    '''
    To provide combinations of lambda and miu that have an average queue size of 1, 10, 100 and 1000, use the following parameters for each target average queue size
    Lq = 1 -> rho ≃ 0.70710 -> lambda = 7071 and miu = 10000
    Lq = 10 -> rho ≃ 0.95346 -> lambda = 9534 and miu = 10000
    Lq = 100 -> rho ≃ 0.99503 -> lambda = 9950 and miu = 10000
    Lq = 1000 -> rho ≃ 0.99950 -> lambda = 9995 and miu = 10000

    '''
    lambda_ = [0.7]
    miu_ = [1]
    arrivals = 1000

    # Run simulation
    for i in range(len(lambda_)):
        simulation = MM1Queue(lambda_[i], miu_[i],arrivals)
        simulation.schedule_event(0,'arrival')
        simulation.simulation_loop()
        '''
        average_queue_size = np.mean([(simulation.packet_queue.qsize())])
        Lq = simulation.rho**2 / (1 - simulation.rho)
        print("Average queue size",average_queue_size)
        print("Theoretical average queue size",Lq)
        '''
        simulation.print_statistics()

if __name__== "__main__":
    main()