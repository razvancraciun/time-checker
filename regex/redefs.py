import re

# definitions

număr_arab = r"([1-9]?[0-9]{0,100}[0-9])"

cifră_română = r"(unu|doi|trei|patru|cinci|şase|şapte|opt|nouă)"
română_11_19 = r"(unsprezece|doisprezece|treisprezece|paisprezece|cincisprezece|șaisprezece|șaptesprezece|optsprezece|nouăsprezece)"
română_zeci = f"({cifră_română}|zece|{română_11_19}|(două|{cifră_română}) zeci( şi {cifră_română})?)"
num_română = f"({română_zeci})"

număr = f"({număr_arab}|{num_română})"

num_roman = r"(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))"

zi = "((0?[1-9])|([12][0-9])|(3[01]))"
lună = "((0?[1-9])|(1[0-2]))"
eră = r"(((î|d|a)\.?(Hr|Chr)\.)|î.e.n.|î.e.c|a.e.n.|e.n.)"
an = r"(([1-9]?[0-9]{0,2}[0-9])|([1-9][0-9]'))"
secol = f"secolul ((al {num_roman}-lea)|{num_roman})"

unități_măsură=r"(secunda|secundă|secunde|secundele|secundelor|minut|minute|minutele|minutelor|ora|oră|ore|orele|orelor|zi|zile|zilele|zilelor|săptămâna|săptămâni|săptămână|saptămânile|săptămânilor|luna|luni|lună|lunile|lunilor|ani|anul|anilor|veac|secol|veacuri|secole|secolul|secolele|veacul|miluniu|mileniul|milenii|mileniile)"

prep = r"(din|în|circa o?|de la|la|câteva|până|o dată pe)"
prep_perioadă= r"(până (în|la)|de mai bine de (o|un)|timp de|în timpul|pe timpul|în epoca)"
cuvinte_legatura=r"(lui|la|pe|de)"

cuvinte_cheie=r"(timp|timpului|azi|astăzi|mâine|ieri|începutul|început|anterior|curent|viitor|viitoare|viitorul|sfârșit|sfârșitul|ultimul|ultima|trecut|trecută|prezent|prezentă|acum|semstru|trimestru|perioada|perioadă|durata|durată|vreme|vremea)"

perioadă_expresie = r"(antichitate|evul mediu|zilele noastre|an|deceniu|secol)"
perioadă = f"(((o|un) (zi|săptămână|lună|an|deceniu|secol))|(({număr}|{prep}) (zile|săptămâni|luni|ani|decenii|secole)(le|lor)? (noastre)?))"

lunile_anului=r"(ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie)"

anotimpuri=r"(primăvara|primavară|primăveri|vară|vara|veri|tomnă|tomana|toamne|iarna|iarnă|ierni)"
expr_anotimpuri=f"({prep_perioadă} {anotimpuri})"

dată = f"({prep} )?({an}|{secol})( {eră})?"
dată_istorică = f"{prep} {perioadă_expresie}"
perioadă_istorică = f"(({prep_perioadă} ({perioadă_expresie}|{perioadă}))|({prep} {secol}))"

prep_perioadă_cuvânt =f"(({prep_perioadă} {număr} \w+)|({prep_perioadă} (lui|la)? \w+))"

unități_temporale=f"(({prep} ({număr} )?{unități_măsură})|({prep_perioadă} ({număr} )?{unități_măsură}))"
unități_temporale2=f"(({cuvinte_cheie} ({cuvinte_legatura} )?({unități_măsură}|{perioadă}|{lunile_anului}|{anotimpuri}))|({prep} {cuvinte_cheie}))"

#========

_INTEX = 0
_DATE = "DATE"
_TIME = "TIME"
_DURATION = "DURATION"

defs = {
	perioadă_istorică: _DURATION,
	perioadă: _DURATION,
	dată_istorică: _DATE,
	dată: _DATE,
	expr_anotimpuri: _TIME,
	anotimpuri: _TIME,
	prep_perioadă_cuvânt: _TIME,
	unități_temporale: _TIME,
	unități_temporale2: _TIME,
	#lunile_anului: _TIME,
}

class Timex:
	def __init__(self, i: int, t: str, c: str):
		self.i = i
		self.t = t
		self.c = c

	def __str__(self):
		return f'<TIMEX3 tid="t{self.i}" type="{self.t}">{self.c}</TIMEX3>'

def timex(text: str):
	global _INTEX

	timexs = []
	
	txt1, txt2 = text, text
	diff = 0
	while True:
		txt1 = txt2
		for definition, deftype in defs.items():
			match = re.search(definition, txt2, flags = re.I)
			if (match != None):
				timexs += [(match.start(), Timex(-1, deftype, match.group(0)))]
				txt2 = (txt2[:match.start()] + '█' * (match.end() - match.start()) + txt2[match.end():])

		if txt1 == txt2:
			break
	
	timexs = list(sorted(timexs, key = lambda el: el[0]))

	acc = txt2.replace(' ', '')
	result = txt2
	for (_, t) in timexs:
		_INTEX += 1
		t.i = _INTEX
		result = re.sub('(█+)', str(t), result, 1)

	return (result, acc.count('█'), len(acc))