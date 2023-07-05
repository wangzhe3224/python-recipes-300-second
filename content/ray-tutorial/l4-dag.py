import ray

ray.init()

@ray.remote
def func(src, inc=1):
    return src + inc

a = func.bind(1, inc=2)
b = func.bind(a, inc=3)
c = func.bind(a, inc=b)

print(ray.get(c.execute()))