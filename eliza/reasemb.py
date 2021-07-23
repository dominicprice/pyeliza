class ReasembList(list):
	"Reassembly list"
	def add(self, reasmb):
		"Append a reassembly rule"
		self.append(reasmb)
		
	def pprint(self, indent):
		for elem in self:
			print(' ' * indent, end='')
			print("reasemb: " + elem)

__all__ = [ "ReasembList" ]