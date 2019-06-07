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
	tabs = re.search('^\s*', line).group(0)
	line = re.sub('^\s*((' + types + ')\s+)+', 'def ', line) #REMOVE FUNCTION TYPE
	line = re.sub('(' + types + ')' + '\s+', '', line) #REMOVE TYPES OF FUNCTION ARGUMENTS
	line = re.sub('\s*{\s*', ':', line) #REPLACE { WITH :
	return tabs + line + '\n'

def function_content_line(line):
	if re.search('(' + types + ')' + '\s+', line): #IF VARIABLE
		if re.search('=', line): #IF INITIALIZATION
			line = re.sub('(' + types + ')' + '\s+', '', line) #REMOVE TYPE
			line = re.sub('\[\d*\]', '', line) #REMOVE [FROM HERE]
			line = re.sub('{', '[', line)
			line = re.sub('}', ']', line)
		else: #JUST A DECLARATION OF VARIABLE
			line = ''
	elif re.search('(\s|{)*' + states + '\s*\(.+\)\s*', line): #IF ELSE WHILE
			line = re.sub('\(|\)|{|\n', '', line)
			line = re.sub('\s*$', '', line)
			line = re.sub('}\s*', '', line)
			line = re.sub('else\s+if', 'elif', line)
			line = re.sub('&&', 'and', line)
			line = re.sub('\|\|', 'or', line)
			if re.search('![^=]', line):
				line = re.sub('!', 'not ', line)
			line = line + ':\n'
	elif re.search('\s*for\s*\(.*\)\s*', line):
		# print(line)
		tabs = re.search('^\s*', line).group(0) #REMEMBER SPACES BEFORE FOR
		variable = re.search('\(\s*\w+', line).group(0) #
		variable = re.sub('\(', '', variable)
		start = re.search('\(\s*[\w\s=]+;', line).group(0)
		start = re.sub('[\(a-z\s]+', '', start)
		start = re.sub('=\s*', '', start)
		start = re.sub(';', '', start)
		step = re.search(';\s*[^\);]+\)', line).group(0)
		step = re.sub('[^=]+=\s*', '', step)
		step = re.sub('\s*\)', '', step)
		end = re.search(';[^;]+;', line).group(0)
		end = re.sub('[^<>=!]+[<>=!]\s*', '', end)
		end = re.sub(';', '', end)
		# print(end)
		line = tabs + 'for ' + variable + ' in range(' + start + ', ' + end + ', ' + step + '):\n'
		# print(line)
	elif re.search('\s*}\s*', line): #REMOVING FUNCTION CLOSING BRACKET
		line = re.sub('\s*}\s*', '', line)
		# print(line)
	line = re.sub(';','', line) #REMOVE ;	
	line = re.sub('\+\+', ' += 1', line)
	line = re.sub('--', ' -= 1', line)
	line = re.sub('\s*{\s*', '', line)
	line = re.sub('true', 'True', line)
	line = re.sub('false', 'False', line)
	return line

def is_empty_func(function):
	for i in range(1, len(function)):
		if not (function[i] == '' or function[i].isspace()):
			return 0
	return 1

#CONVERTING EACH FUNCTION
"""
def convert_function(lines, start, end):
	# print(start, end)
	function = []
	isempty = 0
	name = function_name(lines[start])
	# print(name)
	function.append(name)
	start += 1
	#CONVERTING FUNCTION CONTENT
	while (start < end):
		line = function_content(lines[start])
		if line != '':
			function.append(line)
		start += 1
	#IF FUNCTION IS EMPTY
	if (is_empty_func(function)):
		function.clear()
		function.append(name)
		function.append('\tpass\n\n')
	return function
"""

"""
def function_content(function, lines, i, name):
	start = re.search('^\s*', lines[i]).group(0)
	while True:
		i += 1
		end = re.search('^\s*', lines[i]).group(0)
		line = function_content_line(lines[i])
		if line != '':
			function.append(line)
		if start == end:
			break
	if (is_empty_func(function)): #ADD pass IF FUNCTION IS EMPTY
		function.clear()
		function.append(name)
		tabs = re.search('^\s*', name).group(0)
		function.append(tabs + '\tpass\n\n')
"""

def convert_function(outputfile, lines, i):
	function = []

	name = function_name(lines[i])
	function.append(name)
	start = re.search('^\s*', lines[i]).group(0)
	while True:
		i += 1
		end = re.search('^\s*', lines[i]).group(0)
		line = function_content_line(lines[i])
		if line != '':
			function.append(line)
		if start == end:
			break
	if (is_empty_func(function)): #ADD pass IF FUNCTION IS EMPTY
		function.clear()
		function.append(name)
		tabs = re.search('^\s*', name).group(0)
		function.append(tabs + '\tpass\n\n')
	append_line_to_pyfile(outputfile, function)
	function.clear()
	return i

# def class_name(line):


def convert_file(inputfile, outputfile):
	pos = [0]
	classes = []
	j = 0
	with open(inputfile, 'r') as in_file:
		lines = in_file.readlines()
	creat_py_file(outputfile)
	libraries = convert_libraries(lines, pos) #CONVERTED LIBRARIES
	append_line_to_pyfile(outputfile, libraries)
	i = pos[0]
	while i < len(lines):
		if re.search('\s.+\s*\(\D*?\)\s*{\s*', lines[i]):
			i = convert_function(outputfile, lines, i)
		# if re.search('\s*class\s+', lines[i]):
		# 	start = re.search('^\s*', lines[i]).group(0)
		# 	name = classes.append(re.sub('\s*{\s*', ':', lines[i])) #CONVERT CLASS NAME
		# 	while True:
		# 		i += 1
		# 		end = re.search('^\s*', lines[i]).group(0)
		# 		if re.search('\s.+\s*\(\D*?\)\s*{\s*', lines[i]):
		# 			function_content(classes, lines, i, name)
		# 		if start == end:
		# 			break
		elif lines[i].isspace():
			append_line_to_pyfile(outputfile, lines[i])
		i += 1
			
	# for i in range(len(func_positions) - 1):
		# function = convert_function(lines, func_positions[i], func_positions[i + 1])
		# append_line_to_pyfile(outputfile, function)

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
