class WordList(list):
	"List of words"
	def add(self, word: str):
		"Append a word to the list"
		self.append(word)
		
	def pprint(self, indent: int):
		for elem in self:
			print(elem, end='  ')
		print()
	
	def find(self, s: str) -> bool:
		"Find a string in the word list, returning True or False"
		for elem in self:
			if s == elem:
				return True
		return False

__all__ = [ "WordList" ]