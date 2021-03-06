#!/usr/bin/env python

""" Main Class housing all the UI components from Kivy and providing methods for easily controlling the
CryptoSuite Class. Does some file handling with keys and saves private keys to device. Works on Android and Windows
"""

__author__ = "Tom van Meer"
__version__ = "2.1."

# Importing Kivy classes and CryptoSuite class
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import CryptoSuite
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
import os
import AESClass
import ConnectClass
import urllib2
import hashlib
import random
import base64
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.core.window import Window



# Class for custom self-scaling button:
class MultiLineLabel(Button):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)


# Class app, used for building app
class EncryptionApp(App):
    # Global variables:
    sm = ScreenManager()
    password = ""
    username = ""
    touser = ""
    subject = ""
    offline = False
    tab = False
    passwordBox = TextInput(password=True, multiline=False, size_hint_y=None, text="")
    passwordBox2 = TextInput(password=True, multiline=False, size_hint_y=None, text="")
    usernameBox = TextInput(multiline=False, size_hint_y=None, text="")

    # Method for building the app
    def build(self):
        self.title = "Crypto Suite V" + str(__version__)
        self.bind(on_start=self.post_build_init)
        self.sm.add_widget(homescreen(name="homescreen"))
        self.sm.current = 'homescreen'
        self.sm.add_widget(mainmenu(name="mainmenu"))
        self.sm.add_widget(touser(name="touserscreen"))
        self.sm.add_widget(encryption(name="encryptionscreen"))
        self.sm.add_widget(decryption(name="decryptionscreen"))
        return self.sm

    #Method for esc/back button
    def post_build_init(self, *args):
        if platform() == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    # Method for esc/back button
    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            if self.sm.current == "homescreen":
                app.stop()
            if self.sm.current == "mainmenu":
                self.passwordBox.text = ""
                self.usernameBox.text = ""
                self.sm.current = "homescreen"
            if self.sm.current == "decryptionscreen" or self.sm.current == "touserscreen" or self.sm.current == "encryptionscreen":
                self.sm.current = "mainmenu"
            screenlist = (self.sm.screen_names)
            screenlist.remove('homescreen')
            screenlist.remove('mainmenu')
            screenlist.remove('touserscreen')
            screenlist.remove('encryptionscreen')
            screenlist.remove('decryptionscreen')
            for i in screenlist:
                if self.sm.current == str(i):
                    self.sm.current = "decryptionscreen"
            return True
        return False


