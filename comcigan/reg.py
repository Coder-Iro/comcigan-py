import re

routereg: re.Pattern = re.compile(r'\./\d{6}\?\d{5}l')
prefixreg: re.Pattern = re.compile(r"'\d+_'")
orgdatareg: re.Pattern = re.compile(r'원자료=자료\.자료\d+')
daydatareg: re.Pattern = re.compile(r'일일자료=자료\.자료\d+')
thnamereg: re.Pattern = re.compile(r'성명=자료\.자료\d+')
sbnamereg: re.Pattern = re.compile(r'자료.자료\d+\[sb\]')


def regsearch(reg: re.Pattern, org: str) -> str:
    return reg.search(org).group(0)


def extractint(org: str) -> int:
    return int("".join([x for x in org if x.isdigit()]))
