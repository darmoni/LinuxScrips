#!/usr/bin/env python

from threading import Thread
from kafka import KafkaConsumer, KafkaProducer
import ConfigParser as configparser
import signal, time

client_id='XCASTLABS_events_debug_consumer'
resources=[]
def safe_exit():
    counter=1
    for r in resources:
        print ("deleting {}\n".format(counter))
        del r
        counter +=1
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def read_consumer(consumer,topic):
    try:
        #consumer.seek_to_beginning()
        print("ready to consume topic {}".format(topic))
        metrics = consumer.metrics()
        for key in metrics:
            print ("{}:{}\n".format(key,metrics[key]))
        while True:
            print(topic+"\n")
            for msg in consumer:
                print (msg.value)
            else:
                time.sleep(0.1)
            continue
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')
        resources.remove(consumer)
    consumer.close()
    resources.remove(consumer)

if __name__ == '__main__':
    file_config = configparser.ConfigParser()
    file_config.read(['middle_producer_setup.cfg'])
    #log.configure(file_config.get('log', 'level'))

    cfg_bootstrap_servers = file_config.get('consumer', 'bootstrap_servers')
    if (cfg_bootstrap_servers):
        bootstrap_servers= cfg_bootstrap_servers.split(", ")
        if(len(bootstrap_servers)>1):
            consumer_bootstrap_server=bootstrap_servers[0]
    #print (bootstrap_servers)
    #topic=file_config.get('access', 'testing_topic')
    security_protocol = file_config.get('access', 'security_protocol')
    if('SASL_PLAINTEXT'== security_protocol):
        sasl_mechanism= file_config.get('access', 'sasl_mechanism')
        user = file_config.get('access', 'sasl_plain_username')
        password = file_config.get('access', 'sasl_plain_password')
    compression=file_config.get('access', 'compression') 

    topics=file_config.get('access', 'topics').split(",")
    '''
    if(2 > topics):
        print(len(topics))
        topic=topics[0]
    '''

    for t in topics:
        consumer = KafkaConsumer(t, client_id=client_id, bootstrap_servers=consumer_bootstrap_server,
            security_protocol=security_protocol, sasl_mechanism=sasl_mechanism,
            sasl_plain_username=user,sasl_plain_password=password)
        if consumer:
            middle_worker = Thread(target=read_consumer, args=(consumer,t))
            middle_worker.setDaemon(True)
            middle_worker.start()
            resources.append(consumer)
    while resources:
        time.sleep(3)
