import eliza.EString as EString
from eliza.key import Key, KeyList, KeyStack
from eliza.syn import SynList
from eliza.prepost import PrePostList
from eliza.word import WordList
from eliza.memory import Mem
from eliza.decomp import Decomp, DecompList
from eliza.reasemb import ReasembList
from typing import List, TextIO

class ElizaMain:
	"""
	Main Eliza class which can load and store a script as well as
	respond to input through the command line
	"""

	def __init__(self, scriptname=None):
		self.ps1 = "  YOU: "
		self.ps2 = "ELIZA: "

		self.reset()
		if scriptname is not None:
			with open(scriptname, 'r') as f:
				self.read_script(f)

	def reset(self):
		"Reset entire internal state"
		self.keys: KeyList = KeyList()
		self.syns: SynList = SynList()
		self.pre: PrePostList = PrePostList()
		self.post: PrePostList = PrePostList()
		self.initial: str = "Hello."
		self.finl: str = "Goodbye."
		self.stop: WordList = WordList()
		self.key_stack: KeyStack = KeyStack()
		self.mem: Mem = Mem()
		self.last_decomp: DecompList = None
		self.last_reasemb: ReasembList = None
		self.finished: bool = False

	def reset_memory(self):
		"Reset conversation memory retaining the currently loaded script"
		self.mem = Mem()


	def read_script(self, script: TextIO, echo: bool = False):
		"Process a script file from file file object `script`"
		for line in script:
			self._collect(line.rstrip("\r\n"))
		if echo:
			self.pprint()

	def respond(self, s: str) -> str:
		"Form a response to an input string"
		reply = ""
		s = EString.translate(s, "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
								 "abcdefghijklmnopqrstuvwxyz")
		s = EString.translate(s, "@#$%^&*()_-+=~`{[}]|:;<>\\\"",
								 "                          "  )
		s = EString.translate(s, ",?!", "...")
		s = EString.compress(s)
		lines = [''] * 2
		while EString.match(s, "*.*", lines):
			reply = self._sentence(lines[0])
			if reply is not None:
				return reply
			s = EString.trim(lines[1])
		if len(s) != 0:
			reply = self._sentence(s)
			if reply is not None:
				return reply
		m = self.mem.get()
		if m is not None:
			return m
		key = self.keys.get_key("xnone")
		if key is not None:
			dummy = None
			reply = self._decompose(key, s, dummy)
			if reply is not None:
				return reply
		return "I am at a loss for words."
		
	def run_program(self, eliza_says_first: bool = True):
		"Basic command-line based interaction using self.ps1 and self.ps2 for prompts"
		if eliza_says_first:
			reply = self.respond("Hello")
			print(self.ps2 + reply)
		while True:
			from time import sleep
			s = input(self.ps1)
			reply = self.respond(s)
			print(self.ps2 + reply)
			if self.finished:
				break

	def pprint(self):
		"Print the stored script"
		self.keys.pprint(0)
		self.syns.pprint(0)
		self.pre.pprint(0)
		self.post.pprint(0)
		print("initial: " + self.initial)
		print("final:   " + self.finl)
		self.stop.pprint(0)

	def _collect(self, s: str):
		"Process a line of script input"
		s = s.rstrip("\r\n")
		lines = [''] * 4
		if EString.match(s, "*reasmb: *", lines):
			if self.last_reasemb is None:
				print("Error: no last reasemb")
				return
			self.last_reasemb.add(lines[1])
		elif EString.match(s, "*decomp: *", lines):
			if self.last_decomp is None:
				print("Error: no last decomp")
				return
			self.last_reasemb = ReasembList()
			temp = lines[1]
			if EString.match(temp, "$ *", lines):
				self.last_decomp.add(lines[0], True, self.last_reasemb)
			else:
				self.last_decomp.add(temp, False, self.last_reasemb)
		elif EString.match(s, "*key: * #*", lines):
			self.last_decomp = DecompList()
			self.last_reasemb = None
			n = 0
			if len(lines[2]) != 0:
				n = int(lines[2])
			self.keys.add(lines[1], n, self.last_decomp)
		elif EString.match(s, "*key: *", lines):
			self.last_decomp = DecompList()
			self.last_reasemb = None
			self.keys.add(lines[1], 0, self.last_decomp)
		elif EString.match(s, "*synon: * *", lines):
			self.words = WordList()
			self.words.add(lines[1])
			s = lines[2]
			while EString.match(s, "* *", lines):
				self.words.add(lines[0])
				s = lines[1]
			self.words.add(s)
			self.syns.add(self.words)
		elif EString.match(s, "*pre: * *", lines):
			self.pre.add(lines[1], lines[2])
		elif EString.match(s, "*post: * *", lines):
			self.post.add(lines[1], lines[2])
		elif EString.match(s, "*initial: *", lines):
			self.initial = lines[1]
		elif EString.match(s, "*final: *", lines):
			self.finl = lines[1]
		elif EString.match(s, "*quit: *", lines):
			self.stop.add(" " + lines[1] + " ")
		else:
			print("Unrecognised input: " + s)
		
	def _sentence(self, s: str) -> str:
		"""
		Process a sentence by making pre transformations, checking for a 
		quit word, scanning sentences for keys to build a key stack and then
		trying decompositions for each key
		"""
		s = self.pre.translate(s)
		s = EString.pad(s)
		if self.stop.find(s):
			self.finished = True
			return self.finl
			
		self.key_stack = self.keys.build_key_stack(s)
		for key in self.key_stack:
			goto_key = Key()
			reply = self._decompose(key, s, goto_key)
			if reply is not None:
				return reply
			while goto_key.key is not None:
				reply = self._decompose(goto_key, s, goto_key)
				if reply is not None:
					return reply
		return None
		
	def _decompose(self, key: Key, s: str, goto_key: Key) -> str:
		"""
		Decompose a string according to the given key by trying each
		decomposition rule in order trying to `assemble` a reply and return
		it. If the assembly is a goto rule, return None and give the key.
		"""
		reply = [''] * 10
		for d in key.decomp:
			pat = d.pattern
			if self.syns.match_decomp(s, pat, reply):
				rep = self._assemble(d, reply, goto_key)
				if rep is not None:
					return rep
				if goto_key.key is not None:
					return None
		return None
		
	def _assemble(self, d: Decomp, reply: List[str], goto_key: Key) -> str:
		"""
		Assemble a reply from a decomposition rule and the input. If the
		reassembly rule is goto, return None and give the `goto_key` to use.
		"""
		lines = [''] * 3
		d.step_rule()
		rule = d.next_rule()
		if EString.match(rule, "goto *", lines):
			goto_key.copy_in(self.keys.get_key(lines[0]))
			if goto_key.key is not None:
				return None
			print("Goto rule did not match key: " + lines[0])
			return None
		work = ""
		while EString.match(rule, "* (#)*", lines):
			rule = lines[2]
			n = int(lines[1]) - 1
			if n < 0 or n >= len(reply):
				print("Substitution number is bad " + lines[1])
				return None
			reply[n] = self.post.translate(reply[n])
			work += lines[0] + " " + reply[n]
		work += rule
		if d.mem:
			self.mem.save(work)
			return None

		# Clean up by ensuring single spaces between everything except punctuation
		work = ' '.join(work.split())
		work = work.replace(" .", ".").replace(" ,", ",").replace(" ?", "?")
		return work

__all__ = [ "ElizaMain" ]