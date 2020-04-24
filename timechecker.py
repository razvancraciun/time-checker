#!/usr/bin/env python3
import sys

def errprint(*args, **kwargs):
	print(*args, file = sys.stderr, **kwargs)

if __name__ != "__main__":
	errprint("Cannot use timechecker as a module")
	sys.exit()

if len(sys.argv) < 3:
	errprint("> 2 argumets must be given: input file path and output file path")
	sys.exit()

print("Reading input data...")
input_text = ""
with open(sys.argv[1], "r") as f:
    input_text = f.read()

print("Instantiating classifier...")
from ml.bayes import BayesClassifier
classifier = BayesClassifier()

print("Running classifier...")
time_expressions = classifier.run_on_text(input_text)

print("Generating output...")
with open(sys.argv[2], "w") as f:
	for (stat, expr) in time_expressions:
		s = "T" if stat else "F"
		f.write(f"{s}: {expr.strip()}\n")

print("Done.")