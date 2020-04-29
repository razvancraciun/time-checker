from sys import argv
from redefs import timex

if __name__ == "__main__":
	text = ''
	with open(argv[1], 'r') as f:
		text = f.read()

	total, found = 0, 0

	exprs = [expr.strip() for expr in text.split('\n')]
	for expr in exprs:
		t = timex(expr)
		print(f'"{expr}"\t-> "{t[0]}"')

		found += t[1]
		total += t[2]

	print('\n' + '%.2f' % (found / total * 100) + '% accuracy')