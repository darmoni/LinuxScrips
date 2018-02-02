from multiprocessing import Process, Queue

def my_function(q, x):
    q.put(x + 100)

if __name__ == '__main__':
    queue = Queue()
    p = Process(target=my_function, args=(queue, 1))
    p.start()
    p.join() # this blocks until the process terminates
    result = queue.get()
    print result
