#!/usr/bin/env python

""" Main Class housing all the UI components from Kivy and providing methods for easily controlling the
CryptoSuite Class. Does some file handling with keys and saves private keys to device. Works on Android and Windows
"""

__author__ = "Tom van Meer"
__version__ = "3.2.1"

# Importing Kivy classes and CryptoSuite class, also importing all modules:
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import CryptoSuite
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import os
import ConnectClass
import hashlib
import random
import base64
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.uix.image import Image
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
        if platform() == 'android':
            x,y = self.size
            self.padding_x = x / 15
        else:
            self.padding_x = 20
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
    debug = True
    reply = False
    sm = ScreenManager()
    password = ""
    enpassword = ""
    username = ""
    touser = ""
    subject = ""
    offline = False
    passwordBox = TextInput(password=True, multiline=False, size_hint_y=None, text="")
    usernameBox = TextInput(multiline=False, size_hint_y=None, text="")
    scrolltimeout = 38
    admin = True

    # Method for building the app
    def build(self):
        Window.clearcolor = (0, 0.314, 0.42,1)
        self.title = "Crypto Suite V" + str(__version__)
        self.bind(on_start=self.post_build_init)
        self.sm.add_widget(loginscreen(name="loginscreen"))
        self.sm.current = "loginscreen"
        self.sm.add_widget(pre_loginscreen(name="pre_loginscreen"))
        self.sm.add_widget(mainmenu(name="mainmenu"))
        self.sm.add_widget(touser(name="touserscreen"))
        self.sm.add_widget(sendscreen(name="sendscreen"))
        self.sm.add_widget(decryption(name="decryptionscreen"))

        # Try for file-rights:
        try:
            f = open("test.txt","w")
            f.write("test")
            f.close()
            os.listdir("/")
            os.remove("test.txt")
        except IOError:
            self.admin = False
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
            if self.sm.current == "loginscreen":
                app.stop()
            if self.sm.current == "pre_loginscreen":
                self.sm.current = "loginscreen"
            if self.sm.current == "mainmenu":
                self.passwordBox.text = ""
                self.usernameBox.text = ""
                self.sm.current = "loginscreen"
            if self.sm.current == "decryptionscreen" or self.sm.current == "touserscreen":
                self.sm.current = "mainmenu"
            if self.sm.current == "sendscreen":
                self.sm.current = "mainmenu"
            screenlist = (self.sm.screen_names)
            screenlist.remove('loginscreen')
            screenlist.remove('mainmenu')
            screenlist.remove('touserscreen')
            screenlist.remove('sendscreen')
            screenlist.remove('decryptionscreen')
            for i in screenlist:
                if self.sm.current == str(i):
                    self.sm.current = "decryptionscreen"
            return True
        return False

