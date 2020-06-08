import base64
import json
from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup

from .reg import *

comci_resp = requests.get("http://comci.kr:4082/st")
comci_resp.encoding = 'EUC-KR'
comcigan_html = BeautifulSoup(comci_resp.text, 'html.parser')
script = comcigan_html.find_all('script')[1].contents[0]
route = regsearch(routereg, script)
PREFIX = regsearch(prefixreg, script)[1:-1]
orgnum = extractint(regsearch(orgdatareg, script))
daynum = extractint(regsearch(daydatareg, script))
thnum = extractint(regsearch(thnamereg, script))
sbnum = extractint(regsearch(sbnamereg, script))
BASEURL = "http://comci.kr:4082" + route[1:8]
SEARCHURL = BASEURL + route[8:]


class School:
    name: str
    sccode: int
    _timeurl: str
    _week_data: List[List[List[List[Tuple[str, str, str]]]]]

    def __init__(self, name: str):
        sc_search = requests.get(SEARCHURL + "%".join(str(name.encode("EUC-KR")).upper()[2:-1]
                                                      .replace("\\X", "\\").split("\\")))
        sc_search.encoding = "UTF-8"

        sc_list = json.loads(sc_search.text.replace("\0", ""))["학교검색"]

        if len(sc_list) > 1:
            raise ValueError("More than one school is searched by the name passed.")
        elif len(sc_list) == 0:
            raise NameError("No schools have been searched by the name passed.")
        else:
            self.name = sc_list[0][2]
            self.sccode = sc_list[0][3]

        self._timeurl = BASEURL + "?" + base64.b64encode(f"{PREFIX}{str(self.sccode)}_0_1".encode("UTF-8")).decode(
            "UTF-8")
        self._week_data = [[[[("", "", "")]]]]
        self.refresh()

    def refresh(self):
        time_res = requests.get(self._timeurl)
        time_res.encoding = "UTF-8"
        rawtimetable = json.loads(time_res.text.replace("\0", ""))
        subjects: list = rawtimetable[f'자료{sbnum}']
        long_subjects: list = rawtimetable[f'긴자료{sbnum}']
        teachers: list = rawtimetable[f'자료{thnum}']
        self._week_data = [
            [
                [
                    [
                        (
                            subjects[int(str(x)[-2:])],
                            long_subjects[int(str(x)[-2:])],
                            "" if int(str(x)[:-2]) >= len(teachers) else teachers[int(str(x)[:-2])]
                        ) for x in oneday[1:] if x != 0
                    ] for oneday in oneclass[1:5]
                ] for oneclass in onegrade[1:]
            ] for onegrade in rawtimetable[f'자료{daynum}'][1:]
        ]

    def __getitem__(self, item: Union[tuple, int]) -> Union[List, Tuple, str]:
        return self._week_data.__getitem__((x-1 for x in item[:2])+item[2:])
