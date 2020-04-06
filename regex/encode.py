import re
from redefs import defs, timex

# <TIMEX3
# 	tid="<integer>t"
#	type="DATE"|"TIME"|"DURATION"
#	! value=CDATA
# >
# 
# </TIMEX3>

if __name__ == "__main__":
	from sys import argv 
	if len(argv) != 2:
		print("> Invalid number of arguments givens")
		exit(1)
	file_path = argv[1]
	input_text = ""
	try:
		with open(file_path, "r") as f:
			input_text = f.read()
	except Exception as e:
		print(f'> {e.args[1]} "{file_path}"')
		exit(1)

	total, found = input_text.count("\n") + 1, 0
	txt1, txt2 = input_text, input_text

	done = False
	while not done:
		txt1 = txt2
		for def_, type_ in defs.items():
			match = re.search(def_, txt2, flags = re.I)
			if (match != None):
				print(timex(match.group(0), type_))
				txt2 = txt2[:match.start()] + txt2[match.end():]
				found += 1

		if txt1 == txt2:
			done = True
	
	print(f'found {found}/{total}')
	# print(txt2)