# Class for pre_login screen:
class pre_loginscreen(Screen):
    def __init__(self, **kwargs):
        super(pre_loginscreen, self).__init__(**kwargs)

        self.bind(on_start=self.post_build_init)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.image = Image(source="icon 2.png", size_hint_y=None,size=self.size)
        self.bind(size=self.getsize)
        self.layout.add_widget(self.image)
        self.greeting = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129, 1),
                                       text="\n\nWelkom!\n\n",halign="center")
        self.layout.add_widget(self.greeting)

        # Login forum:
        self.layout.add_widget(MultiLineLabel(text='\n\nGebruikersnaam:\n', size_hint_y=None,
                                              background_color=(1, 1, 1, 1), background_normal="",
                                              color=(0, 0, 0, 1)))
        self.userbox = (TextInput(multiline=False, size_hint_y=None, text=""))
        self.layout.add_widget(self.userbox)
        self.layout.add_widget(MultiLineLabel(text='\n\nWachtwoord:\n', size_hint_y=None,
                                              background_color=(1, 1, 1, 1),
                                              background_normal="", color=(0, 0, 0, 1)))
        self.pasbox = (TextInput(password=True, multiline=False, size_hint_y=None, text=""))
        self.layout.add_widget(self.pasbox)
        self.layout.add_widget(MultiLineLabel(text='\n\nHerhaal wachtwoord:\n', size_hint_y=None,
                                              background_color=(1, 1, 1, 1),
                                              background_normal="", color=(0, 0, 0, 1)))
        self.pasbox2 = (TextInput(password=True, multiline=False, size_hint_y=None, text=""))
        self.layout.add_widget(self.pasbox2)

        # Accept button:
        self.acceptbutton = (MultiLineLabel(background_normal="", background_color=(0.4, 0.416, 0.42, 1),
                                            text='\n\n[Registreren]\n\n',halign="center"))
        self.acceptbutton.bind(on_release=self.login)
        self.layout.add_widget(self.acceptbutton)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            if self.userbox.focus == True:
                self.userbox.focus = False
            if self.pasbox.focus == True:
                self.pasbox.focus = False
            if self.pasbox2.focus == True:
                self.pasbox2.focus = False

    def post_build_init(self, *args):
        if platform() == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def getsize(self, obj, event):
        x, y = self.size
        self.image.size = (x / 7, y / 7)

    def login(self, obj):
        self.userbox.focus = False
        self.pasbox.focus = False

        # Checking for rights!
        if EncryptionApp.admin == False:
            try:
                self.layout.remove_widget(self.error2)
            except:
                None
            self.error2 = (MultiLineLabel(text="\n\n---De app heeft niet genoeg rechten, "
                                               "raadpleeg de handleiding!---\n\n",
                                          background_normal="", background_color=(1, 0, 0, 0.4)))
            self.layout.add_widget(self.error2)
            return

        if EncryptionApp.offline == True:
            try:
                self.layout.remove_widget(self.error1)
            except:
                None
            self.error1 = (MultiLineLabel(text="\n\n---Server offline, probeer later opnieuw.---\n\n",
                                          background_normal="", background_color=(1, 0, 0, 0.4)))
            self.layout.add_widget(self.error1)
            CC = ConnectClass.Connections()
            if CC.getuserlist() != False:
                EncryptionApp.offline = False
                try:
                    self.layout.remove_widget(self.error1)
                except:
                    None
        else:
            if self.pasbox.text is None or self.pasbox.text == "" or \
                            self.userbox.text is None or self.userbox.text == "":
                return False
            if self.pasbox.text != self.pasbox2.text:
                try:
                    self.layout.remove_widget(self.error)
                except:
                    None
                self.error = (
                    MultiLineLabel(text="\n\n---Wachtwoorden zijn niet gelijk!---\n\n", background_normal="",
                                   background_color=(1, 0, 0, 0.4)))
                self.layout.add_widget(self.error)
            else:
                EncryptionApp.username = str(self.userbox.text).replace(" ", "").replace("\t", "")
                CC = ConnectClass.Connections()
                list = CC.getuserlist()
                if EncryptionApp.username in list:
                    try:
                        self.layout.remove_widget(self.error)
                    except:
                        None
                    self.error = (
                        MultiLineLabel(text="\n\n---Gebruiker bestaat al!---\n\n", background_normal="",
                                       background_color=(1, 0, 0, 0.4)))
                    self.layout.add_widget(self.error)
                else:
                    t_sha = hashlib.sha512()
                    t_sha.update(self.pasbox.text)
                    passw = base64.urlsafe_b64encode(t_sha.digest())
                    C = ConnectClass.Connections()
                    status = C.register(str(EncryptionApp.username), str(passw).replace("/", "++"),EncryptionApp.enpassword)

                    if status == True:
                        try:
                            self.layout.remove_widget(self.error)
                        except:
                            None
                        EncryptionApp.password = str(passw)
                        EncryptionApp.enpassword = self.pasbox.text
                        self.userbox.text = ""
                        self.pasbox.text = ""
                        self.pasbox2.text = ""
                        EncryptionApp.sm.current = "mainmenu"
                    else:
                        try:
                            self.layout.remove_widget(self.error)
                        except:
                            None
                        self.error = (
                            MultiLineLabel(text="\n\n---Fouten, probeer opnieuw.---\n\n", background_normal="",
                                           background_color=(1, 0, 0, 0.4)))
                        self.layout.add_widget(self.error)


