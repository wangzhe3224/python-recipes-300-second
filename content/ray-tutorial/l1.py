from typing import Callable
from dataclasses import dataclass
import ray
import time

@dataclass
class Node:
 
    func: Callable

    def compute(self):
        ...

ray.init()

# task 
@ray.remote
def square(x):
    return x * x 

futures = [square.remote(i) for i in range(4)]

print(ray.get(futures))

# actor
@ray.remote
class Counter:
    def __init__(self) -> None:
        self._i = 0
        
    def get(self):
        return self._i 
    
    def inrc(self, value):
        print(f"sleep for {value}")
        time.sleep(value)
        self._i += value

        
c = Counter.remote()
c2 = Counter.remote()
for i in range(10):
    c.inrc.remote(1) # type: ignore
    c2.inrc.remote(1) # type: ignore

    
print(ray.get(c.get.remote())) # type: ignore
print(ray.get(c2.get.remote())) # type: ignore

## Objects
import numpy as np 

@ray.remote
def sum_matrix(m):
    return np.sum(m)

print(ray.get(sum_matrix.remote(np.ones((100, 100)))))

m_ref = ray.put(np.ones((1000, 1000)))

print(ray.get(sum_matrix.remote(m_ref)))

## More tasks
import operator
@ray.remote
def inc(x):
    return x + 1

@ray.remote
def double(x):
    return x * 2

@ray.remote
def add(x, y):
    return x + y

@ray.remote
def _sum(*args):
    return sum(args)

data = [1, 2, 3, 4, 5]

outs = []
for x in data:
    a = inc.remote(x)
    b = double.remote(x)
    c = add.remote(a, b)
    print(f"{a = }\n{b = }\n{c = }")
    outs.append(c)

total = _sum.remote(*outs)  # When an object is passed within a nested object, for example, within a Python list, Ray will not de-reference it

ray.get(total)  # ray.get, get ref value, if not computed, trigger computation
type(total)  # type: ObjectRef, .remote method create a ObjectRef
num_100 = ray.put(100)  # ray.put puts a value in store, gives back a ObjectRef


@ray.remote
def echo_and_get(x_list):  # List[ObjectRef]
    """This function prints its input values to stdout."""
    print("args:", x_list)
    print("values:", ray.get(x_list))


# Put the values (1, 2, 3) into Ray's object store.
a, b, c = ray.put(1), ray.put(2), ray.put(3)
# Passing an object as a nested argument to `echo_and_get`. Ray does not
# de-reference nested args, so `echo_and_get` sees the references.
echo_and_get.remote([a, b, c])
# -> prints args: [ObjectRef(...), ObjectRef(...), ObjectRef(...)]
#           values: [1, 2, 3]

## Multiple returns
@ray.remote(num_returns=3)
def return_multiple():
    return 1, 2, 3

r1, r2, r3 = return_multiple.remote() # type: ignore

@ray.remote(num_returns=3)
def return_multiple_gen():
    for i in range(3):
        yield i

r1, r2, r3 = return_multiple_gen.remote() # type: ignore

## Nested function call
@ray.remote
def f():
    return 1

@ray.remote
def g():
    return [f.remote() for _ in range(4)] 

@ray.remote 
def h():
    return ray.get([f.remote() for _ in range(4)])

ray.get(g.remote())
ray.get(h.remote())