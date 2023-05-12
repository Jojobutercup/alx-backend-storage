#!/usr/bin/env python3

class Cache:
    def __init__(self):
        self.calls = []

    def store(self, value):
        call = (value, str(uuid.uuid4()))
        self.calls.append(call)
        return call[1]

def replay(func):
    calls = [call for call in func.calls if call[0] == func.store]
    print(f"{func.__name__} was called {len(calls)} times:")
    for call in calls:
        args_str = ", ".join([repr(arg) for arg in call[:-1]])
        print(f"{func.__name__}(*({args_str},)) -> {call[-1]}")

cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store("egg")
cache.store("eggsperiment")
replay(cache.store)