# Class for loginscreen:
class loginscreen(Screen):
    def __init__(self, **kwargs):
        super(loginscreen, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.image = Image(source="icon 2.png", size_hint_y=None,size=self.size)
        self.bind(size=self.getsize)
        self.layout.add_widget(self.image)
        self.greeting = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129, 1),
                                       text="\n\nWelkom!\n\n",halign="center")
        self.layout.add_widget(self.greeting)

        # Register button:
        self.registerButton = (MultiLineLabel(background_normal="", background_color=(0.4, 0.416, 0.42, 1),
                                            text='\n\n[Registreren]\n\n',halign="center"))
        self.registerButton.bind(on_release=self.register)
        self.layout.add_widget(self.registerButton)

        # Login forum:
        self.layout.add_widget(MultiLineLabel(text='\n\nGebruikersnaam:\n', size_hint_y=None,
                                              background_color=(1, 1, 1, 1), background_normal="",
                                              color=(0, 0, 0, 1)))
        self.layout.add_widget(EncryptionApp.usernameBox)
        self.layout.add_widget(MultiLineLabel(text='\n\nWachtwoord:\n', size_hint_y=None,
                                              background_color=(1, 1, 1, 1),
                                              background_normal="", color=(0, 0, 0, 1)))
        self.layout.add_widget(EncryptionApp.passwordBox)

        # Accept button:
        self.acceptbutton = (MultiLineLabel(background_normal="", background_color=(0.4, 0.416, 0.42, 1),
                                            text='\n\n[Inloggen]\n\n',halign="center"))
        self.acceptbutton.bind(on_release=self.login)
        self.layout.add_widget(self.acceptbutton)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def register(self,obj):
        EncryptionApp.sm.current = "pre_loginscreen"
        try:
            self.layout.remove_widget(self.error)
        except:
            None
        EncryptionApp.usernameBox.text = ""
        EncryptionApp.passwordBox.text = ""

    def getsize(self,obj,event):
        x,y = self.size
        self.image.size = (x/7,y/7)

    def login(self, obj):
        EncryptionApp.usernameBox.focus = False
        EncryptionApp.passwordBox.focus = False

        # Checking for rights!
        if EncryptionApp.admin == False:
            try:
                self.layout.remove_widget(self.error2)
            except:
                None
            self.error2 = (MultiLineLabel(text="\n\n---De app heeft niet genoeg rechten, "
                                               "raadpleeg de handleiding!---\n\n",
                                          background_normal="", background_color=(1, 0, 0, 0.4)))
            self.layout.add_widget(self.error2)
            return

        if EncryptionApp.offline == True:
            try:
                self.layout.remove_widget(self.error1)
            except:
                None
            self.error1 = (MultiLineLabel(text="\n\n---Server offline, probeer later opnieuw.---\n\n",
                                          background_normal="", background_color=(1, 0, 0, 0.4)))
            self.layout.add_widget(self.error1)
            CC = ConnectClass.Connections()
            if CC.getuserlist() != False:
                EncryptionApp.offline = False
                try:
                    self.layout.remove_widget(self.error1)
                except:
                    None
        else:
            if EncryptionApp.passwordBox.text is None or EncryptionApp.passwordBox.text == "" or \
                            EncryptionApp.usernameBox.text is None or EncryptionApp.usernameBox.text == "":
                return False
            else:
                EncryptionApp.username = str(EncryptionApp.usernameBox.text).replace(" ", "").replace("\t", "")
                t_sha = hashlib.sha512()
                t_sha.update(EncryptionApp.passwordBox.text)
                passw = base64.urlsafe_b64encode(t_sha.digest())
                C = ConnectClass.Connections()
                status = C.login(str(EncryptionApp.username), str(passw).replace("/", "++"))
                if status == True:
                    try:
                        self.layout.remove_widget(self.error)
                    except:
                        None
                    EncryptionApp.password = str(passw)
                    EncryptionApp.usernameBox.text = ""
                    EncryptionApp.passwordBox.text = ""
                    EncryptionApp.sm.current = "mainmenu"
                elif status == 3:
                    try:
                        self.layout.remove_widget(self.error)
                    except:
                        None
                    self.error = (
                    MultiLineLabel(text="\n\n---Gebruiker niet gevonden!---\n---Registreer AUB---\n\n",
                                   background_normal="",
                                   background_color=(1, 0, 0, 0.4)))
                    self.layout.add_widget(self.error)
                else:
                    try:
                        self.layout.remove_widget(self.error)
                    except:
                        None
                    self.error = (
                    MultiLineLabel(text="\n\n---Fouten, probeer opnieuw.---\n\n", background_normal="",
                                   background_color=(1, 0, 0, 0.4)))
                    self.layout.add_widget(self.error)


