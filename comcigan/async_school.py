from base64 import b64encode
from json import loads
from typing import List, Tuple

from aiohttp import ClientSession
from bs4 import BeautifulSoup

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


async def AsyncRequest(url: str, encoding: str | None = None):
    async with ClientSession() as sess:
        async with sess.get(url) as res:
            return await res.text(encoding)


def trim(lis):
    while lis and not lis[-1]:
        del lis[-1]
    return lis


URL = "http://112.186.226.178:4082"


class CONSTANT:
    __slots__ = ("PREFIX", "orgnum", "daynum", "thnum", "sbnum", "BASEURL", "SEARCHURL")

    async def refresh(self):
        comci_resp = await AsyncRequest(f"{URL}/st")

        comcigan_html = BeautifulSoup(comci_resp, "lxml")
        script = comcigan_html.find_all("script")[1].contents[0]

        route = regsearch(routereg, script)
        self.PREFIX = regsearch(prefixreg, script)[1:-1]

        self.orgnum = extractint(regsearch(orgdatareg, script))
        self.daynum = extractint(regsearch(daydatareg, script))
        self.thnum = extractint(regsearch(thnamereg, script))
        self.sbnum = extractint(regsearch(sbnamereg, script))

        self.BASEURL = f"{URL}{route[1:8]}"
        self.SEARCHURL = f"{self.BASEURL}{route[8:]}"


class AsyncSchool:
    __slots__ = ("name", "sccode", "region", "_timeurl", "_week_data", "CONSTS")

    name: str
    sccode: int
    _timeurl: str
    _week_data: List[List[List[List[Tuple[str, str, str]]]]]

    @classmethod
    async def init(cls, name: str):
        res = cls()

        CONSTS = CONSTANT()
        await CONSTS.refresh()

        PREFIX = CONSTS.PREFIX
        BASEURL = CONSTS.BASEURL
        SEARCHURL = CONSTS.SEARCHURL

        res.CONSTS = CONSTS

        sc_search = await AsyncRequest(
            SEARCHURL
            + "%".join(
                str(name.encode("EUC-KR"))
                .upper()[2:-1]
                .replace("\\X", "\\")
                .split("\\")
            )
        )
        sc_list = loads(sc_search.replace("\0", ""))["학교검색"]

        if len(sc_list) == 1:
            res.region = sc_list[0][1]
            res.name = sc_list[0][2]
            res.sccode = sc_list[0][3]
        elif len(sc_list) > 1:
            raise ValueError("More than one school is searched by the name passed.")
        else:
            raise NameError("No schools have been searched by the name passed.")

        res._timeurl = f"{BASEURL}?" + b64encode(
            f"{PREFIX}{str(res.sccode)}_0_1".encode("UTF-8")
        ).decode("UTF-8")
        res._week_data = [[[[("", "", "")]]]]
        await res.refresh()
        return res

    async def refresh(self):
        time_res = await AsyncRequest(self._timeurl)
        rawtimetable: dict = loads(time_res.replace("\0", ""))

        sbnum = self.CONSTS.sbnum
        thnum = self.CONSTS.thnum
        daynum = self.CONSTS.daynum

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
