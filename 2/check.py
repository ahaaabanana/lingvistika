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

	#IF, WHILE, ELSE
	"""
	inputfile = sys.argv[1]
	with open(inputfile, 'r') as in_file:
		lines = in_file.readlines()
	for line in lines:
		if re.search('(\s|{)*' + states + '\s*\(.+\)\s*', line):
			line = re.sub('\(|\)|{|\n', '', line)
			line = re.sub('\s*$', '', line)
			line = re.sub('}\s*', '', line)
			line = re.sub('else\s+if', 'elif', line)
			line = re.sub('&&', 'and', line)
			line = re.sub('\|\|', 'or', line)
			line = re.sub('!', 'not ', line)
			line = line + ':\n'
			print(line)
	"""
	x = '   for (counter = 0; i < 10; i += 1) {}  '
	if re.search('\s*for\s*\(.*\)\s*{\s*', x):
		tabs = re.search('^\s*', x).group(0)
		variable = re.search('\(\s*\w+', x).group(0)
		variable = re.sub('\(', '', variable)
		start = re.search('\(\s*[\w\s=]+;', x).group(0)
		start = re.sub('[\(a-z\s]+', '', start)
		start = re.sub('=\s*', '', start)
		start = re.sub(';', '', start)
		step = re.search(';\s*[^\);]+\)', x).group(0)
		step = re.sub('[^=]+=\s*', '', step)
		step = re.sub('\s*\)', '', step)
		end = re.search(';[^;]+;', x).group(0)
		end = re.sub('[^<>=!]+[<>=!]\s*', '', end)
		end = re.sub(';', '', end)
		# print(end)
		line = tabs + 'for ' + variable + ' in range(' + start + ', ' + end + ', ' + step + '):\n'
		print(line)
main()
