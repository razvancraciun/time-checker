_INTEX = 0
_DATE = "DATE"
_TIME = "TIME"
_DURATION = "DURATION"

număr_arab = r"([1-9]?[0-9]{0,100}[0-9])"

cifră_română = r"(unu|doi|trei|patru|cinci|şase|şapte|opt|nouă)"
română_11_19 = r"(unsprezece|doisprezece|treisprezece|paisprezece|cincisprezece|șaisprezece|șaptesprezece|optsprezece|nouăsprezece)"
română_zeci = f"({cifră_română}|zece|{română_11_19}|(două|{cifră_română}) zeci( şi {cifră_română})?)"
num_română = f"({română_zeci})"

număr = f"({număr_arab}|{num_română})"

num_roman = r"(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))"

zi = "((0?[1-9])|([12][0-9])|(3[01]))"
lună = "((0?[1-9])|(1[0-2]))"
eră = r"(((î|d|a)\. ?(Hr|Chr)\.)|î.e.n.|î.e.c|a.e.n.|e.n.)"
an = r"(([1-9]?[0-9]{0,2}[0-9])|([1-9][0-9]'))"
secol = f"secolul ((al {num_roman}-lea)|{num_roman})"

prep = r"(din|în|circa|de la)"
prep_perioadă= r"(până (în|la)|de mai bine de (o|un)|timp de)"

perioadă_expresie = r"(antichitate|evul mediu|zilele noastre|an|deceniu|secol)"
perioadă = f"(((o|un) (zi|săptămână|lună|an|deceniu|secol))|({număr} (zile|săptămâni|luni|ani|decenii|secole)))"

anotimp=r"(ianuarie|fabruarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie)"

dată = f"({prep} )?({an}|{secol})( {eră})?"
dată_istorică = f"{prep} {perioadă_expresie}"
perioadă_istorică = f"{prep_perioadă} ({perioadă_expresie}|{perioadă})"

#-------

defs = {
	perioadă: _DURATION,
	perioadă_istorică: _DURATION,
	dată_istorică: _DATE,
	dată: _DATE,
}

def timex(content, type):
	global _INTEX
	_INTEX += 1
	return f'type={type}\t "{content}"'
	# return f'<TIMEX3 tid="t{_INTEX}" type="{type}">{content}</TIMEX3>'