# Class for mainemenu:
class mainmenu(Screen):
    def __init__(self, **kwargs):
        super(mainmenu, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.greeting = MultiLineLabel(background_normal="",background_color=(0.129, 0.129, 0.129,1),
                                       text="\n\nHoofdmenu, active gebruiker: %s\n\n"% \
                                        str(EncryptionApp.username),halign = "center")
        self.image = Image(source="icon 2.png",size_hint_y=None)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.greeting)
        self.bind(on_pre_enter=self.refresh)
        self.bind(size=self.getsize)

        # Option to send message
        self.encrypt = MultiLineLabel(text="\n\n[Een versleuteld bericht versturen]\n\n")
        self.encrypt.bind(on_release=self.encrypts)
        self.layout.add_widget(self.encrypt)

        # Option to read message
        self.decrypt = MultiLineLabel(text="\n\n[Een ontvangen versleuteld bericht lezen]\n\n")
        self.decrypt.bind(on_release=self.decrypts)
        self.layout.add_widget(self.decrypt)

        if EncryptionApp.debug:
            # Option to reset
            self.reset = MultiLineLabel(text="\n\n[Mijn account resetten]\n\n")
            self.reset.bind(on_release=self.resets)
            self.layout.add_widget(self.reset)

        # Option to logout
        self.logout = MultiLineLabel(text="\n\n[uitloggen]\n\n")
        self.logout.bind(on_release=self.logouts)
        self.layout.add_widget(self.logout)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def getsize(self, obj, event):
        x, y = self.size
        self.image.size = (x / 7, y / 7)

    def refresh(self,obj):
        self.greeting.text = ("\n\nHoofdmenu, active gebruiker: %s \n\n"%str(EncryptionApp.username))

    def logouts(self,obj):
        EncryptionApp.passwordBox.text = ""
        EncryptionApp.sm.current = "loginscreen"

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
        EncryptionApp.sm.current = "loginscreen"

    def decrypts(self,obj):
        EncryptionApp.sm.current = "decryptionscreen"


