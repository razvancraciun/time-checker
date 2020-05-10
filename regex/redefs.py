import re

# definitions

număr_arab = r"([1-9]?[0-9]{0,100}[0-9])"

cifră_română = r"(unu|una|prima|un|doi|două|doua|treia|trei|patru|patra|cinci|cincea|șasea|șase|șaptea|șapte|opta|opt|nouă|noua)"
română_11_19 = r"(unsprezece|doisprezece|treisprezece|paisprezece|cincisprezece|șaisprezece|șaptesprezece|optsprezece|nouăsprezece)"
română_zeci = f"({cifră_română}|zece|{română_11_19}|(două|{cifră_română}) zeci( şi {cifră_română})?)"
num_română = f"({română_zeci})"

număr = f"({număr_arab}|{num_română})"

num_roman = r"(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))"

zi = "((0?[1-9])|([12][0-9])|(3[01]))"
lună = "((0?[1-9])|(1[0-2]))"
eră = r"(((î|d|a)\.?(Hr|Chr)\.)|î.e.n.|î.e.c|a.e.n.|e.n.)"
an = r"(([1-9]?[0-9]{0,2}[0-9])|([1-9][0-9]'))"
secol = f"((secolul(ui)? ((al {num_roman}-lea)|{num_roman})( {eră})?)|(secolele (al )?{num_roman}(-lea)? și (al )?{num_roman}(-lea)?( {eră})?)|(secol {num_roman}( și {num_roman})?)|(sec(.)? {num_roman}( {eră})?))"

an_plus = f"(({an} (sau|\/) {an})|({an}(-|\/|, ){an})|({an}))"

unități_măsură=r"(secunda|secundă|secundelor|secundele|secunde|minutelor|minutele|minute|minut|ora|oră|orele|orelor|ore|zilele|zilelor|zile|zi|săptămâna|săptămânilor|saptămânile|săptămâni|săptămână|luna|lunile|lunilor|lunii|luni|lună|anilor|anual|anii|ani|anului|anul|an|deceniile|decenii|deceniu|veacuri|veacul|veac|secolul|mileniul|mileniile|milenii|mileuniu)"

prep = r"(încă|în|circa( o|un)?|un|de la|la|câteva|până la|până|o dată pe|al|de|din acea|acea|din|toată|tot)"
prep_perioadă= r"(până (în|la)|de mai bine de (o|un)|timp de|vreme de|în timpul|pe timpul|în epoca|epoca|ca\.|o parte a|restul|în fiecare|într-o)"
cuvinte_legatura=r"(lui|la|pe|de)"

timp_al_zilei = f"(dimineața|dimineață|amiaza|amiază|după-amiaza|după-amiază|după amiaza|după amiază|seara|seară|noaptea|noapte|zi|ziua|miezul nopții)"
cuvinte_cheie=r"(timp|timpului|azi|astăzi|mâine|ieri|începutul|început|anteriori|anterior|curent|viitor|viitoare|viitorul|sfârșitul|sfârșit|prima|primul|ultimul|ultima|ultimele|trecut|trecută|înainte|prezent|prezentă|acum|semestru|trimestru|perioada|perioadă|durata|durată|vreme|vremea|vremurile|vremuri)"

perioadă_expresie = r"(antichitate|evul mediu|zilele noastre|anului|anul|deceniu|epocă)"
#perioadă = f"(((o|un) (zi|săptămână|lună|an|deceniu|secol))|(({număr}|{prep}) (zile|săptămâni|luni|ani|decenii|secol)(le|lor)? (noastre)?))"

lunile_anului=r"(ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie)"

zilele_săptămânii=r"(luni|lunea|marția|marți|miercurea|miercuri|joia|joi|vineri|vinerea|sâmbătă|sâmbăta|duminică|duminica)"

anotimpuri=r"(primăvara|primavară|primăveri|vară|vara|verii|tomnă|tomana|toamne|iarna|iarnă|ierni)"
expr_anotimpuri=f"({prep} {anotimpuri} ({unități_măsură}|{cuvinte_cheie}) {an})|({prep_perioadă} {anotimpuri})|({anotimpuri})"

