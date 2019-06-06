#ALL AVAILABLE TYPES IN C/C++
types = 'const|int|void|char|float|bool|unsigned|'
types += 'char\*|int\*|float\*|void\*|bool\*'

#STATEMENTS IN C/C++
states = 'if|else|while'

#ALL MATCHIN LIBRARIES BETWEEN C/C++ AND PYTHON
d = {
	'regex.h': 're',
	'iostream': 'sys',
	'cmath': 'math',
	'math.h': 'math'
	}