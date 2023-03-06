""" 
TypedDict since Python 3.8

Ref: https://docs.python.org/3.10/library/typing.html#typing.TypedDict

A simple typed namespace. At runtime it is equivalent to a plain dict.
"""
from typing import TypedDict


# 常规定义
class Point2D(TypedDict):
    x: int
    y: int
    label: str

a: Point2D = {'x': "ss", 'y': 2, 'label': 'good'}  # OK
b: Point2D = {'z': 3, 'label': 'bad'}           # Fails type check

assert Point2D(x=1, y=2, label='first') == dict(x=1, y=2, label='first')

# 快速定义
Point2D = TypedDict('Point2D', x=int, y=int, label=str)
Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})