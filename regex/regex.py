import re

class Res:
	pass

res = Res()

def redef(name, content):
	global res
	setattr(res, name, f"(?P<{name}>{content})")

redef("c_ore_nr", r"0?[1-9]|1[0-9]|2[0-3]")
redef("c_minute_nr", r"0?[1-9]|[1-5][0-9]")
redef("c_secunde_nr", r"0?[1-9]|[1-5][0-9]")
redef("oră_nr", f"{res.c_ore_nr}:{res.c_minute_nr}:{res.c_secunde_nr}")
redef("c_expresie_temporală", f"{res.oră_nr}")

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

	res = re.search(res.c_expresie_temporală, input_text, flags = re.I).groupdict()
	res = {k : v for k, v in res.items() if k[0:2] != "c_"}
	print(res)