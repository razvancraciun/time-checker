import re
from redefs import defs, timex

# <TIMEX3
# 	tid="<integer>t"
#	type="DATE"|"TIME"|"DURATION"
#	! value=CDATA
# >
# 
# </TIMEX3>

def extract_timex(text):
	res = []
	txt1, txt2 = text, text

	while True:
		txt1 = txt2
		for def_, type_ in defs.items():
			match = re.search(def_, txt2, flags = re.I)
			if (match != None):
				res += [timex(match.group(0), type_)]
				txt2 = txt2[:match.start()] + txt2[match.end():]

		if txt1 == txt2:
			return res

if __name__ == "__main__":
	from sys import argv 
	if len(argv) != 2:
		print("> Invalid number of arguments givens")
		exit(1)
	file_path = argv[1]
	input_text = ""
	try:
		with open(file_path, "r") as f:
			input_text = f.read().strip()
	except Exception as e:
		print(f'> {e.args[1]} "{file_path}"')
		exit(1)

	total = len(input_text.split("\n"))
	res = extract_timex(input_text)

	for timex in res:
		print(timex)
	print(f"{len(res)}/{total}")