dată_celendaristică=f"(({zi}(\.|\/| )({lună}|{lunile_anului})(\.|\/| ){an})|({zi}(\.|\/| )({lună}|{lunile_anului}))|(({lună}|{lunile_anului})(\.|\/| ){an}))"
dată = f"((({prep} )?{dată_celendaristică})|(({prep}|{prep_perioadă}) ({an}|{secol}|{anotimpuri}|({lunile_anului} și {lunile_anului})|{lunile_anului})( {eră}| {unități_măsură})?)|((({prep} |{prep_perioadă} )?({an}|{secol}) ({eră}|{unități_măsură})))|(({prep} )?{cuvinte_cheie} {secol})|({secol}))"
dată_istorică = f"({prep} {perioadă_expresie}( {an})?)"
perioadă_istorică = f"(({prep_perioadă} {perioadă_expresie})|(({prep}|{prep_perioadă}) {an}(-|, ){an}( {eră}|{lunile_anului})?)|({an}(-|\/){an}( {unități_măsură}|( și {an}(-|\/){an}))?)( {lunile_anului} ({an})?)?)"

intervale = f"((din {an} până în {an})|((în perioada )?({dată_celendaristică}|{zi}|{lună}|{an})( {lunile_anului})?( - |-|\/)({dată_celendaristică}|{zi}|{lună}|{an})( {lunile_anului})?)|({prep} )?{unități_măsură} {unități_măsură})"

prep_perioadă_cuvânt =f"(({prep_perioadă} {număr} \w+)|({prep_perioadă} (lui|la)? \w+))"

perioadă_litere = f"(({num_română} {unități_măsură}, {num_română} {unități_măsură} și {num_română} {unități_măsură})|({num_română} {unități_măsură} și {num_română} {unități_măsură})|((( )?a )?{num_română} {unități_măsură}( și \w+)?))"
unități_temporale=f"(({număr} |{num_română} )?({prep_perioadă} ({număr} |{num_română} )?{unități_măsură})|({număr} |{num_română} )?({prep} ({număr} |{num_română} )?{unități_măsură}( {dată_celendaristică}| {an})?)|(({număr}|{num_română}) ({unități_măsură}|{cuvinte_cheie}|{timp_al_zilei})))"
unități_temporale2=f"(({cuvinte_cheie} ({cuvinte_legatura} )?({unități_măsură}|{lunile_anului}|{anotimpuri}))|({prep} {cuvinte_cheie}( {unități_măsură} {an}| {unități_măsură})?)|({prep} {prep_perioadă} \w+)|({unități_măsură} {lunile_anului})|((a|{prep}) {num_română} {unități_măsură})|({prep} {timp_al_zilei})|(({prep}|{prep_perioadă}|{prep} {prep_perioadă}) {zilele_săptămânii}))"

cazuri_particulare=f"(în această perioadă|în aceeași zi|după moartea artistului|În ultimii săi ani de viață|Vreme de mulți ani|din tinerețe|timp de aproape o jumătate de mileniu|către sfârșitul vieții|de-a lungul perioadei preistorice|în ultimele decenii ale secolului al-{num_roman}-lea)|în scurt timp|la scurt timp după|după intrarea României în cel de-al doilea război balcanic|între timp|din acele zile|în cel de-al treilea an|mai târziu|în acest timp|de-a lungul timpului|paleoliticului|paleolitic|de-a lungul istoriei|în Egiptul antic|în primele luni de viață|din primele zile de viață|cel de-al Doilea Război Mondial|Primul(ui)? Razboi Mondial|vreme de război|în jurul anului {an}|astăzi|în fiecare zi|în urmă cu {an} de mii de ani"


#========

_INTEX = 0
_DATE = "DATE"
_TIME = "TIME"
_DURATION = "DURATION"

defs = {
	perioadă_istorică: _DURATION,
	#perioadă: _DURATION,
	intervale: _TIME,
	dată_istorică: _DATE,
	expr_anotimpuri: _TIME,
	prep_perioadă_cuvânt: _TIME,
	perioadă_litere: _TIME,
	unități_temporale: _TIME,
	unități_temporale2: _TIME,
	dată: _DATE,
	an_plus: _TIME,
	cazuri_particulare: _TIME,
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
