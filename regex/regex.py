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

def reor(*args):
	return f"({'|'.join(args)})"

redef("c_ore_nr", r"0?[1-9]|1[0-9]|2[0-3]")
redef("c_minute_nr", r"[1-5][0-9]|0?[1-9]")
redef("c_secunde_nr", res.minute_nr)
redef("oră_completă_nr", f"{res.ore_nr}:{res.minute_nr}:{res.secunde_nr}")
redef("oră_simplă_nr", f"{res.ore_nr}:{res.minute_nr}")

redef("c_luni_txt", r"ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie|Ianuarie|Februarie|Martie|Aprilie|Mai|Iunie|Iulie|August|Septembrie|Octombrie|Noiembrie|Decembrie|ian|feb|mar|apr|mai|iun|iul|aug|sep|oct|dec")
redef("c_luni_nr", r"10|11|12|0?[1-9]")
redef("c_ani", r"\d{4}|\d{2}'?")  #1990 / 90'
redef("c_zile_calendar", r"[1-2][0-9]|3[0-1]|0?[1-9]")

redef("c_interval_ani", f"{res.ani}-{res.ani}")


redef("dată_calendaristică", f"{res.zile_calendar}" + r"(\/|\.)" + f"({res.luni_txt}|{res.luni_nr})" + r"(\/|\.)" + f"{res.ani}")
redef("interval_ani_simplu", res.interval_ani)
redef("dată_zi_lună", f"{res.zile_calendar}(\/|\.)({res.luni_txt}|{res.luni_nr})")

redef("c_zilele_săptămânii", r"luni|Luni|marți|Marți|miercuri|Miercuri|joi|Joi|vineri|Vineri|sâmbătă|Sâmbătă|duminică|Duminică")
redef("c_zilele_săptămânii_articulate", r"lunea|Lunea|marția|Marția|miercurea|Miercurea|joia|Joia|vinerea|Vinerea|sâmbăta|Sâmbăta|duminica|Duminica")

redef("c_numerale_ordinale", r"primul|prima|întâia|al ([2-9]|[1-9][0-9])-lea|al doilea|a ([2-9]|[1-9][0-9])-a|a doua|al treilea|a treia|al patrulea|a patra|al cincilea|a cincea|al șaselea|a șasea|al șaptelea|a șaptea|al optulea|a opta|al nouălea|a noua|al zecelea|a zecea")
redef("c_numere_txt", r"(((două|trei|patru|cinci|șase|șapte|opt|nouă)zeci) și (unu|doi|trei|patru|cinci|șase|șapte|opt|nouă))|((două|trei|patru|cinci|șase|șapte|opt|nouă)zeci)|((un|doi|trei|patru|cinci|șase|șapte|opt|nouă)sprezece)|(unu|una|doi|două|trei|patru|cinci|șase|șapte|opt|nouă|zece)")
#doar 1-99(de rescris_numeralele ordinale cu numere_txt)

redef("c_unități_măsură", r"secunda|secundă|secunde|secundele|secundelor|minut|minute|minutele|minutelor|ora|oră|ore|orele|orelor|zi|zile|zilele|zilelor|săptămâna|săptămâni|săptămână|saptămânile|săptămânilor|luna|luni|lună|lunile|lunilor|ani|anul|anilor|veac|secol|veacuri|secole|secolul|secolele|veacul|miluniu|mileniul|milenii|mileniile")

redef("c_anotimpuri", r"primăvara|primavară|primăveri|vară|vara|veri|tomnă|tomana|toamne|iarna|iarnă|ierni")

redef("c_timp_al_zilei", r"dimineața|dimineață|amiaza|amiază|după-amiaza|după-amiază|seara|seară|noaptea|noapte|zi|ziua")

redef("c_cuvinte_cheie", r"timp|timpului|azi|astăzi|mâine|ieri|începutul|început|anterior|curent|viitor|viitoare|sfârșit|sfârșitul|ultimul|ultima|trecut|trecută|prezent|prezentă|acum|semstru|trimestru|perioada|perioadă|durata|durată|vreme|vremea")
#aceeasi problema ca la geolocatie: evenimet sau timp? ex: Evul mediu, dupa razboi
#8-10 de 2 // 2-4 de trei

redef("interval", r"[1-9][0-9][0-9]" + r"-" + r"[1-9][0-9][0-9]" + f"{res.unități_măsură}")
redef("cheie_zi", f"{res.cuvinte_cheie} {res.timp_al_zilei}")
redef("numar_unitate", f"{res.numerale_ordinale} {res.unități_măsură}")
redef("unitate_numar", f"{res.unități_măsură} {res.numerale_ordinale}")
redef("unitate_numar_txt", f"{res.unități_măsură} {res.numere_txt}")
redef("numar_anotimp", f"{res.numerale_ordinale} {res.anotimpuri}")
redef("unitate_cheie", f"{res.unități_măsură} {res.cuvinte_cheie}")
redef("saptamana_zi", f"{res.zilele_săptămânii} {res.timp_al_zilei}")
redef("saptamana_art_zi", f"{res.zilele_săptămânii_articulate} {res.timp_al_zilei}")
redef("unitate_ani", f"{res.unități_măsură} {res.ani}")
redef("unitate_interval_ani", f"{res.unități_măsură} {res.interval_ani}")
redef("minute_unitate_secunde_unitate", f"{res.minute_nr} {res.unități_măsură} {res.secunde_nr} {res.unități_măsură}")
redef("cheie_unitate_numartxt", f"{res.cuvinte_cheie} {res.unități_măsură} {res.numere_txt}")
redef("cheie_unitate_numar", f"{res.cuvinte_cheie} {res.unități_măsură} {res.numerale_ordinale}")
redef("cheie_unitate_ani", f"{res.cuvinte_cheie} {res.unități_măsură} {res.ani}")

redef("c_expresie_temporală", reor(
	res.oră_completă_nr,
	res.oră_simplă_nr,
	res.dată_calendaristică,
	res.interval_ani_simplu,
	res.dată_zi_lună,
	res.interval,
	res.cheie_zi,
	res.numar_unitate,
	res.unitate_numar,
	res.unitate_numar_txt,
	res.numar_anotimp,
	res.unitate_cheie,
	res.saptamana_zi,
	res.saptamana_art_zi,
	res.unitate_ani,
	res.unitate_interval_ani,
	res.minute_unitate_secunde_unitate,
	res.cheie_unitate_numartxt,
	res.cheie_unitate_numar,
	res.cheie_unitate_ani,
))

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

	txt1 = input_text
	txt2 = input_text

	while True:
		txt1 = txt2
		search = re.search(res.expresie_temporală, txt1, flags = re.I)
		if (search == None):
			exit(0)
		
		result = search.groupdict()
		result = {k : v for k, v in result.items() if v != None}
		
		if (len(result) == 0):
			exit(0)

		for k, v in result.items():
			print(f'{k}: "{v}"')
			txt2 = txt2.replace(v, "")

		if txt1 == txt2:
			break