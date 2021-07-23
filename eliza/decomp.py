from random import randrange
from typing import List
from eliza.reasemb import ReasembList

class Decomp:
	"Single decomposition rule for a key"
	def __init__(self, pattern: str, mem: bool, reasemb: ReasembList):
		self.pattern: str = pattern
		self.mem: bool = mem
		self.reasemb: ReasembList = reasemb
		self.cur_reasemb: int = 100

	def pprint(self, indent: int):
		m = "true" if self.mem else "false"
		print(' ' * indent, end='')
		print("decomp: " + self.pattern + " " + m)
		self.reasemb.pprint(indent + 2)
		
	def next_rule(self):
		"Get the next reassembly rule"
		if len(self.reasemb) == 0:
			print("No reassembly rule.")
			return None
		return self.reasemb[self.cur_reasemb]
		
	def step_rule(self):
		"Step to the next reassembly rule. If `mem=True` then picks a random rule"
		size = len(self.reasemb)
		if self.mem:
			self.cur_reasemb = randrange(len(self.reasemb))
		self.cur_reasemb += 1
		if self.cur_reasemb >= size:
			self.cur_reasemb = 0


class DecompList(list):
	"Stores all the decompositions of a single key"
	def add(self, word: str, mem: bool, reasmb: ReasembList):
		"Construct a Decomp from parameters and append"
		self.append(Decomp(word, mem, reasmb))

	def pprint(self, indent: int):
		for elem in self:
			elem.pprint(indent)

__all__ = [ "Decomp", "DecompList" ]