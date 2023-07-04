import ray
import time 
import numpy as np

def partiotion(collection):
    pivot = collection.pop()
    greater, lesser = [], []
    for elem in collection:
        if elem > pivot:
            greater.append(elem)
        else:
            lesser.append(elem)
    
    return greater, pivot, lesser

@ray.remote
def quick_sort(collection):
    if len(collection) < 100000:
        return sorted(collection)
    else:
        greater, pivot, lesser = partiotion(collection)
        lesser = quick_sort.remote(lesser)
        greater = quick_sort.remote(greater)
        return ray.get(lesser) + [pivot] + ray.get(greater)

    
unsorted = np.random.randint(1000000, size=(1000000)).tolist()
s = time.time()
ray.get(quick_sort.remote(unsorted))
print(f"Distributed execution: {(time.time() - s):.3f}")