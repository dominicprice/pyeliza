import sys, os
sys.path.append(os.path.abspath("."))
from eliza import ElizaMain
from time import sleep

if __name__ == "__main__":
	e1 = ElizaMain("scripts/original1966.txt")
	e2 = ElizaMain("scripts/original1966.txt")

	s = e1.respond("Hello")
	print("ELIZA:", s)
	while True:
		sleep(1)
		s = e2.respond(s)
		print("ALIZE:", s)
		sleep(1)
		s = e1.respond(s)
		print("ELIZA:", s)