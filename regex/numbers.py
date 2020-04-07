import urllib.request
import re

def număr_română(nr):
	url = "https://numar-text.calculators.ro/numar-transformat-in-text-scris-cu-litere-cuvinte.php?numar="
	url += str(nr)

	fp = urllib.request.urlopen(url)
	mybytes = fp.read()
	html = mybytes.decode("utf8")
	fp.close()

	return re.search("<h4>(.*?)</h4>", html).groups(1)[0].strip()


if __name__ == "__main__":
	from sys import argv
	from time import sleep
	if len(argv) != 2:
		exit(1)
	
	with open(f"./regex/numbers.txt", "w") as f:
		for ii in range(1, int(argv[1]) + 1):
			f.write(număr_română(ii) + "\n")
			# sleep(0.1)
			
