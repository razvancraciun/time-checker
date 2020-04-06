_INTEX = 0
DATE = "DATE"
TIME = "TIME"
DURATION = "DURATION"

an = r"([1-9]?[1-9]?[1-9]?[0-9])|([1-9][0-9]')"

defs = [an]

types = {
	an: DATE
}

def timex(content, type):
	global _INTEX
	_INTEX += 1
	return f'<TIMEX3 tid="t{_INTEX}" type="{type}">{content}</TIMEX3>'