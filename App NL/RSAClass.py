#!/usr/bin/env python

""" Class housing the core RSA methods
"""

__author__ = "Tom van Meer"
__version__ = "4.0."


class RSAKeys:
    import random
    from fractions import gcd
    def __init__(self,bitsize,precisebits,output):
        self.output = output
        self.bitsize = bitsize
        self.precisebits = precisebits

    def isqrt(self,n):
        x = n
        y = (x + 1) // 2
        while y < x:
            x = y
            y = (x + n // x) // 2
        return x

    def mod_inverse(self,a, b):
        r = -1
        B = b
        A = a
        eq_set = []
        full_set = []
        mod_set = []

        #euclid's algorithm
        while r!=1 and r!=0:
            r = b%a
            q = b//a
            eq_set = [r, b, a, q*-1]
            b = a
            a = r
            full_set.append(eq_set)

        for i in range(0, 4):
            mod_set.append(full_set[-1][i])

        mod_set.insert(2, 1)
        counter = 0

        #extended euclid's algorithm
        for i in range(1, len(full_set)):
            if counter%2 == 0:
                mod_set[2] = full_set[-1*(i+1)][3]*mod_set[4]+mod_set[2]
                mod_set[3] = full_set[-1*(i+1)][1]

            elif counter%2 != 0:
                mod_set[4] = full_set[-1*(i+1)][3]*mod_set[2]+mod_set[4]
                mod_set[1] = full_set[-1*(i+1)][1]

            counter += 1

        if mod_set[3] == B:
            return mod_set[2]%B
        return mod_set[4]%B

    def calcKeys(self,p,q):
            from fractions import gcd
            while True:
                m = p * q  # called modules, m is public
                phiM = ((p - 1) * (q - 1))  # phiM is secret.
                while True:
                    i = self.random.randint(2, (m - 1))
                    if (gcd(phiM, i)) == 1: # Make sure i and phiM are co-primes (GDC=1)
                        e = i
                        break
                d = (self.mod_inverse(e, phiM))
                if self.precisebits:
                    if (len(bin(m)))-2 == self.bitsize and (len(bin(e)))-2 == self.bitsize and \
                                            (len(bin(d)))-2 == self.bitsize:
                        break
                else:
                    break
            if self.output:
                print("$Public keys:\n" + str(e) + "\n" + str(m))
                print("$Secret key:\n" + str(d))
            return (d, e, m)

class RSACrypt:
    def __init__(self):
        None
    def encrypt(self, e, m, message):
        return (pow(message, e, m))

    def decrypt(self, d, m, secret):
        return pow(secret, d, m)


