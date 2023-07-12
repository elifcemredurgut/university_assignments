from abc import ABC, abstractmethod
from multiprocessing import Process
import zmq

class MapReduce:
    def __init__(self, num_worker):
        self.num_worker = num_worker

    @abstractmethod
    def Map(self, map_input):
        pass

    @abstractmethod
    def Reduce(self, reduce_input):
        pass

    def Producer(self, l):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://127.0.0.1:5557")
        n = self.num_worker
        work_per_worker = len(l) // n
        remainder = len(l) % n
        for i in range(n):
            message = ""
            for j in range(work_per_worker):
                message += l[0]
                l.pop(0)
            if remainder > 0:
                message += l[0]
                l.pop(0)
                remainder -= 1
            work_message = {'num' : message}
            socket.send_json(work_message)

    def Consumer(self):
        context = zmq.Context()
        # receive work
        consumer_receiver = context.socket(zmq.PULL)
        consumer_receiver.connect("tcp://127.0.0.1:5557")
        
        # send work
        consumer_sender = context.socket(zmq.PUSH)
        consumer_sender.connect("tcp://127.0.0.1:5558")
        
        work = consumer_receiver.recv_json()
        data = work['num']
        list_to_be_sent = []
        l = data.split('\n')
        for i in l:
            m = i.split('\t')
            FromNodeId = m[0]
            ToNodeId = m[1]
            list_to_be_sent.append({FromNodeId : ToNodeId})
        result = self.Map(list_to_be_sent)
        consumer_sender.send_json(result) #????
    
    def ResultCollector(self):
        context = zmq.Context()
        # receive work
        collector_receiver = context.socket(zmq.PULL)
        collector_receiver.connect("tcp://127.0.0.1:5558")       

        num_of_workers_so_far = 0  #burda sorun olabilir
        results = []
        while True:
            work = collector_receiver.recv_json()
            results.append(work)
            if num_of_workers_so_far >= 10:
                break
            num_of_workers_so_far += 1

        final = self.Reduce(results)
        f = open("results.txt", "w")
        f.write(final)
        f.close()


    def start(self, filename):
        lines = ""
        with open(filename, "r") as f:
            lines = f.readlines()

        Producer_process = Process(target=self.Producer, args=(lines,))
        Producer_process.start()
        
        Consumer_process = Process(target=self.Consumer)
        Consumer_process.start()

        Collector_process = Process(target=self.ResultCollector)
        Collector_process.start()

        Producer_process.join()
        Consumer_process.join()
        Collector_process.join()
    