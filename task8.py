import hazelcast
import multiprocessing

def create_client():
    return hazelcast.HazelcastClient(cluster_name="hello-world", smart_routing=True)

def produce():
    client = create_client()
    queue = client.get_queue("bounded-queue").blocking()
    
    for i in range(100):
        print(f"putting {i + 1}")
        queue.put(i + 1)  
        print(f"put {i + 1}")
    
    print("producer done")
    client.shutdown()

def consume(id):
    client = create_client()
    queue = client.get_queue("bounded-queue").blocking()

    while True:
        item = queue.take()  
        print(f"{id}: consumed {item}")

    client.shutdown()

if __name__ == "__main__":
    client = create_client()
    client.shutdown()

    prod = multiprocessing.Process(target=produce)
    cons1 = multiprocessing.Process(target=consume, args=(1,))
    cons2 = multiprocessing.Process(target=consume, args=(2,))

    prod.start()
    cons1.start()
    cons2.start()

    prod.join()
    cons1.terminate()
    cons2.terminate()