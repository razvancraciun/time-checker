#!/usr/bin/env python3
from sys import argv, stderr
from os import path

def errprint(*args, **kwargs):
	print(*args, file = stderr, **kwargs)

if __name__ != '__main__':
	errprint('Cannot use timechecker as a module')
	exit(1)

if len(argv) < 2:
	errprint('!> input file path must be given')
	exit(1)

input_file = argv[1]
output_file = f'{path.splitext(input_file)[0]}.xml'

print('Reading input data...')
input_text = ''
with open(input_file, 'r') as f:
	input_text = f.read()

print('Instantiating classifier...')
from ml.bayes import BayesClassifier
classifier = BayesClassifier()

print('Running classifier...')
time_expressions = classifier.run_on_text(input_text)

print('Generating output...')

from regex.redefs import timex
import xml.etree.ElementTree as et

def indent(el: et.Element, lvl = 0):
	TAB = '\t'
	INDENT = '\n' + lvl * TAB
	if len(el):
		if not el.text or not el.text.strip():
			el.text = INDENT + TAB
		if not el.tail or not el.tail.strip():
			el.tail = INDENT
		for el in el:
			indent(el, lvl + 1)
		if not el.tail or not el.tail.strip():
			el.tail = INDENT
	else:
		if lvl and (not el.tail or not el.tail.strip()):
			el.tail = INDENT

# for (is_time, expr) in time_expressions:
# 	if is_time:
# 		print(f'"{expr}"\t-> "{timex(expr)}"')

TimeML = et.Element('TimeML')
TEXT = et.Element('TEXT')
TimeML.append(TEXT)

content = []
for (is_time, expr) in time_expressions:
	content += [timex(expr) if is_time else expr]
	# encoding += timex(expr) if is_time else expr

TEXT.text = ' '.join(content).strip()

f = open(output_file, 'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<!DOCTYPE TimeML>\n')

indent(TimeML)

content = et.tostring(TimeML, encoding = 'UTF-8').decode('utf-8').replace(" /", "/").strip()
content = content.replace('&lt;', '<').replace('&gt;', '>')
f.write(content)

f.close()
print("Done.")
exit(0)

# et.ElementTree(TimeML).write(output_file, encoding = 'UTF-8', xml_declaration = True)

# f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
# # f.write('<!DOCTYPE TimeML SYSTEM "../../dtd/ISO-TimeML-Ro.dtd">')
# f.write('<!DOCTYPE TimeML>\n')
# f.write('<TimeML>\n')
# # add <DATE_TIME>
# f.write('<TEXT>\n')

# f.write('</TEXT>\n')
# f.write('</TimeML>')