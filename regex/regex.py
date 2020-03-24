import re

class Res:
	pass

res = Res()

def redef(name, content):
	global res
	if name[0:2] == "c_":
		name = name[2:]
		if (content[0] == "(" and content[-1] == ")"):
			setattr(res, name, f"{content}")
		else:
			setattr(res, name, f"({content})")
	else:
		setattr(res, name, f"(?P<{name}>{content})")

redef("c_ore_nr", r"0?[1-9]|1[0-9]|2[0-3]")
redef("c_minute_nr", r"0?[1-9]|[1-5][0-9]")
redef("c_secunde_nr", res.minute_nr)
redef("oră_nr", f"{res.ore_nr}:{res.minute_nr}:{res.secunde_nr}")
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

	print("computed res:")
	computed_res = {k : v for k, v in res.__dict__.items() if k[0:2] != "__" }
	for k, v in computed_res.items():
		print(f'{k}: "{v}"')

	print("\nmatched res:")
	res = re.search(res.expresie_temporală, input_text, flags = re.I).groupdict()
	for k, v in res.items():
		print(f'{k}: "{v}"')