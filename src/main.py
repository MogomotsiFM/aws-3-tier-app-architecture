from typing import Union

from fastapi import FastAPI

import math
import random
from functools import reduce

app = FastAPI()

# https://www.javatpoint.com/python-program-to-print-prime-factor-of-given-number
def prime_factors(num):
    factors = [1]

    # Using the while loop, we will print the number of two's that divide n
    while num % 2 == 0:
        print(2,)
        num = num / 2
  
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        # while i divides n , print i ad divide n
        while num % i == 0:
            factors.append(int(num))
            num = num / i
    if num > 2:
        factors.append(int(num))

    return factors


@app.get("/")
def read_root():
    N = 1000000000000001
    
    print("Working on it...")
    
    return prime_factors(N)


@app.get("/health")
def health_check():
    return "alive"