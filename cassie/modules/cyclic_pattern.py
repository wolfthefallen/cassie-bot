from cassie.argparselite import ArgumentParserLite
from cassie.templates import CassieXMPPBotModule

# some clients don't like large messages
MAX_PATTERN_SIZE = 4096

def create_cyclic_pattern(size):
	char1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	char2 = "abcdefghijklmnopqrstuvwxyz"
	char3 = "0123456789"

	charcnt = 0
	pattern = ""
	max = int(size)
	while charcnt < max:
		for ch1 in char1:
			for ch2 in char2:
				for ch3 in char3:
					if charcnt < max:
						pattern = pattern + ch1
						charcnt = charcnt + 1
					if charcnt < max:
						pattern = pattern + ch2
						charcnt = charcnt + 1
					if charcnt < max:
						pattern = pattern + ch3
						charcnt = charcnt + 1
	return pattern

class Module(CassieXMPPBotModule):
	permissions = {'cyclic_pattern': 'user'}
	def cmd_cyclic_pattern(self, args, jid, is_muc):
		parser = ArgumentParserLite('cyclic_pattern', 'create and search a cyclic pattern')
		parser.add_argument('-s', '--size', dest='size', type=int, required=True, help='pattern size to create')
		parser.add_argument('-p', '--pattern', dest='pattern', help='pattern to find')
		parser.add_argument('--code', dest='code', action='store_true', help='format the pattern for code')
		if not len(args):
			return parser.format_help()
		results = parser.parse_args(args)

		size = results['size']
		if size > MAX_PATTERN_SIZE:
			return 'size is too large, max is ' + str(MAX_PATTERN_SIZE)
		pattern = create_cyclic_pattern(size)
		if results['pattern'] is None:
			if results['code']:
				code = "# Cyclic Pattern Length: {0}\n".format(len(pattern))
				code += 'pattern  = ""\n'
				for idx in range(0, len(pattern), 32):
					code += "pattern += \"{0}\"\n".format(pattern[idx:idx + 32])
				return code
			return pattern
		search_pattern = results['pattern']
		if len(search_pattern) == 8:
			search_pattern = search_pattern.decode('hex')
			search_pattern = list(search_pattern)
			search_pattern.reverse()
			search_pattern = ''.join(search_pattern)
		if len(search_pattern) != 4:
			return 'the search pattern is invalid'
		index = pattern.find(search_pattern)
		if index == -1:
			return 'could not find the search pattern'
		return 'found exact match at ' + str(index)
