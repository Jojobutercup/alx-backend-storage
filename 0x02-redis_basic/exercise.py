#!/usr/bin/env python3

from typing import Callable

def replay(func: Callable) -> None:
    """Replay the history of calls to a function."""
    # Retrieve the keys for the input and output lists
    input_key = f"{func.__qualname__}:inputs"
    output_key = f"{func.__qualname__}:outputs"
    # Get the input and output lists from Redis
    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)
    # Zip the inputs and outputs together
    calls = list(zip(inputs, outputs))
    # Print the function name and number of calls
    print(f"{func.__qualname__} was called {len(calls)} times:")
    # Loop over the calls and print each one
    for i, (input_str, output_str) in enumerate(calls):
        input_args = eval(input_str)  # Convert the input string to a tuple
        output = output_str.decode()  # Convert the output bytes to a string
        print(f"{func.__qualname__}{input_args} -> {output}")