# Class for mainemenu:
class mainmenu(Screen):
    def __init__(self, **kwargs):
        super(mainmenu, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.greeting = MultiLineLabel(background_normal="",background_color=(0,102,255,0.3),text="\n\n---Hoofdmenu---\n\n")
        self.layout.add_widget(self.greeting)

        # Option to send message
        self.encrypt = MultiLineLabel(text="\n\n[Een versleuteld bericht versturen]\n\n")
        self.encrypt.bind(on_release=self.encrypts)
        self.layout.add_widget(self.encrypt)

        # Option to read message
        self.decrypt = MultiLineLabel(text="\n\n[Een ontvangen versleuteld bericht lezen]\n\n")
        self.decrypt.bind(on_release=self.decrypts)
        self.layout.add_widget(self.decrypt)

        # Option to reset
        self.reset = MultiLineLabel(text="\n\n[Mijn account resetten]\n\n")
        self.reset.bind(on_release=self.resets)
        self.layout.add_widget(self.reset)

        # Option to logout
        self.logout = MultiLineLabel(text="\n\n[uitloggen]\n\n",background_normal="",background_color=(0,102,255,0.3))
        self.logout.bind(on_release=self.logouts)
        self.layout.add_widget(self.logout)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = 52
        root.add_widget(self.layout)
        self.add_widget(root)

    def logouts(self,obj):
        EncryptionApp.passwordBox.text = ""
        EncryptionApp.sm.current = "homescreen"

    def encrypts(self,obj):
        EncryptionApp.sm.current = "touserscreen"

    def resets(self,obj):
        C = ConnectClass.Connections()
        C2 = CryptoSuite.CryptoSuite(False)
        keylist = C2.listIDs()
        for i in keylist:
            try:
                os.remove("PrivateKey "+(str(i)).split("Pr")[1]+".dat")
            except: None
            try:
                os.remove("PublicKey " + (str(i)).split("Pu")[1] + ".dat")
            except: None
        filelist = (os.listdir(os.path.dirname(os.path.abspath(__file__))))
        for i in filelist:
            if os.path.isfile(i):
                if "Encrypted" in i:
                    try:
                        os.remove(i)
                    except: None
        C.deluser(EncryptionApp.username,EncryptionApp.password)
        EncryptionApp.passwordBox.text = ""
        EncryptionApp.usernameBox.text = ""
        EncryptionApp.sm.current = "homescreen"

    def decrypts(self,obj):
        EncryptionApp.sm.current = "decryptionscreen"


# Class for reading received messages:
class decryption(Screen):
    def __init__(self, **kwargs):
        super(decryption, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Option to get messages
        self.getmsg = MultiLineLabel(text="\n\n[Berichten ophalen]\n\n")
        self.getmsg.bind(on_release=self.getmsgs)
        self.layout.add_widget(self.getmsg)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = 52
        root.add_widget(self.layout)
        self.add_widget(root)


    def home(self, obj):
        EncryptionApp.sm.current = "mainmenu"

    def getmsgs(self,obj):
        self.layout.clear_widgets()
        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),
                                       text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Option to get messages
        self.getmsg = MultiLineLabel(text="\n\n[Berichten ophalen]\n\n")
        self.getmsg.bind(on_release=self.getmsgs)
        self.layout.add_widget(self.getmsg)
        C = ConnectClass.Connections()
        datalist = ((C.getmsg(EncryptionApp.username,EncryptionApp.password)))
        if datalist == False or datalist == "False":
            return 0
        else:
            new = str(datalist).replace("['", "").replace("']", "").split("', '")
            self.subjectlist = []
            for i in new:
                if "+---------+" in i:
                    self.subjectlist.append(str(i).replace("+---------+","").replace(".txt",""))
                    new.remove(str(i))
            amount = (len(new))
            self.msglist = []
            self.msglabel1 = MultiLineLabel(text='\n\nBerichten:\n\n', size_hint_y=None, background_color=(255, 255, 255, 1),
                               background_normal="", color=(0, 0, 0, 1))
            self.layout.add_widget(self.msglabel1)
            for i in range(0,amount):
                try:
                    datalist = []
                    datalist = self.stringToList(str(new[i]))
                    f = open("Encrypted "+str(datalist[0])+".dat","w")
                    f.write(str(datalist[0])+"\n")
                    f.write(str(datalist[1])+"\n")
                    f.write(str(datalist[2])+"\n")
                    f.close()
                except IOError:
                    None
                CC = CryptoSuite.CryptoSuite(False)
                msg = (CC.decrypt(256,EncryptionApp.password,str(datalist[0])))
                if msg != False:
                    self.msglist.append(str(msg))
                    self.layout.add_widget(MultiLineLabel(text='\n\n Onderwerp: '+str(self.subjectlist[i])+'\n\n',on_press=self.read,id=str(i)))

    def read(self,obj):
        message = []
        message.append(self.subjectlist[int(obj.id)])
        message.append(self.msglist[int(obj.id)])
        EncryptionApp.sm.add_widget(readscreen(name=str(self.subjectlist[int(obj.id)]),id=self.listToString(message)))
        EncryptionApp.sm.current = str(self.subjectlist[int(obj.id)])

    def stringToList(self,string):
        return (string.split("--+--"))

    def listToString(self,list):
        return ("--+--".join(list))


# Class for reading a message
class readscreen(Screen):
    def __init__(self, **kwargs):
        super(readscreen, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),text="\n\n[Terug]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Messagelabel:
        new = self.id.split("=-=-")[0]
        self.message= (MultiLineLabel(text='\n\n Onderwerp: '+str(self.stringToList(new)[0])+
                                           "\n---------------------------\n Bericht: "+str(self.stringToList(new)[1])+"\n "+self.id.split("=-=-")[1]+"\n",
                                      size_hint_y=None))
        self.layout.add_widget(self.message)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = 52
        root.add_widget(self.layout)
        self.add_widget(root)

    def home(self,obj):
        self.id = None
        EncryptionApp.sm.current = "decryptionscreen"

    def stringToList(self,string):
        return (string.split("--+--"))


# Class for encryption screen:
class encryption(Screen):
    def __init__(self, **kwargs):
        super(encryption, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.layout.clear_widgets()


        try:
            self.layout.remove_widget(self.error)
        except:
            None
        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Subject box:
        self.subjectlabel1 = (MultiLineLabel(text="\n\nOnderwerp van bericht:\n",size_hint_y=None))
        self.layout.add_widget(self.subjectlabel1)
        self.subject = TextInput(multiline=False, size_hint_y=None,text="")
        self.layout.add_widget(self.subject)

        # Message box:
        self.subjectlabel = (MultiLineLabel(text="\n\nBericht:\n",size_hint_y=None))
        self.layout.add_widget(self.subjectlabel)
        self.message = TextInput(multiline=False, size_hint_y=None,text="")
        self.layout.add_widget(self.message)

        # send button:
        self.sendbutton = (MultiLineLabel(text='\n\n[Bericht verzenden]\n\n', size_hint_y=None))
        self.sendbutton.bind(on_release=self.send)
        self.layout.add_widget(self.sendbutton)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = 52
        root.add_widget(self.layout)
        self.add_widget(root)


    def home(self,obj):
        EncryptionApp.sm.current = "mainmenu"

    def listToString(self,list):
        return ("--+--".join(list))

    def stringToList(self,string):
        return (string.split("--+--"))

    def send(self,obj):
        if self.subject.text == "" or self.subject.text == " " or self.subject.text == None or self.message.text == "" or self.message.text == " " or self.message.text == None:
            try:
                self.layout.remove_widget(self.error)
            except: None
            self.error = MultiLineLabel(text="\n\n---Er ging iets fout, probeer het opnieuw!---\n\n",background_normal="", background_color=(0, 102, 255, 0.3))
            self.layout.add_widget(self.error)
        else:
            try:
                self.layout.remove_widget(self.error)
            except: None
            EncryptionApp.subject = str(self.subject.text)
            self.subject.text = ""
            C = ConnectClass.Connections()
            ss = False
            idlist = C.getkeys(EncryptionApp.touser)
            if idlist != False:
                CC = CryptoSuite.CryptoSuite(False)
                if str(CC.listIDs()) != "[]":
                    try:
                        ID = idlist[random.randint(0,len(idlist)-1)]
                        CC.encrypt(256,(str(self.message.text)+ " =-=-Verzonden door: "+str(EncryptionApp.username)),ID)
                        datalist = []
                        with open("Encrypted "+str(ID)+".dat","r") as f:
                            for line in f:
                                datalist.append(line.replace("\n", ""))
                        f.close()
                        msg = self.listToString(datalist)
                        if C.addmsg(str(EncryptionApp.touser),str(EncryptionApp.subject),str(msg)):
                            ss = True
                    except:
                        self.layout.remove_widget(self.subjectlabel)
                        self.layout.remove_widget(self.message)
                        self.layout.remove_widget(self.subject)
                        self.layout.remove_widget(self.subjectlabel1)
                        self.message.text = ""
                        self.layout.remove_widget(self.sendbutton)
                        self.succes = MultiLineLabel(text="\n\n---Er ging iets fout, probeer het opnieuw!---\n\n",on_release=self.home)
                        self.layout.add_widget(self.succes)
                    else:
                        if ss == True:
                            self.layout.remove_widget(self.subjectlabel)
                            self.layout.remove_widget(self.subjectlabel1)
                            self.layout.remove_widget(self.subject)
                            self.layout.remove_widget(self.message)
                            self.message.text = ""
                            self.layout.remove_widget(self.sendbutton)
                            self.succes = MultiLineLabel(text="\n\n---Bericht verstuurd!---\n\n",on_release=self.home)
                            self.layout.add_widget(self.succes)
            else:
                try:
                    self.layout.remove_widget(self.error)
                except:
                    None
                self.error = MultiLineLabel(text="\n\n---Er ging iets fout, voer de app uit als administrator!---\n\n",
                                            background_normal="", background_color=(0, 102, 255, 0.3))
                self.layout.add_widget(self.error)


# Class for encryption screen:
class touser(Screen):
    def __init__(self, **kwargs):
        super(touser, self).__init__(**kwargs)
        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # User list:
        C = ConnectClass.Connections()
        userlist = C.getuserlist()
        if userlist == False:
            EncryptionApp.offline = True
        userlist = (str(userlist).replace("'", "")).replace("[", "").replace("]", "").replace(",", "")
        userlist = userlist.split(" ")

        # Refresh:
        self.refreshbutton = MultiLineLabel(text="\n\n[Gebruikers ophalen]\n\n")
        self.refreshbutton.bind(on_release=self.refresh)
        self.layout.add_widget(self.refreshbutton)

        # To user box:
        self.touserlabel = MultiLineLabel(text="\n\n Naar wie wilt u een bericht sturen:\n",size_hint_y=None,background_normal="",
                                   background_color=(255, 255, 255, 1),color=(0, 0, 0, 1))
        self.layout.add_widget(self.touserlabel)
        for i in userlist:
            self.layout.add_widget(MultiLineLabel(text='\n\n Gebruiker: ' + i + '\n\n', on_press=self.nexts, id=i))

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = 52
        root.add_widget(self.layout)
        self.add_widget(root)

    def nexts(self,obj):
        EncryptionApp.touser = str(obj.id)
        EncryptionApp.sm.current = "encryptionscreen"

    def refresh(self,obj):
        self.layout.clear_widgets()

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),
                                       text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # User list:
        C = ConnectClass.Connections()
        userlist = C.getuserlist()
        if userlist == False:
            EncryptionApp.offline = True
        userlist = (str(userlist).replace("'", "")).replace("[", "").replace("]", "").replace(",", "")
        userlist = userlist.split(" ")

        # Refresh:
        self.refreshbutton = MultiLineLabel(text="\n\n[Gebruikers ophalen]\n\n")
        self.refreshbutton.bind(on_release=self.refresh)
        self.layout.add_widget(self.refreshbutton)

        # To user box:
        self.touserlabel = MultiLineLabel(text="\n\n Naar wie wilt u een bericht sturen:\n",size_hint_y=None,background_normal="",
                                   background_color=(255, 255, 255, 1),color=(0, 0, 0, 1))
        self.layout.add_widget(self.touserlabel)
        for i in userlist:
            self.layout.add_widget(MultiLineLabel(text='\n\n Gebruiker: ' + i + '\n\n', on_press=self.nexts, id=i))

    def home(self,obj):
        EncryptionApp.sm.current = "mainmenu"


# Class for homescreen:
class homescreen(Screen):
    def __init__(self, **kwargs):
        super(homescreen, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size=self.size, pos=self.pos)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.greeting = MultiLineLabel(background_normal="", background_color=(0, 102, 255, 0.3),text="\n\nWelkom!\n\n")
        self.layout.add_widget(self.greeting)

        # Login forum:
        self.layout.add_widget(MultiLineLabel(text='\n\nGebruikersnaam:', size_hint_y=None, background_color=(255, 255, 255, 1),background_normal="", color=(0, 0, 0, 1)))
        self.layout.add_widget(EncryptionApp.usernameBox)
        self.layout.add_widget(MultiLineLabel(text='\n\nWachtwoord:', size_hint_y=None, background_color=(255, 255, 255, 1),background_normal="", color=(0, 0, 0, 1)))
        self.layout.add_widget(EncryptionApp.passwordBox)

        # Accept button:
        self.acceptbutton = (MultiLineLabel(text='\n\n[Inloggen]\n\n', size_hint_y=None))
        self.acceptbutton.bind(on_release=self.login)
        self.layout.add_widget(self.acceptbutton)

        # Draw all widgets
        self.add_widget(self.layout)

    def login(self, obj):
        if EncryptionApp.offline == True:
            try:
                self.layout.remove_widget(self.error1)
            except:
                None
            self.error1 = (MultiLineLabel(text="\n\nServer offline, probeer later opnieuw.\n\n", background_normal="",
                                         background_color=(0, 102, 255, 0.3)))
            self.layout.add_widget(self.error1)
            CC = ConnectClass.Connections()
            if CC.getuserlist() != False:
                EncryptionApp.offline = False
                try:
                    self.layout.remove_widget(self.error1)
                except:
                    None
        else:
            if EncryptionApp.passwordBox.text == None or EncryptionApp.passwordBox.text == "" or EncryptionApp.usernameBox.text == None or EncryptionApp.usernameBox.text == "":
                return False
            else:
                EncryptionApp.username = str(EncryptionApp.usernameBox.text)
                t_sha = hashlib.sha512()
                t_sha.update(EncryptionApp.passwordBox.text)
                passw = base64.urlsafe_b64encode(t_sha.digest())
                C = ConnectClass.Connections()
                if C.login(str(EncryptionApp.username), str(passw).replace("/","++")):
                    try:
                        self.layout.remove_widget(self.error)
                    except:
                        None
                    EncryptionApp.password = str(passw)
                    EncryptionApp.usernameBox.text = ""
                    EncryptionApp.passwordBox.text = ""
                    EncryptionApp.sm.current = "mainmenu"
                else:
                    try:
                        self.layout.remove_widget(self.error)
                    except:
                        None
                    self.error = (MultiLineLabel(text="\n\nFouten, probeer opnieuw.\n\n", background_normal="",background_color=(0, 102, 255, 0.3)))
                    self.layout.add_widget(self.error)

# Main loop
if __name__ == '__main__':
    app = EncryptionApp()
    app.run()
