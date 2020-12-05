from re import compile as rcompile, Pattern

routereg = rcompile(r'\./\d{6}\?\d{6}l')
prefixreg = rcompile(r"'\d+_'")
orgdatareg = rcompile(r'원자료=자료\.자료\d+')
daydatareg = rcompile(r'일일자료=자료\.자료\d+')
thnamereg = rcompile(r'성명=자료\.자료\d+')
sbnamereg = rcompile(r'자료.자료\d+\[sb\]')


def regsearch(reg: Pattern, org: str) -> str:
    return reg.search(org).group(0)


def extractint(org: str) -> int:
    return int("".join([x for x in org if x.isdigit()]))
