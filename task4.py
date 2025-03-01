import hazelcast
import multiprocessing

def create_client():
    return hazelcast.HazelcastClient(cluster_name="hello-world", smart_routing=True)

def increment():
    client = create_client()
    map4 = client.get_map("map4").blocking()
    for _ in range(10_000):
        value = map4.get("key")  
        new_value = value + 1        
        map4.put("key", new_value)
    client.shutdown()

if __name__ == "__main__":
    client = create_client()
    map4 = client.get_map("map4").blocking()
    map4.put_if_absent("key", 0)
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
    map4 = client.get_map("map4").blocking()
    final_value = map4.get("key")
    print(f"Key value: {final_value}")
    client.shutdown()