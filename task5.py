import time
import hazelcast
import multiprocessing

def create_client():
    return hazelcast.HazelcastClient(cluster_name="hello-world", smart_routing=True)

def increment():
    client = create_client()
    map5 = client.get_map("map5").blocking()
    for _ in range(10_000):
        map5.lock("key")
        value = map5.get("key")  
        new_value = value + 1        
        map5.put("key", new_value)
        map5.unlock("key")
    client.shutdown()

if __name__ == "__main__":
    a = time.time()
    client = create_client()
    map5 = client.get_map("map5").blocking()
    map5.put_if_absent("key", 0)
    client.shutdown()

    process1 = multiprocessing.Process(target=increment)
    process2 = multiprocessing.Process(target=increment)
    process3 = multiprocessing.Process(target=increment)

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    client = create_client()
    map5 = client.get_map("map5").blocking()
    final_value = map5.get("key")
    b = time.time()
    print(f"Key value: {final_value}")
    print(f"Time: {b - a}s")
    client.shutdown()