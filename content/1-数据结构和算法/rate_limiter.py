import time
from typing import Callable

class TokenBucket:
    
    def __init__(self, token: int, time_unit: int, forward_callback: Callable, drop_callback: Callable) -> None:
        self.token = token
        self.time_unit = time_unit
        self.forward = forward_callback
        self.drop = drop_callback
        
        self._last_check = time.time()
        self._bucket = token

    def handle(self, message):
        """
        Case 1:
        
        every 1 seconds, not more than 1 msg.

        token = 1
        time_unit = 1
        token / time_unit = 1
        bucket = token = 1
        
        time, time pass, bucket, last check
        0, 1, 0
        5, 5, 1, 5, pass, 0
        5.1, 0.1, 0.1, 5.1, stop
        5.2, 0.1, 0.2, 5.2, stop
        6.1, 1.1, 0.3, 6.1, pass
        """
        current = time.time()
        time_passed = current - self._last_check
        self._last_check = current

        self._bucket += time_passed * (self.token / self.time_unit)
        print(f"{ self._bucket = }")
        print(f"{ self.token / self.time_unit = }")

        if self._bucket > self.token:
            self._bucket = self.token
        
        if self._bucket < 1:
            self.drop(message)
        else:
            self._bucket -= 1
            self.forward(message)


class LeakyBucket:
    def __init__(self, capacity, rate):
        self.capacity = float(capacity)
        self.rate = float(rate)
        # self.tokens = capacity  # <
        self.tokens = 0  # <
        self.last_updated = time.time()

    def consume(self, amount):
        # Calculate the time elapsed since last update
        now = time.time()
        elapsed_time = now - self.last_updated

        # Add tokens to the bucket based on the elapsed time and rate
        self.tokens = min(self.capacity, self.tokens + elapsed_time * self.rate)

        # Check if there are enough tokens to consume
        if amount <= self.tokens:
            self.tokens -= amount
            self.last_updated = now
            return True
        else:
            return False
            
class FixedWindow:

    def __init__(self, capacity, forward_callback, drop_callback):
        self.current_time = int(time.time())
        self.allowance = capacity
        self.capacity = capacity
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback

    def handle(self, packet):
        if (int(time.time()) != self.current_time):
            self.current_time = int(time.time())
            self.allowance = self.capacity

        if (self.allowance < 1):
            return self.drop_callback(packet)

        self.allowance -= 1
        return self.forward_callback(packet)


if __name__ == "__main__":

    def forward(packet):
        print("Packet Forwarded: " + str(packet))


    def drop(packet):
        print("Packet Dropped: " + str(packet))


    throttle = TokenBucket(1, 1, forward, drop)

    # packet = 0
    # while True:
    #     time.sleep(0.2)
    #     throttle.handle(packet)
    #     packet += 1


    # bucket = LeakyBucket(10, 1)  # Allow 2 requests per 2 seconds

    # for i in range(20):
    #     if bucket.consume(1):
    #         print(f"Request {i} allowed")
    #     else:
    #         print(f"Request {i} denied")
        # time.sleep(0.99)  # Wait 0.1 seconds between requests
        
    bucket = LeakyBucket(10, 1)  # Allow 10 requests per second

    # Simulate a burst of 100 requests in a 1-second window
    for i in range(100):
        if bucket.consume(1):
            print(f"Request {i} allowed")
        else:
            print(f"Request {i} denied")

    # Wait for the bucket to refill
    time.sleep(1)

    # Simulate 10 requests per second after the burst
    for i in range(10):
        if bucket.consume(1):
            print(f"Request {i+100} allowed")
        else:
            print(f"Request {i+100} denied")