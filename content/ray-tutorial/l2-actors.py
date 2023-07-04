import asyncio
import ray
from ray.util.queue import Queue, Empty


@ray.remote
class Actor:
    pass 

@ray.remote
class Greeter:
    def __init__(self, value):
        self.value = value

    def say_hello(self):
        return self.value


# Actor `g1` doesn't yet exist, so it is created with the given args.
a = Greeter.options(name="g1", get_if_exists=True).remote("Old Greeting") # type: ignore
assert ray.get(a.say_hello.remote()) == "Old Greeting"

# Actor `g1` already exists, so it is returned (new args are ignored).
b = Greeter.options(name="g1", get_if_exists=True).remote("New Greeting") # type: ignore
assert ray.get(b.say_hello.remote()) == "Old Greeting"

## Terminating Actor
ray.kill(b)

## Async IO
@ray.remote
class AsyncActor:
    # multiple invocation of this method can be running in
    # the event loop at the same time
    async def run_concurrent(self):
        print("started")
        await asyncio.sleep(2) # concurrent workload here
        print("finished")

actor = AsyncActor.remote()

ray.get([actor.run_concurrent.remote() for _ in range(4)]) # type: ignore

### Set max concurrency
actor = AsyncActor.options(max_concurrency=2).remote()
ray.get([actor.run_concurrent.remote() for _ in range(4)]) # type: ignore

### Concurrency Group
@ray.remote(concurrency_groups={"io": 2, "compute": 4})
class AsyncIOActor:
    def __init__(self):
        pass

    @ray.method(concurrency_group="io")
    async def f1(self):
        pass

    @ray.method(concurrency_group="io")
    async def f2(self):
        pass

    @ray.method(concurrency_group="compute")
    async def f3(self):
        pass

    @ray.method(concurrency_group="compute")
    async def f4(self):
        pass

    async def f5(self):
        pass

a = AsyncIOActor.remote()
a.f1.remote()  # executed in the "io" group.
a.f2.remote()  # executed in the "io" group.
a.f3.remote()  # executed in the "compute" group.
a.f4.remote()  # executed in the "compute" group.
a.f5.remote()  # executed in the default group.

### Queue
queue = Queue(maxsize=100)

@ray.remote
def consumer(id, queue):
    try:
        while True:
            next_item = queue.get(block=True, timeout=1)
            print(f"consumer {id} got work {next_item}")
    except Empty:
        pass


[queue.put(i) for i in range(10)]
print("Put work 1 - 10 to queue...")

consumers = [consumer.remote(id, queue) for id in range(2)]
ray.get(consumers)