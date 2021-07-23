#!/usr/bin/env python3

import sys
from eliza.elizamain import ElizaMain
from discord import Client

class Eliza(Client):
	def __init__(self):
		super().__init__()
		self.sessions = {}

	async def on_message(self, message):
		if message.author == self.user:
			print("Ignoring message from self")
			return
		msg = message.content.lower()		
		
		if message.author in self.sessions:
			eliza = self.sessions[message.author]
			reply = eliza.respond(msg)
			if eliza.finished:
				del self.sessions[message.author]
			await message.reply(reply)
			return
					
		if self.user in message.mentions:
			if any(x in message.content for x in ["hi", "hello", "howdy", "yo"]):
				eliza = ElizaMain()
				self.sessions[message.author] = eliza
				with open("scripts/original1966.txt") as f:
					eliza.read_script(f)
				reply = eliza.respond("hello")
				await message.reply(reply)
			
if __name__ == "__main__":
	if len(sys.argv != 2):
		print(f"Usage: {sys.argv[0]} <discord-token>")
	eliza = Eliza()
	eliza.run(sys.argv[1])