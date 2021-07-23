import eliza.EString as EString
from eliza.decomp import DecompList
from typing import List

class Key:
	"Object containing a key, rank and associated list of decomopsition rules"
	def __init__(self, key: str = None, rank: int = 0, decomp: DecompList = None):
		self.key: str = key
		self.rank: int = rank
		self.decomp: DecompList = decomp

	def __repr__(self):
		return f"<Key '{self.key}'>"
		
	def copy_in(self, other):
		"Copy `other` into `self`"
		self.key = other.key
		self.rank = other.rank
		self.decomp = other.decomp
		
	def pprint(self, indent):
		print(' ' * indent, end='')
		print("key: " + self.key + " " + self.rank)
		self.decomp.pprint(indent + 2)
		
	def print_key(self, indent):
		print(' ' * indent, end = '')
		print("key: " + self.key + " " + self.rank)


class KeyStack(list):
	max_stack_size = 20 # set to -1 for unlimited
		
	def key(self, n: int) -> Key:
		"Get a key from the stack"
		if n < 0:
			raise IndexError
		return self[n]
		
	def push_key(self, key: Key):
		"Push a key onto the stack, keeping the highest ranked keys at the bottom"
		if key is None:
			raise ValueError("Tried to push None to KeyStack")
		# bisect would be better, but does not support sort-by-key
		for i, elem in enumerate(self):
			if key.rank > elem.rank:
				self.insert(i, key)
				return
		self.append(key)


class KeyList(list):
	def add(self, key: str, rank: int, decomp: DecompList):
		"Construct a Key object from parameters and append"
		self.append(Key(key, rank, decomp))
		
	def pprint(self, indent: int):
		for i in range(len(self)):
			self[i].pprint(indent)
			
	def get_key(self, s: str) -> Key:
		"Get key by string value, or None if not found"
		for elem in self:
			if elem.key == s:
				return elem
		return None
		
	def build_key_stack(self, s: str) -> KeyStack:
		stack = KeyStack()
		s = s.strip()
		lines = [''] * 2
		k = None
		while EString.match(s, "* *", lines):
			k = self.get_key(lines[0])
			if k is not None:
				stack.push_key(k)
			s = lines[1]
		k = self.get_key(s)
		if k is not None:
			stack.push_key(k)
		return stack

__all__ = [ "Key", "KeyStack", "KeyList" ]