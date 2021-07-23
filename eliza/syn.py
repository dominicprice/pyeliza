import eliza.EString as EString
from eliza.word import WordList
from typing import List

class SynList(list):
	"Collection of synonyms"
	def add(self, words):
		"Add a WordList of synonyms to the list"
		self.append(words)
		
	def pprint(self, indent):
		for elem in self:
			print(' ' * indent, end='')
			elem.pprint(indent)
			
	def find(self, s: str) -> WordList:
		"Find a word list containing `s` , or None if none exist"
		for elem in self:
			if elem.find(s):
				return elem
		return None
		
	def match_decomp(self, s: str, pat: str, lines: List[str]) -> bool:
		"""
		Decomposition match: if decomp has no synonyms, do a regular
		match, otherwise try all synonyms
		"""
		if not EString.match(pat, "*@* *", lines):
			return EString.match(s, pat, lines)
		
		first = lines[0]
		syn_word = lines[1]
		the_rest = " " + lines[2]
		syn = self.find(syn_word)
		if syn is None:
			print("Could not find syn list for " + syn_word)
			return False
		for elem in syn:
			pat = first + elem + the_rest
			if EString.match(s, pat, lines):
				n = EString.count(first, '*')
				for j in range(len(lines)-2, n-1, -1):
					lines[j+1] = lines[j];
				lines[n] = elem
				return True
		return False

__all__ = [ "SynList" ]