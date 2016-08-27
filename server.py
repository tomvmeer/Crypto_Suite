from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
import sys
app = Flask(__name__)

def stringToList(string):
    return (string.split("--+--"))

def listToString(list):
    return ("--+--".join(list))

def listIDs(name):
    filelist = os.listdir(str(name))
    listfiles = []
    for file_ in filelist:
        name = str(file_).split("PrivateKey ")
        try:
            listfiles.append("Pr" + str((name[1].split(".dat"))[0]))
        except IndexError:
            None
    for file_ in filelist:
        name = str(file_).split("PublicKey ")
        try:
            listfiles.append("Pu" + str((name[1].split(".dat"))[0]))
        except IndexError:
            None
    return listfiles

@app.route('/log')
def log():
        f = open("server.log","r")
        log = f.read()
        return """<xmp>"""+log+"""</xmp>"""

@app.route('/')
def home():
    datalist = []
    for i in (os.listdir(os.path.dirname(os.path.abspath(__file__)))):
        if os.path.isdir(i):
            if i != ".idea":
                datalist.append(i)
    logger.info("Send %s to user."%str(datalist))
    return str(datalist)


@app.route('/<name>/<password>')
def index(name,password):
    logger.info("User %s contacted server with password %s in function %s." %(str(name),str(password),str(sys._getframe().f_code.co_name)))
    try:
        f = open(str(name)+"/password.dat","r")
        f.close()
    except IOError:
        os.mkdir(str(name))
        f = open(str(name)+"/password.dat", "w")
        f.write(password)
        f.close()
        logger.info("Send %s to user in function %s ." % (str(3),str(sys._getframe().f_code.co_name)))
        return str(3)
    else:
        try:
            f = open(str(name)+"/password.dat","r")
            if f.read() == password:
                logger.info("Send %s to user in function %s ." % (str(1), str(sys._getframe().f_code.co_name)))
                return str(1)
            else:
                logger.info("Send %s to user in function %s ." % (str(2), str(sys._getframe().f_code.co_name)))
                return str(2)
        except IOError:
            logger.info("Send %s to user in function %s ." % (str(2), str(sys._getframe().f_code.co_name)))
            return str(2)


@app.route('/<name>/keys/del/<password>')
def deletekeys(name,password):
    if os.path.isdir(str(name)) == True:
        try:
            f = open(str(name)+"/password.dat")
            if f.read() == str(password):
                f.close()
                shutil.rmtree(str(name),ignore_errors=True)
                logger.info("Deleted keys in function %s ." % str(sys._getframe().f_code.co_name))
                return "True"
        except None:
            logger.info("Send %s to user in function %s ." % ((str(False), str(sys._getframe().f_code.co_name))))
            return "False"


@app.route('/<name>/keys')
def sendkeys(name):
    if os.path.isdir(str(name)) != True:
        logger.info("Send %s to user in function %s ." % ((str(False), str(sys._getframe().f_code.co_name))))
        return "False"
    else:
        if (str((listIDs(name)))) != "[]":
            try:
                datalist = []
                datalist.append(str(len(listIDs(name))))
                for i in range(0,((len(listIDs(name))))):
                    datalist.append(str(listIDs(name)[i]).split("Pu")[1])
                    with open((str(name)+"/PublicKey " + str(listIDs(name)[i]).split("Pu")[1] + ".dat"), "r") as f:
                        for line in f:
                            datalist.append(line.replace("\n", ""))
            except IOError:
                logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
                return "False"
            else:
                logger.info("Send %s to user in function %s ." % (str(datalist),str(sys._getframe().f_code.co_name)))
                return listToString(datalist)
        else:
            logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
            return "False"


@app.route('/<name>/msgs')
def getmsg(name):
    if os.path.isdir(str(name)+"/msgs") != True:
        logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
        return "False"
    else:
        list = os.listdir(str(name)+"/msgs")
        datalist = []
        try:
            for i in list:
                f = open(str(name)+"/msgs/"+str(i),"r")
                datalist.append(str(i)+"+---------+")
                datalist.append(f.read())
                f.close()
        except IOError:
            if datalist != []:
                logger.info("Send %s to user." % str(datalist))
                return str(datalist)
            else:
                logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
                return "False"
        else:
            if datalist != []:
                logger.info("Send %s to user in function %s ." % (str(datalist),str(sys._getframe().f_code.co_name)))
                return str(datalist)
            else:
                logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
                return "False"

@app.route('/<name>/msgs/<subject>/<msg>')
def savemsg(name,subject,msg):
    if os.path.isdir(str(name)) != True:
        logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
        return "False"
    else:
        if os.path.isdir(str(name)+"/msgs") != True:
            os.mkdir(str(name)+"/msgs")
        try:
            if os.path.isfile(str(name) + "/msgs/" + str(subject) + ".txt") == True:
                i = 1
                while True:
                    if os.path.isfile(str(name) + "/msgs/" + str(subject) + "("+str(i)+")" ".txt") != True:
                        f = open(str(name) + "/msgs/" + str(subject) + "("+str(i)+")" ".txt","w")
                        break
                    else:
                        i = i + 1
            else:
                f = open(str(name) + "/msgs/" + str(subject) + ".txt","w")
            f.write(str(msg))
            f.close()
            logger.info("Send %s to user in function %s ." % (str(True), str(sys._getframe().f_code.co_name)))
            return "True"
        except IOError:
            logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
            return "False"
        except IndexError:
            logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
            return "False"

@app.route('/<name>/keys/<id>/<keys>')
def newkeys(name,id,keys):
    if os.path.isdir(str(name)) != True:
        logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
        return "False"
    try:
        f = open((str(name) + "/PublicKey " + str(id) + ".dat"), "w")
    except IOError:
        logger.info("Send %s to user in function %s ." % (str(False), str(sys._getframe().f_code.co_name)))
        return "False"
    datalist = stringToList(str(keys).replace("._.", " "))
    items = len(datalist)
    p = 0
    for i in datalist:
        p = p + 1
        if p == items:
            f.write(i)
        else:
            f.write(i + "\n")
    f.close()
    logger.info("Send %s to user in function %s ." % (str(True), str(sys._getframe().f_code.co_name)))
    return ("True")


import logging
logger = logging.getLogger()
handler = logging.FileHandler("server.log")
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
app.run(debug=True,host='192.168.2.169',port=5000)

