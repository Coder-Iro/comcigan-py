import base64
import json
from typing import List, Tuple

import requests

BASEURL = "http://comci.kr:4082/191401?"


class School:
    name: str
    sccode: int
    _timeurl: str

    def __init__(self, name: str):
        sc_search = requests.get(BASEURL + "80670l" + "%".join(str(name.encode("EUC-KR")).upper()[2:-1]
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

        self._timeurl = BASEURL + base64.b64encode(f"54952_{str(self.sccode)}_0_1".encode("UTF-8")).decode("UTF-8")

    def refresh(self):
        time_res = requests.get(self._timeurl)
        time_res.encoding = "UTF-8"
        rawtimetable = json.loads(time_res.text.replace("\0", ""))
        week_data = rawtimetable['자료318']

    @staticmethod
    def get_class_timetable(time_json, grade, classes):
        """시간표 json에서 특정 학년, 특정 반의 데이터를 가져와 반환합니다.
        :param json time_json: 불러올 시간표 json데이터
        :param int grade: 학년 정보
        :param int classes: 반 정보

        :return: 요일-교시-(과목, 선생님 성함) 순서로 저장되어있음 [[(과목, 선생님 성함), ...], ...]
        """
        # author: Kinetic(https://github.com/Kinetic27)

        processed_week_table = []  # [월, 화, ... , 금]
        week_data = time_json['자료318'][grade][classes]  # 특정반의 일주일치 시간표 가져옴

        for index, day in enumerate(week_data[1:-1], start=1):
            class_num = time_json['요일별시수'][grade][index]  # 수업 몇교시인지 가져옴
            subject = time_json['자료563']  # 과목 이름 데이터
            teacher = time_json['자료432']  # 선생님 성함 데이터

            processed_day = []  # 하루치

            for one_timetable in day[1: class_num + 1]:  # 일주일치 순회
                # one_timetable이 3자리 혹은 4자리 숫자임
                # 3자리는 1자/2자, 4자리는 2자/2자로 끊어서 선생님/과목의 인덱스를 나타냄

                subject_name = subject[int(str(one_timetable)[-2:])]  # 과목 이름
                teacher_name = teacher[int(str(one_timetable)[:-2])]  # 선생님 이름

                processed_day.append((subject_name, teacher_name))  # 튜플로 (과목, 썜)으로 저장

            processed_week_table.append(processed_day)  # 하루치를 요일배열에 저장

        return processed_week_table

    def get_timetable(self, grade, classes, week):
        rawtimetable = self.refresh()
        week_table = self.get_class_timetable(rawtimetable, grade, classes)[week]

        for i in week_table:
            print(i)

    def __getitem__(self, item: tuple) -> List[Tuple[str, str]]:
        if len(item) != 3:
            raise IndexError("Indices must be [grade][class][day]")
        return []