# Class for selecting received messages:
class decryption(Screen):
    def __init__(self, **kwargs):
        super(decryption, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.bind(on_enter=self.getmsgs)
        self.image = Image(source="icon 2.png", size_hint_y=None,size=self.size)
        self.bind(size=self.getsize)
        self.layout.add_widget(self.image)

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                       text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Option to get messages
        self.getmsg = MultiLineLabel(text="\n\n[Berichten ophalen]\n\n",background_normal="",
                                     background_color=(0.129, 0.129, 0.129,1))
        self.getmsg.bind(on_release=self.getmsgs)
        self.layout.add_widget(self.getmsg)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def getsize(self, obj, event):
        x, y = self.size
        self.image.size = (x / 7, y / 7)

    def home(self, obj):
        EncryptionApp.sm.current = "mainmenu"

    def getmsgs(self,obj):
        self.layout.clear_widgets()

        self.layout.add_widget(self.image)
        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                       text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Option to get messages
        self.getmsg = MultiLineLabel(text="\n\n[Berichten ophalen]\n\n",background_normal="",
                                     background_color=(0.129, 0.129, 0.129,1))
        self.getmsg.bind(on_release=self.getmsgs)
        self.layout.add_widget(self.getmsg)
        C = ConnectClass.Connections()
        datalist = ((C.getmsg(EncryptionApp.username,EncryptionApp.password)))
        if datalist == False or datalist == "False":
            return 0
        else:
            new = str(datalist).replace("['", "").replace("']", "").split("', '")
            self.subjectlist = []
            msgID = []
            for i in range (0,len(new)-1,2):
                msgID.append(new[i].replace(".txt+---------+",""))
            for i in new:
                if "+---------+" in i:
                    self.subjectlist.append(str(i).replace("+---------+","").replace(".txt",""))
                    new.remove(str(i))
            amount = (len(new))
            self.msglist = []
            self.msglabel1 = MultiLineLabel(text='\n\nBerichten:\n\n', size_hint_y=None)
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
                msg = (CC.decrypt(128,EncryptionApp.enpassword,str(datalist[0])))
                if msg != False:
                    msg = msg + "=-=-" + msgID[i]
                    self.msglist.append(str(msg))
                    self.layout.add_widget(MultiLineLabel(text='\n\n Bericht met onderwerp: '+
                                                               str(msg).split("=-=-")[0]+'\n\n',
                                                          on_press=self.read,id=str(i),background_normal="",
                                                          background_color=(1, 1, 1, 1),color=(0,0,0,1)))
                    os.remove("Encrypted "+str(datalist[0])+".dat")
                else:
                    os.remove("Encrypted " + str(datalist[0]) + ".dat")
                    self.layout.remove_widget(self.msglabel1)

    def read(self,obj):
        EncryptionApp.sm.add_widget(readscreen(name=str(self.subjectlist[int(obj.id)]),id=(self.msglist[int(obj.id)])))
        EncryptionApp.sm.current = str(self.subjectlist[int(obj.id)])

    def stringToList(self,string):
        return (string.split("--+--"))

    def listToString(self,list):
        return ("--+--".join(list))


# Class for reading selected message:
class readscreen(Screen):
    def __init__(self, **kwargs):
        super(readscreen, self).__init__(**kwargs)

        # Define layout:
        self.layout = GridLayout(cols=1, spacing=3, size_hint_y=None, pos=self.pos)
        self.image = Image(source="icon 2.png", size_hint_y=None,size=self.size)
        self.bind(size=self.getsize)
        self.layout.add_widget(self.image)

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                       text="\n\n[Terug]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)

        # Messagelabel:
        self.new = self.id.split("=-=-")
        self.subject = (MultiLineLabel(text='| Onderwerp: '+str(self.new[0])+" |",size_hint_y=None,background_normal="",
                                       background_color=(1, 1, 1, 1),color=(0,0,0,1)))
        self.message = (MultiLineLabel(text="\n"+str(self.new[1])+"\n\n",size_hint_y=None,background_normal="",
                                       background_color=(1, 1, 1, 1),color=(0,0,0,1)))
        self.sender = (MultiLineLabel(text="| "+ str(self.new[2])+" |",size_hint_y=None,background_normal="",
                                      background_color=(1, 1, 1, 1),color=(0,0,0,1)))
        self.layout.add_widget(self.subject)
        self.layout.add_widget(self.message)
        self.layout.add_widget(self.sender)

        # Delete button:
        self.delete = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                     text="\n\n[Bericht verwijderen]\n\n")
        self.delete.bind(on_release=self.deleteMsg)
        self.layout.add_widget(self.delete)

        # Delete button:
        self.reply = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                    text="\n\n[Reageren op bericht]\n\n")
        self.reply.bind(on_release=self.replyMsg)
        self.layout.add_widget(self.reply)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def deleteMsg(self,obj):
        C = ConnectClass.Connections()
        C.delmsg(EncryptionApp.username,EncryptionApp.password,str(self.new[3]))
        self.message.text = "\nBericht verwijderd!\n\n"

    def replyMsg(self,obj):
        EncryptionApp.touser = (self.new[2].split("Verzonden door: ")[1])
        EncryptionApp.reply = ("Verzonden door: "+EncryptionApp.username+" |\n| Als reactie op bericht met onderwerp: "+
                               str(self.new[0]))
        EncryptionApp.sm.current = "sendscreen"

    def getsize(self, obj, event):
        x, y = self.size
        self.image.size = (x / 7, y / 7)
        self.subject.size = (x,y/10)

    def home(self,obj):
        self.id = None
        EncryptionApp.sm.current = "decryptionscreen"

    def stringToList(self,string):
        return (string.split("--+--"))


