"""
问题：给对象的内部属性设置类型限制
"""

# Descriptor attribute
class Integer:
    def __init__(self, name) -> None:
        self.name = name
    
    # get, set, delete 就是所谓的属性访问操作，
    # 比如 `x.a = 1` `x.a` 这类
    # 就会调用 set 和 get 。
    def __get__(self, instance, cls):
        print(f"calling get method in Integer")
        if instance is None:
            return self 
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        print(f"calling set method in Integer")
        if not isinstance(value, int):
            raise TypeError(f"Expected an int, provided {type(value)}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Point:
    # 这里我们通过类属性施加约束类型
    # 注意这里的 x，y 要跟 init 里面的 self.x self.y 名字一样
    x = Integer("x")
    y = Integer("y")

    def __init__(self, x, y) -> None:
        self.x = x  # 这里其实就在调用 Instance 
        # 的 __set__
        self.y = y

        
p = Point(1, 2)
print(p.x)
p.y = 2
p = Point(1, 1.1)
# Raise TypeError here due 1.1 