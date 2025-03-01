import time
import hazelcast
import multiprocessing

def create_client():
    return hazelcast.HazelcastClient(cluster_name="hello-world", smart_routing=True)

def increment():
    client = create_client()
    map6 = client.get_map("map6").blocking()
    for _ in range(10_000):
        while True:
            value = map6.get("key")  
            new_value = value + 1        
            if map6.replace_if_same("key", value, new_value):  
                break 
    client.shutdown()


if __name__ == "__main__":
    a = time.time()
    client = create_client()
    map5 = client.get_map("map6").blocking()
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
    map5 = client.get_map("map6").blocking()
    final_value = map5.get("key")
    b = time.time()
    print(f"Key value: {final_value}")
    print(f"Time: {b - a}s")
    client.shutdown()