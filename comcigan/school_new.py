import re
from base64 import b64encode
from json import loads
from typing import cast
from urllib.parse import quote

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response, get

BASEURL = "http://comci.net:4082"
SCSEARCH_REGEX = re.compile(r"(?<=url:['\"]\.).*?(?=['\"])")
TIMEGET_REGEX = re.compile(r"(?<=var sc3=['\"]\.).*?(?=['\"])")
PREFIX_REGEX = re.compile(r"(?<=sc_data\(['\"]).*?(?=['\"])")
THNAME_REGEX = re.compile(r"(?<=자료\.)자료\d*?(?=\.length)")

while True:
    comci_resp: Response = get(f"{BASEURL}/st", timeout=60)
    comci_resp.encoding = "EUC-KR"
    comci = comci_resp.text.replace("\0", "")
    if "refresh" in comci:
        continue
    break

script = cast(
    Tag,
    BeautifulSoup(comci, "lxml").find_all(
        "script", attrs={"language": "JavaScript", "type": "text/JavaScript"}
    )[0],
).text
SEARCHPATH = SCSEARCH_REGEX.findall(script)[0]
TIMEPATH = TIMEGET_REGEX.findall(script)[0]
PREFIX = PREFIX_REGEX.findall(script)[0]
THNAME = THNAME_REGEX.findall(script)[0]


class School:
    name: str
    school_code: int
    _timeurl: str

    def __init__(self, name: str, region: str | None = None):
        sc_search = get(
            BASEURL + SEARCHPATH + quote(name, encoding="EUC-KR"), timeout=60
        )
        sc_search.encoding = "UTF-8"
        sc_list = loads(sc_search.text.replace("\0", ""))["학교검색"]
        sc_list = sc_list if not region else [x for x in sc_list if x[1] == region]
        if len(sc_list) > 1:
            raise ValueError(
                "More than one school is searched by the query passed.",
            )
        if len(sc_list) == 0:
            raise NameError("No schools have been searched by the query passed.")

        self.region = sc_list[0][1]
        self.name = sc_list[0][2]
        self.sccode = sc_list[0][3]
        self._timeurl = (
            f"{BASEURL}{TIMEPATH}"
            + b64encode(f"{PREFIX}{str(self.sccode)}_0_1".encode()).decode()
        )
        print(self._timeurl)
        print(THNAME)
        self.refresh()

    def refresh(self):
        time_res = get(self._timeurl, timeout=60)
        time_res.encoding = "UTF-8"
        rawtimetable = loads(time_res.text.replace("\0", ""))
        print(rawtimetable[THNAME])


if __name__ == "__main__":
    School("컴시간")
