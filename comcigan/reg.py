import re

routereg = re.compile(r"\./\d+\?\d+l")
prefixreg = re.compile(r"'\d+_'")
orgdatareg = re.compile(r"원자료=Q자료\(자료\.자료\d+")
daydatareg = re.compile(r"일일자료=Q자료\(자료\.자료\d+")
thnamereg = re.compile(r"성명=자료\.자료\d+")
sbnamereg = re.compile(r"자료.자료\d+\[sb\]")


def regsearch(reg, org: str) -> str:
    return reg.search(org).group(0)


def extractint(org: str) -> int:
    return int("".join([x for x in org if x.isdigit()]))
