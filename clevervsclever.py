import sys, time, cleverbot
from colorama import *

seed = sys.argv[1]


cb1 = cleverbot.Cleverbot()
cb2 = cleverbot.Cleverbot()

i = 0

def log(name, message, color):
	print(color + name + Style.RESET_ALL + ": " + message)

while True:
	try:
		msg1 = cb1.ask(msg2)
	except NameError:
		log("Bot 2", seed, Fore.BLUE)
		msg1 = cb1.ask(seed)
		pass
	log("Bot 1", msg1, Fore.RED)
	msg2 = cb2.ask(msg1)
	log("Bot 2", msg2, Fore.BLUE)
	time.sleep(0.5)