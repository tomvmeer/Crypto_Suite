#!/usr/bin/env python

""" Class combining the RSA, Primes and AES classes into one solid data flow,
housing functions to operate above stated classes with custom standards.
"""

__author__ = "Tom van Meer"
__version__ = "4.0."


class CryptoSuite:
    #importing modules:
    import random
    import os
    import re
    import Crypto
    from Crypto.PublicKey import RSA
    import PrimesClass as Pclass
    import RSAClass as Rclass
    import AESClass as Aclass

    # Initiate class, with output True or False
    def __init__(self,output):
        self.output = output


    # Method for constructing keys and saving them:
    def construct(self,RSAKeyBitSize,probPrimeTestTimes,preciseBitsMode,passphrase):
        # getting primes and calculating d e and m
        Primes = self.Pclass.PrimesClass(RSAKeyBitSize,probPrimeTestTimes,self.output)
        p,q = Primes.getPrimes()
        RSAk = self.Rclass.RSAKeys(RSAKeyBitSize,preciseBitsMode,self.output)
        d, e, m = RSAk.calcKeys(p,q)

        # saving keys m and e.
        f = open("PublicKey "+(str(m)[:5])+".dat","w")
        f.write("-----RSA "+str(RSAKeyBitSize)+" public keys-----" + '\n')
        f.write(str(e)+'\n')
        f.write(str(m))
        f.close()
        if self.output:
            print("$Saved Public key!")

        # saving encrypted with passphrase d and plain m in private key
        f = open("PrivateKey "+(str(m)[:5])+".dat","w")
        AESk = self.Aclass.AESCipherPassphrase(str(passphrase))
        f.write(str(AESk.encrypt(str(d)))+'\n')
        f.write(str(m))
        f.close()

        #returns first 5 numbers of m, this is the ID
        return (str(m)[:5])


    # Method for encrypting using own standards
    def encrypt(self,AESKeyBitSize,msg,ID):
        # getting the right keys with ID
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            if "PublicKey "+str(ID) in file_:
                f = open(file_,"r")
                break
        try:
            header = f.readline()
        except UnboundLocalError:
            return False

        # reading keys and making AES key
        e = int(f.readline())
        m = int(f.readline())
        f.close()
        AES = self.Aclass.AESCrypt(AESKeyBitSize, self.output) # 256 or 128 bit
        enMsg, AESkeyNum = AES.encrypt(msg) # encrypting msg using AES
        RSAc = self.Rclass.RSACrypt()

        # encrypting AES key and saving all data
        encrypted = RSAc.encrypt(e, m, int(AESkeyNum))
        f = open("Encrypted "+(str(m)[:5])+".dat","w")
        f.write((str(m)[:5])+'\n')
        f.write(str(encrypted)+'\n')
        f.write(str(enMsg))
        f.close()
        if self.output:
            print("$Encrypted file!")
        return True


    # Method for decrypting using own standards:
    def decrypt(self,AESKeyBitSize,passphrase,ID):
        # getting the right keys with ID
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            if "Encrypted "+str(ID) in file_:
                f = open(file_, "r")
                break
        try:
            m = int(f.readline())
        except UnboundLocalError:
            return False
        key = int(f.readline())
        msg = (f.readline())
        f.close()
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            if "PrivateKey "+str(m) in file_:
                f = open(file_, "r")
                break

        # decrypting private key using passphrase
        AESk = self.Aclass.AESCipherPassphrase(str(passphrase))
        try:
            d = int(AESk.decrypt(f.readline()))
            if d == False:
                return False
        except UnboundLocalError:
            return False
        except ValueError:
            return False
        m = int(f.readline())
        f.close()
        # using decrypted key to decrypt the AES key and decrypt the msg using it
        RSAc = self.Rclass.RSACrypt()
        if RSAc == False:
            return False
        AESkeyNum = RSAc.decrypt(d,m,key)
        AES = self.Aclass.AESCrypt(AESKeyBitSize, self.output) # 256 or 128 bit
        return AES.decrypt(AESkeyNum,msg)


    # Method that returns a list of key ID's in current path
    def listIDs(self):
        filelist = self.os.listdir(__file__[:-15])
        listfiles = []
        for file_ in filelist:
            name = str(file_).split("PrivateKey ")
            try:
                listfiles.append("Pr"+str((name[1].split(".dat"))[0]))
            except IndexError:
                None
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            name = str(file_).split("PublicKey ")
            try:
                listfiles.append("Pu"+str((name[1].split(".dat"))[0]))
            except IndexError:
                None
        return listfiles

# method that is used for timing functions with variabls (debug function, no real use):
def doTest(funcname,funcvars,filename,tests):
    import timeit
    file = open(filename,"w")
    for i in range(1,tests):
        start_time = timeit.default_timer()
        funcname(*funcvars)
        file.write(str(timeit.default_timer() - start_time)+'\n')
    file.close()
    return 0



#!/usr/bin/env python

