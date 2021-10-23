# comcigan-py
[![Travis (.com)](https://img.shields.io/travis/com/Team-IF/comcigan-py?logo=travis&style=flat-square)](https://www.travis-ci.com/github/Team-IF/comcigan-py) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/comcigan?logo=python&style=flat-square)](https://pypi.org/project/comcigan/) [![PyPI](https://img.shields.io/pypi/v/comcigan?logo=python&style=flat-square)](https://pypi.org/project/comcigan/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/comcigan?style=flat-square)](https://pypi.org/project/comcigan/) [![Codecov](https://img.shields.io/codecov/c/github/Team-IF/comcigan-py?logo=codecov&style=flat-square)](https://app.codecov.io/gh/Team-IF/comcigan-py) 

[English](./README.md)  |  [**한국어**](./README.ko.md)

comcigan-py는 파이썬으로 제작된 ["컴시간 학생시간표"](http://컴시간학생.kr)의 파서 입니다.
## 설치
[pip](https://pip.pypa.io/en/stable/quickstart/) 를 통해 다음과 같이 입력해서 라이브러리를 설치/업데이트 합니다 :
```sh
$ pip install comcigan
```
## 예제
동기/비동기 버전에 대한 간단한 예제
```python
from comcigan import School, AsyncSchool

myschool = School("학교 이름")
myschool = await AsyncSchool.init("학교 이름")  # 비동기 사용하시려면 이렇게 사용하세요.
# "학교 이름"은 꼭 학교의 전체 이름이 아니어도 됩니다.
# comcigan-py는 자동으로 "학교 이름"을 검색어로 인식합니다.
# 학교가 한개만 검색되면 그 결과가 반환됩니다.
# 만약 2개 이상의 학교가 검색되면, ValueError가 발생합니다.
# 만일 학교가 검색되지 않으면, NameError가 발생합니다.

print(myschool.name)  # 이 코드는 학교의 이름을 출력합니다.
# 이 값은 본인이 처음에 입력한 "학교 이름"과 같지 않을수도 있습니다.

print(myschool[2][3][3][3])
# 이 코드는 2학년 3반의 목요일 3교시 일정을 출력합니다.
```

## 라이선스
이 프로젝트는 GNU Lesser General Public License version 3.0 or later (LGPL v3.0+)의 라이선스를 따릅니다.
자세한 사항은 위 라이선스를 참조해주시길 바랍니다.
