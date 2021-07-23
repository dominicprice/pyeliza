class Mem:
	"Stack structure representing persistent storage"
	mem_max = 20
	def __init__(self):
		self.memory = [''] * 20
		self.mem_top = 0
		
	def save(self, s: str):
		"Add a string to memory"
		if (self.mem_top < Mem.mem_max):
			self.memory[self.mem_top] = s
			self.mem_top += 1
			
	def get(self) -> str:
		"Retrieve a string from memory, or None if memory is empty"
		if self.mem_top == 0:
			return None
		m, self.memory = self.memory[0], self.memory[1:]
		self.mem_top -= 1
		return m

__all__ = [ "Mem" ]