""" Class combining the RSA, Primes and AES classes into one solid data flow,
housing functions to operate above stated classes with custom standards.
"""

__author__ = "Tom van Meer"
__version__ = "4.0."


class CryptoSuite:
    #importing modules:
    import random
    import os
    import re
    import Crypto
    from Crypto.PublicKey import RSA
    import PrimesClass as Pclass
    import RSAClass as Rclass
    import AESClass as Aclass

    # Initiate class, with output True or False
    def __init__(self,output):
        self.output = output


    # Method for constructing keys and saving them:
    def construct(self,RSAKeyBitSize,probPrimeTestTimes,preciseBitsMode,passphrase):
        # getting primes and calculating d e and m
        Primes = self.Pclass.PrimesClass(RSAKeyBitSize,probPrimeTestTimes,self.output)
        p,q = Primes.getPrimes()
        RSAk = self.Rclass.RSAKeys(RSAKeyBitSize,preciseBitsMode,self.output)
        d, e, m = RSAk.calcKeys(p,q)

        # saving keys m and e.
        f = open("PublicKey "+(str(m)[:5])+".dat","w")
        f.write("-----RSA "+str(RSAKeyBitSize)+" public keys-----" + '\n')
        f.write(str(e)+'\n')
        f.write(str(m))
        f.close()
        if self.output:
            print("$Saved Public key!")

        # saving encrypted with passphrase d and plain m in private key
        f = open("PrivateKey "+(str(m)[:5])+".dat","w")
        AESk = self.Aclass.AESCipherPassphrase(str(passphrase))
        f.write(str(AESk.encrypt(str(d)))+'\n')
        f.write(str(m))
        f.close()

        #returns first 5 numbers of m, this is the ID
        return (str(m)[:5])


    # Method for encrypting using own standards
    def encrypt(self,AESKeyBitSize,msg,ID):
        # getting the right keys with ID
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            if "PublicKey "+str(ID) in file_:
                f = open(file_,"r")
                break
        try:
            header = f.readline()
        except UnboundLocalError:
            return False

        # reading keys and making AES key
        e = int(f.readline())
        m = int(f.readline())
        f.close()
        AES = self.Aclass.AESCrypt(AESKeyBitSize, self.output) # 256 or 128 bit
        enMsg, AESkeyNum = AES.encrypt(msg) # encrypting msg using AES
        RSAc = self.Rclass.RSACrypt()

        # encrypting AES key and saving all data
        encrypted = RSAc.encrypt(e, m, int(AESkeyNum))
        f = open("Encrypted "+(str(m)[:5])+".dat","w")
        f.write((str(m)[:5])+'\n')
        f.write(str(encrypted)+'\n')
        f.write(str(enMsg))
        f.close()
        if self.output:
            print("$Encrypted file!")
        return True


    # Method for decrypting using own standards:
    def decrypt(self,AESKeyBitSize,passphrase,ID):
        # getting the right keys with ID
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            if "Encrypted "+str(ID) in file_:
                f = open(file_, "r")
                break
        try:
            m = int(f.readline())
        except UnboundLocalError:
            return False
        key = int(f.readline())
        msg = (f.readline())
        f.close()
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            if "PrivateKey "+str(m) in file_:
                f = open(file_, "r")
                break

        # decrypting private key using passphrase
        AESk = self.Aclass.AESCipherPassphrase(str(passphrase))
        try:
            d = int(AESk.decrypt(f.readline()))
            if d == False:
                return False
        except UnboundLocalError:
            return False
        except ValueError:
            return False
        m = int(f.readline())
        f.close()
        # using decrypted key to decrypt the AES key and decrypt the msg using it
        RSAc = self.Rclass.RSACrypt()
        if RSAc == False:
            return False
        AESkeyNum = RSAc.decrypt(d,m,key)
        AES = self.Aclass.AESCrypt(AESKeyBitSize, self.output) # 256 or 128 bit
        return AES.decrypt(AESkeyNum,msg)


    # Method that returns a list of key ID's in current path
    def listIDs(self):
        filelist = self.os.listdir(__file__[:-15])
        listfiles = []
        for file_ in filelist:
            name = str(file_).split("PrivateKey ")
            try:
                listfiles.append("Pr"+str((name[1].split(".dat"))[0]))
            except IndexError:
                None
        filelist = self.os.listdir(__file__[:-15])
        for file_ in filelist:
            name = str(file_).split("PublicKey ")
            try:
                listfiles.append("Pu"+str((name[1].split(".dat"))[0]))
            except IndexError:
                None
        return listfiles

# method that is used for timing functions with variabls (debug function, no real use):
def doTest(funcname,funcvars,filename,tests):
    import timeit
    file = open(filename,"w")
    for i in range(1,tests):
        start_time = timeit.default_timer()
        funcname(*funcvars)
        file.write(str(timeit.default_timer() - start_time)+'\n')
    file.close()
    return 0



