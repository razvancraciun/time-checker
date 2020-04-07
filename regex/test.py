from sys import argv
from encode import extract_timex

if __name__ == "__main__":
	debug = False
	if len(argv) == 2 and argv[1] == "d":
		debug = True

	total, found = 0, 0

	for ii in range(1, 5):
		with open(f"./ml/data/raw/ctimes_art{ii}.txt", "r") as f:
			input_text = f.read().strip()
			timexs = extract_timex(input_text)

			ctotal = len(input_text.split("\n")) + 1
			cfount = len(timexs)
			total += ctotal
			found += cfount
			if debug:
				print(f"ctimes_art{ii}.txt:")
				for timex in timexs:
					print(timex)
				print(f"{cfount}/{ctotal}")

	print("%.2f" % (found / total * 100) + "% matched")