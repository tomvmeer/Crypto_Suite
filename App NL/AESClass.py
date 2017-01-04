#!/usr/bin/env python

""" Class housing the AES key generation and the AES encryption
"""

__author__ = "Tom van Meer"
__version__ = "4.0."


# Random AES key generation:
class AESCipher:
    from Crypto.Cipher import AES
    from Crypto import Random
    import base64

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        raw = pad(raw)
        iv = self.Random.new().read(self.AES.block_size)
        cipher = self.AES.new(self.key, self.AES.MODE_CBC, iv)
        return self.base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        unpad = lambda s: s[:-ord(s[len(s)-1:])]
        enc = self.base64.b64decode(enc)
        iv = enc[:16]
        cipher = self.AES.new(self.key, self.AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


# AES key formatting and encryption using the AESCipher class:
class AESCrypt:
    import os

    # Method for initiating:
    def __init__(self,bitsize,output): #256 or 128 bit
        self.bitsize = bitsize
        self.output = output

    def encrypt(self,msg):
        randBits = self.os.urandom((self.bitsize / 8))
        cypher = AESCipher(randBits)
        hex, length = (randBits.encode('hex'), 32)
        num = self.hexToInt(hex)
        text = cypher.encrypt((str(msg)))
        if self.output:
            print("$AES key is:\n"+str(num))
        return (text,num)

    def decrypt(self,num,enText):
        hex = self.intToHex(num)
        try:
            bits, size = hex.decode('hex'), 32
        except:
            return False
        cypher = AESCipher(bits)
        data = (cypher.decrypt(enText))
        return data

    def listToString(self, list):
        return ("202".join(list))

    def stringToList(self, string):
        return (string.split("202"))

    def hexToInt(self, num):
        total = []
        for i in str(num):
            try:
                int(i)
                total.append(i)
            except ValueError:
                total.append(str(ord(i)))
        return (self.listToString(total))

    def intToHex(self, num):
        total = self.stringToList(str(num))
        total2 = []
        for i in total:
            if len(str(i)) > 1:
                total2.append(chr(int(i)))
            else:
                total2.append(i)
        return ("".join(total2))


# AES encryption using unformatted Passphrase keys:
class AESCipherPassphrase(object):
    from Crypto.Cipher import AES
    from Crypto import Random
    import base64
    import hashlib

    def __init__(self, key):
        self.bs = 32
        self.key = self.hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = self.Random.new().read(self.AES.block_size)
        cipher = self.AES.new(self.key, self.AES.MODE_CBC, iv)
        return self.base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = self.base64.b64decode(enc)
        iv = enc[:self.AES.block_size]
        cipher = self.AES.new(self.key, self.AES.MODE_CBC, iv)
        try:
            return self._unpad(cipher.decrypt(enc[self.AES.block_size:])).decode('utf-8')
        except:
            return False

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