# Class for sending a message:
class sendscreen(Screen):
    def __init__(self, **kwargs):
        super(sendscreen, self).__init__(**kwargs)

        # Define layout:
        self.bind(on_start=self.post_build_init)
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.layout.clear_widgets()
        self.image = Image(source="icon 2.png", size_hint_y=None,size=self.size)
        self.bind(size=self.getsize)
        self.layout.add_widget(self.image)

        try:
            self.layout.remove_widget(self.error)
        except:
            None

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                       text="\n\n[Terug naar het hoofdmenu]\n\n")
        self.backhome.bind(on_release=self.home)
        self.layout.add_widget(self.backhome)
        self.bind(on_enter=self.refresh)

        # Subject box:
        self.subjectlabel1 = (MultiLineLabel(text="\nVersturen naar: " + str(EncryptionApp.touser) +
                                                  "\nOnderwerp van bericht:\n",size_hint_y=None))
        self.layout.add_widget(self.subjectlabel1)
        self.subject = TextInput(multiline=False, size_hint_y=None,size=self.size,text="")
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
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            if self.message.focus == True:
                self.message.focus = False
            if self.subject.focus == True:
                self.subject.focus = False

    def post_build_init(self, *args):
        if platform() == 'android':
            import android
            android.map_key(android.KEYCODE_BACK, 1001)
        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def getsize(self, obj, event):
        x, y = self.size
        self.image.size = (x / 7, y / 7)
        self.subject.size=(x,y/14)

    def refresh(self,obj):
        self.subjectlabel1.text = ("\nVersturen naar: " + str(EncryptionApp.touser) +
                                   "\nOnderwerp van bericht:\n")
        try:
            self.layout.add_widget(self.subjectlabel1)
            self.layout.add_widget(self.subject)
            self.layout.add_widget(self.subjectlabel)
            self.layout.add_widget(self.message)
            self.layout.add_widget(self.sendbutton)
        except: None
        try:
            self.subject.text = ""
            self.message.text = ""
        except AttributeError: None
        try:
            self.layout.remove_widget(self.error)
        except:None
        try:
            self.layout.remove_widget(self.succes)
        except:None

    def home(self,obj):
        try:
            self.subject.text = ""
            self.message.text = ""
        except AttributeError: None
        EncryptionApp.sm.current = "mainmenu"

    def listToString(self,list):
        return ("--+--".join(list))

    def stringToList(self,string):
        return (string.split("--+--"))

    def send(self,obj):
        self.message.focus = False
        self.subject.focus = False
        if self.subject.text == "" or self.subject.text == " " or self.subject.text is None or self.message.text == "" \
                or self.message.text == " " or self.message.text is None:
            try:
                self.layout.remove_widget(self.error)
            except: None
            self.error = MultiLineLabel(text="\n\n---Er ging iets fout, probeer het opnieuw!---\n\n",
                                        background_normal="", background_color=(1, 0, 0, 0.4))
            self.layout.add_widget(self.error)
        else:
            try:
                self.layout.remove_widget(self.error)
            except: None
            EncryptionApp.subject = str(self.subject.text)
            C = ConnectClass.Connections()
            ss = False
            idlist = C.getkeys(EncryptionApp.touser)
            if idlist != False:
                CC = CryptoSuite.CryptoSuite(False)
                if str(CC.listIDs()) != "[]":
                    try:
                        ID = idlist[random.randint(0,len(idlist)-1)]
                        if EncryptionApp.reply == False:
                            CC.encrypt(128,(str(EncryptionApp.subject)+"=-=-"+str(self.message.text)+
                                            " =-=-Verzonden door: "+str(EncryptionApp.username)),ID)
                        else:
                            CC.encrypt(128, (str(EncryptionApp.subject) + "=-=-" + str(
                                self.message.text) + " =-=-"+str(EncryptionApp.reply)), ID)
                            EncryptionApp.reply = False
                        datalist = []
                        with open("Encrypted "+str(ID)+".dat","r") as f:
                            for line in f:
                                datalist.append(line.replace("\n", ""))
                        f.close()
                        msg = self.listToString(datalist)
                        if C.addmsg(str(EncryptionApp.touser),str(random.randint(1,1000)),str(msg)):
                            ss = True
                    except:
                        self.succes = MultiLineLabel(text="\n\n---Er ging iets fout, probeer het opnieuw!---\n\n",
                                                     on_release=self.home,background_normal="",
                                                     background_color=(1, 0, 0, 0.4))
                        self.layout.add_widget(self.succes)
                    else:
                        self.layout.remove_widget(self.subject)
                        self.layout.remove_widget(self.subjectlabel)
                        self.layout.remove_widget(self.message)
                        self.layout.remove_widget(self.subjectlabel1)
                        self.layout.remove_widget(self.sendbutton)
                        if ss == True:
                            try:
                                self.layout.remove_widget(self.succes)
                            except: None
                            self.message.text = ""
                            self.subject.text = ""
                            self.succes = MultiLineLabel(text="\n\n---Bericht verstuurd!---\n\n",on_release=self.home,
                                                         background_normal = "",
                                                         background_color = (0.129, 0.129, 0.129, 1))
                            self.layout.add_widget(self.succes)
                        else:
                            try:
                                self.layout.remove_widget(self.error)
                            except:
                                None
                            self.error = MultiLineLabel(
                                text="\n\n---Er ging iets fout, probeer het opnieuw!---\n\n",
                                background_normal="", background_color=(1, 0, 0, 0.4))
                            self.layout.add_widget(self.error)
            else:
                try:
                    self.layout.remove_widget(self.error)
                except:
                    None
                self.error = MultiLineLabel(text="\n\n---Er ging iets fout, raadpleeg de handleiding over 'rechten'!"
                                                 "---\n\n",
                                            background_normal="", background_color=(1, 0, 0, 0.4))
                self.layout.add_widget(self.error)


