#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 08.07.2009

@author: eurekafag
'''

import sys
import xmpp
from xmpp import *
import threading
import Queue
import traceback
from config import *
import hashlib

quitting = False
handler = 2
counter = 1
admins = []

class FloodBot:

    presence = {}
    plugins_instances = []
    flood = {}
    text = None
    
    prefix = "*"
    def __init__(self, user):
        self.jid = xmpp.JID(user[0])
        self.password = user[1]
        self.nick = user[2]

    def quit(self, sender, command):
        print "Quitting"
        self.quitting = 1

    def join(self, sender, command):
        self.bot.sendPresence(command[1] + "/" + Nick)

    def send(self, sender, command):
        self.word = " ".join(command[1:])
        self.say(sender[0], self.word)

    def messageCB(self, conn, msg):
        for i in msg.getTags("x"):
            if i.has_attr("stamp"):
                return
        if not msg.getBody():
            return

        sender = str(msg.getFrom()).split("/", 1)
        nick = " ".join(sender[1:])
        print "Message from " + str(msg.getFrom()) + " received: " + msg.getBody()
        if msg.getType() == "chat":
            if nick in self.flood and time.time() - self.flood[nick] > secflood or not nick in self.flood:
                self.flood[nick] = time.time()

# filter the shit
                filtered = "\n".join(msg.getBody()[:maxlen].splitlines()[:maxlines])
                if filtered[:5] == "pass " and filtered[5:] == password:
                    admins.append(nick)
                    self.bot.send(msg.buildReply("Теперь вы администратор бота."))
                    return
                
                if filtered[:6] == "unpass" and nick in admins:
                    admins.remove(nick)
                    self.bot.send(msg.buildReply("Права администратора сняты."))
                    return

                if filtered[:4] == "cmd " and nick in admins:
                    try:
                        exec(filtered[4:])
                    except:
                        # exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                        self.bot.send(msg.buildReply("Случилась НЁХ:\n" + str("".join(traceback.format_exception(*sys.exc_info())))))
                    return

#                myqueue.put( ( sender[0], str(filtered) ) )

		global counter
                if filtered[0] == "%" or filtered[0] == "!":
		    myqueue.put( ( sender[0], str.format("{1}", counter, filtered) ), True);
                else:
		    tripcode = ""
		    prefix = ""
		    if filtered[0] == "*":
		    	m = hashlib.md5()
			m.update(nick + salt)
			tripcode = "[" + m.hexdigest()[:6] + "] "
			filtered = filtered[1:]

	            if filtered[:4] == "/me ":
		        prefix = "/me "
			filtered = filtered[4:]

	            myqueue.put( ( sender[0], str.format("{3}<{2}{0:06d}> {1}", counter, filtered, tripcode, prefix) ), True);
                    lock.acquire()
                    counter += 1
		    lock.release()

            elif nick in self.flood and time.time() - self.flood[nick] < secflood:
                self.bot.send(msg.buildReply(str.format("Следующее сообщение можно будет послать через {0:.2f} секунд", secflood - time.time() + self.flood[nick])))
        if msg.getType() == "groupchat" and self.text != None:
            if msg.getBody() == self.text[1]:
                if msg.getTag("error") and msg.getTag("error").getAttr("code") == 500:
                    myqueue.put(self.text, True)
                if not msg.getTag("error"):
                    self.text = None
                    myqueue.task_done()

    def presenceCB(self, conn, msg):
        if msg.getAttr("type") == "unavailable":
            print msg.getFrom(), "was kicked"
            return

        sender = str(msg.getFrom()).split("/", 1)
        print "Presence from: ", sender
        nick = " ".join(sender[1:])

    def say(self, conf, text, typ = "groupchat"):
        self.bot.send(xmpp.protocol.Message(conf, text, typ))

    def connect(self, number):
        self.quitting = 0
        self.bot = xmpp.Client(self.jid.getDomain(), debug=[])
        self.bot.connect()
        self.bot.auth(self.jid.getNode(), self.password)
        self.bot.sendInitPresence()
        self.bot.RegisterHandler("message", self.messageCB)
        self.bot.RegisterHandler("presence", self.presenceCB)
        for conf in Conferences:
            self.bot.sendPresence(conf + "/" + self.nick)

        global quitting
        while not quitting:
            self.bot.Process(0)
            global handler
            if self.text == None and handler == number:
                try:
                    self.text = myqueue.get(False)
                    self.say(self.text[0], self.text[1])
                    lock.acquire()
                    handler += 1
                    if handler > threadnum:
                        handler = 1
                    lock.release()
                except:
                    pass
            time.sleep(1)

        self.bot.disconnect()

class botthread(threading.Thread):

    def __init__(self, num):
        threading.Thread.__init__(self)
        self.nick = Names[num - 1]

        self.number = num

    def run(self):
        self.localsettings = Settings[:]
        self.localsettings.append(self.nick)
        mybot = FloodBot(self.localsettings)
        mybot.connect(self.number)

lock = threading.Lock()
reload(sys)
sys.setdefaultencoding( "utf-8" )
myqueue = Queue.Queue()
fcnt = open("counter", "r+")
counter = int(fcnt.read())

for i in range(1, threadnum + 1):
    botthread(i).start()

try:
    while True:
        time.sleep(60)
        fcnt.seek(0)
        fcnt.write(str(counter))

except:
    traceback.print_exc()
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    traceback.print_tb(exceptionTraceback)
    quitting = True
    fcnt.seek(0)
    fcnt.write(str(counter))
