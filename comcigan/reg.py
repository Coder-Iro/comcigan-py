import re

routereg: re.Pattern = re.compile(r'\./\d{6}\?\d{5}l')
prefixreg: re.Pattern = re.compile(r"'\d{5,6}_'")
orgdatareg: re.Pattern = re.compile(r'원자료=자료\.자료\d{3}')
daydatareg: re.Pattern = re.compile(r'일일자료=자료\.자료\d{3}')
thnamereg: re.Pattern = re.compile(r'성명=자료\.자료\d{3}')


def regsearch(reg: re.Pattern, org: str) -> str:
    return reg.search(org).group(0)
