import eliza.EString as EString

class PrePost:
	"Stores pre and post text transformations"
	def __init__(self, src: str, dest: str):
		self.src: str = src
		self.dest: str = dest
		
	def pprint(self, indent):
		print(' ' * indent, end='')
		print("pre-post: " + src + "  " + dest)


class PrePostList(list):
	"""
	List of pre-port emtries used to perform word transformations
	prior to or after other processing
	"""
	def add(self, src: str, dest: str):
		"Construct a PrePost object and append"
		self.append(PrePost(src, dest))
		
	def pprint(self, indent):
		for elem in self:
			elem.pprint(indent)
			
	def xlate(self, s: str) -> str:
		"""
		Translate a word: if `s` matches a `src` string on the list,
		return the corresponding `dest`; else return the input
		"""
		for elem in self:
			if s == elem.src:
				return elem.dest
		return s
		
	def translate(self, s: str) -> str:
		"""
		Translate a string `s` by trimming off spaces, breaking it into words
		and word each word substituting the matching `src` word with `dest`
		"""
		lines = [''] * 2
		work = EString.trim(s)
		s = ''
		while EString.match(work, "* *", lines):
			s += self.xlate(lines[0]) + " "
			work = EString.trim(lines[1])
		s += self.xlate(work)
		return s
	
__all__ = [ "PrePost", "PrePostList" ]