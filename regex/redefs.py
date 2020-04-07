_INTEX = 0
_DATE = "DATE"
_TIME = "TIME"
_DURATION = "DURATION"

num_roman = r"(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))"

eră = r"(((î|d|a)\. ?(Hr|Chr)\.)|î.e.n.|î.e.c|a.e.n.|e.n.)"
an = r"(([1-9]?[1-9]?[1-9]?[0-9])|([1-9][0-9]'))"
secol = f"secolul ((al {num_roman}-lea)|{num_roman})"

prep = r"(din|în|circa)"

dată = f"({prep} )?({an}|{secol})( {eră})?"

#-------

defs = {
	dată: _DATE
}

def timex(content, type):
	global _INTEX
	_INTEX += 1
	return f'type={type}\t "{content}"'
	# return f'<TIMEX3 tid="t{_INTEX}" type="{type}">{content}</TIMEX3>'