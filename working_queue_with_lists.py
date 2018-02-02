from Queue import Queue
from threading import Thread

def do_stuff(q):
  while True:
    res=q.get()
    print("res =" + str(res['x+y']))
    print
    q.task_done()

q = Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
  worker = Thread(target=do_stuff, args=(q,))
  worker.setDaemon(True)
  worker.start()

for y in range (100):
  for x in range(10):
    q.put({'x':x,'y':y,'x+y':x + y * 100})
  q.join()
  print "Batch " + str(y) + " Done"
