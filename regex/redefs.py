import re

# definitions

număr_arab = r"([1-9]?[0-9]{0,100}[0-9])"

cifră_română = r"(unu|una|un|doi|două|trei|patru|cinci|șase|șapte|opt|nouă)"
română_11_19 = r"(unsprezece|doisprezece|treisprezece|paisprezece|cincisprezece|șaisprezece|șaptesprezece|optsprezece|nouăsprezece)"
română_zeci = f"({cifră_română}|zece|{română_11_19}|(două|{cifră_română}) zeci( şi {cifră_română})?)"
num_română = f"({română_zeci})"

număr = f"({număr_arab}|{num_română})"

num_roman = r"(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))"

zi = "((0?[1-9])|([12][0-9])|(3[01]))"
lună = "((0?[1-9])|(1[0-2]))"
eră = r"(((î|d|a)\.?(Hr|Chr)\.)|î.e.n.|î.e.c|a.e.n.|e.n.)"
an = r"(([1-9]?[0-9]{0,2}[0-9])|([1-9][0-9]'))"
secol = f"((secolul ((al {num_roman}-lea)|{num_roman}))|(secolele {num_roman} și {num_roman})|(secol {num_roman}( și {num_roman})?))"

an_plus = f"(({an} (sau|\/) {an})|({an}(-|\/|, ){an})|({an}))"

unități_măsură=r"(secunda|secundă|secundelor|secundele|secunde|minutelor|minutele|minute|minut|ora|oră|orele|orelor|ore|zilele|zilelor|zile|zi|săptămâna|săptămânilor|saptămânile|săptămâni|săptămână|luna|lunile|lunilor|luni|lună|anilor|ani|anului|anul|veacuri|veacul|veac|secolul|mileniul|mileniile|milenii|mileuniu)"

prep = r"(din|în|circa( o|un)?|de la|la|câteva|până|o dată pe|al|de|din acea)"
prep_perioadă= r"(până (în|la)|de mai bine de (o|un)|timp de|în timpul|pe timpul|în epoca|ca\.)"
cuvinte_legatura=r"(lui|la|pe|de)"

timp_al_zilei = f"(dimineața|dimineață|amiaza|amiază|după-amiaza|după-amiază|seara|seară|noaptea|noapte|zi|ziua)"
cuvinte_cheie=r"(timp|timpului|azi|astăzi|mâine|ieri|începutul|început|anterior|curent|viitor|viitoare|viitorul|sfârșit|sfârșitul|prima|primul|ultimul|ultima|trecut|trecută|prezent|prezentă|acum|semstru|trimestru|perioada|perioadă|durata|durată|vreme|vremea)"

perioadă_expresie = r"(antichitate|evul mediu|zilele noastre|anul|deceniu|epocă)"
#perioadă = f"(((o|un) (zi|săptămână|lună|an|deceniu|secol))|(({număr}|{prep}) (zile|săptămâni|luni|ani|decenii|secol)(le|lor)? (noastre)?))"

lunile_anului=r"(ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie)"

anotimpuri=r"(primăvara|primavară|primăveri|vară|vara|verii|tomnă|tomana|toamne|iarna|iarnă|ierni)"
expr_anotimpuri=f"({prep} {anotimpuri} ({unități_măsură}|{cuvinte_cheie}) {an})|({prep_perioadă} {anotimpuri})|({anotimpuri})"

dată_celendaristică=f"(({zi}(\.|\/| )({lună}|{lunile_anului})(\.|\/| ){an})|({zi}(\.|\/| )({lună}|{lunile_anului}))|(({lună}|{lunile_anului})(\.|\/| ){an}))"
dată = f"((({prep} )?{dată_celendaristică})|(({prep}|{prep_perioadă}) ({an}|{secol})( {eră}| {unități_măsură})?)|((({prep} |{prep_perioadă} )?({an}|{secol}) ({eră}|{unități_măsură}))))"
dată_istorică = f"({prep} {perioadă_expresie}( {an})?)"
perioadă_istorică = f"(({prep_perioadă} {perioadă_expresie})|(({prep}|{prep_perioadă}) {an}(-|, ){an}( {eră}|{lunile_anului})?)|({an}(-|\/){an})( {lunile_anului})?)"

intervale = f"(din {an} până în {an})|((în perioada )?({dată_celendaristică}|{zi}|{lună}|{an})( {lunile_anului})?( - |-|\/)({dată_celendaristică}|{zi}|{lună}|{an})( {lunile_anului})?)"

prep_perioadă_cuvânt =f"(({prep_perioadă} {număr} \w+)|({prep_perioadă} (lui|la)? \w+))"

perioadă_litere = f"(({num_română} {unități_măsură}, {num_română} {unități_măsură} și {num_română} {unități_măsură})|({num_română} {unități_măsură} și {num_română} {unități_măsură})|({num_română} {unități_măsură}( și \w+)?))"
unități_temporale=f"(({număr} |{num_română} )?({prep_perioadă} ({număr} |{num_română} )?{unități_măsură})|({număr} |{num_română} )?({prep} ({număr} |{num_română} )?{unități_măsură})|(({număr}|{num_română}) ({unități_măsură}|{cuvinte_cheie}|{timp_al_zilei})))"
unități_temporale2=f"(({cuvinte_cheie} ({cuvinte_legatura} )?({unități_măsură}|{lunile_anului}|{anotimpuri}))|({prep} {cuvinte_cheie}))"

cazuri_particulare=f"(un an și jumătate|în primăvara anului {an})"

#========

_INTEX = 0
_DATE = "DATE"
_TIME = "TIME"
_DURATION = "DURATION"

defs = {
	perioadă_istorică: _DURATION,
	#perioadă: _DURATION,
	intervale: _TIME,
	dată: _DATE,
	dată_istorică: _DATE,
	expr_anotimpuri: _TIME,
	prep_perioadă_cuvânt: _TIME,
	perioadă_litere: _TIME,
	unități_temporale: _TIME,
	unități_temporale2: _TIME,
	an_plus: _TIME,
	cazuri_particulare: _TEST
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

	result = txt2
	for (_, t) in timexs:
		_INTEX += 1
		t.i = _INTEX
		result = re.sub('(█+)', str(t), result, 1)

	acc = txt2.replace(' ', '')
	return (result, acc.count('█'), len(acc))
