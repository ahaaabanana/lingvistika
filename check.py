#!/usr/bin/env python3

import re
import sys
from data import *

def main():
	#REG FOR FUNCTIONS
	"""
	types = 'const|int|void|char|float|bool|unsigned|char\*|int\*'
	x = 'unsigned char* double_value(int in, char z) {'
	x = re.sub('^\s*((' + types + ')\s+)+', 'def ', x)
	x = re.sub('(' + types + ')' + '\s+', '', x)
	x = re.sub('\s*{\s*', ':', x)
	print(x)
	"""

	#REG FOR FUNCTION VARIABLES
	"""
	types = 'const|int|float|void|char|bool|unsigned|char\*|int\*'
	inputfile = sys.argv[1]
	with open(inputfile, 'r') as in_file:
		lines = in_file.readlines()
	for line in lines:
		line = re.sub(';','', line) #REMOVE ;
		if re.search('(' + types + ')' + '\s+', line): #IF VARIABLE
			if re.search('=', line): #IF INITIALIZATION
				line = re.sub('(' + types + ')' + '\s+', '', line) #REMOVE TYPE
				line = re.sub('\[\d*\]', '', line) #REMOVE [FROM HERE]
				line = re.sub('{', '[', line)
				line = re.sub('}', ']', line)
				line = re.sub('true', 'True', line)
				line = re.sub('false', 'False', line)
			else:
				line = ''
		if line != '':
			print(line)
		"""

main()
