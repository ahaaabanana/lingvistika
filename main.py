#!/usr/bin/env python3

import sys
import os.path
import re
from array import array
from data import *

#CONVERTING LIBRARIES
def convert_libraries(lines, pos):
	libraries = []
	keys = d.keys()
	for line in lines:
		if re.search('#include', line):
			pos[0] += 1
			for key in keys:
				if re.search(key, line):
					libraries.append('import ' + d[key] + '\n')
					break
	libraries.append('\n')
	return libraries

#ADDING LINES TO PYTHON FILE
def append_line_to_pyfile(outputfile, lines):
	with open(outputfile, 'a') as out_file:
		for line in lines:
			out_file.write(line)

#CREATE FILE
def creat_py_file(outputfile):
	f = open(outputfile, 'w')
	f.close()

#FUNCTION POSITIONS
def function_positions(lines, pos):
	f = []
	for i in range(pos[0], len(lines)):
		if re.search('\s.+\s*\(\D*?\)\s*{\s*', lines[i]):
			f.append(i)
	f.append(len(lines) - 1)
	return f

#CONVERTING FUNCTION DECLARATION
def function_name(line):
	line = re.sub('^\s*((' + types + ')\s+)+', 'def ', line) #REMOVE FUNCTION TYPE
	line = re.sub('(' + types + ')' + '\s+', '', line) #REMOVE TYPES OF FUNCTION ARGUMENTS
	line = re.sub('\s*{\s*', ':', line) #REPLACE { WITH :
	return line + '\n'

def function_content(line):
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
	elif re.search('\s*}\s*', line):
		line = re.sub('}', '', line)
	return line

def is_empty_func(function):
	for i in range(1, len(function)):
		if not (function[i] == '' or function[i].isspace()):
			return 0
	return 1

#CONVERTING EACH FUNCTION
def convert_function(lines, start, end):
	print(start, end)
	function = []
	isempty = 0
	name = function_name(lines[start])
	function.append(name)
	start += 1
	while (start < end):
		line = function_content(lines[start])
		if line != '':
			function.append(line)
		start += 1
	if (is_empty_func(function)):
		function.clear()
		function.append(name)
		function.append('\tpass\n\n')
	return function

def convert_file(inputfile, outputfile):
	pos = [0]
	with open(inputfile, 'r') as in_file:
		lines = in_file.readlines()
	creat_py_file(outputfile)
	libraries = convert_libraries(lines, pos) #CONVERTED LIBRARIES
	append_line_to_pyfile(outputfile, libraries)
	func_positions = function_positions(lines, pos) #FUNCTION POSITIONS
	for i in range(len(func_positions) - 1):
		function = convert_function(lines, func_positions[i], func_positions[i + 1])
		append_line_to_pyfile(outputfile, function)

def main():
	if len(sys.argv) != 2:
		print('Number of arguments must be 1', file=sys.stderr)
		sys.exit(-1)
	elif os.path.isfile(sys.argv[1]):
		py_file_name = os.path.basename(sys.argv[1])
		py_file_name = os.path.dirname(sys.argv[1]) + '/' + os.path.splitext(py_file_name)[0] + '.py'
		convert_file(sys.argv[1], py_file_name)
	else:
		print('No such file', sys.argv[1], file=sys.stderr)

if __name__ == '__main__':
	main()
