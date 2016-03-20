#!/usr/bin/python

# 15/4/13
# omCleverbot
# A cleverbot <-> omegle bot, written in python
# terry@bogaurd.net

# Uses pycleverbot(https://code.google.com/p/pycleverbot/) for cleverbot interaction

# Email me any interesting conversations or things you build on this :-)

import time, urllib, urllib2, cleverbot, simplejson
import sys
from colorama import *

def log(message, name="[LOG]", color=Fore.GREEN):
	message = unicode(message)
	print(color + name + Style.RESET_ALL + ": " + message)
	convLog.write(name + ": " + message + '\n')
	convLog.flush()

def typing(id):
	try:
		typing = urllib2.urlopen('http://omegle.com/typing', '&id='+id)
		typing.close()
	except: pass

def sendMessage(id, msg):
	try:
		msgReq = urllib2.urlopen('http://omegle.com/send', '&msg='+msg+'&id='+id)
		msgReq.close()
		log (msg, 'CleverBot', Fore.BLUE)
	except: pass

def pollEvents(id, events):
	cb = cleverbot.Cleverbot()
	lastMessage = time.time()
	
	while 1:
	
		# Read from Omegle to see if anything is happening
		try:
			omegle = urllib2.urlopen(events)
			data = omegle.read()
			omegle.close()
			eventsJson = simplejson.loads(data)
		except:
			log('Hmm... Something went wrong...', Fore.RED)
			break
		
		# print data 						# uncomment if you want the to see the raw response
		
		if eventsJson == None: break
		
		for json in eventsJson:

			if json[0] == 'connected':
				log("Connected!")
				if len(sys.argv) < 2:
					seed = cb.think()			# make this a random selection
				else:
					seed = sys.argv[1]
				sendMessage(id, seed)
				#cb.Ask(seed)

			elif json[0] == 'typing':
				log("Omegle User is typing...")
				lastMessage = time.time()
			    
			elif json[0] == 'gotMessage':
				
				incomingMsg = json[1]
				log(incomingMsg,'Omegle User', Fore.RED)
				
				# respond
				try:
					typing(id)
					outgoingMsg = cb.ask(incomingMsg)
					sendMessage(id, outgoingMsg)
				except Exception as e:
					log(str(e))
					sendMessage(id, "Huh?!")	# something went wrong with cleverbot (timeout, whatever)
					
				lastMessage = time.time()
			
			elif json[0] == 'strangerDisconnected':
				log('Omegle User has disconnected.', color=Fore.YELLOW)
				break
				
		if time.time() - lastMessage > 60:
			log("Idle timeout, disconnecting", color=Fore.YELLOW)
			break
		
def omegleConnect():
	global convLog
	while 1:
		convLog = open('./logs/' + str(int(time.time())) + '.txt', 'a')
		omegle = urllib2.urlopen('http://omegle.com/start','')
		id = omegle.read()
		omegle.close()
		id = id[1:len(id) - 1]
		#print('Session ID: ' + id)
		events = urllib2.Request('http://omegle.com/events', urllib.urlencode( {'id':id}))
		log('Looking for a partner...')
		pollEvents(id, events)
		print '==================================================='
		convLog.close()

# go.
omegleConnect()