# Class for selecting the user to send a message to screen:
class touser(Screen):
    def __init__(self, **kwargs):
        super(touser, self).__init__(**kwargs)
        # Define layout:
        self.layout = GridLayout(cols=1, spacing=0, size_hint_y=None, pos=self.pos)
        self.bind(on_enter=self.refresh)
        self.image = Image(source="icon 2.png", size_hint_y=None,size=self.size)
        self.bind(size=self.getsize)
        self.layout.add_widget(self.image)

        # Home button:
        self.backhome = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
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
        self.refreshbutton = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                            text="\n\n[Gebruikers-lijst opnieuw ophalen]\n\n")
        self.refreshbutton.bind(on_release=self.refresh)
        self.layout.add_widget(self.refreshbutton)

        # Draw scrollview:
        self.layout.bind(minimum_height=self.layout.setter('height'))
        root = ScrollView(do_scroll_x=False)
        root.scroll_timeout = EncryptionApp.scrolltimeout
        root.add_widget(self.layout)
        self.add_widget(root)

    def getsize(self, obj, event):
        x, y = self.size
        self.image.size = (x / 7, y / 7)

    def nexts(self,obj):
        EncryptionApp.touser = str(obj.id)
        EncryptionApp.sm.current = "sendscreen"

    def refresh(self,obj):
        self.layout.clear_widgets()

        # Home button:
        self.layout.add_widget(self.image)
        self.backhome = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
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
        userlist.remove(str(EncryptionApp.username))

        # Refresh:
        self.refreshbutton = MultiLineLabel(background_normal="", background_color=(0.129, 0.129, 0.129,1),
                                            text="\n\n[Gebruikers-lijst opnieuw ophalen]\n\n")
        self.refreshbutton.bind(on_release=self.refresh)
        self.layout.add_widget(self.refreshbutton)

        # To user box:
        self.touserlabel = MultiLineLabel(text="\n\n Naar wie wilt u een bericht sturen:\n",size_hint_y=None)
        self.layout.add_widget(self.touserlabel)
        for i in userlist:
            self.layout.add_widget(MultiLineLabel(text='\n\n -  ' + i + '\n\n', on_press=self.nexts,
                                                  id=i,background_normal="",background_color=(1, 1, 1, 1),
                                                  color=(0,0,0,1)))

    def home(self,obj):
        EncryptionApp.sm.current = "mainmenu"


# Main loop
if __name__ == '__main__':
    app = EncryptionApp()
    app.run()
