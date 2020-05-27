import base64
import json

import requests

BASEURL = "http://comci.kr:4082/191401?"


class School:
    name: str
    sccode: int
    _timeurl: str

    def __init__(self, name):
        scsearch = requests.get(BASEURL + "80670l" + "%".join(str(name.encode("EUC-KR")).upper()[2:-1]
                                                              .replace("\\X", "\\").split("\\")))
        scsearch.encoding = "UTF-8"
        sclist = json.loads(scsearch.text.replace("\0", ""))["학교검색"]
        if len(sclist) > 1:
            raise ValueError("More than one school is searched by the name passed.")
        elif len(sclist) == 0:
            raise NameError("No schools have been searched by the name passed.")
        else:
            self.name = sclist[0][2]
            self.sccode = sclist[0][3]
        self._timeurl = BASEURL + base64.b64encode(f"54952_{self.sccode}_0_1".encode("UTF-8"))
        self.refresh()

    def refresh(self):
        time_res = requests.get(self._timeurl)
        time_res.encoding = "UTF-8"
        rawtimetable = json.loads(time_res.text.replace("\0", ""))

