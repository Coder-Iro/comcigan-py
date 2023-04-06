from base64 import b64encode
from json import loads
from typing import List, Tuple

from bs4 import BeautifulSoup
from requests import get

from .reg import (
    daydatareg,
    extractint,
    orgdatareg,
    prefixreg,
    regsearch,
    routereg,
    sbnamereg,
    thnamereg,
)


def trim(lis):
    while lis and not lis[-1]:
        del lis[-1]
    return lis


URL = "http://112.186.226.178:4082"

comci_resp = get(f"{URL}/st")
comci_resp.encoding = "EUC-KR"

comcigan_html = BeautifulSoup(comci_resp.text, "lxml")
script = comcigan_html.find_all("script")[1].contents[0]

route = regsearch(routereg, script)
PREFIX = regsearch(prefixreg, script)[1:-1]

orgnum = extractint(regsearch(orgdatareg, script))
daynum = extractint(regsearch(daydatareg, script))
thnum = extractint(regsearch(thnamereg, script))
sbnum = extractint(regsearch(sbnamereg, script))

BASEURL = f"{URL}{route[1:8]}"
SEARCHURL = f"{BASEURL}{route[8:]}"


class School:
    __slots__ = ("name", "sccode", "region", "_timeurl", "_week_data", "CONSTS")

    name: str
    sccode: int
    _timeurl: str
    _week_data: List[List[List[List[Tuple[str, str, str]]]]]

    def __init__(self, name: str):
        sc_search = get(
            SEARCHURL
            + "%".join(
                str(name.encode("EUC-KR"))
                .upper()[2:-1]
                .replace("\\X", "\\")
                .split("\\")
            )
        )
        sc_search.encoding = "UTF-8"
        sc_list = loads(sc_search.text.replace("\0", ""))["학교검색"]

        if len(sc_list) == 1:
            self.region = sc_list[0][1]
            self.name = sc_list[0][2]
            self.sccode = sc_list[0][3]
        elif len(sc_list) > 1:
            raise ValueError("More than one school is searched by the name passed.")
        else:
            raise NameError("No schools have been searched by the name passed.")

        self._timeurl = f"{BASEURL}?" + b64encode(
            f"{PREFIX}{str(self.sccode)}_0_1".encode("UTF-8")
        ).decode("UTF-8")
        self._week_data = [[[[("", "", "")]]]]
        self.refresh()

    def refresh(self):
        time_res = get(self._timeurl)
        time_res.encoding = "UTF-8"
        rawtimetable = loads(time_res.text.replace("\0", ""))

        subjects: list = rawtimetable[f"자료{sbnum}"]
        long_subjects: list = rawtimetable[f"자료{sbnum}"]
        teachers: list = rawtimetable[f"자료{thnum}"]

        for i in rawtimetable[f"자료{daynum}"][1:]:
            i[0] = [i[0]]
        self._week_data = [
            [
                [
                    [
                        (
                            subjects[int(str(x)[-2:])],
                            long_subjects[int(str(x)[-2:])],
                            ""
                            if int(str(x)[:-2]) >= len(teachers)
                            else teachers[int(str(x)[:-2])],
                        )
                        for x in filter(lambda x: str(x)[:-2], trim(oneday[1:]))
                    ]
                    for oneday in oneclass[1:6]
                ]
                for oneclass in onegrade
            ]
            for onegrade in rawtimetable[f"자료{daynum}"][1:]
        ]

    def __getitem__(self, item: int) -> List:
        return self._week_data[item - 1]

    def __repr__(self) -> str:
        return f"School('{self.name}')"

    def __str__(self) -> str:
        return str(self._week_data)

    def __iter__(self):
        return iter(self._week_data)
