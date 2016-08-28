#!/usr/bin/env python

""" Class housing the methods to generate strong pseudo primes with given bitsizes
"""

__author__ = "Tom van Meer"
__version__ = "4.0."


class PrimesClass:
    import math
    import random
    import os
    from random import SystemRandom

    def __init__(self,bitsize,prob,output):
        self.bitsize = bitsize
        self.prob = prob
        self.output = output

    def isStrongPseudoprime(self, n, a):
        d = n - 1
        s = 0
        while d % 2 == 0:
            d = d / 2
            s = s + 1
        t = pow(a, d, n)
        if t == 1:
            return True
        while s > 0:
            if t == n - 1:
                return True
            t = (t * t) % n
            s = s - 1
        return False

    def fernet(self, n, k):
        for i in range(0, k):
            a = PrimesClass.random.randint(2, n - 2)
            if (pow(a, n - 1, n)) != 1:
                return False
        return True

    def isPrime(self, n, k):
        for i in range(1, k):
            a = self.random.randint(2, n - 1)
            if self.isStrongPseudoprime(n, a) == False:
                return False
        return True

    def getPrimes(self):
        cryptogen = self.random.SystemRandom()
        while True:
            while True:
                nr = cryptogen.randrange((2**((self.bitsize/2)-1)),2**(self.bitsize/2))
                if self.fernet(nr, self.prob):
                    if (self.isPrime(nr, self.prob)):
                        p = nr
                        break
            while True:
                nr = cryptogen.randrange((2**((self.bitsize/2)-1)),2**(self.bitsize/2))
                if self.fernet(nr, self.prob):
                    if (self.isPrime(nr, self.prob)):
                        q = nr
                        break
            if (len(bin(q*p)) - 2) == self.bitsize:
                break
        if self.output:
            print("$Primes are: \n" + str(p) + "\n" + str(q))
        return p, q
