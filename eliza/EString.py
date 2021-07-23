def amatch(s: str, pat: str) -> int:
	"""
	Returns number of matching characters in `s` and `pat` before
	a "*" or "#" character in pat. Returns -1 if strings do not match
	Example:
		amatch("abc", "a*") -> 1
		amatch("wx", "wx") -> 2
		amatch("xy", "xz") -> -1
	"""
	for count, (c, p) in enumerate(zip(s, pat)):
		if p in "*#":
			return count
		if c != p:
			return -1
	return len(s)
	
def find_pat(s: str, pat: str) -> int:
	"""
	Try to match `s[i:]` against `pat` using `amatch`. Returns the value
	of `i` which matches, or -1 if no match.
	"""
	for i in range(len(s)):
		if amatch(s[i:], pat) >= 0:
			return i
	return -1
	
def find_num(s: str) -> int:
	"""
	Return number of numeric digits 0-9 at start of string
	"""
	num = "0123456789"
	for i, c in enumerate(s):
		if c not in num:
			return i
	return len(s)
	
def match(s: str, pat: str, matches: list) -> bool:
	"""
	Match `s` against `pat`, returning the pieces
	which matched '*' and '#'
	"""
	i, j, k = 0, 0, 0 # position in `s`, `pat` and `matches`
	while j < len(pat):
		p = pat[j]
		if p == '*':
			# Calculate length of wildcard expression in `s`
			if j + 1 == len(pat):
				n = len(s) - i
			else:
				n = find_pat(s[i:], pat[j+1:])
			# Return False if find_pat returned no match
			if n < 0:
				return False
			matches[k] = s[i:i+n]
			i += n
			j += 1
			k += 1
		elif p == '#':
			n = find_num(s[i:])
			matches[k] = s[i:i+n]
			i += n
			j += 1
			k += 1
		else:
			n = amatch(s[i:], pat[j:])
			if n <= 0:
				return False
			i += n
			j += n
	return (i >= len(s) and j >= len(pat))
	
def translate(s: str, src: str, dest: str) -> str:
	"""
	Converts characters from `s` that appear in `src` with the
	characters at corresponding positions in `dest`
	"""
	if len(src) != len(dest):
		raise RuntimeError("impossible error")
	for a, b in zip(src, dest):
		s = s.replace(a, b)
	return s
	
def compress(s: str) -> str:
	"""
	Compress `s` by dropping spaces before ' ,.' characters and
	ensuring there is exactly one space before question mark
	"""
	dest = ""
	for a, b in zip(s, s[1:]):
		if a == ' ' and b in " ,.":
			pass # do not append to dest
		elif a != ' ' and b == '?':
			dest += a + ' '
		else:
			dest += a
	return dest + s[-1]
	
def trim(s: str) -> str:
	"""
	Remove leading spaces
	"""
	for i, c in enumerate(s):
		if c != ' ':
			return s[i:]
	return ''
	
def pad(s: str) -> str:
	"""
	Ensure the first and last characters of `s` are spaces
	"""
	if len(s) == 0:
		return ' '
	if s[0] != ' ':
		s = ' ' + s
	if s[-1] != ' ':
		s = s + ' '
	return s
	
def count(s: str, c: str) -> int:
	"""
	Count the number of occurences of `c` in `s`
	"""
	return sum(1 for k in s if k == c)

__all__ = [ "amatch", "find_pat", "find_num", "match", "translate", "compress", "trim", "pad", "count" ]