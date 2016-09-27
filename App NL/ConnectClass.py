#!/usr/bin/env python

""" Class used for interacting with the server, sending messages, getting messages, logging in and saving keys.
"""

__author__ = "Tom van Meer"
__version__ = "1.0."

import urllib2
import CryptoSuite
import socket
RSAkeysize = 1028

# Class for connecting and interacting with the server
class Connections:

    def __init__(self):
        pass

    def listToString(self,list):
        return ("--+--".join(list))

    def stringToList(self,string):
        return (string.split("--+--"))

    def login(self,username,password): #returns true if logon was successful
        link = ("http://connectit.asuscomm.com:5000/"+str(username)+"/"+str(password))
        response = (urllib2.urlopen(link.replace(" ","._."))).read()
        if int(response) == 1: #user excists, password correct
            return True
        elif int(response) == 2: #user excists, password incorrect
            return False
        elif int(response) == 3:  # user doesnt excist, create new!
            c = CryptoSuite.CryptoSuite(False)
            id = c.construct(RSAkeysize, 5, False, password)
            datalist = []
            with open(("PublicKey " + str(id) + ".dat"), "r") as f:
                for line in f:
                    datalist.append(line.replace("\n", ""))
            f.close()
            link = (
            "http://connectit.asuscomm.com:5000/" + str(username) + "/keys/" + str(id) + "/" + self.listToString(
                datalist)).replace(" ", "._.")
            response = (urllib2.urlopen(link.replace(" ", "._."))).read()
            if response == "False":
                return False
            if response == "True":
                return True

    def addkeys(self,username,password):
        link = ("http://connectit.asuscomm.com:5000/"+str(username)+"/"+str(password))
        response = (urllib2.urlopen(link.replace(" ","._."))).read()
        if response == "1":
            c = CryptoSuite.CryptoSuite(False)
            id = c.construct(RSAkeysize, 5, False, str(password))
            datalist = []
            with open(("PublicKey " + str(id) + ".dat"), "r") as f:
                for line in f:
                    datalist.append(line.replace("\n", ""))
            f.close()
            link = ("http://connectit.asuscomm.com:5000/" + str(username) + "/keys/" + str(id) + "/" + self.listToString(datalist)).replace(" ", "._.")
            response = (urllib2.urlopen(link.replace(" ", "._."))).read()
            if response == "False":
                return False
            if response == "True":
                return True
        else:
            return False

    def getuserlist(self):
        link = ("http://connectit.asuscomm.com:5000/")
        try:
            response = (urllib2.urlopen(link,timeout=1).read())
        except urllib2.URLError:
            return False
        except socket.timeout:
            return False
        else:
            return response

    def getkeys(self,user):
        link = ("http://connectit.asuscomm.com:5000/" + str(user) + "/keys")
        response = (urllib2.urlopen(link.replace(" ","._."))).read()
        if response == "False":
            return False
        else:
            datalist = self.stringToList(str(response).replace("._.", " "))
            amount = int(datalist[0])
            idlist = []
            for h in range(0,amount):
                try:
                    f = open("PublicKey " + str(datalist[1]) + ".dat", "w")
                except IOError:
                    return False
                idlist.append(str(datalist[1]))
                datalist.pop(1)
                for i in range(1,4):
                    if i == 3:
                        f.write(datalist[i])
                    else:
                        f.write(datalist[i]+"\n")
                f.close()
                datalist.pop(1)
                datalist.pop(1)
                datalist.pop(1)
            return idlist

    def deluser(self,user,password):
        link = ("http://connectit.asuscomm.com:5000/" + str(user).replace("/","(*)") + "/keys/del/"+str(password).replace("/","(*)"))
        response = (urllib2.urlopen(link.replace(" ", "._."))).read()
        if response == "False":
            return False
        elif response == "True":
            return True

    def addmsg(self,user,subject,msg):
        link = ("http://connectit.asuscomm.com:5000/" + str(user).replace("/","(*)") + "/msgs/"+str(subject).replace("/","(*)")+"/"+str(msg).replace("/","(*)"))
        response = (urllib2.urlopen(link.replace(" ", "._."))).read()
        if response == "False":
            return False
        elif response == "True":
            return True
    
    def getmsg(self,username,password):
        link = ("http://connectit.asuscomm.com:5000/"+str(username)+"/"+str(password))
        response = (urllib2.urlopen(link.replace(" ","._."))).read()
        if int(response) == 1: #user excists, password correct
            link = ("http://connectit.asuscomm.com:5000/" + str(username) + "/msgs")
            response = (urllib2.urlopen(link.replace(" ", "._."))).read()
            return response.replace("._."," ").replace("(*)","/")
        elif int(response) == 2: #user excists, password incorrect
            return False
