"""
接口（Interface）的实现

接口是软件工程中最重要的工具之一，是依赖注入的基础，也是增加软件拓展性的方法。
"""
from abc import ABC, abstractmethod


class IStream(ABC):

    @abstractmethod
    def read(self, maxbytes: int=-1) -> bytes:
        raise NotImplemented()
    
    @abstractmethod
    def write(self, data: bytes):
        raise NotImplemented()


class SocketStream(IStream):
    
    def read(self, maxbytes: int = -1) -> bytes:
        ...

    def write(self, data: bytes):
        ...

        
class SomethingUseStream:
    
    def __init__(self, stream: IStream) -> None:
        self.s = stream


if __name__ == "__main__":
    ...   
    # 不能直接实例化抽象类（也就是我们的接口）
    # interface = IStream()

    stream = SocketStream()