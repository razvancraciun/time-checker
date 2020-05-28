#!/usr/bin/env python3
from sys import argv, stderr
from os import path
import re

if __name__ != '__main__':
	print('Cannot use timechecker as a module')
	exit(1)

if len(argv) < 2:
	print('!> input file path must be given')
	exit(1)

if len(argv) > 3:
	print('!> too many arguments')
	exit(1)

INPUT_FILE = argv[1]
OUTPUT_FILE = f'{path.splitext(INPUT_FILE)[0]}.xml'
DEBUG_FILE = f'{path.splitext(INPUT_FILE)[0]}_debug.txt'
DEBUG = len(argv) == 3

print('Reading input data...')
input_text = ''
with open(INPUT_FILE, 'r') as f:
	input_text = f.read()

print('Instantiating classifier...')
from ml.bayes import BayesClassifier
classifier = BayesClassifier()

print('Running classifier...')
time_expressions = classifier.run_on_text(input_text)

from regexs.redefs import timex
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

debug_info = []

print('Filtering and encoding...')
content = []
for (is_time, expr) in time_expressions:
	if (is_time):
		t = timex(expr)
		content += [t[0]]
		if DEBUG:
			debug_info += [f'"{expr}" -> "{t[0]}"']
	else:
		content += [expr]

if DEBUG:
	print('Generating debug info...')
	with open(DEBUG_FILE, 'w+') as f:
		f.write('\n'.join(debug_info))

print('Generating output...')
TimeML = et.Element('TimeML')
TEXT = et.Element('TEXT')
TimeML.append(TEXT)
aux = ' '.join(content).strip()
aux = re.sub(r'„ ', '„', re.sub(r'\( ', '(', re.sub(r'\- ', '-', re.sub(r'[ ]+', ' ', aux))))
TEXT.text = aux

f = open(OUTPUT_FILE, 'w+')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<!DOCTYPE TimeML>\n')
indent(TimeML)
content = et.tostring(TimeML, encoding = 'UTF-8').decode('utf-8').replace(" /", "/").strip()
content = content.replace('&lt;', '<').replace('&gt;', '>')
f.write(content)
f.close()

print(f'Done.')
exit(0)